import talisker.requests

from canonicalwebteam.discourse import DiscourseAPI, DocParser, Docs

from canonicalwebteam.search import build_search_view


def init_docs(app):
    discourse_index_id = 1087

    session = talisker.requests.get_session()
    discourse_docs = Docs(
        parser=DocParser(
            api=DiscourseAPI(
                base_url="https://discourse.charmhub.io/", session=session
            ),
            index_topic_id=discourse_index_id,
            url_prefix="/docs",
        ),
        document_template="docs/document.html",
        url_prefix="/docs",
    )

    discourse_docs.init_app(app)

    sdk_docs_id = 4449
    sdk_docs = Docs(
        parser=DocParser(
            api=DiscourseAPI(
                base_url="https://discourse.charmhub.io/", session=session
            ),
            index_topic_id=sdk_docs_id,
            url_prefix="/docs/sdk",
        ),
        document_template="docs/document.html",
        url_prefix="/docs/sdk",
        blueprint_name="sdk_docs",
    )

    sdk_docs.init_app(app)

    app.add_url_rule(
        "/docs/search",
        "docs-search",
        build_search_view(
            session=session,
            site="juju.is/docs",
            template_path="docs/search.html",
        ),
    )
