import talisker.requests

from canonicalwebteam.search import build_search_view
from flask import render_template

RTD_DOCS_BASE_URL = "https://canonical-juju.readthedocs.io/en/latest/"


def init_docs(app):
    session = talisker.requests.get_session()

    def render_juju_docs_page():
        return render_template("docs/juju-ecosystem-docs.html")

    app.add_url_rule("/docs", "juju-ecosystem-docs", render_juju_docs_page)

    app.add_url_rule(
        "/docs/search",
        "docs-search",
        build_search_view(
            app=app,
            session=session,
            site="https://canonical-juju.readthedocs-hosted.com/en/latest",
            template_path="docs/search.html",
        ),
    )
