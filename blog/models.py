from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="الرابط")
    description = models.TextField(blank=True, verbose_name="الوصف")
    order = models.IntegerField(default=0, verbose_name="الترتيب")
    
    class Meta:
        verbose_name = "تصنيف"
        verbose_name_plural = "التصنيفات"
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])
    
    def article_count(self):
        return self.articles.filter(is_published=True).count()


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="العنوان")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="الرابط")
    excerpt = models.TextField(max_length=500, verbose_name="نبذة")
    content = RichTextField(verbose_name="المحتوى")
    featured_image = models.ImageField(
        upload_to='articles/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="الصورة الرئيسية"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="التصنيف"
    )
    tags = TaggableManager(blank=True, verbose_name="الوسوم")
    views = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    is_published = models.BooleanField(default=True, verbose_name="منشور")
    
    class Meta:
        verbose_name = "مقال"
        verbose_name_plural = "المقالات"
        ordering = ['created_at']  # ترتيب تصاعدي: الأقدم أولاً
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.slug])
    
    def reading_time(self):
        words_per_minute = 200
        word_count = len(self.content.split())
        minutes = word_count // words_per_minute
        if minutes == 0:
            return "أقل من دقيقة"
        elif minutes == 1:
            return "دقيقة واحدة"
        elif minutes <= 10:
            return f"{minutes} دقائق"
        else:
            return f"{minutes} دقيقة"
    
    def next_article(self):
        """الدرس التالي في نفس التصنيف"""
        return Article.objects.filter(
            category=self.category,
            created_at__gt=self.created_at,
            is_published=True
        ).order_by('created_at').first()
    
    def previous_article(self):
        """الدرس السابق في نفس التصنيف"""
        return Article.objects.filter(
            category=self.category,
            created_at__lt=self.created_at,
            is_published=True
        ).order_by('-created_at').first()
    
    def similar_articles(self):
        """دروس مشابهة في نفس التصنيف"""
        return Article.objects.filter(
            category=self.category,
            is_published=True
        ).exclude(id=self.id)[:3]
