# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University
# Distributed under the terms of the BSD-3-Clause license

import inspect
import re
import sys
from pathlib import Path

import igwn_auth_utils

# -- metadata ---------------

project = "igwn-auth-utils"
copyright = "2021 Cardiff University"
author = "Duncan Macleod"
top_module = igwn_auth_utils
release = top_module.__version__
version = release.split('.dev', 1)[0]
git_url = "https://github.com/duncanmmacleod/{}".format(project)

# parse version number to get git reference
_setuptools_scm_version_regex = re.compile(
    r"\+g(\w+)(?:\Z|\.)",
)
if match := _setuptools_scm_version_regex.search(release):
    git_ref, = match.groups()
else:
    git_ref = 'v{}'.format(version)

# -- sphinx config ----------

needs_sphinx = "4.0"
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",
    "sphinx_automodapi.automodapi",
]
default_role = "obj"

# -- theme options ----------

html_theme = "sphinx_material"
html_sidebars = {
    "**": [
        "logo-text.html",
        "globaltoc.html",
        "localtoc.html",
        "searchbox.html",
    ],
}
html_theme_options = {
    "repo_url": git_url,
    "repo_name": project,
    "master_doc": False,
    "nav_links": [],
}
html_static_path = ["_static"]

# -- extensions -------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "requests": ("https://docs.python-requests.org/en/stable/", None),
    "requests-gracedb": (
        "https://requests-gracedb.readthedocs.io/en/stable/",
        None,
    ),
}

automodapi_inherited_members = False


def linkcode_resolve(domain, info):
    """Determine the URL corresponding to Python object

    This code is stolen with thanks from the scipy team.
    """
    if domain != "py" or not info["module"]:
        return None

    def find_source(module, fullname):
        obj = sys.modules[module]
        for part in fullname.split("."):
            obj = getattr(obj, part)
        try:  # unwrap a decorator
            obj = obj.im_func.func_closure[0].cell_contents
        except (AttributeError, TypeError):
            pass
        # get filename
        filename = Path(inspect.getsourcefile(obj)).relative_to(
            Path(top_module.__file__).parent,
        ).as_posix()
        # get line numbers of this object
        source, lineno = inspect.getsourcelines(obj)
        if lineno:
            return "{}#L{:d}-L{:d}".format(
                filename,
                lineno,
                lineno + len(source) - 1,
            )
        return filename

    try:
        fileref = find_source(info["module"], info["fullname"])
    except (
        AttributeError,  # object not found
        OSError,  # file not found
        TypeError,  # source for object not found
        ValueError,  # file not
    ):
        raise
        return None

    return "{}/tree/{}/{}/{}".format(
        git_url,
        git_ref,
        top_module.__name__,
        fileref,
    )


# -- setup ------------------

def setup(app):
    app.add_css_file("css/igwnauthutils.css")
