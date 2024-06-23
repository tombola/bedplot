from django.shortcuts import render
from .models import Bed


def bed_list(request):
    beds = Bed.objects.all()
    return render(request, 'beds/bed_list.html', {'beds': beds})