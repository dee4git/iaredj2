from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

from django.core import serializers
from . import forms


def get_things(key):
    if key == 'Staffs':
        data = serializers.serialize("python", Staff.objects.filter(hidden=False))
        pks = Staff.objects.filter(hidden=False)
        fields = Staff._meta.get_fields()
    elif key == 'White-papers':
        data = serializers.serialize("python", WhitePaper.objects.filter(hidden=False))
        pks = WhitePaper.objects.filter(hidden=False)
        fields = WhitePaper._meta.get_fields()
    elif key == 'Solutions':
        data = serializers.serialize("python", Solution.objects.filter(hidden=False))
        pks = Solution.objects.filter(hidden=False)
        fields = Solution._meta.get_fields()
    elif key == 'Solution-categories':
        data = serializers.serialize("python", SolutionCategory.objects.filter(hidden=False))
        pks = SolutionCategory.objects.filter(hidden=False)
        fields = SolutionCategory._meta.get_fields()
        fields = fields[1:]
    return data, pks, fields


def get_hidden_things(key):
    if key == 'Staffs':
        data = serializers.serialize("python", Staff.objects.filter(hidden=True))
        pks = Staff.objects.filter(hidden=True)
        fields = Staff._meta.get_fields()
    elif key == 'White-papers':
        data = serializers.serialize("python", WhitePaper.objects.filter(hidden=True))
        pks = WhitePaper.objects.filter(hidden=True)
        fields = WhitePaper._meta.get_fields()
    elif key == 'Solutions':
        data = serializers.serialize("python", Solution.objects.filter(hidden=True))
        pks = Solution.objects.filter(hidden=True)
        fields = Solution._meta.get_fields()
    elif key == 'Solution-categories':
        data = serializers.serialize("python", SolutionCategory.objects.filter(hidden=True))
        pks = SolutionCategory.objects.filter(hidden=True)
        fields = SolutionCategory._meta.get_fields()
        fields = fields[1:]
    return data, pks, fields


def control_center(request, key):
    if request.user.is_superuser:
        data, pks, fields = get_things(key)
        hidden, hid_pks, fields = get_hidden_things(key)

        # print('data: ', len(data), len(pks))
        # print('hidden: ', len(hidden), len(hid_pks))

        my_list = zip(data, pks)
        hidden = zip(hidden, hid_pks)
        return render(request, 'control-center.html', {
            "my_list": my_list,
            "hidden": hidden,
            "key": key,
            "fields": fields,
        })

    else:
        return HttpResponse('Unauthorised Access')


def form_selector(request, key, obj):
    if key == 'Staffs':
        return forms.StaffForm(request.POST or None, request.FILES or None, instance=obj)
    elif key == 'White-papers':
        return forms.WhitePaperForm(request.POST or None, request.FILES or None, instance=obj)
    elif key == 'Solutions':
        return forms.SolutionForm(request.POST or None, request.FILES or None, instance=obj)
    elif key == 'Solution-categories':
        return forms.SolutionCategoryForm(request.POST or None, request.FILES or None, instance=obj)


def create(request, key):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = form_selector(request, key, None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('control-center', key)
        else:
            form = form_selector(request, key, None)
        return render(request, 'crud-template.html',
                      {
                          "form": form,
                          "context": 'Create New ' + key
                      },
                      )
    else:
        return HttpResponse('Unauthorised Access')


def object_selector(request, key, pk):
    if key == 'Staffs':
        return Staff.objects.get(pk=pk)
    elif key == 'White-papers':
        return WhitePaper.objects.get(pk=pk)
    elif key == 'Solutions':
        return Solution.objects.get(pk=pk)
    elif key == 'Solution-categories':
        return SolutionCategory.objects.get(pk=pk)


def update(request, key, pk):
    obj = object_selector(request, key, pk)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = form_selector(request, key, obj)
            if form.is_valid():
                instance = form.save(commit=False)
                print(instance.hidden)
                instance.hidden = False
                instance.save()
                return redirect('control-center', key)
        else:
            form = form_selector(request, key, obj)
        return render(request, 'crud-template.html',
                      {
                          "form": form,
                          "context": 'update ' + key
                      },
                      )
    else:
        return HttpResponse('Unauthorised Access')


def hide(request, key, pk):
    obj = object_selector(request, key, pk)
    obj.hidden = True
    obj.save()
    return redirect('control-center', key)


def destroy(request, key, pk):
    obj = object_selector(request, key, pk)
    obj.delete()
    return redirect('control-center', key)


def view_profile(request, s_id):
    edit_access = 0
    staff = get_object_or_404(Staff, pk=s_id)
    try:
        current_staff = get_object_or_404(Staff, user=request.user)
    except:
        current_staff = None
    if staff == current_staff:
        edit_access = 1
    return render(request, 'view-profile.html', {
        'staff': staff,
        'edit_access': edit_access,
    })


@login_required
def set_profile(request):
    if request.method == 'POST':
        form = form_selector(request, 'Staffs', None)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('home')
    else:
        form = form_selector(request, 'Staffs', None)
        # form.fields['user'].disabled = 'disabled'
        form.fields['hidden'].disabled = 'disabled'
    return render(request, 'crud-template.html',
                  {
                      "form": form,
                      "context": 'Set Profile'
                  },
                  )


@login_required
def update_profile(request, pk):
    key = 'Staffs'
    obj = object_selector(request, key, pk)
    print(obj.user)
    print(request.user)
    if obj.user == request.user:
        if request.method == 'POST':
            form = form_selector(request, key, obj)
            if form.is_valid():
                instance = form.save(commit=False)
                print(instance.hidden)
                # instance.hidden = False
                instance.save()
                return redirect('view-profile', pk)
        else:
            form = form_selector(request, key, obj)
            # form.fields['user'].disabled = 'disabled'
        return render(request, 'crud-template.html',
                      {
                          "form": form,
                          "context": 'update ' + key
                      },
                      )
    else:
        return HttpResponse('Unauthorised Access')
