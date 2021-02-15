from django.shortcuts import render,HttpResponse,redirect

def cantAccessAfterLogin(get_response):
    def middleware(request):
        email=request.session.get('email')
        if email:
            return redirect('/Download/home/')
        else:
            return get_response(request)
    return middleware
