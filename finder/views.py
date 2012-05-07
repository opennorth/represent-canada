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
  # @todo Can we put this logic in the model, without making it Canada-specific?
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

  # http://www12.statcan.ca/census-recensement/2006/dp-pd/hlt/97-550/Index.cfm?TPL=P1C&Page=RETR&LANG=Eng&T=307&S=3&O=D&RPP=699
  populations = {
    'Brampton City Council'        : 433806,
    'Caledon City Council'         : 57050,
    'Calgary City Council'         : 988193,
    'Charlottetown City Council'   : 32174,
    'Edmonton City Council'        : 730372,
    'London City Council'          : 352395,
    'Mississauga City Council'     : 668549,
    'Conseil municipal de Montréal': 1620693,
    'Ottawa City Council'          : 812129,
    'Conseil municipal de Québec'  : 491142,
    'Regina City Council'          : 179246,
    'Stratford Town Council'       : 7083,
    'Summerside City Council'      : 14500,
    'Toronto City Council'         : 2503281,
    'Vancouver City Council'       : 578041,
    'Windsor City Council'         : 216473,
  }

  boundary_sets = list(BoundarySet.objects.all().order_by('name').values('slug', 'name', 'domain'))
  representative_sets = list(RepresentativeSet.objects.all().values('slug', 'name', 'boundary_set'))

  # Partition representative sets into those that are associated to a boundary
  # set and those that are not.
  total = 0
  by_boundary_set = defaultdict(list)
  no_boundary_set = []
  for x in representative_sets:
    if x.get('boundary_set'):
      by_boundary_set[x['boundary_set']].append(x)
    else:
      no_boundary_set.append(x)
    if populations.get(x['name']):
      total += populations[x['name']]

  # Associate boundary sets to representative sets and group them by level of
  # government. @todo Couldn't we use Django associations?
  categories = defaultdict(list)
  for boundary_set in boundary_sets:
    boundary_set['representative_sets'] = by_boundary_set.get(boundary_set['slug'], [])
    categories[domain_to_category_map.get(boundary_set['domain'], 'Municipal')].append(boundary_set)

  return render_to_response('index.html', RequestContext(request, {
    'categories': dict(categories), # @wtf Django templates can't iterate defaultdict
    # Add remaining representative sets to the default level of government.
    'representative_sets': {'Municipal': no_boundary_set},
    # Source for "most comprehensive" claim: http://www.azavea.com/products/cicero/about/availability/
    'progress': round(total / 31612897.0 * 100),
  }))

def api(request):
  return render_to_response('api.html', RequestContext(request))
