from django.core.paginator import Paginator
from django.db.models import Min, Max
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import generic
import datetime

from .models import Detection


def index(request):
    by_page = 3
    pages_before_after = (by_page - 1) / 2

    min_id = Detection.objects.aggregate(Min('id')).get('id__min')
    max_id = Detection.objects.aggregate(Max('id')).get('id__max')

    if not request.GET.get("id"):
        detections = \
            Detection.objects \
                .order_by("-date")[:by_page]
        detections = list(detections)

        has_pages = len(detections) > 1
        current_id = detections[0].id
        prev_id = False
        next_id = detections[1].id if has_pages and detections[-1].id >= min_id  else False
    else:
        current_id = int(request.GET.get("id"))
        is_min = current_id <= min_id
        is_max = current_id >= max_id

        query_min_id = max(current_id - pages_before_after, 1) \
            if not is_max else current_id - (by_page - 1)
        query_max_id = min(current_id + pages_before_after, max_id) \
            if not is_min else current_id + (by_page - 1)

        detections = \
            Detection.objects\
                .filter(id__gte=query_min_id, id__lte=query_max_id)\
                .order_by("-date")[:by_page]
        detections = list(detections)

        has_pages = len(detections) > 1

        prev_id = current_id + 1 if has_pages and current_id < max_id else False
        next_id = current_id - 1 if has_pages and current_id > min_id else False

    # .filter(id__gte=min_id, id__lte=max_id)\
    # Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])
    # Sample.objects.filter(date__year='2011', date__month='01')
    # Sample.objects.filter(sampledate__gte=datetime.date(2011, 1, 1))

    return render(request, "index.html", {
        "detections": detections,
        "has_items": len(detections) > 0,
        "current_id": current_id,
        "prev_id": prev_id,
        "next_id": next_id,
    })


class DetailView(generic.DetailView):
    model = Detection
    template_name = "detection.html"
