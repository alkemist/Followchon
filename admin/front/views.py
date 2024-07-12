from detections.models import Capture
from django.db.models import Min, Max
from django.shortcuts import render
from django.views import generic


def index(request):
    by_page = 3
    pages_before_after = (by_page - 1) / 2

    min_id = Capture.objects.aggregate(Min('id')).get('id__min')
    max_id = Capture.objects.aggregate(Max('id')).get('id__max')

    if not request.GET.get("id"):
        captures = \
            Capture.objects \
                .order_by("-date")[:by_page]
        captures = list(captures)

        has_pages = len(captures) > 1
        current_id = captures[0].id
        prev_id = False
        next_id = captures[1].id if has_pages and captures[-1].id >= min_id else False
    else:
        current_id = int(request.GET.get("id"))
        is_min = current_id <= min_id
        is_max = current_id >= max_id

        query_min_id = max(current_id - pages_before_after, 1) \
            if not is_max else current_id - (by_page - 1)
        query_max_id = min(current_id + pages_before_after, max_id) \
            if not is_min else current_id + (by_page - 1)

        captures = \
            Capture.objects \
                .filter(id__gte=query_min_id, id__lte=query_max_id) \
                .order_by("-date")[:by_page]
        captures = list(captures)

        has_pages = len(captures) > 1

        prev_id = current_id + 1 if has_pages and current_id < max_id else False
        next_id = current_id - 1 if has_pages and current_id > min_id else False

    return render(request, "index.html", {
        "captures": captures,
        "has_items": len(captures) > 0,
        "current_id": current_id,
        "prev_id": prev_id,
        "next_id": next_id,
    })


class DetailView(generic.DetailView):
    model = Capture
    template_name = "capture.html"
