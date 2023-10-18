from mutagen.flac import FLAC
import os

class AlbumScanner:
    def __init__(self, flac_folder, start_range, end_range):
        self.flac_folder = flac_folder
        self.start_range = start_range
        self.end_range = end_range
        self.albums_info = {} 
        self.current_album_number = 0
        self.total_albums_in_range = end_range - start_range + 1

    def scan_albums(self):
        for root, dirs, files in os.walk(self.flac_folder):
            for album_file in files:
                if album_file.endswith(".flac"):
                    self.current_album_number += 1
                    if self.start_range <= self.current_album_number <= self.end_range:
                        album_info = self.extract_album_info(os.path.join(root, album_file))
                        if album_info:
                            self.albums_info[album_info["Album"]] = album_info


    def extract_album_info(self, album_path):
        try:
            tags = FLAC(album_path)
            album_info = {
                "Album": tags.get("album", [""])[0],
                "Artist": tags.get("artist", [""])[0],
                "Codec": f"Flac {tags.info.sample_rate // 1000}kHz/{tags.info.bits_per_sample}bit",
                "Genre": tags.get("genre", [""])[0],
                "Comment": tags.get("comment", [""])[0],
                "DiscNumber":f"{self.current_album_number}/{self.total_albums_in_range}",
            }
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


    def clean_folder_name(self, folder_name):
        # Reemplaza caracteres no válidos en el nombre de la carpeta
        invalid_chars = ['?', ':']
        for char in invalid_chars:
            folder_name = folder_name.replace(char, '_')
        return folder_name