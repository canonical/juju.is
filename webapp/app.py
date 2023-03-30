import datetime
import os

import requests
import semver
import talisker.requests
from cachetools import TTLCache, cached
from canonicalwebteam import image_template
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from canonicalwebteam.yaml_responses.flask_helpers import (
    prepare_deleted,
    prepare_redirects,
)
from flask import render_template
from flask_cors import cross_origin

from webapp.blog.views import init_blog
from webapp.docs.views import init_docs
from webapp.greenhouse import Greenhouse
from webapp.template_utils import current_url_with_query, static_url

CACHE_TTL = 60 * 60  # 1 hour cache

# Rename your project below
app = FlaskBase(
    __name__,
    "juju.is",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
    favicon_url="https://assets.ubuntu.com/v1/5d4edefd-jaas-favicon.png",
)

app.before_request(prepare_redirects())
app.before_request(prepare_deleted())

session = talisker.requests.get_session()
greenhouse = Greenhouse(
    session=session, api_key=os.environ.get("GREENHOUSE_API_KEY")
)


@app.route("/careers")
def careers():
    vacancies = greenhouse.get_vacancies_by_site("juju.is")
    return render_template("careers.html", vacancies=vacancies)


@app.route("/get-in-touch")
def get_in_touch():
    return render_template("partials/_get-in-touch.html")


@app.route("/latest.json")
@cross_origin()
@cached(cache=TTLCache(maxsize=128, ttl=CACHE_TTL))
def get_latest_versions():
    try:
        result = {}

        # get dashboard verion
        dashboard_response = requests.get(
            "/".join(
                [
                    "https://api.github.com",
                    "repos",
                    "canonical",
                    "jaas-dashboard",
                    "releases",
                    "latest",
                ]
            )
        )
        dashboard_json_response = dashboard_response.json()
        result["dashboard"] = dashboard_json_response["tag_name"]

        # Get juju versions
        juju_response = requests.get(
            "https://api.github.com/repos/juju/juju/releases"
        )
        juju_json_response = juju_response.json()
        juju_versions = []
        for release in juju_json_response:
            # get semver
            version = semver.VersionInfo.parse(
                release["tag_name"].replace("juju-", "")
            )
            # Reduce to latest for each major.minor
            if not list(
                filter(
                    lambda value: version.major == value.major
                    and version.minor == value.minor,
                    juju_versions,
                )
            ):
                juju_versions.append(version)

        # Reformat to a string
        juju_versions = [
            str(version.finalize_version()) for version in juju_versions
        ]
        result["juju"] = sorted(juju_versions)
        return result
    except Exception:
        return {}


template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)

init_docs(app)
init_blog(app, "/blog")


@app.context_processor
def utility_processor():
    return {"image": image_template}


@app.context_processor
def inject_utilities():
    return {
        "current_url_with_query": current_url_with_query,
        "static_url": static_url,
    }


@app.context_processor
def inject_today_date():
    return {"current_year": datetime.date.today().year}
