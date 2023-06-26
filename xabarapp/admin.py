from django.contrib import admin
from .models import News,Catigor,Contact

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display=['title','category','publish_time','status','photo']
    list_filter=['status','created_time','publish_time']
    prepopulated_fields={'slug':('title',)}
    date_hierarchy='publish_time'
    search_fields=['title','body']
    ordering=['status','publish_time']

@admin.register(Catigor)
class NewsAdmin(admin.ModelAdmin):
    list_display=['id','name']
    list_filter=['name',]
    search_fields=['name']
    ordering=['name']
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=['name','email']
    search_fields=['name','email','message']
    ordering=['name']
    list_filter=['name','email','message']