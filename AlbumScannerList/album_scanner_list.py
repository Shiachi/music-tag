from mutagen.flac import FLAC
import os

class AlbumScannerList: 
    def __init__(self):
        self.albums_info = {}

    def scan_albums(self, flac_folder):
        for root, dirs, files in os.walk(flac_folder):
            for album_file in files:
                if album_file.endswith(".flac"):
                    album_info = self.extract_album_info(os.path.join(root, album_file))
                    if album_info:
                        album_name = album_info["Album"]
                        if album_name not in self.albums_info:
                            self.albums_info[album_name] = album_info

    def extract_album_info(self, album_path):
        try:
            tags = FLAC(album_path)
            album_info = {
                "Album": tags.get("album", [""])[0],
                "Artist": tags.get("artist", [""])[0],
                "Codec": f"Flac {tags.info.sample_rate // 1000}kHz/{tags.info.bits_per_sample}bit",
                "Genre": tags.get("genre", [""])[0],
            }
            return album_info
        except Exception as e:
            print(f"Error processing {album_path}: {e}")
            return None

    def save_album_info(self, output_file):
        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))

        with open(output_file, 'w', encoding='utf-8') as file:
            for i, (album_name, album_info) in enumerate(self.albums_info.items(), start=1):
                file.write("________________________________________________________________________________\n")
                file.write(f"Álbum: {album_info['Album']}\n")
                file.write(f"Artista: {album_info['Artist']}\n")
                file.write(f"Códec: {album_info['Codec']}\n")
                file.write(f"Género: {album_info['Genre']}\n")
                file.write(f"Etiqueta: #flac #lossless #hires\n")
                file.write(f"No. Disco subido hoy: {i}\n")
                file.write("Fuente: Comprado en MoraJP\n")
                file.write("Enlace a drive:\n")
                file.write("________________________________________________________________________________\n\n")