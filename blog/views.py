from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Article

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # ترتيب تصاعدي: الدرس 1 ثم 2 ثم 3... إلخ
    articles_list = category.articles.filter(is_published=True).order_by('created_at')
    
    sort = request.GET.get('sort')
    if sort == 'popular':
        articles_list = category.articles.filter(is_published=True).order_by('-views')
    elif sort == 'newest':
        articles_list = category.articles.filter(is_published=True).order_by('-created_at')
    
    paginator = Paginator(articles_list, 9)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    context = {
        'category': category,
        'articles': articles,
    }
    return render(request, 'blog/category.html', context)

def article_list(request):
    articles_list = Article.objects.filter(is_published=True)
    
    sort = request.GET.get('sort', 'newest')
    if sort == 'popular':
        articles_list = articles_list.order_by('-views')
    elif sort == 'oldest':
        articles_list = articles_list.order_by('created_at')
    else:
        articles_list = articles_list.order_by('-created_at')
    
    paginator = Paginator(articles_list, 12)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    context = {
        'articles': articles,
    }
    return render(request, 'blog/article_list.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    article.views += 1
    article.save()
    
    context = {
        'article': article,
        'next_article': article.next_article(),
        'previous_article': article.previous_article(),
        'similar_articles': article.similar_articles(),
    }
    return render(request, 'blog/article_detail.html', context)
