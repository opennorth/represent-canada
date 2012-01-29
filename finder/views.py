from django.shortcuts import render_to_response
from django.template import RequestContext

from boundaries.models import BoundarySet
try:
    from representatives.models import RepresentativeSet
    USE_REPS = True
except ImportError:
    USE_REPS = False

def index(request):
    sets = list(BoundarySet.objects.all().order_by('name').values('slug', 'name'))
    set_slugs_with_reps = dict(RepresentativeSet.objects.all().values_list('boundary_set', 'slug'))
    for s in sets:
        s['reps'] = set_slugs_with_reps.get(s['slug'])
    return render_to_response('index.html', RequestContext(request, {'boundary_sets': sets}))

def api(request):
    return render_to_response('api.html', RequestContext(request))
