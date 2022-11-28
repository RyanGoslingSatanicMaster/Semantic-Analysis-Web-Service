from django.shortcuts import render
from django.http import HttpResponse

from main.models import Course, Vacancy


def index(request):
    courses = Course.objects.all()
    vacancies = Vacancy.objects.all()
    return render(request, 'main/parent.html', {'parent': courses, 'child': vacancies})

def vacancy(request):
    courses = Course.objects.all()
    vacancies = Vacancy.objects.all()
    return render(request, 'main/parent.html', {'parent': vacancies, 'child': courses})



