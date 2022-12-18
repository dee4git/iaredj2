from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

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
