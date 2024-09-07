from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('products/', include('product.urls')),
    path('', include('cart.urls')),
    path('', include('blog.urls')),
    path('payments/', include('payment.urls')),
    path('order/', include('order.urls')),
    path('dashboard/', include('admin_dashboard.urls')),

] + debug_toolbar_urls()