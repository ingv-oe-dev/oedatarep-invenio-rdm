"""Additional views."""

from flask import Blueprint
from .support.support import MySiteSupport
from .search.search import SearchView

#
# Registration
#
def create_blueprint(app):
    """Register blueprint routes on app."""
    blueprint = Blueprint(
        "oedatarep_invenio_rdm",
        __name__,
        template_folder="./templates",
    )

    blueprint.add_url_rule(
        "/support",
        view_func=MySiteSupport.as_view("support_form"),
    )

    blueprint.add_url_rule(
        "/",
        view_func=SearchView.as_view("landing_page"),
    )

    # Add URL rules
    return blueprint

