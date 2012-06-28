# coding: utf-8
from coffin.shortcuts import render_to_response
from django.template import RequestContext
from collections import defaultdict
from boundaries.models import BoundarySet

try:
  from representatives.models import RepresentativeSet
except ImportError:
  pass

def index(request):
  # http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/Table-Tableau.cfm?LANG=Eng&TABID=1&T=301&SR=1&RPP=200&S=3&O=D&CMA=0&PR=0#C2
  populations = {
    'Brampton City Council'           : 523911,
    'Caledon City Council'            : 59460,
    'Calgary City Council'            : 1096833,
    'Cambridge City Council'          : 126748,
    'Charlottetown City Council'      : 34562,
    'Edmonton City Council'           : 812201,
    'Conseil municipal de Gatineau'   : 265349,
    'Greater Sudbury City Council'    : 160274,
    'Guelph City Council'             : 121688,
    'Halifax City Council'            : 390096,
    'Kitchener City Council'          : 219153,
    'Conseil municipal de Lévis'      : 138769,
    'London City Council'             : 366151,
    'Mississauga City Council'        : 713443,
    'Conseil municipal de Montréal'   : 1649519,
    'Oakville Town Council'           : 182520,
    'Ottawa City Council'             : 883391,
    'Conseil municipal de Québec'     : 516622,
    'Regina City Council'             : 193100,
    'Saskatoon City Council'          : 222189,
    'Conseil municipal de Sherbrooke' : 154601,
    'Stratford Town Council'          : 8574,
    'Summerside City Council'         : 14751,
    'Toronto City Council'            : 2615060,
    'Windsor City Council'            : 210891,
    'Winnipeg City Council'           : 663617,
    'Vancouver City Council'          : 603502,
    # Population totals are done by each script.
    'Municipal officials of Alberta': 1056096,
    'Municipal officials of British Columbia': 3311861,
    u'Élus municipaux du Québec': 1292650, # source is MAMROT
  }

  representative_sets = list(RepresentativeSet.objects.all().values('slug', 'name', 'boundary_set'))

  total = 0
  for x in representative_sets:
    if populations.get(x['name']):
      total += populations[x['name']]

  # @todo display the total number of representatives and boundaries in the database
  return render_to_response('index.html', RequestContext(request, {
    # Source for "most comprehensive" claim: http://www.azavea.com/products/cicero/about/availability/
    'progress': int(total / 33476688.0 * 100),
  }))

def data(request):
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
  # government. @todo Couldn't we use Django associations?
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
