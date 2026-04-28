**Local Claw AI Agent**

Local Claw adalah asisten AI berbasis Discord yang berjalan di dalam container Docker. Ditenagai oleh Gemini 2.5 Flash (dengan sistem fallback otomatis), bot ini dirancang untuk menjadi partner riset dan asisten pengembangan sistem yang aman dan efisien.

**Fitur Utama :**
- Autonomous Research: Mampu melakukan riset real-time di internet menggunakan DuckDuckGo Search untuk menjawab pertanyaan yang butuh data terbaru.
- System Control (Sandbox): Menjalankan perintah terminal, membaca file, dan mengecek status server lokal langsung dari Discord tanpa membahayakan host OS (MacBook Air).
- Adaptive Model Fallback: Secara otomatis berpindah ke model cadangan jika terkena rate limit (Error 429), dengan tetap mempertahankan riwayat obrolan.
- Smart Message Chunking: Menangani batasan 2000 karakter Discord dengan memecah jawaban panjang menjadi beberapa pesan berurutan.
- Privacy First: Konfigurasi berbasis environment variables untuk menjaga keamanan API Key.

**Cara Instalasi :**

1. Prasyarat
•	Pastikan Docker Desktop sudah terinstal di Mac/Windows kamu.
•	Siapkan Gemini API Key dan Discord Bot Token.

2. Clone & Setup
```
# Clone repositori ini

git clone https://github.com/username/local-claw-project.git
cd local-claw-project

# Buat file .env
touch .env
```

3. Konfigurasi Environment
Isi file .env dengan kredensial kamu:

```
GEMINI_API_KEY=your_gemini_api_key_here
DISCORD_TOKEN=your_discord_bot_token_here
```

4. Menjalankan Bot
Jalankan perintah berikut di terminal:

```
docker compose up -d --build
```

Dibuat untuk experiment. 