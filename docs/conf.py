# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ISDE-project-F'
copyright = '2025, Deidda Riccardo, Monni Alessandro, Murgioni Alessio & Navarro Lucas'
author = 'Deidda Riccardo, Monni Alessandro, Murgioni Alessio & Navarro Lucas'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_js'
]

# Corrected js_source_path for Windows
js_source_path = os.path.abspath('../app/static')

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
