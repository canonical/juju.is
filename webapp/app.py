import datetime

from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from canonicalwebteam import image_template
from flask import render_template

from webapp.docs.views import init_docs
from webapp.template_utils import current_url_with_query, static_url
from webapp.tutorials.views import init_tutorials

# Rename your project below
app = FlaskBase(
    __name__,
    "juju.is",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)


@app.route("/integration")
def integration():
    return render_template("overview/integration.html")


@app.route("/model-driven-operations")
def model_driven_operations():
    return render_template("overview/model-driven-operations.html")


@app.route("/devsecops")
def devsecops():
    return render_template("overview/devsecops.html")


@app.route("/universal-operators")
def universal_operators():
    return render_template("overview/universal-operators.html")


@app.route("/operator-services")
def operator_services():
    return render_template("overview/operator-services.html")


@app.route("/mission")
def mission():
    return render_template("overview/mission.html")


@app.route("/high-availability-enterprise-olm")
def high_availability_enterprise_olm():
    return render_template("overview/high-availability-enterprise-olm.html")


@app.route("/architecture")
def architecture():
    return render_template("overview/architecture.html")


@app.route("/operator-lifecycle-manager")
def operator_lifecycle_manager():
    return render_template("overview/operator-lifecycle-manager.html")


@app.route("/ops-code-quality")
def ops_code_quality():
    return render_template("overview/ops-code-quality.html")


@app.route("/hosted-olm")
def hosted_olm():
    return render_template("overview/hosted-olm.html")


@app.route("/multi-cloud-operations")
def multi_cloud_operations():
    return render_template("overview/multi-cloud-operations.html")


@app.route("/beyond-configuration-management")
def beyond_configuration_management():
    return render_template("overview/beyond-configuration-management.html")


template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)

init_docs(app, "/docs")
init_tutorials(app, "/tutorials")


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
