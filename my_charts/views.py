import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
from graphos.sources.model import ModelDataSource
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import BarChart, LineChart, ColumnChart, PieChart
from tablib import Dataset

from .forms import UploadForm
from models import Location, SaveLocation
from .resources import LocationResource


@login_required
def draw(request):

    queryset = Location.objects.filter(user__pk=request.user.id)
    data_source = ModelDataSource(queryset,  fields=['place', 'population'])

    if request.method == 'GET' and not 'charts' in request.GET:
        chart = BarChart(data_source)
    elif request.GET['charts'] == "BarChart":
        chart = BarChart(data_source)
    elif request.GET['charts'] == "LineChart":
        chart = LineChart(data_source)
    elif request.GET['charts'] == "PieChart":
        chart = PieChart(data_source)
    elif request.GET['charts'] == "ColumnChart":
        chart = ColumnChart(data_source)

    context = {'chart': chart}
    return render(request, 'my_charts/draw.html', context)


@login_required
def drawsaved(request, graph_id):

    datasaved = [['place', 'populationn']]
    queryset = SaveLocation.objects.get(id=graph_id)

    for o in queryset.json:
        datasaved.append([o['place'], o['population']])

    data_source = SimpleDataSource(data=datasaved)
    chart = BarChart(data_source)
    context = {'chart': chart}
    return render(request, 'my_charts/drawsaved.html', context)


@login_required
def export_csv(request):
    location_resource = LocationResource()
    queryset = Location.objects.filter(user__pk=request.user.id)
    dataset = location_resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response


@login_required
def export_json(request):
    location_resource = LocationResource()
    queryset = Location.objects.filter(user__pk=request.user.id)
    dataset = location_resource.export(queryset)
    response = HttpResponse(dataset.json, content_type='text/json')
    response['Content-Disposition'] = 'attachment; filename="locations.json"'
    return response


def export_xls(request):
    location_resource = LocationResource()
    queryset = Location.objects.filter(user__pk=request.user.id)
    dataset = location_resource.export(queryset)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


@login_required
def savegraph(request):

    location_resource = LocationResource()
    queryset = Location.objects.filter(user__pk=request.user.id)
    dataset = location_resource.export(queryset)
    j = dataset.json
    SaveLocation.objects.create(user=request.user, json=json.loads(j)).save()
    return HttpResponseRedirect("/charts/draw/")


@login_required
def savedgraphs(request):

    graphs = SaveLocation.objects.filter(user__pk=request.user.id)
    context = {'graphs': graphs}
    return render(request, 'my_charts/savedgraphs.html', context)


@login_required
def simple_upload(request):
    if request.method == 'POST':
        person_resource = LocationResource()
        dataset = Dataset()
        try:
            new_persons = request.FILES['myfile']
            imported_data = dataset.load(new_persons.read())
            result = person_resource.import_data(dataset, dry_run=True)  # Test the data import
            if not result.has_errors():
                person_resource.import_data(dataset, dry_run=False)  # Actually import now
        except Exception as ex:
            print ex.message
    return HttpResponseRedirect("/charts/draw/")


@method_decorator(login_required, name='dispatch')
class ManualUpload(View):
    form_class = UploadForm
    template_name = 'my_charts/upload.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user
            location.save()
            return HttpResponseRedirect(reverse('charts:draw'))

        return render(request, self.template_name, {'form': form})
