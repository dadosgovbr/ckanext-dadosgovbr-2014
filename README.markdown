Custom CKAN Extension for dados.gov.br
======================================

1. Install the dadosgovbr CKAN extension in your Python virtual environment.
   Make sure that your virtualenv is activated, then do:

       $ pip install -e 'git+git@github.com:dadosgovbr/ckanext-dados.gov.br.git#egg=ckanext-dadosgovbr'

   Then `cd` into the `ckanext-dadosgovbr` directory and run:

       $ python setup.py develop

2. Enable the extension. Edit your CKAN ini file (e.g. development.ini), find
   the `plugins = ` line and add the dadosgovbr_theme plugin:

       plugins = dadosgovbr_theme
