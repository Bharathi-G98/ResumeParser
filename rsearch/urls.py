from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

app_name = 'rsearch'

urlpatterns = [

    url('user_detail/',views.justrender, name='user_detail'),
    path('user_detail_search/<str:userName>/<str:phone>/<str:email>/<str:college>/<str:degree>/<str:grad_year>/<str:company>/', views.get_user_details, name='user_detail_search'),
    path('uploaded/', views.upload, name='uploaded')

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
