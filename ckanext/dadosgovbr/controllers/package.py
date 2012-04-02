# -*- coding: utf-8 -*-
import datetime

from pylons import config

from ckan.logic import get_action, check_access
from ckan.lib.helpers import date_str_to_datetime
from ckan.logic import NotFound, NotAuthorized, ValidationError
from ckan.lib.base import request, c, BaseController, model, abort, h, g, render
from ckan.lib.base import response, redirect, gettext
from ckan.lib.package_saver import PackageSaver, ValidationException
from ckan.lib.helpers import json
import ckan.logic.action.get

from ckan.controllers.package import PackageController

class DadosGovBrDatasetController(PackageController):
    """A customized controller for the dataset related views on the
    ckanext-dadosgovbr theme.
    """
    def read(self, id):
        package_type = self._get_package_type(id.split('@')[0])
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'extras_as_string': True,
                   'for_view': True}
        data_dict = {'id': id}

        # interpret @<revision_id> or @<date> suffix
        split = id.split('@')
        if len(split) == 2:
            data_dict['id'], revision_ref = split
            if model.is_id(revision_ref):
                context['revision_id'] = revision_ref
            else:
                try:
                    date = date_str_to_datetime(revision_ref)
                    context['revision_date'] = date
                except TypeError, e:
                    abort(400, _('Invalid revision format: %r') % e.args)
                except ValueError, e:
                    abort(400, _('Invalid revision format: %r') % e.args)
        elif len(split) > 2:
            abort(400, _('Invalid revision format: %r') % 'Too many "@" symbols')
            
        #check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            c.pkg_json = json.dumps(c.pkg_dict)
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)
        
        #set a cookie so we know whether to display the welcome message
        c.hide_welcome_message = bool(request.cookies.get('hide_welcome_message', False))
        response.set_cookie('hide_welcome_message', '1', max_age=3600) #(make cross-site?)
        
        # used by dadosgovbr_dataset plugin
        import re
        extras = c.pkg.extras
        subject = extras.get("VCGE", None)
        vcge_re = r"([^[]+)\s*\[(http://[^[\]]+)\]\s?[,;]?\s?"
        c.subjects = []
        if subject:
            for name, url in re.findall(vcge_re, subject):
                c.subjects.append((name,url))
            try:
                del c.pkg.extras["VCGE"]
            except KeyError:
                pass
        
        # used by disqus plugin
        c.current_package_id = c.pkg.id

        # Add the package's activity stream (already rendered to HTML) to the
        # template context for the package/read.html template to retrieve
        # later.
        c.package_activity_stream = \
                ckan.logic.action.get.package_activity_list_html(context,
                    {'id': c.current_package_id})

        if config.get('rdf_packages'):
            accept_header = request.headers.get('Accept', '*/*')
            for content_type, exts in negotiate(autoneg_cfg, accept_header):
                if "html" not in exts: 
                    rdf_url = '%s%s.%s' % (config['rdf_packages'], c.pkg.id, exts[0])
                    redirect(rdf_url, code=303)
                break

        PackageSaver().render_package(c.pkg_dict, context)
        return render('package/read.html')

