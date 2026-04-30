import discord
import google.generativeai as genai
import os
import glob

from skills.system_tools import execute_terminal_command, baca_isi_file
from skills.dev_tools import cek_status_server_lokal
from skills.automation_tools import cari_folder_klien
from skills.web_tools import cari_di_internet
from skills.pdf_tools import buat_pdf_dari_teks

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

list_semua_skill = [
    execute_terminal_command, 
    baca_isi_file, 
    cek_status_server_lokal, 
    cari_folder_klien,
    cari_di_internet,
    buat_pdf_dari_teks
]

instruksi_sistem = """
Kamu adalah Local Claw, asisten AI dan partner riset milik Agung.

Tugas utamamu:
1. Mengeksekusi perintah sistem atau server jika diminta (gunakan tool lokal).
2. Menjawab pertanyaan umum, ngobrol, atau brainstorming ide.
3. Melakukan Riset: Jika ditanya info terbaru, tren teknologi, medis, atau data yang butuh akurasi tinggi, Wajib gunakan tool 'cari_di_internet'.
4. Membuat Dokumen: Jika Agung memintamu merangkum riset ke dalam file atau mengekspor teks ke PDF, gunakan tool 'buat_pdf_dari_teks.

Berikan jawaban yang rapi, komprehensif, tapi tetap menggunakan bahasa yang santai dan asyik khas teman ngobrol.
"""

nama_model_aktif = 'gemini-2.5-flash'
agent_model = genai.GenerativeModel(
    model_name=nama_model_aktif,
    tools=list_semua_skill,
    system_instruction=instruksi_sistem
)

chat_session = agent_model.start_chat(enable_automatic_function_calling=True)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

total_token_terpakai = 0

async def kirim_pesan_panjang(teks, channel):
    batas_karakter = 1900
    if len(teks) > batas_karakter:
        for i in range(0, len(teks), batas_karakter):
            await channel.send(teks[i : i + batas_karakter])
    else:
        await channel.send(teks)

@client.event
async def on_ready():
    print(f'Local Claw berhasil login ke Discord sebagai {client.user}')
    print(f'Model aktif saat ini: {nama_model_aktif}')

@client.event
async def on_message(message):
    global chat_session
    global nama_model_aktif
    global total_token_terpakai

    if message.author == client.user:
        return

    if client.user in message.mentions:
        user_command = message.content.replace(f'<@{client.user.id}>', '').strip()

        perintah_cek = ["cek limit", "cek token", "info kuota", "usage"]
        if user_command.lower() in perintah_cek:
            laporan = (
                f"**Statistik Penggunaan Claw (Sesi Ini)**\n"
                f"Model Aktif: `{nama_model_aktif}`\n"
                f"Total Token Terpakai: **{total_token_terpakai}** token\n\n"
                f"*(Info: Limit gratis Gemini Flash adalah 1 juta token per menit & 1.500 request per hari)*"
            )
            await message.channel.send(laporan)
            return

        async with message.channel.typing():
            try:
                response = await chat_session.send_message_async(user_command)

                if response.usage_metadata:
                    total_token_terpakai += response.usage_metadata.total_token_count

                    await kirim_pesan_panjang(response.text, message.channel)

                import glob
                import os
                
                file_pdf_ditemukan = glob.glob("*.pdf")
                
                if file_pdf_ditemukan:
                    file_terbaru = max(file_pdf_ditemukan, key=os.path.getctime)
                    
                    async with message.channel.typing():
                        try:
                            with open(file_terbaru, 'rb') as f:
                                dokumen_discord = discord.File(f, filename=file_terbaru)
                                await message.channel.send(
                                    content=f"Ini dokumennya ya!", 
                                    file=dokumen_discord
                                )
                            
                            os.remove(file_terbaru)
                            print(f"File {file_terbaru} berhasil dikirim dan dihapus dari container.")
                            
                        except Exception as e_upload:
                            await message.channel.send(f"Gagal mengunggah file: {str(e_upload)}")
    
                if response.usage_metadata:
                    token_sekali_jalan = response.usage_metadata.total_token_count
                    total_token_terpakai += token_sekali_jalan

            except Exception as e:
                pesan_error = str(e)
                
                if "429" in pesan_error or "ResourceExhausted" in pesan_error:
                    await message.channel.send(f"*Model {nama_model_aktif} kena limit. Tunggu sebentar, sedang mindahin memori ke otak cadangan...*")
                    
                    try:
                        model_cadangan = 'gemini-2.5-flash-lite' if nama_model_aktif == 'gemini-2.5-flash' else 'gemini-2.5-flash'
                        
                        agen_cadangan = genai.GenerativeModel(
                            model_name=model_cadangan,
                            tools=list_semua_skill,
                            system_instruction=instruksi_sistem
                        )

                        riwayat_lama = chat_session.history
                        chat_session = agen_cadangan.start_chat(
                            history=riwayat_lama,
                            enable_automatic_function_calling=True
                        )
                        nama_model_aktif = model_cadangan
                        
                        response_baru = await chat_session.send_message_async(user_command)
                        
                        await message.channel.send(f"*Berhasil pindah ke {nama_model_aktif}! Ini jawabannya:*")
                        await kirim_pesan_panjang(response_baru.text, message.channel)
                        
                    except Exception as ex:
                        await message.channel.send(f"Gagal ganti model cadangan: {str(ex)}")
                
                else:
                    await message.channel.send(f"Terjadi kesalahan sistem Claw: {pesan_error}")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("CRITICAL ERROR: DISCORD_TOKEN tidak ditemukan di env!")
    else:
        client.run(DISCORD_TOKEN)