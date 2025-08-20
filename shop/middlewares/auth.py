from django.shortcuts import redirect

def auth_middleware(get_response):
    def middleware(request, *args, **kwargs):
        if not request.session.get('user'):
            return redirect('login')
        return get_response(request, *args, **kwargs)
    return middleware