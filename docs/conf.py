# -*- coding: utf-8 -*-
# Copyright 2021-2024 Cardiff University
# Distributed under the terms of the BSD-3-Clause license

import igwn_auth_utils
import sphinx_github_style

# -- metadata ---------------

project = "igwn-auth-utils"
copyright = "2021-2024 Cardiff University"
author = "Duncan Macleod"
top_module = igwn_auth_utils
release = top_module.__version__
version = release.split('.dev', 1)[0]

# -- sphinx config ----------

needs_sphinx = "4.0"
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]
default_role = "obj"

# -- theme options ----------

html_theme = "furo"
templates_path = [
    "_templates",
]

# -- extensions -------------

# autosummary
autosummary_generate = True
autoclass_content = "class"
autodoc_default_flags = [
    "show-inheritance",
    "members",
    "no-inherited-members",
]

# intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "requests": ("https://requests.readthedocs.io/en/stable/", None),
    "requests-gracedb": (
        "https://requests-gracedb.readthedocs.io/en/stable/",
        None,
    ),
}

# linkcode
linkcode_url = sphinx_github_style.get_linkcode_url(
    blob=sphinx_github_style.get_linkcode_revision("head"),
    url=f"https://git.ligo.org/computing/software/{project}",
)
linkcode_resolve = sphinx_github_style.get_linkcode_resolve(linkcode_url)
