from django.contrib import admin
from .models import Post, Category, BlogSettings
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    exclude = ['posted', 'author']
    prepopulated_fields = {'slug': ('title',),}

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogSettings)

