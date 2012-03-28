from ckan.lib.base import c, h
from ckan.controllers.home import HomeController

class DadosGovBrHomeController(HomeController):
    """dados.gov.br theme customized home controller
    """
    
    # auxiliary static methods
    @staticmethod
    def limita_tamanho(s, tamanho):
        s = unicode(s)
        return s if (len(s) < tamanho) else s[:(tamanho - 5)].rsplit(u" ", 1)[0] + u" ..."
    
    @staticmethod
    def formata_data(d):
        return d.strftime("%d/%m/%Y")

    @classmethod
    def set_news_section(cls):
        from feedreader.parser import from_url
        parsed = from_url('http://189.9.137.65/wp/index.php/feed')
        c.articles = []
        for entry in parsed.entries[:3]:
            c.articles.append((
                entry.link,
                cls.formata_data(entry.published),
                cls.limita_tamanho(entry.title, 70),
                cls.limita_tamanho(entry.description, 165)
            ))

    @classmethod
    def set_most_viewed_datasets(cls):
        from ckanext.googleanalytics import dbutil
        tamanho = 58
        c.top_packages = []
        for package, recent, ever in dbutil.get_top_packages(limit=5):
            if getattr(package, "title", False):
                package.title = cls.limita_tamanho(package.title, tamanho)
            c.top_packages.append((package, recent, ever))

        # Enable to set resources variable, don't forget to enable it on template too!
        #c.top_resources = dbutil.get_top_resources(limit=10)
    
    @staticmethod
    def set_top_tags():
        """Sets the c.top_tags variable for a template to render the
        most used tags.
        """
        from ckan.logic import get_action
        
        tag_limit = 40
        
        data_dict = {}        
        data_dict['limit'] = tag_limit
        data_dict['return_objects'] = True
        results = get_action('tag_list')(context,data_dict)
        c.top_tags = results
    
    def index(self):
        """This handles dados.gov.br's index home page.
        All extra data displayed on the home page should be handled here.
        """
        # news section, parsed from feed
        self.set_news_section()

        # featured datasets section, read from a specific dataset group

        # most recent datasets section
        
        # most viewed datasets section, from ckanext-googleanalytics
        self.set_most_viewed_datasets()

        # top tags section
        self.set_top_tags()
        return super(DadosGovBrHomeController, self).index()
