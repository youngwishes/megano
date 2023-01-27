from django.shortcuts import render


def csrf_failure(request, reason='', **kwargs):
    return render(request, template_name='errors/403.html', status=403)


def page_not_found(request, exception):
    return render(request, template_name='errors/404.html', status=404)
