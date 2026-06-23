import os
import yaml
import logging
from invenio_search.proxies import current_search_client
from flask import current_app
from flask_babel import get_locale

log = logging.getLogger(__name__)

# Variabile globale usata come "Cache in memoria" per evitare di leggere il disco ad ogni visita
_CACHED_CLASSIFICATIONS_MAP = None

def get_classifications_map():
    """Legge il file YAML e lo converte in un dizionario. Usa la cache se già letto."""
    global _CACHED_CLASSIFICATIONS_MAP
    
    # Se abbiamo già letto il file in precedenza, restituiamo subito la cache
    if _CACHED_CLASSIFICATIONS_MAP is not None:
        return _CACHED_CLASSIFICATIONS_MAP

    # Leggiamo il path pulito e assoluto direttamente dalla configurazione di Flask
    vocabularies_path = current_app.config.get("OEDATAREP_VOCABULARIES_PATH")

    if not vocabularies_path:
        log.error("Configurazione OEDATAREP_VOCABULARIES_PATH mancante in invenio.cfg")
        return {}
    
    yaml_path = os.path.join(vocabularies_path, "classifications.yaml")
    
    new_map = {}
    try:
        # Apriamo il file YAML in modalità lettura sicura
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        # Il file YAML è una lista, lo trasformiamo in un dizionario basato sull'ID
        if data:
            for item in data:
                cid = str(item.get("id"))
                new_map[cid] = item.get("title", {})
                
        # Salviamo il risultato nella cache globale
        _CACHED_CLASSIFICATIONS_MAP = new_map
        log.info("Vocabolario YAML delle classificazioni caricato in memoria con successo.")
        
    except Exception as e:
        log.error(f"Errore durante la lettura di classifications.yaml: {e}")
    
    return new_map

def get_repository_stats():
    """Interroga OpenSearch dinamicamente in base a invenio.cfg."""
    
    show_files = current_app.config.get("OEDATAREP_STATS_SHOW_FILES", True)
    show_subjects = current_app.config.get("OEDATAREP_STATS_SHOW_SUBJECTS", True)
    show_classifications = current_app.config.get("OEDATAREP_STATS_SHOW_CLASSIFICATIONS", True)
    
    current_lang = str(get_locale().language) if get_locale() else "en"
    if current_lang not in ["it", "en"]:
        current_lang = "en"
    
    stats = {
        "total_records": 0,
        "file_extensions": [],
        "top_subjects": [],
        "top_classifications": [],
        "config": {
            "show_files": show_files,
            "show_subjects": show_subjects,
            "show_classifications": show_classifications
        }
    }
    
    index_name = "rdmrecords-records"
    
    aggs = {}
    if show_files:
        aggs["file_types"] = { "terms": { "field": "files.entries.ext", "size": 5 } }
    if show_subjects:
        aggs["top_subjects"] = { "terms": { "field": "metadata.subjects.subject.keyword", "size": 15 } }
    if show_classifications:
        aggs["top_classifications"] = { "terms": { "field": "custom_fields.ingv:classification.id", "size": 15 } }
        
    query = {
        "size": 0, 
        "query": {
            "bool": {
                "must": [
                    { "term": { "is_published": True } },
                    { "term": { "versions.is_latest": True } },
                    { "term": { "is_deleted": False } }
                ]
            }
        },
        "aggs": aggs
    }
    
    try:
        res = current_search_client.search(index=index_name, body=query)
        stats["total_records"] = res["hits"]["total"]["value"]
        
        if show_files and "file_types" in res.get("aggregations", {}):
            buckets = res["aggregations"]["file_types"]["buckets"]
            stats["file_extensions"] = [{"ext": b["key"], "count": b["doc_count"]} for b in buckets]
            
        if show_subjects and "top_subjects" in res.get("aggregations", {}):
            subject_buckets = res["aggregations"]["top_subjects"]["buckets"]
            merged_subjects = {}
            for b in subject_buckets:
                normalized_key = b["key"].lower()
                if normalized_key in merged_subjects:
                    merged_subjects[normalized_key]["count"] += b["doc_count"]
                else:
                    merged_subjects[normalized_key] = {"display_name": b["key"], "count": b["doc_count"]}
            
            sorted_subjects = sorted(merged_subjects.values(), key=lambda x: x["count"], reverse=True)
            stats["top_subjects"] = sorted_subjects[:5]
            
        if show_classifications and "top_classifications" in res.get("aggregations", {}):
            class_buckets = res["aggregations"]["top_classifications"]["buckets"]
            
            # Carichiamo la mappa dinamicamente (da RAM o da Disco)
            dynamic_class_map = get_classifications_map()
            
            for b in class_buckets:
                cid = str(b["key"])
                translated_name = dynamic_class_map.get(cid, {}).get(current_lang, f"Classification {cid}")
                
                stats["top_classifications"].append({
                    "id": cid,
                    "display_name": translated_name,
                    "count": b["doc_count"]
                })

    except Exception as e:
        log.warning(f"Errore statistiche OpenSearch: {e}")
        
    return stats