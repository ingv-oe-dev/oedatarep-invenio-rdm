"""Additional views."""

from flask import Blueprint
from .support.support import MySiteSupport

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

    # Add URL rules
    return blueprint

