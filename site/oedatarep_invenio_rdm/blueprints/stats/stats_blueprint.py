from flask import Blueprint, current_app

from .stats_logic import get_people_stats, get_repository_stats


def create_stats_blueprint(app):
    """Statistics blueprint factory."""
    blueprint = Blueprint("oedatarep_stats", __name__)

    @blueprint.app_context_processor
    def inject_stats():
        ui_config = {
            "show_sidebar": current_app.config.get("OEDATAREP_STATS_SHOW_SIDEBAR", True),
            "show_authors": current_app.config.get("OEDATAREP_STATS_SHOW_AUTHORS", True),
            "show_classifications": current_app.config.get("OEDATAREP_STATS_SHOW_CLASSIFICATIONS", True),
            "show_files": current_app.config.get("OEDATAREP_STATS_SHOW_FILES", True),
            "show_subjects": current_app.config.get("OEDATAREP_STATS_SHOW_SUBJECTS", True)
        }

        return dict(
            get_repository_stats=get_repository_stats, 
            get_people_stats=get_people_stats,
            stats_config=ui_config
        )

    return blueprint
