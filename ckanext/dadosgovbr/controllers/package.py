# -*- coding: utf-8 -*-
from ckan.lib.base import c, g, h, model
from ckan.controllers.package import PackageController

class DadosGovBrDatasetController(PackageController):
    """A customized controller for the dataset related views on the
    ckanext-dadosgovbr theme.
    """
    def read(self, id, format="html"):
        # method signature to be changed in/after CKAN 1.6.1
        rendered = super(DadosGovBrDatasetController, self).read(id) #, format)
        import re
        extras = c.pkg.extras
        subject = extras.get("VCGE", None)
        vcge_re = r"([^[]+)\s*\[(http://[^[\]]+)\]\s?[,;]?\s?"
        c.subjects = []
        import pdb; pdb.set_trace()
        if subject:
            for name, url in re.findall(vcge_re, subject):
                c.subjects.append((name,url))
        return rendered

