from duckduckgo_search import DDGS

def cari_di_internet(query: str) -> str:
    """Skill wajib untuk mencari informasi entah itu berita, dokumentas atau riset di internet.
    Gunakan ini untuk user ketika menanyakan hal general, maupun hal yang bersifat membutuhkan
    fakta real-time dan riset umum yang tidak kamu ketahui secara pasti!."""

    try:
        results = DDGS().text(query, max_results=3)

        if not results:
            return "Tidak ada hasil yang ditemukan di internet."
        
        jawaban = "Hasil pencarian web:\n"

        for res in results:
            jawaban += f"[{res['title']}]\nRingkasan: {res['body']}\nSumber: {res['href']}\n\n"

            return jawaban
    except Exception as e:
        return f"Sistem pencarian error: {str(e)}"