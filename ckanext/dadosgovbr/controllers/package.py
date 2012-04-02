# -*- coding: utf-8 -*-
from ckan.lib.base import c, g, h, model
from ckan.controllers.package import PackageController

class DadosGovBrDatasetController(PackageController):
    """A customized controller for the dataset related views on the
    ckanext-dadosgovbr theme.
    """
    def read(self, id, format='html'):
        # Check we know the content type, if not then it is likely a revision
        # and therefore we should merge the format onto the end of id
        ctype,extension,loader = self._content_type_for_format(format)
        if not ctype:
            # Reconstitute the ID if we don't know what content type to use
            ctype = "text/html; charset=utf-8"
            id = "%s.%s" % (id, format)
            format = 'html'
        else:
            format = extension

        response.headers['Content-Type'] = ctype

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
            c.resources_json = json.dumps(c.pkg_dict.get('resources',[]))
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

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

        PackageSaver().render_package(c.pkg_dict, context)

        template = self._read_template( package_type )
        template = template[:template.index('.')+1] + format

        return render( template, loader_class=loader)

