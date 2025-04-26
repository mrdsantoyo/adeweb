from django.contrib.auth import views as auth_views 
from django.contrib import admin
from django.urls import path, include
from usuarios import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),

    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    
    path('django_plotly_dash/', include(('django_plotly_dash.urls', 'django_plotly_dash'), namespace='the_django_plotly_dash')),
    ]




urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

