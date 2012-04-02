import os
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes

class DadosGovBrDatasetView(SingletonPlugin):
    '''The customized dataset view screen.
    '''
    implements(IRoutes, inherit=True)

    def before_map(self, map):
        map.connect('dataset', '/dataset/{id}',
                    controller='ckanext.dadosgovbr.controllers.package:DadosGovBrDatasetController',
                    action='read')
        return map

