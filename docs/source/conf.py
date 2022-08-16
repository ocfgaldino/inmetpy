# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


project = 'InmetPy'
copyright = '2022, Felippe Galdino, Tobias Ramalho'
author = 'Felippe Galdino'
release = '0.1.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.doctest',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.napoleon',
        'sphinx_exec_code'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


html_context = {
    "display_github": True, 
    "github_user": "ocfgaldino",
    "github_repo": "inmetpy",
    "github_version": "master", 
    "conf_py_path": "/source/", 
}