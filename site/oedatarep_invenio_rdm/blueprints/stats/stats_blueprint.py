from flask import Blueprint
from .stats_logic import get_repository_stats, get_people_stats

def create_stats_blueprint(app):
    """Factory per il blueprint isolato delle statistiche."""
    blueprint = Blueprint("oedatarep_stats", __name__)
    
    @blueprint.app_context_processor
    def inject_stats():
        return dict(
            get_repository_stats=get_repository_stats,
            get_people_stats=get_people_stats
        )

    return blueprint