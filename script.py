import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import django
import time
import random

# Configura Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movies.settings")
django.setup()

from tendencias.models import Pelicula  

def buscar_y_guardar_imagen(pelicula):
    search_url = f"https://www.imdb.com/find?q={pelicula.titulo.replace(' ', '+')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Buscar el primer resultado de película
    result = soup.find('li', class_='ipc-metadata-list-summary-item')
    if result:
        link = result.find('a')
        if link:
            movie_url = urljoin("https://www.imdb.com", link['href'])
            
            # Visitar la página de la película
            movie_response = requests.get(movie_url, headers=headers)
            movie_soup = BeautifulSoup(movie_response.content, 'html.parser')
            
            # Buscar la imagen del póster
            poster = movie_soup.find('img', class_='ipc-image')
            if poster and 'src' in poster.attrs:
                image_url = poster['src']
                
                # Descargar la imagen
                image_data = requests.get(image_url, headers=headers)
                
                if image_data.status_code == 200:
                    # Crear la carpeta si no existe
                    folder_path = os.path.join('media', 'imgPelicula')
                    os.makedirs(folder_path, exist_ok=True)
                    
                    # Guardar la imagen
                    file_name = f"{pelicula.titulo.replace(' ', '_').lower()}.jpg"
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'wb') as f:
                        f.write(image_data.content)
                    
                    # Actualizar el campo imagen en el modelo
                    pelicula.imagen = f'imgPelicula/{file_name}'
                    pelicula.save()
                    
                    print(f"Imagen guardada para {pelicula.titulo}")
                    return
    
    print(f"No se pudo encontrar o guardar la imagen para {pelicula.titulo}")

# Obtener todas las películas y buscar imágenes para cada una
peliculas = Pelicula.objects.all()
for pelicula in peliculas:
    buscar_y_guardar_imagen(pelicula)
    # Esperar un tiempo aleatorio entre solicitudes para ser respetuoso con el servidor
    time.sleep(random.uniform(1, 3))