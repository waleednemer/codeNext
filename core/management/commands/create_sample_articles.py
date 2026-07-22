from django.core.management.base import BaseCommand
from blog.models import Category, Article
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'إنشاء مقالات تجريبية للاختبار'

    def handle(self, *args, **kwargs):
        # الحصول على التصنيفات
        try:
            basics = Category.objects.get(slug='python-basics')
            oop = Category.objects.get(slug='python-oop')
            advanced = Category.objects.get(slug='python-advanced')
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ قم بإنشاء التصنيفات أولاً: python manage.py create_initial_data'))
            return
        
        sample_articles = [
            {
                'title': 'مقدمة إلى لغة Python',
                'category': basics,
                'excerpt': 'تعرف على لغة Python ولماذا تعتبر الخيار الأمثل للمبتدئين في عالم البرمجة.',
                'content': '<h2>ما هي لغة Python؟</h2><p>بايثون هي لغة برمجة عالية المستوى، سهلة التعلم، ومتعددة الاستخدامات...</p>',
            },
            {
                'title': 'تثبيت Python على جهازك',
                'category': basics,
                'excerpt': 'دليل خطوة بخطوة لتثبيت Python على أنظمة Windows، macOS، و Linux.',
                'content': '<h2>تحميل Python</h2><p>لتحميل Python، اذهب إلى الموقع الرسمي python.org...</p>',
            },
            {
                'title': 'المتغيرات وأنواع البيانات',
                'category': basics,
                'excerpt': 'تعلم كيفية تعريف المتغيرات والتعامل مع أنواع البيانات المختلفة في Python.',
                'content': '<h2>المتغيرات في Python</h2><p>المتغير هو مساحة في الذاكرة لتخزين البيانات...</p>',
            },
            {
                'title': 'مقدمة إلى الكلاسات في Python',
                'category': oop,
                'excerpt': 'تعلم مفهوم الكلاسات والكائنات في Python وكيفية إنشائها.',
                'content': '<h2>ما هي الكلاسات؟</h2><p>الكلاس هو قالب لإنشاء الكائنات...</p>',
            },
            {
                'title': 'الوراثة في Python',
                'category': oop,
                'excerpt': 'فهم مفهوم الوراثة Inheritance في البرمجة كائنية التوجه.',
                'content': '<h2>الوراثة Inheritance</h2><p>الوراثة تسمح للكلاس ب inheriting خصائص وطرق كلاس آخر...</p>',
            },
            {
                'title': 'مقدمة إلى الديكورات Decorators',
                'category': advanced,
                'excerpt': 'تعلم كيف تعمل الديكورات في Python وكيفية استخدامها.',
                'content': '<h2>ما هي الديكورات؟</h2><p>الديكورات هي دوال تعدل سلوك دوال أخرى...</p>',
            },
        ]
        
        created_count = 0
        for article_data in sample_articles:
            slug = slugify(article_data['title'])
            article, created = Article.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': article_data['title'],
                    'category': article_data['category'],
                    'excerpt': article_data['excerpt'],
                    'content': article_data['content'],
                    'is_published': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ تم إنشاء المقال: {article.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ المقال موجود مسبقاً: {article.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 تم إنشاء {created_count} مقالات جديدة'))
        self.stdout.write(self.style.SUCCESS(f'📊 إجمالي المقالات: {Article.objects.count()}'))
