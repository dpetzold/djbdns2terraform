import os
from string import Template

BASE_PATH = os.path.dirname(__file__)


def render_template(template_name, **kwargs):
    with open(os.path.join(BASE_PATH, 'templates', template_name), 'r') as f:
        return Template(f.read()).safe_substitute(**kwargs)
