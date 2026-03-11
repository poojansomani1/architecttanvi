from django.contrib import admin
from django.urls import path
from portfolio import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('p/', views.login_view, name='login'),
    path('o/', views.logout_view, name='logout'),

    path('d/', views.dashboard, name='dashboard'),

    path('a/', views.add_project, name='add_project'),

    path('edit/<int:id>/', views.edit_project, name='edit_project'),

    path('x/<int:id>/', views.delete_project, name='delete_project'),

    path('e/', views.edit_profile, name='edit_profile'),

]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)