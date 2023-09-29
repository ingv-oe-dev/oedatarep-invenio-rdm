"""Frontpage records."""
from flask import render_template
from invenio_rdm_records.resources.serializers import UIJSONSerializer
from opensearch_dsl.query import Q
from flask.views import MethodView
from invenio_search.api import RecordsSearch


def records_serializer(records=None):
    """Serialize list of records."""
    record_list = []
    for record in records:
        record_list.append(UIJSONSerializer().dump_obj(record.to_dict()))
    return record_list


class SearchView(MethodView):
    """MySite support view."""

    def __init__(self):
        self.template = "oedatarep_invenio_rdm/frontpage.html"

    def get(self):
        """Renders the support template."""
        records = FrontpageRecordsSearch()[:10].sort("-created").execute()
        return render_template(self.template, records=records_serializer(records))


class FrontpageRecordsSearch(RecordsSearch):
    """Search class for records that goes on the frontpage."""

    class Meta:
        """Default index and filter for frontpage search."""

        index = "rdmrecords-records"
        default_filter = Q(
            "query_string",
            query=("access.record:public " "AND versions.is_latest:true"),
        )
