import datetime

from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from canonicalwebteam import image_template

from webapp.docs.views import init_docs
from webapp.template_utils import current_url_with_query, static_url

# Rename your project below
app = FlaskBase(
    __name__,
    "juju.is",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)


template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)

init_docs(app, "/docs")


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
