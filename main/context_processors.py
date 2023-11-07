
def mobile(request):
    user_agent = request.META['HTTP_USER_AGENT']
    is_mobile = 'Mobile' in user_agent
    return {'is_mobile': is_mobile}

def authenticated_info(request):
    if request.user.is_authenticated:
        return {'request':request,'is_authenticated': True,'username': request.user.username}
    else:
        return {'request':request,'is_authenticated': False}
