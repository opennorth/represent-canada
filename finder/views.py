# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from collections import defaultdict
from boundaries.models import BoundarySet

try:
  from representatives.models import RepresentativeSet
except ImportError:
  pass

def index(request):
  domain_to_category_map = {
    u'Canada'                   : 'Federal',
    u'British Columbia'         : 'Provincial',
    u'Alberta'                  : 'Provincial',
    u'Saskatchewan'             : 'Provincial',
    u'Manitoba'                 : 'Provincial',
    u'Ontario'                  : 'Provincial',
    u'Québec'                   : 'Provincial',
    u'New Brunswick'            : 'Provincial',
    u'Prince Edward Island'     : 'Provincial',
    u'Nova Scotia'              : 'Provincial',
    u'Newfoundland and Labrador': 'Provincial',
    u'Yukon'                    : 'Territorial',
    u'Northwest Territories'    : 'Territorial',
    u'Nuvavut'                  : 'Territorial',
  }

  boundary_sets = list(BoundarySet.objects.all().order_by('name').values('slug', 'name', 'domain'))
  representative_sets = list(RepresentativeSet.objects.all().values('slug', 'name', 'boundary_set'))

  # @note Assumes boundary sets have at most one representative set.
  representative_sets = dict((x['boundary_set'], x) for x in representative_sets if x.get('boundary_set'))

  categories = defaultdict(list)
  for boundary_set in boundary_sets:
    boundary_set['representative_set'] = representative_sets.get(boundary_set['slug'])
    categories[domain_to_category_map.get(boundary_set['domain'], 'Municipal')].append(boundary_set)

  return render_to_response('index.html', RequestContext(request, {'categories': categories.iteritems()}))

def api(request):
  return render_to_response('api.html', RequestContext(request))
