# -*- coding: utf-8 -*-
from ckan.lib.base import c, g, h, model
from ckan.controllers.package import PackageController

class DadosGovBrDatasetController(PackageController):
    """A customized controller for the dataset related views on the
    ckanext-dadosgovbr theme.
    """
    def read(self, id, format="html"):
        import re
        subject = c.pkg_extras.get(VCGE, None)
        vcge_re = r"([^[]+)\s*\[(http://[^[\]]+)\]\s?[,;]?\s?"
        c.subjects = []
        if subject:
            for name, url in re.findall(subject):
                c.subjects.append((name,url))
        return super(DadosGovBrDatasetController, self).read(id, format)
