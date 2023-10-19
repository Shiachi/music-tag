from mutagen.flac import FLAC
import os

class AlbumScanner: 
    def __init__(self):
        self.albums_info = {}
        self.album_count = 0

    def scan_albums(self, flac_folder, start_range, end_range):
        album_names = set()

        for root, dirs, files in os.walk(flac_folder):
            album_info = None
            for album_file in files:
                if album_file.endswith(".flac"):
                    album_info = self.extract_album_info(os.path.join(root, album_file))
                    if album_info:
                        album_name = album_info["Album"]
                        if album_name not in album_names:
                            album_names.add(album_name)
                            self.album_count += 1
                            if start_range <= self.album_count <= end_range:
                                self.albums_info[album_name] = album_info


    def extract_album_info(self, album_path):
        try:
            tags = FLAC(album_path)
            album_info = {
                "Album": tags.get("album", [""])[0],
                "Artist": tags.get("artist", [""])[0],
                "Codec": f"Flac {tags.info.sample_rate // 1000}kHz/{tags.info.bits_per_sample}bit",
                "Genre": tags.get("genre", [""])[0],
                "Comment": tags.get("comment", [""])[0]
            }

            # Extraer la carátula (front cover) si está presente
            pictures = tags.pictures
            for p in pictures:
                if p.type == 3:  # Tipo 3 indica carátula frontal
                    album_info["CoverArt"] = p.data
            
            return album_info
        except Exception as e:
            print(f"Error processing {album_path}: {e}")
            return None

    def save_album_info(self, output_folder):
        output_folder = os.path.normpath(output_folder)  # Normaliza la ruta de la carpeta de salida
        os.makedirs(output_folder, exist_ok=True)

        for album_name, album_info in self.albums_info.items():
            album_name = self.clean_folder_name(album_name)
            album_folder = os.path.join(output_folder, album_name)
            os.makedirs(album_folder, exist_ok=True)  # Crea la carpeta del álbum

            album_file = os.path.join(album_folder, f'{album_name}_info.txt')

            with open(album_file, 'w', encoding='utf-8') as file:
                file.write("📦 Álbum: {}\n".format(album_info['Album']))
                file.write("🎤 Artista: {}\n".format(album_info['Artist']))
                file.write("🛡 Códec: {}\n".format(album_info['Codec']))
                file.write("🎵 Género: {}\n".format(album_info['Genre']))
                file.write("Etiqueta: {}\n".format(album_info['Comment']))
                file.write("1️⃣ No. Disco subido hoy: \n")
                file.write("⤵️ Fuente: \n")
                file.write("🔗 Enlace a drive: \n")
                file.write("\n")

                # Guardar la carátula en la carpeta del álbum
                if "CoverArt" in album_info:
                    cover_path = os.path.join(album_folder, f'{album_name}_cover.jpg')
                    with open(cover_path, 'wb') as cover_file:
                        cover_file.write(album_info["CoverArt"])
                    file.write(f"🖼️ Carátula: {cover_path}\n")


    def clean_folder_name(self, folder_name):
        # Reemplaza caracteres no válidos en el nombre de la carpeta
        invalid_chars = ['?', ':']
        for char in invalid_chars:
            folder_name = folder_name.replace(char, '_')
        return folder_name