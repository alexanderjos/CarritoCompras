from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from accounts import views
from core.views import home
from accounts.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(home), name='home'),
    # URLs de autenticación
    path('login/', login_view, name='login'),
    path('accounts/login/', login_view, name='login'),  # <-- Esta línea es clave
    path('logout/', logout_view, name='logout'),
    # Incluir URLs de apps
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
    # URLs para el Carrito de Compras
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('carrito/agregar/<uuid:articulo_id>/', views.cart_add,name='cart_add'),
    path('carrito/eliminar/<uuid:articulo_id>/', views.cart_remove,name='cart_remove'),
    path('carrito/vaciar/', views.cart_clear, name='cart_clear'),
    path('checkout/', views.checkout, name='checkout'),
    path('orden/<uuid:pedido_id>/', views.order_detail, name='order_detail'),
    path('orden/cancelar/<uuid:pedido_id>/', views.cancel_order,name='cancel_order'),
    path('orden/pdf/<uuid:pedido_id>/', views.generate_pdf_order,name='generate_pdf_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
