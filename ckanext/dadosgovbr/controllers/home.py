from ckan.lib.base import c, g, h, model
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
        
        tag_limit = 28
        
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
        
        data_dict = {
            'all_fields': True,
            'return_objects': True,
        }
        results = get_action('tag_list')(context,data_dict)
        tags = [
            (
                g.site_url+'tag/'+result['name'],
                result['name'],
                len(result['packages'])
            ) for result in results ]
        c.top_tags = sorted(tags, key=lambda result: result[2], reverse=True)[:tag_limit]

    @classmethod
    def set_featured_datasets(cls):
        """Sets the c.featured_datasets variable for a template to render.
        """
        from ckan.logic import get_action
        from random import shuffle
        from copy import deepcopy

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
        
        data_dict = {'id': 'dados-em-destaque'}
        results = deepcopy(get_action('group_package_show')(context,data_dict))
        shuffle(results)
        results = results[:3]
        c.featured_datasets = [
            (
                g.site_url+'dataset/'+result['name'],
                cls.limita_tamanho(result['title'],70),
                cls.limita_tamanho(result['notes'],155),
            )
            for result in results]

    @classmethod
    def set_most_recent_datasets(cls):
        """Sets the c.most_recent_datasets variable for a template to render.
        """
        import ckan.lib.dictization as d
        from ckan.logic import get_action
        from sqlalchemy import desc

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
  
        #model = context['model']
        query = model.Session.query(model.Package, model.Activity)
        query = query.filter(model.Activity.object_id==model.Package.id)
        query = query.filter(model.Activity.activity_type == 'new package')
        query = query.filter(model.Package.state == 'active')
        query = query.order_by(desc(model.Activity.timestamp))
        query = query.limit(5)
        most_recent_from_bd = query.all()

        #Query:
        #select act.activity_type, act.timestamp, pck.name
        #from activity act
        #join package pck on pck.id = act.object_id
        #where act.activity_type = 'new package' and pck.state = 'active' order by act.timestamp desc;
        
        #Trace of how i got to the final line =p
        #model_dictize.package_dictize
        #obj_list_dictize
        #recent_dict = model_dictize.package_dictize(most_recent_from_bd, context)

        c.most_recent_datasets = d.obj_list_dictize(most_recent_from_bd, context)

    def index(self):
        """This handles dados.gov.br's index home page.
        All extra data displayed on the home page should be handled here.
        """
        # news section, parsed from feed
        self.set_news_section()

        # featured datasets section, read from a specific dataset group
        self.set_featured_datasets()

        # most recent datasets section
        self.set_most_recent_datasets()
        
        # most viewed datasets section, from ckanext-googleanalytics
        self.set_most_viewed_datasets()

        # top tags section
        self.set_top_tags()

        return super(DadosGovBrHomeController, self).index()

