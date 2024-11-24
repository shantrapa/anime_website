import requests
from datetime import datetime
from .models import Anime, Genre

def fetch(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get("data", {})
        
        title = data.get("title")
        description = data.get("synopsis")
        
        release_date_str = data.get("aired", {}).get("from")
        release_date = None
        if release_date_str:
            release_date_str = release_date_str.split("T")[0]
            release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
        
        rating = data.get("score")
        image_url = data.get("images", {}).get("jpg", {}).get("large_image_url")
        episodes = data.get("episodes")
        
        genres_data = data.get("genres", [])
        genres = []
        
        for genre in genres_data:
            genre_obj, _ = Genre.objects.get_or_create(name=genre["name"])
            genres.append(genre_obj)

        anime, created = Anime.objects.update_or_create(
            title=title,
            defaults={
                "description": description,
                "release_date": release_date,
                "rating": rating,
                "image": image_url,
                "episodes": episodes,
            }
        )
        
        anime.genres.set(genres)
        anime.save()
        
        print(f"Anime '{title}' has been {'created' if created else 'updated'}.")
    else:
        print(f"Failed to fetch anime data for ID {anime_id}. Status code: {response.status_code}")