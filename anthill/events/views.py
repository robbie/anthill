from datetime import datetime
from django.views.generic import simple, date_based, list_detail
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from anthill.events.models import Event, Attendance
from anthill.events.forms import EventForm, SearchForm, AttendForm

def search(request):
    upcoming_events = Event.objects.future().select_related()[0:5]
    if request.GET:
        form = SearchForm(request.GET)
        form.is_valid()
        name = form.cleaned_data['name']
        location = form.cleaned_data['location']
        location_range = form.cleaned_data['location_range']

        # only events that haven't happened
        events = Event.objects.future().select_related()
        if name:
            events = events.filter(title__icontains=name)
        if location:
            events = events.search_by_distance(location, location_range)
        context = {'form': form, 'searched': True, 'search_results': events,
                   'event_list': upcoming_events}
    else:
        context = {'form': SearchForm(), 'event_list': upcoming_events}

    return render_to_response('events/search.html', context,
                              context_instance=RequestContext(request))

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    now = datetime.now()
    if event.end_date:
        finished = event.end_date < now
    else:
        finished = event.start_date < now

    if not finished and request.method == 'POST' and request.user.is_authenticated():
        form = AttendForm(request.POST)
        if form.is_valid():
            Attendance.objects.create(user=request.user, event_id=event_id,
                                      guests=form.cleaned_data['guests'],
                                      message=form.cleaned_data['message'])
    else:
        form = AttendForm()
    return render_to_response('events/event_detail.html',
                              {'event':event, 'form':form, 'finished':finished},
                              context_instance=RequestContext(request))

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.creator != request.user:
        return HttpResponseForbidden('Only the creator of an event may edit it.')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect(event.get_absolute_url())
    else:
        form = EventForm(instance=event)

    return render_to_response('events/edit_event.html',
                              {'form':form, 'event':event},
                             context_instance=RequestContext(request))

@login_required
def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect(event.get_absolute_url())
    else:
        form = EventForm()

    return render_to_response('events/edit_event.html',
                              {'form':form},
                             context_instance=RequestContext(request))

def archive(request):
    return list_detail.object_list(request,
                                   queryset=Event.objects.future().select_related().all(),
                                   template_object_name='event')

def archive_year(request, year):
    return date_based.archive_year(request, year=year,
                                   queryset=Event.objects.all(),
                                   allow_future=True,
                                   date_field='start_date',)

def archive_month(request, year, month):
    return date_based.archive_month(request, year=year, month=month,
                                    queryset=Event.objects.all(),
                                    date_field='start_date', month_format='%m',
                                    allow_future=True,
                                    template_object_name='event')
