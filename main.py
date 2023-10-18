from album_scanner import AlbumScanner

if __name__ == "__main__":
    flac_folder = 'D:/Music/ost'
    start_range = 1
    end_range = 2
    output_folder = 'D:/Music/album_info'

    scanner = AlbumScanner(flac_folder, start_range, end_range)
    scanner.scan_albums()
    scanner.save_album_info(output_folder)
    print(f"1️⃣ No. Disco subido hoy: {scanner.current_album_number}/{scanner.total_albums_in_range}")