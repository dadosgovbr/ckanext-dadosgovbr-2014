from ckan.controllers.home import HomeController

class DadosGovBrHomeController(HomeController):
    """dados.gov.br theme customized home controller
    """
    def index(self):
        return super(DadosGovBrHomeController).index()
