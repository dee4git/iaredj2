from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import FileResponse, Http404

from contents.models import *


def home(request):
    """views the home page
    u_stuff is user as stuff. currently logged in user as stuff"""

    staffs = Staff.objects.filter(hidden=False).order_by('level')
    solution_categories = SolutionCategory.objects.filter(hidden=False)
    white_papers = WhitePaper.objects.filter(hidden=False)
    return render(request, "index.html", {
        "staffs": staffs,
        "solution_categories": solution_categories,
        "white_papers": white_papers,
    })


def browse_products(request, key):
    category = get_object_or_404(SolutionCategory, name=key)
    print(category)
    solutions = Solution.objects.filter(hidden=False, solution_category=category)
    print(len(solutions))
    return render(request, 'browse-products.html', {
        "solutions": solutions,
        "key": key,
    })


def pdf_view(request, file):
    try:
        return FileResponse(open(file, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


def white_paper_view(request, pk):

    paper = get_object_or_404(WhitePaper, pk=pk)
    return redirect('home')

    # paper = paper.pdf.url

    # # pdf = pdf_view(request, paper.pdf.url)
    # return render(request, 'white-paper-view.html', {
    #     "paper": paper,
    #     # "pdf": pdf,
    # })
