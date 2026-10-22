from flask import Blueprint, current_app
from . import config
from .stats_logic import get_people_stats, get_repository_stats


def create_stats_blueprint(app):
    """Statistics blueprint factory."""
    blueprint = Blueprint("oedatarep_stats", __name__)

    for k in dir(config):
        if k.startswith('OEDATAREP_STATS_'):
            # setdefault set the value only if the key does NOT exists in app.config already
            app.config.setdefault(k, getattr(config, k))

    @blueprint.app_context_processor
    def inject_stats():
        ui_config = {
            "show_sidebar": current_app.config["OEDATAREP_STATS_SHOW_SIDEBAR"],
            "show_authors": current_app.config["OEDATAREP_STATS_SHOW_AUTHORS"],
            "show_classifications": current_app.config["OEDATAREP_STATS_SHOW_CLASSIFICATIONS"],
            "show_files": current_app.config["OEDATAREP_STATS_SHOW_FILES"],
            "show_subjects": current_app.config["OEDATAREP_STATS_SHOW_SUBJECTS"]
        }

        return dict(
            get_repository_stats=get_repository_stats, 
            get_people_stats=get_people_stats,
            stats_config=ui_config
        )

    return blueprint
