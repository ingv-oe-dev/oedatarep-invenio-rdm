import logging
import os

import yaml
from flask import current_app
from flask_babel import get_locale
from invenio_search.proxies import current_search_client

log = logging.getLogger(__name__)

# Global variable used as "in-memory cache" to avoid reading disk at every visit
_CACHED_CLASSIFICATIONS_MAP = None


def get_classifications_map():
    """Reads YAML file and converts it to dictionary. Uses cache if already read."""
    global _CACHED_CLASSIFICATIONS_MAP

    # If we already read the file previously, return cache immediately
    if _CACHED_CLASSIFICATIONS_MAP is not None:
        return _CACHED_CLASSIFICATIONS_MAP

    # Read the clean and absolute path directly from Flask configuration
    vocabularies_path = current_app.config.get("OEDATAREP_VOCABULARIES_PATH")

    if not vocabularies_path:
        log.error("Configurations OEDATAREP_VOCABULARIES_PATH missing in invenio.cfg")
        return {}

    yaml_path = os.path.join(vocabularies_path, "classifications.yaml")

    new_map = {}
    try:
        # Open YAML file in safe read mode
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # YAML file is a list, transform it into a dictionary based on ID
        if data:
            for item in data:
                cid = str(item.get("id"))
                new_map[cid] = item.get("title", {})

        # Save result in global cache
        _CACHED_CLASSIFICATIONS_MAP = new_map
        log.info("YAML classifications vocabulary loaded in memory successfully.")

    except Exception as e:
        log.error(f"Error during reading classifications.yaml: {e}")

    return new_map


def get_repository_stats():
    """Queries OpenSearch dynamically based on invenio.cfg."""

    if not current_app.config.get("OEDATAREP_STATS_SHOW_SIDEBAR", True):
        return {}
    
    show_files = current_app.config.get("OEDATAREP_STATS_SHOW_FILES", True)
    show_subjects = current_app.config.get("OEDATAREP_STATS_SHOW_SUBJECTS", True)
    show_classifications = current_app.config.get(
        "OEDATAREP_STATS_SHOW_CLASSIFICATIONS", True
    )

    current_lang = str(get_locale().language) if get_locale() else "en"
    if current_lang not in ["it", "en"]:
        current_lang = "en"

    stats = {
        "total_records": 0,
        "file_extensions": [],
        "top_subjects": [],
        "top_classifications": []
    }

    index_name = "rdmrecords-records"

    aggs = {}
    if show_files:
        aggs["file_types"] = {"terms": {"field": "files.entries.ext", "size": 5}}
    if show_subjects:
        aggs["top_subjects"] = {
            "terms": {"field": "metadata.subjects.subject.keyword", "size": 15}
        }
    if show_classifications:
        aggs["top_classifications"] = {
            "terms": {"field": "custom_fields.ingv:classification.id", "size": 15}
        }

    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"term": {"is_published": True}},
                    {"term": {"versions.is_latest": True}},
                    {"term": {"is_deleted": False}},
                ]
            }
        },
        "aggs": aggs,
    }

    try:
        res = current_search_client.search(index=index_name, body=query)
        stats["total_records"] = res["hits"]["total"]["value"]

        if show_files and "file_types" in res.get("aggregations", {}):
            buckets = res["aggregations"]["file_types"]["buckets"]
            stats["file_extensions"] = [
                {"ext": b["key"], "count": b["doc_count"]} for b in buckets
            ]

        if show_subjects and "top_subjects" in res.get("aggregations", {}):
            subject_buckets = res["aggregations"]["top_subjects"]["buckets"]
            merged_subjects = {}
            for b in subject_buckets:
                normalized_key = b["key"].lower()
                if normalized_key in merged_subjects:
                    merged_subjects[normalized_key]["count"] += b["doc_count"]
                else:
                    merged_subjects[normalized_key] = {
                        "display_name": b["key"],
                        "count": b["doc_count"],
                    }

            sorted_subjects = sorted(
                merged_subjects.values(), key=lambda x: x["count"], reverse=True
            )
            stats["top_subjects"] = sorted_subjects[:5]

        if show_classifications and "top_classifications" in res.get(
            "aggregations", {}
        ):
            class_buckets = res["aggregations"]["top_classifications"]["buckets"]

            # Load the map dynamically (from RAM or disk)
            dynamic_class_map = get_classifications_map()

            for b in class_buckets:
                cid = str(b["key"])
                translated_name = dynamic_class_map.get(cid, {}).get(
                    current_lang, f"Classification {cid}"
                )

                stats["top_classifications"].append(
                    {
                        "id": cid,
                        "display_name": translated_name,
                        "count": b["doc_count"],
                    }
                )

    except Exception as e:
        log.warning(f"Error statistichs OpenSearch: {e}")

    return stats


def get_people_stats():
    """Retrieves total count and top list of creators and contributors."""

    if not current_app.config.get("OEDATAREP_STATS_SHOW_AUTHORS", True):
        return {}
    
    index_name = "rdmrecords-records"

    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"term": {"is_published": True}},
                    {"term": {"versions.is_latest": True}},
                    {"term": {"is_deleted": False}},
                ]
            }
        },
        "aggs": {
            "unique_authors_total": {
                "cardinality": {
                    "field": "metadata.creators.person_or_org.identifiers.identifier"
                }
            },
            "unique_contributors_total": {
                "cardinality": {
                    "field": "metadata.contributors.person_or_org.identifiers.identifier"
                }
            },
        },
    }

    stats = {
        "unique_creators_count": 0,
        "unique_contributors_count": 0,
        "top_creators_list": [],
    }

    try:
        res = current_search_client.search(index=index_name, body=query)
        aggs = res.get("aggregations", {})

        if "unique_authors_total" in aggs:
            stats["unique_creators_count"] = aggs["unique_authors_total"]["value"]

        if "unique_contributors_total" in aggs:
            stats["unique_contributors_count"] = aggs["unique_contributors_total"][
                "value"
            ]

        if "top_authors" in aggs:
            buckets = aggs["top_authors"]["buckets"]
            stats["top_creators_list"] = [
                {"name": b["key"], "count": b["doc_count"]} for b in buckets
            ]

    except Exception as e:
        log.warning(f"Error query persons OpenSearch: {e}")

    return stats
