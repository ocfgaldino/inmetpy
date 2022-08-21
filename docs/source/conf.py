# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

import plotly.io as pio

pio.renderers.default = "plotly_mimetype+notebook"

project = "InmetPy"
copyright = "2022, Felippe Galdino, Tobias Ramalho"
author = "Felippe Galdino"
release = "0.1.3"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "numpydoc",
    #       'sphinx.ext.napoleon',
    "sphinx_exec_code",
    "nbsphinx",
    "sphinx_rtd_size",
]


templates_path = ["_templates"]
exclude_patterns = []

pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_js_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"
]


html_context = {
    "display_github": True,
    "github_user": "ocfgaldino",
    "github_repo": "inmetpy",
    "github_version": "master",
    "conf_py_path": "/source/",
}

sphinx_rtd_size_width = "90%"

napoleon_use_ivar = True
