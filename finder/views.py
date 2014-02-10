# coding: utf-8
from coffin.shortcuts import render_to_response
from django.template import RequestContext
from collections import defaultdict
from boundaries.models import BoundarySet

try:
  from representatives.models import RepresentativeSet
except ImportError:
  pass

from finder.populations import population_by_boundary_set, population_by_representative_set

def index(request):
  aggregations = {
    # https://scraperwiki.com/docs/api?name=alberta_municipal_affairs#sqlite
    # SELECT * FROM swvariables;
    'Municipal officials of Alberta': 1056096,
    # https://scraperwiki.com/docs/api?name=civicinfo_bc#sqlite
    # SELECT * FROM swvariables;
    'Municipal officials of British Columbia': 3311861,
    # https://scraperwiki.com/docs/api?name=alberta_municipal_affairs#sqlite
    # SELECT SUM(population) FROM municipalities;
    u'Élus municipaux du Québec': 1292650, # source is MAMROT
  }

  boundary_sets = list(BoundarySet.objects.all().values('name'))
  bounded = 0
  for x in boundary_sets:
    if population_by_boundary_set.get(x['name']):
      bounded += population_by_boundary_set[x['name']]

  for k, v in aggregations.iteritems():
    bounded += v

  representative_sets = list(RepresentativeSet.objects.all().values('name'))
  represented = 0
  for x in representative_sets:
    if aggregations.get(x['name']):
      represented += aggregations[x['name']]
    else:
      if population_by_representative_set.get(x['name']):
        represented += population_by_representative_set[x['name']]

  return render_to_response('index.html', RequestContext(request, {
    'boundary_progress': int(bounded / 33476688.0 * 100),
    # Source for "most comprehensive" claim: http://www.azavea.com/products/cicero/about/availability/
    'representative_progress': int(represented / 33476688.0 * 100),
  }))

def data(request):
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

  # Partition representative sets into those that are associated to a boundary
  # set and those that are not.
  by_boundary_set = defaultdict(list)
  no_boundary_set = []
  for x in representative_sets:
    if x.get('boundary_set'):
      by_boundary_set[x['boundary_set']].append(x)
    else:
      no_boundary_set.append(x)

  # Associate boundary sets to representative sets and group them by level of
  # government.
  categories = defaultdict(list)
  for boundary_set in boundary_sets:
    boundary_set['representative_sets'] = by_boundary_set.get(boundary_set['slug'], [])
    categories[domain_to_category_map.get(boundary_set['domain'], 'Municipal')].append(boundary_set)

  return render_to_response('data.html', RequestContext(request, {
    'categories': categories,
    # Add remaining representative sets to the default level of government.
    'representative_sets': {'Municipal': no_boundary_set},
  }))

def api(request):
  return render_to_response('api.html', RequestContext(request))

def privacy(request):
  return render_to_response('privacy.html', RequestContext(request))
