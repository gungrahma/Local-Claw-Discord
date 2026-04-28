import subprocess
import os

def execute_terminal_command(command: str) -> str:
    """Menjalankan perintah terminal di dalam environment lokal Docker."""

    try:
        result = subprocess.run(command, shell=True, check=True,
                                capture_output=True, text=True,
                                timeout=15)
        return f"SUCCESS:\n{result.stdout}"
    except Exception as e:
        return f"ERROR:\n{str(e)}"
    
def baca_isi_file(filepath: str) -> str:
    """Membaca isi teks dari sebuah file (misal: baca log error, baca config)."""

    if not os.path.exists(filepath):
        return f"Error: File {filepath} tidek ditemukan."
    with open(filepath, 'r') as f:
        return f.read()