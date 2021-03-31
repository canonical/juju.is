import datetime
import os

import talisker.requests
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from canonicalwebteam import image_template
from canonicalwebteam.yaml_responses.flask_helpers import (
    prepare_deleted,
    prepare_redirects,
)
from flask import render_template

from webapp.docs.views import init_docs
from webapp.template_utils import current_url_with_query, static_url
from webapp.tutorials.views import init_tutorials
from webapp.blog.views import init_blog
from webapp.greenhouse import Greenhouse

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
    vacancies = greenhouse.get_vacancies_by_department_slug("juju")
    return render_template("careers.html", vacancies=vacancies)


@app.route("/integration")
def integration():
    return render_template("about/integration.html")


@app.route("/model-driven-operations")
def model_driven_operations():
    return render_template("about/model-driven-operations.html")


@app.route("/devsecops")
def devsecops():
    return render_template("about/devsecops.html")


@app.route("/universal-operators")
def universal_operators():
    return render_template("about/universal-operators.html")


@app.route("/operator-services")
def operator_services():
    return render_template("about/operator-services.html")


@app.route("/mission")
def mission():
    return render_template("about/mission.html")


@app.route("/overview")
def overview():
    return render_template("about/overview.html")


@app.route("/high-availability-enterprise-olm")
def high_availability_enterprise_olm():
    return render_template("about/high-availability-enterprise-olm.html")


@app.route("/architecture")
def architecture():
    return render_template("about/architecture.html")


@app.route("/operator-lifecycle-manager")
def operator_lifecycle_manager():
    return render_template("about/operator-lifecycle-manager.html")


@app.route("/ops-code-quality")
def ops_code_quality():
    return render_template("about/ops-code-quality.html")


@app.route("/hosted-olm")
def hosted_olm():
    return render_template("about/hosted-olm.html")


@app.route("/multi-cloud-operations")
def multi_cloud_operations():
    return render_template("about/multi-cloud-operations.html")


@app.route("/beyond-configuration-management")
def beyond_configuration_management():
    return render_template("about/beyond-configuration-management.html")


@app.route("/get-in-touch")
def get_in_touch():
    return render_template("partials/_get-in-touch.html")


template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)

init_docs(app, "/docs")
init_tutorials(app, "/tutorials")
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
