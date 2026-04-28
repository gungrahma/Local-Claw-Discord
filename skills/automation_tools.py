import os

def cari_folder_klien(nama_klien: str) -> str:
    """Mencari lokasi folder aset klien berdasarkan namanya."""

    base_dir = "/app/data_klien"
    if not os.path.exists(base_dir):
        return "Folder data_klien utama tidak ditemukan."
    
    hasil = []

    for root, dirs, files in os.walk(base_dir):
        if nama_klien.lower() in root.lower():
            hasil.append(root)
    
    if hasil:
        return f"Ditemukan folder klien di: {', '.jon(hasil)}"
    return f"Klien '{nama_klien}' tidak ditemukan."