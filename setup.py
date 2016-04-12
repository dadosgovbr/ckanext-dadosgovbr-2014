from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(
	name='ckanext-dadosgovbr',
	version=version,
	description="Extensão do CKAN com o tema para o portal dados.gov.br.",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='',
	author_email='',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.dadosgovbr'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
        'feedreader',
        # dateutil version 2.0 is incompatible with feedreader
        'python-dateutil==1.5',
	],
	entry_points=\
	"""
        [ckan.plugins]
        dadosgovbr_theme=ckanext.dadosgovbr.theme:DadosGovBrTheme
        dadosgovbr_newssection=ckanext.dadosgovbr.newssection_plugin:DadosGovBrNewsSection
        dadosgovbr_dataset=ckanext.dadosgovbr.dataset_plugin:DadosGovBrDatasetView
	""",
)
