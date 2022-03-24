# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

project_root = Path(__file__).parents[2].resolve().as_posix()

print(f"Project root: {project_root}")
sys.path.insert(0, project_root)


# -- Project information

project = 'NotionApiManager'
copyright = '2022, Rubén Chuliá Mena'
author = 'Rubén Chuliá Mena'

release = '0.1'
version = '0.1.7'


# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
html_static_path = ['_static']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
