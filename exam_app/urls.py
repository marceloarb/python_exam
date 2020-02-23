from django.urls import path
from . import views	

urlpatterns = [
    path('', views.index),
    path('users', views.createUser),
    path('login', views.login),
    path('homepage', views.homepage),
    path('delete_session', views.delete_session),
    path('profile/<int:id>', views.userProfile),
    path('quote', views.createQuote),
    path('like/<int:id>',views.likeQuote),
    path('delete/<int:id>', views.delete_Quote),
    path('display_update/<int:id>', views.display_update),
    path('edit_user/<int:id>', views.edit_user),
]