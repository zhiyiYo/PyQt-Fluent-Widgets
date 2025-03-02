# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.insert(0, target_dir)


project = 'PyQt-Fluent-Widgets'
copyright = '2021, zhiyiYo'
author = 'zhiyiYo'
release = "0.8.8"

# multi-language docs
language = 'en'
locale_dirs = ['../locales/']   # path is example but recommended.
gettext_compact = False  # optional.
gettext_uuid = True  # optional

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}
source_suffix = ['.rst', '.md']
extensions = [
    'autoapi.extension',
    'recommonmark',
    'sphinx_markdown_tables',
    "sphinx.ext.extlinks",
    "sphinx.ext.autosectionlabel",  # To make easy intra-page links: :ref:`Title`
    "sphinx_copybutton",
    "sphinx_design",
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_mock_imports = ['PyQt5']

# configuration for 'autoapi.extension'
autoapi_type = 'python'
autoapi_dirs = ['../../qfluentwidgets']
autoapi_template_dir = '_templates'
autoapi_ignore = ['**/resource.py', "**/_rc"]
add_module_names = False  # makes Sphinx render package.module.Class as Class
autoclass_content = 'both'
suppress_warnings = ["autoapi"]
autoapi_options = ['members', 'undoc-members', 'show-inheritance',
                    'show-module-summary', 'special-members', 'imported-members']



# extlinks alias
extlinks = {"issue": ("https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/%s", "GH %s")}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "sidebar_hide_name": False,
}

html_show_sourcelink = True
html_title = "PyQt-Fluent-Widgets"
html_favicon = "_static/logo.png"
html_css_files = [
    'css/fancybox.css',
    'css/custom.css',
]
html_js_files = [
    'js/fancybox.umd.js',
    'js/fancybox.js',
]

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
