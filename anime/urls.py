from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'animes', views.AnimeViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'users', views.UserRegistrationView)

urlpatterns = [
    path('register/', views.registerPage, name = "register"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),

    path('', views.home, name = 'home'),
    
    path('anime_search/', views.anime_search, name='anime_search'),
    path('anime/add/', views.add_anime, name='add_anime'),
    path('anime/<int:id>/', views.anime_detail, name='anime_detail'),
    path('anime/<int:id>/update/', views.update_anime, name='update_anime'),
    path('anime/<int:id>/delete/', views.delete_anime, name='delete_anime'),
    path('anime/<int:id>/update_status/', views.update_anime_status, name='update_anime_status'),

    path('animes/', views.anime_list, name='anime_list'),

    path('api/', include(router.urls)),

    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),

    path('recommendation/', views.recommendation, name='recommendation'),
    path('random-anime/', views.random_anime, name='random_anime'),

    path('history/', views.anime_history, name='anime_history'),
]