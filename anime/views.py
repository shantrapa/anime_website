import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import DatabaseError
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from datetime import date

from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny

from .models import *
from .forms import *
from .decorators import *
from .serializers import *
from .permissions import *


def home(request):
    sort_by = request.GET.get('sort_by', 'rating')
    if sort_by == 'release_date':
        anime_list = Anime.objects.order_by('-release_date')[:20]
    elif sort_by == 'title':
        anime_list = Anime.objects.order_by('title')[:20]
    elif sort_by == 'episodes':
        anime_list = Anime.objects.order_by('-episodes')[:20]
    else:
        anime_list = Anime.objects.order_by('-rating')[:20]

    context = {
        'anime_list': anime_list,
        'sort_by': sort_by,
    }

    return render(request, 'anime/home.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        try:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
        except DatabaseError:
            messages.warning(request, "Registration completed")
            return redirect('login')
    context = {'form': form}
    return render(request, 'anime/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        except DatabaseError as e:
            messages.error(request, 'Database error occurred during login.')
            print(e)            
    context = {} 
    return render(request, 'anime/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user_profile = request.user.animeshnik

    today = date.today()
    age = (
        today.year - user_profile.date_of_birth.year - 
        ((today.month, today.day) < (user_profile.date_of_birth.month, user_profile.date_of_birth.day))
    ) if user_profile.date_of_birth else None

    status_counts = {
            'Буду_смотреть': UserAnimeStatus.objects.filter(user=user_profile, status='Буду смотреть').count(),
            'Смотрю': UserAnimeStatus.objects.filter(user=user_profile, status='Смотрю').count(),
            'Просмотрено': UserAnimeStatus.objects.filter(user=user_profile, status='Просмотрено').count(),
        }
    
    буду_смотреть_anime = UserAnimeStatus.objects.filter(user=user_profile, status='Буду смотреть').values('anime__id', 'anime__title', 'anime__episodes', 'anime__rating')
    смотрю_anime = UserAnimeStatus.objects.filter(user=user_profile, status='Смотрю').values('anime__id', 'anime__title', 'anime__episodes', 'anime__rating')
    просмотрено_anime = UserAnimeStatus.objects.filter(user=user_profile, status='Просмотрено').values('anime__id', 'anime__title', 'anime__episodes', 'anime__rating')
    
    genre_counts = (
        UserAnimeStatus.objects.filter(user=user_profile)
        .values('anime__genres__name')
        .annotate(count=Count('anime__genres'))
        .order_by('-count')
    )
    max_genre_count = genre_counts[0]['count'] if genre_counts else 0 

    for genre in genre_counts:
        genre['width'] = (genre['count'] / max_genre_count) * 100 if max_genre_count > 0 else 0

    context = {
        'user_profile': user_profile,
        'age': age,
        'буду_смотреть_anime': буду_смотреть_anime,
        'смотрю_anime': смотрю_anime,
        'просмотрено_anime': просмотрено_anime,
        'status_counts': status_counts,
        'genre_counts': genre_counts,
        'max_genre_count': max_genre_count,
    }

    return render(request, 'anime/profile.html', context)

def recommendation(request):
    user_profile = request.user.animeshnik

    genre_counts = (
        UserAnimeStatus.objects.filter(user=user_profile)
        .values('anime__genres__name')
        .annotate(count=Count('anime__genres'))
        .order_by('-count')
    )
    max_genre_count = genre_counts[0]['count'] if genre_counts else 0 

    for genre in genre_counts:
        genre['width'] = (genre['count'] / max_genre_count) * 100 if max_genre_count > 0 else 0

    recommendations = []
    genre_counts = (
        UserAnimeStatus.objects.filter(user=user_profile)
        .values('anime__genres__name')
        .annotate(count=Count('anime__genres'))
        .order_by('-count')
    )

    if genre_counts:
        most_popular_genre_name = genre_counts[0]['anime__genres__name']

        added_anime_ids = list(UserAnimeStatus.objects.filter(user=user_profile).values_list('anime__id', flat=True))

        unwatched_anime = Anime.objects.filter(
            genres__name=most_popular_genre_name
        ).exclude(id__in=added_anime_ids).order_by('-rating')

        recommendations = list(unwatched_anime[:20])
        #recommendations = random.sample(list(unwatched_anime), min(20, len(unwatched_anime)))
    else:
        recommendations = list(Anime.objects.all().order_by('-rating')[:20])

    context = {
        'user_profile': user_profile,
        'genre_counts': genre_counts,
        'max_genre_count': max_genre_count,
        'recommendations': recommendations,
        'most_popular_genre': most_popular_genre_name if genre_counts else None,
    }

    return render(request, 'anime/recommendation.html', context)

def random_anime(request):
    random_anime = random.choice(Anime.objects.all())

    return redirect('anime_detail', id=random_anime.id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['animeshnik'])
def settings(request):
    animeshnik = request.user.animeshnik

    form = AnimeshnikForm(instance=animeshnik)

    if request.method == 'POST':
        form = AnimeshnikForm(request.POST, request.FILES, instance=animeshnik)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, 'anime/settings.html', context)

def anime_search(request):
    form = AnimeSearchForm(request.POST or None)
    anime_list = []
    message = ""
    if request.method == 'POST' and form.is_valid():
        title = form.cleaned_data['title']  
        anime_list = Anime.objects.filter(title__icontains=title)
        if anime_list.exists():
            message = f"Результаты поиска для '{title}':"
        else:
            message = f"По запросу '{title}' ничего не найдено."
    context = {
        'form': form,
        'anime_list': anime_list,
        'message': message,       
    }
    return render(request, 'anime/anime_search.html', context)


def anime_detail(request, id):
    anime = get_object_or_404(Anime, id=id)

    user_anime_status = None
    if request.user.is_authenticated:
        try:
            user_animeshnik = request.user.animeshnik
            user_anime_status = UserAnimeStatus.objects.filter(user=user_animeshnik, anime=anime).first()
        except Animeshnik.DoesNotExist:
            user_animeshnik = None

    status_counts = UserAnimeStatus.objects.filter(anime=anime).values('status').annotate(count=Count('status'))
    status_dict = {
        'Буду_смотреть': 0,
        'Смотрю': 0,
        'Просмотрено': 0
    }
    for item in status_counts:
        key = item['status'].replace(' ', '_')
        status_dict[key] = item['count']

    context = {
        'anime': anime,
        'user_anime_status': user_anime_status.status if user_anime_status else None,
        'status_counts': status_dict
    }
    
    return render(request, 'anime/anime_detail.html', context)

@login_required
def update_anime_status(request, id):
    anime = get_object_or_404(Anime, id=id)
    animeshnik = request.user.animeshnik
    
    if request.method == 'POST':
        status = request.POST.get('status')
        
        if status in ['Буду смотреть', 'Смотрю', 'Просмотрено']:
            UserAnimeStatus.objects.update_or_create(
                user=animeshnik,
                anime=anime,
                defaults={'status': status}
            )
    
    return redirect('anime_detail', id=id)

@allowed_users(allowed_roles=['admin', 'moderator'])
def add_anime(request):
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))

    else:
        form = AnimeForm()

    return render(request, 'anime/add_anime.html', {'form': form})

