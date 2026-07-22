from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Category

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    
    def items(self):
        return Article.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    
    def items(self):
        return Category.objects.all()

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    
    def items(self):
        return ['core:home', 'core:python', 'core:about', 'core:privacy', 'core:terms']
    
    def location(self, item):
        return reverse(item)