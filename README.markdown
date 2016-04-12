Tema para o CKAN utilizado no portal dados.gov.br.

## Instalação

Primeiro, instale a extensão do CKAN dadosgovbr em seu ambiente virtual
Python.  Certifque-se que o seu virtualenv está ativo e faça:

    $ pip install -e 'git+git@github.com:dadosgovbr/ckanext-dados.gov.br.git#egg=ckanext-dadosgovbr'

Então faça `cd` para o diretório `ckanext-dadosgovbr` e execute:

    $ python setup.py develop

Por fim, habilite a extensão. Edite seu arquivo .ini do CKAN ini file (e.g.
development.ini), encontre a linha `plugins = ` e adicione os plugins
desejados:

    plugins = dadosgovbr_theme dadosgovbr_newssection dadosgovbr_dataset

# Plugins

* dadosgovbr_theme: Interface visual da Identidade Digital de Governo (IDG).
* dadosgovbr_newsection: Customizações na página principal (ex.: seção de
  notícias que as traz do feed do Wordpress).
* dadosgovbr_dataset: Customizações da página de visualização do dataset.

