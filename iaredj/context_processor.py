from django.shortcuts import get_object_or_404

from contents.models import Staff


def is_staff(request):
    u_staff = 0
    # u_staff = get_object_or_404(Staff, user=request.user)
    # print(u_staff.name)
    try:
        u_staff = get_object_or_404(Staff, user=request.user)

    except:
        u_staff = 0
    return {"u_staff": u_staff}