@allowed_users(allowed_roles=['admin', 'moderator'])
def update_anime(request, id):
    anime = get_object_or_404(Anime, id=id)
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES, instance=anime)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('anime_detail', args=[id]))

    else:
        form = AnimeForm(instance=anime)

    return render(request, 'anime/update_anime.html', {'form': form, 'anime': anime})

@allowed_users(allowed_roles=['admin', 'moderator'])
def delete_anime(request, id):
    anime = get_object_or_404(Anime, id=id)
    if request.method == 'POST':
        anime.delete()
        return redirect("anime_list")

    return render(request, 'anime/delete_anime.html', {'anime': anime})

def anime_list(request):
    genres = Genre.objects.all()
    sort_by = request.GET.get('sort_by', 'rating')

    selected_genres = request.GET.getlist('genre')
    if selected_genres:
        animes = Anime.objects.filter(genres__id__in=selected_genres).distinct()
    else:
        animes = Anime.objects.all()

    if sort_by == 'release_date':
        animes = animes.order_by('-release_date')
    elif sort_by == 'title':
        animes = animes.order_by('title')
    elif sort_by == 'episodes':
        animes = animes.order_by('-episodes')
    else:
        animes = animes.order_by('-rating')
    
    animes = list(animes)

    paginator = Paginator(animes, 40)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'animes': page_obj,
        'sort_by': sort_by,
        'selected_genres': list(map(int, selected_genres)),
        'genres': genres,
    }

    return render(request, 'anime/anime_list.html', context)

@allowed_users(allowed_roles=['admin', 'moderator'])
def anime_history(request):
    modified_animes = AnimeHistory.objects.filter(change_type='modified').order_by('-changed_at')
    deleted_animes = AnimeHistory.objects.filter(change_type='deleted').order_by('-changed_at')

    context = {
        'modified_animes': modified_animes,
        'deleted_animes': deleted_animes,
    }

    return render(request, 'anime/anime_history.html', context)

# API
class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [IsAdminOrReadOnly]

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]