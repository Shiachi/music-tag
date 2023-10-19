from album_scanner import AlbumScanner

if __name__ == "__main__":
    scanner = AlbumScanner()
    flac_folder = 'D:/Music/ost'
    start_range = 1
    end_range = 5  # Change this to the desired end range
    output_folder = 'D:/Music/album_info'

    scanner.scan_albums(flac_folder, start_range, end_range)
    print(f"1️⃣ Discos escaneados: {end_range} / {scanner.album_count}")
    scanner.save_album_info(output_folder)