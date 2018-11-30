from django.shortcuts import render

# Create your views here.

def vl_home_view(request):
    template_name = 'vanlevy/vl_home.html'
    return render(request, template_name)


def vl_about_view(request):
    template_name = 'vanlevy/vl_about.html'
    return render(request, template_name)


def vl_resources_view(request):
    template_name = 'vanlevy/vl_resources.html'
    return render(request, template_name)


def vl_cool_stuff_view(request):
    template_name = 'vanlevy/vl_cool_stuff.html'
    return render(request, template_name)