from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
def login_required(get_response):

    def middleware(request):
        email=request.session.get('email')
        if email:
            print("......middleware.......")
            response=get_response(request)
            return response
        else:
            print("please Login")
            url=request.path
            print(url)
            return HttpResponseRedirect('/Download/login/')


    return middleware
