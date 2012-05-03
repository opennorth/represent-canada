# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from collections import defaultdict
from boundaries.models import BoundarySet

try:
  from representatives.models import RepresentativeSet
  USE_REPS = True
except ImportError:
  USE_REPS = False

def index(request):
  domain_to_category_map = {
    'Canada'                   : 'Federal',
    'British Columbia'         : 'Provincial',
    'Alberta'                  : 'Provincial',
    'Saskatchewan'             : 'Provincial',
    'Manitoba'                 : 'Provincial',
    'Ontario'                  : 'Provincial',
    u'Québec'                  : 'Provincial',
    'New Brunswick'            : 'Provincial',
    'Prince Edward Island'     : 'Provincial',
    'Nova Scotia'              : 'Provincial',
    'Newfoundland and Labrador': 'Provincial',
    'Yukon'                    : 'Territorial',
    'Northwest Territories'    : 'Territorial',
    'Nuvavut'                  : 'Territorial',
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
