from ckan.lib.base import c, h
from ckan.controllers.home import HomeController

from feedreader.parser import from_url

class DadosGovBrHomeController(HomeController):
    """dados.gov.br theme customized home controller
    """
    @staticmethod
    def limita_tamanho(s, tamanho):
        s = unicode(s)
        return s if (len(s) < tamanho) else s[:(tamanho - 5)].rsplit(u" ", 1)[0] + u" ..."
    @staticmethod
    def formata_data(d):
        return d.strftime("%d/%m/%Y")
    
    def index(self):
        """This handles dados.gov.br's index home page.
        All extra data displayed on the home page should be handled here.
        """
        # featured datasets section, read from a specific dataset group
        
        # news section, parsed from feed
        parsed = from_url('http://189.9.137.65/wp/index.php/feed')
        c.articles = []
        for entry in parsed.entries:
            c.articles.append((
                entry.link,
                self.formata_data(entry.published),
                self.limita_tamanho(entry.title, 70),
                self.limita_tamanho(entry.description, 165)
            ))
        
        # most recent datasets section
        
        # most viewed datasets section, from ckanext-googleanalytics
        
        return super(DadosGovBrHomeController, self).index()
