# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../')

# -- Project information -----------------------------------------------------

project = 'QOL'
copyright = '2019, Matthew Buckley'
author = 'Matthew Buckley'

# The full version, including alpha/beta/rc tags
# Get version from git describe command
import subprocess as sp
gitOut = sp.check_output(['git', 'describe', '--tags', '--always'])
gitOut = gitOut.strip().decode('utf-8')
# Remove the 'v' from version tag
if gitOut.lower().startswith('v'):
    gitOut = gitOut[1:]
version = gitOut
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon'
]

# Don't add package name infront of modules
add_module_names = False

# Change autodoc settings
autodoc_member_order = 'groupwise'
autoclass_content = 'both'
autodoc_default_options = {
    'undoc-members': True
}

# Auto summary options
autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_templates']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Edit the theme
def setup(app):
   app.add_css_file("theme_edit.css")

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']