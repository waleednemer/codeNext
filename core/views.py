from django.shortcuts import render
from blog.models import Category, Article

def home(request):
    categories = Category.objects.all().order_by('order')
    latest_articles = Article.objects.filter(is_published=True).order_by('-created_at')[:6]
    popular_articles = Article.objects.filter(is_published=True).order_by('-views')[:6]
    context = {
        'categories': categories,
        'latest_articles': latest_articles,
        'popular_articles': popular_articles,
    }
    return render(request, 'core/home.html', context)

def python_page(request):
    # تصنيفات Python فقط
    categories = Category.objects.filter(slug__startswith='python').order_by('order')
    context = {'categories': categories}
    return render(request, 'core/python.html', context)

def odoo_page(request):
    # تصنيفات Odoo فقط
    categories = Category.objects.filter(slug__startswith='odoo').order_by('order')
    context = {'categories': categories}
    return render(request, 'core/odoo.html', context)

def about(request):
    return render(request, 'core/about.html')

def privacy_policy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)
