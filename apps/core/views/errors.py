from django.shortcuts import render_to_response



def handler400():
    response = render_to_response("400.html")
    response.status_code = 400
    return response


def handler403():
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handler404():
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handler500():
    response = render_to_response('500.html')
    response.status_code = 500
    return response
