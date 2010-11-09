from WikId.wiki.models import Article, Article_section
from django.contrib import admin

class Article_section_inline(admin.StackedInline):
    model = Article_section
    extra = 1
    
class Article_admin(admin.ModelAdmin):
    inlines = [Article_section_inline]
    
admin.site.register(Article, Article_admin)