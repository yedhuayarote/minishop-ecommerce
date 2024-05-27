from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from . models import *

# Create your views here.


def index(request, c_slug=None):
    print(c_slug)
    if c_slug!=None:
        c_page = get_object_or_404(cate, slug=c_slug)
        prodt = product.objects.filter(category=c_page, available=True)
    else:
        prodt = product.objects.all().filter(available=True)


    paginator = Paginator(prodt, 1)  # number of objects one page contain

    page = request.GET.get('page')
    paginated = paginator.get_page(page)


    cata = cate.objects.all()
    return render(request, 'index.html', {'c': cata, 'p': prodt, "paginated": paginated})



def details(request,c_slug,product_slug):
    prodt = get_object_or_404(product, category__slug=c_slug, slug=product_slug)
    return render(request, 'product-single.html', {'pro': prodt})

def search(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        prod = product.objects.all().filter(Q(name__icontains=query) | Q(desc__icontains=query), available=True)
    if not prod:
        return HttpResponse("<script> alert('not available');window.locations='/';</script>")

    return render(request, 'search.html', {'pr': prod})


