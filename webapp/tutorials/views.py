from os import getenv

import flask
import math
import talisker.requests

from canonicalwebteam.discourse import DiscourseAPI, TutorialParser, Tutorials

DISCOURSE_API_KEY = getenv("DISCOURSE_API_KEY")
DISCOURSE_API_USERNAME = getenv("DISCOURSE_API_USERNAME")


def init_tutorials(app, url_prefix):
    session = talisker.requests.get_session()
    tutorials_discourse = Tutorials(
        parser=TutorialParser(
            api=DiscourseAPI(
                base_url="https://discourse.charmhub.io/",
                session=session,
                api_key=DISCOURSE_API_KEY,
                api_username=DISCOURSE_API_USERNAME,
                get_topics_query_id=2,
            ),
            index_topic_id=2628,
            url_prefix=url_prefix,
        ),
        document_template="tutorials/tutorial.html",
        url_prefix=url_prefix,
        blueprint_name="tutorials",
    )

    @app.route(url_prefix)
    def index():
        page = flask.request.args.get("page", default=1, type=int)
        topics_request = flask.request.args.get(
            "topic", default=None, type=str
        )
        posts_per_page = 12
        tutorials_discourse.parser.parse()
        tutorials_discourse.parser.parse_topic(
            tutorials_discourse.parser.index_topic
        )

        if not topics_request:
            tutorials = tutorials_discourse.parser.tutorials
        else:
            topics = topics_request.split(",")
            tutorials = [
                doc
                for doc in tutorials_discourse.parser.tutorials
                if doc["categories"] in topics
            ]

        total_pages = math.ceil(len(tutorials) / posts_per_page)

        return flask.render_template(
            "tutorials/index.html",
            forum_url=tutorials_discourse.parser.api.base_url,
            tutorials=tutorials,
            page=page,
            posts_per_page=posts_per_page,
            total_pages=total_pages,
            active_section="tutorials",
            topic=topics_request,
        )

    tutorials_discourse.init_app(app)
