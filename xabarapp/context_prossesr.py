from .models import *

def latest_news(request):
    latest_news=News.published.all().order_by('-publish_time')[:10]
    latest_catigorys=Catigor.objects.all()
    context={
        'latest_news':latest_news,
        'latest_catigorys':latest_catigorys
    }

    return context
