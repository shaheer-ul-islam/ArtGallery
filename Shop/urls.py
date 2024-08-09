from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index),
    path('logout',views.handle_logout),
    path('signup',views.signup,name="signup"),
    path('login',views.handle_login,name="login"),
    path('apply_seller', views.apply_seller, name='apply_seller'),
    path('art/<int:art_id>/', views.art_detail, name='art_detail'),
    path('D_Order', views.order, name='order'),
    path('Direct_Order/<int:art_id>/', views.Direct_Order, name='art_detail'),
    path('add_to_cart/<int:art_id>/', views.add_to_cart, name='art_detail'),
    path('review', views.post_review, name='art_detail'),
    path('cart',views.cart,name="contact"),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('search',views.search,name="search"),
    path('profile/', views.profile_page, name='profile_page'),
    path('delete_art/<int:art_id>/', views.delete_art, name='delete_art'),
    path('add_art', views.add_art, name='add_art'),
    path('tracker', views.tracker, name='track'),
    path("contact",views.contact),
    # path('store/<int:store_id>/', views.store_detail, name='store_detail'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)