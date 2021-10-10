
from django.urls import path
from django.conf.urls import url 
from users import views 
from .views import RegisterView, LoginView, UserView, LogoutView

urlpatterns = [
    path('api/register', RegisterView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/user', UserView.as_view()),
    path('api/logout', LogoutView.as_view()),
    url (r'^api/utilisateurs$', views.utilisateur_list),
    url(r'^api/utilisateurs/(?P<pk>[0-9]+)$', views.utilisateur_detail),
    url(r'^api/utilisateurs/published$', views.utilisateur_list_published)
]
