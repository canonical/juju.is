from os import getenv

import talisker.requests

from canonicalwebteam.discourse import DiscourseAPI, DocParser, Docs
from canonicalwebteam.search import build_search_view

DISCOURSE_API_KEY = getenv("DISCOURSE_API_KEY")
DISCOURSE_API_USERNAME = getenv("DISCOURSE_API_USERNAME")


def init_docs(app):
    session = talisker.requests.get_session()
    main_docs = Docs(
        parser=DocParser(
            api=DiscourseAPI(
                base_url="https://discourse.charmhub.io/", session=session
            ),
            index_topic_id=4513,
            url_prefix="/docs",
        ),
        document_template="docs/document.html",
        url_prefix="/docs",
        blueprint_name="main_docs",
    )
    main_docs.init_app(app)

    discourse_index_id = 1087
    tutorials_index_topic_id = 2628
    tutorials_url_prefix = "/tutorials"

    discourse_docs = Docs(
        parser=DocParser(
            api=DiscourseAPI(
                base_url="https://discourse.charmhub.io/",
                session=session,
                api_key=DISCOURSE_API_KEY,
                api_username=DISCOURSE_API_USERNAME,
                get_topics_query_id=2,
            ),
            index_topic_id=discourse_index_id,
            url_prefix="/docs/olm",
            tutorials_index_topic_id=tutorials_index_topic_id,
            tutorials_url_prefix=tutorials_url_prefix,
        ),
        document_template="docs/document.html",
        url_prefix="/docs/olm",
    )

    discourse_docs.init_app(app)

    sdk_docs_id = 4449
    sdk_docs = Docs(
        parser=DocParser(
            api=DiscourseAPI(
                base_url="https://discourse.charmhub.io/",
                session=session,
                api_key=DISCOURSE_API_KEY,
                api_username=DISCOURSE_API_USERNAME,
                get_topics_query_id=2,
            ),
            index_topic_id=sdk_docs_id,
            url_prefix="/docs/sdk",
            tutorials_index_topic_id=tutorials_index_topic_id,
            tutorials_url_prefix=tutorials_url_prefix,
        ),
        document_template="docs/document.html",
        url_prefix="/docs/sdk",
        blueprint_name="sdk_docs",
    )

    sdk_docs.init_app(app)

    lma2_docs_id = 5132
    lma2_docs = Docs(
        parser=DocParser(
            api=DiscourseAPI(
                base_url="https://discourse.charmhub.io/",
                session=session,
                api_key=DISCOURSE_API_KEY,
                api_username=DISCOURSE_API_USERNAME,
                get_topics_query_id=2,
            ),
            index_topic_id=lma2_docs_id,
            url_prefix="/docs/lma2",
            tutorials_index_topic_id=tutorials_index_topic_id,
            tutorials_url_prefix=tutorials_url_prefix,
        ),
        document_template="docs/document.html",
        url_prefix="/docs/lma2",
        blueprint_name="lma2_docs",
    )

    lma2_docs.init_app(app)

    app.add_url_rule(
        "/docs/search",
        "docs-search",
        build_search_view(
            session=session,
            site="juju.is/docs",
            template_path="docs/search.html",
        ),
    )
