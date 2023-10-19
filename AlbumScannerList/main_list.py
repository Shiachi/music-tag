from album_scanner_list import AlbumScannerList

if __name__ == "__main__":
    flac_folder = 'D:/Music/ost'
    output_file = 'D:/Music/album_info/album_info.txt'

    scanner = AlbumScannerList()
    scanner.scan_albums(flac_folder)
    print(f"1️⃣ Discos escaneados: {len(scanner.albums_info)}")
    scanner.save_album_info(output_file)