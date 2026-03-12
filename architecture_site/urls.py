from django.contrib import admin
from django.urls import path
from portfolio import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# SITEMAP IMPORT
from django.contrib.sitemaps.views import sitemap
from portfolio.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

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

    # SITEMAP URL
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # ADD THIS LINE
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)