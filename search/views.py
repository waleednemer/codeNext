from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from blog.models import Article

def search_view(request):
    query = request.GET.get('q', '')
    articles = Article.objects.none()
    
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query),
            is_published=True
        )
    
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search/search.html', context)