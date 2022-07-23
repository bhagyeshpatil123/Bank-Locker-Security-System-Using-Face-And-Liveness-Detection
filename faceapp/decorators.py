from django.http import HttpResponseRedirect
from django.urls import reverse


def user_login_required(view_func, login_url=None):
    def wrap(request, *args, **kwargs):
        if 'user_id' in request.session and 'user_name' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            print("*"*7,login_url)
            if login_url:
                return HttpResponseRedirect(login_url)
            return HttpResponseRedirect(reverse('user_logout'))
    return wrap
