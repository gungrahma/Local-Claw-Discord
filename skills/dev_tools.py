import requests

def cek_status_server_lokal(port: int) -> str:
    """Mengecek apakah server lokal (localost) pada port tertentu sedang menyala.
    Gunakan ini jika ditanya "Cek dong server backend jalan nggaK".
    """

    port_bulat = int(float(port))

    url = f"http://host.docker.internal:{port_bulat}"

    try:
        response = requests.get(url, timeout=3)
        return f"Server di port {port_bulat} AKTIF. Status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return f"Server di port {port_bulat} MATI atau tidak bisa diakses."
    except Exception as e:
        return f"Error saat mengecek: {str(e)}"