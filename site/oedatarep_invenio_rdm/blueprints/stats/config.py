# stats/config.py

# Default configuration for the OEDataRep stats module
OEDATAREP_STATS_SHOW_SIDEBAR = True
OEDATAREP_STATS_SHOW_AUTHORS = True
OEDATAREP_STATS_SHOW_FILES = False
OEDATAREP_STATS_SHOW_SUBJECTS = False
OEDATAREP_STATS_SHOW_CLASSIFICATIONS = True

# Base filter for OpenSearch queries
OEDATAREP_STATS_BASE_FILTER = [
    {"term": {"is_published": True}},
    {"term": {"versions.is_latest": True}},
    {"term": {"is_deleted": False}},
    {"term": {"access.status": "open"}}
]