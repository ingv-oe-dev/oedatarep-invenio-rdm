"""JS/CSS Webpack bundles for My Site."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                # Add your webpack entrypoints
                "oedatarep-landing-page": "./js/oedatarep_invenio_rdm/landing_page/index.js",
            },
            dependencies={
                "leaflet": "^1.8.0",
                "react-leaflet": "^4.0.0",
                "@react-leaflet/core": "^2.0.0",
                "plotly.js-basic-dist-min": "^2.26.1",
                "react-plotly.js": "^2.6.0",
            },
            aliases={
                "themes/oedatarep": "less/site/theme",
            },
        ),
    },
)
