from django.contrib import admin
from .models import Category, Article
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'article_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_editable = ['order']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'views', 'created_at', 'is_published', 'image_preview']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="60" height="60" />', obj.featured_image.url)
        return "-"
    image_preview.short_description = "الصورة"