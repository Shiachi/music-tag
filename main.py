from mutagen.flac import FLAC
import os

# Ruta a la carpeta que contiene los archivos FLAC
carpeta_flac = 'D:/Music/ost'

# Inicializa un diccionario para almacenar la información del álbum
albumes = {}

# Recorre los archivos FLAC en la carpeta
for root, dirs, files in os.walk(carpeta_flac):
    for archivo in files:
        if archivo.endswith(".flac"):
            ruta_completa = os.path.join(root, archivo)

            # Utiliza mutagen para extraer la información del archivo FLAC
            etiquetas = FLAC(ruta_completa)

            # Obtén el nombre del álbum
            album = etiquetas.get('album', [''])[0]

            # Verifica si el álbum ya está en el diccionario
            if album not in albumes:
                # Si el álbum no está en el diccionario, agrega una entrada
                albumes[album] = {
                    'Álbum': album,
                    'Artista': etiquetas.get('artist', [''])[0],
                    'Códec': "FLAC {}kHz/{}bit".format(etiquetas.info.sample_rate // 1000, etiquetas.info.bits_per_sample),
                    'Género': etiquetas.get('genre', [''])[0],
                    'Etiqueta': etiquetas.get('comment', [''])[0]
                }

# Especifica la ubicación y el nombre del archivo de texto
archivo_salida = 'informacion_albumes.txt'

# Abre el archivo para escritura
with open(archivo_salida, 'w', encoding='utf-8') as archivo:
    # Escribe la información de los álbumes en el archivo
    for album_info in albumes.values():
        archivo.write("Álbum: {}\n".format(album_info['Álbum']))
        archivo.write("Artista: {}\n".format(album_info['Artista']))
        archivo.write("Códec: {}\n".format(album_info['Códec']))
        archivo.write("Género: {}\n".format(album_info['Género']))
        archivo.write("Etiqueta: {}\n".format(album_info['Etiqueta']))
        archivo.write("\n")


