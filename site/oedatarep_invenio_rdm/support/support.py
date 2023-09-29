from flask import render_template
from flask.views import MethodView


class MySiteSupport(MethodView):
    """MySite support view."""

    def __init__(self):
        self.template = "oedatarep_invenio_rdm/support.html"

    def get(self):
        """Renders the support template."""
        return render_template(self.template)