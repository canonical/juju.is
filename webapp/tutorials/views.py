import flask
import math
import talisker.requests

from canonicalwebteam.discourse import DiscourseAPI, TutorialParser, Tutorials


def init_tutorials(app, url_prefix):
    session = talisker.requests.get_session()
    tutorials_discourse = Tutorials(
        parser=TutorialParser(
            api=DiscourseAPI(
                base_url="https://discourse.charmhub.io/", session=session
            ),
            index_topic_id=2628,
            category_id=34,
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

        if not topics_request:
            metadata = tutorials_discourse.parser.metadata
        else:
            topics = topics_request.split(",")
            metadata = [
                doc
                for doc in tutorials_discourse.parser.metadata
                if doc["categories"] in topics
            ]

        total_pages = math.ceil(len(metadata) / posts_per_page)

        return flask.render_template(
            "tutorials/index.html",
            navigation=tutorials_discourse.parser.navigation,
            forum_url=tutorials_discourse.parser.api.base_url,
            metadata=metadata,
            page=page,
            posts_per_page=posts_per_page,
            total_pages=total_pages,
            active_section="tutorials",
            topic=topics_request,
        )

    tutorials_discourse.init_app(app)
