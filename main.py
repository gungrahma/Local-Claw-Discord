import discord
import google.generativeai as genai
import os

from skills.system_tools import execute_terminal_command, baca_isi_file
from skills.dev_tools import cek_status_server_lokal
from skills.automation_tools import cari_folder_klien
from skills.web_tools import cari_di_internet

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

list_semua_skill = [
    execute_terminal_command, 
    baca_isi_file, 
    cek_status_server_lokal, 
    cari_folder_klien,
    cari_di_internet
]

instruksi_sistem = """
Kamu adalah Local Claw, asisten AI dan partner riset milik Agung.

Tugas utamamu:
1. Mengeksekusi perintah sistem atau server jika diminta (gunakan tool lokal).
2. Menjawab pertanyaan umum, ngobrol, atau brainstorming ide.
3. Melakukan Riset: Jika ditanya info terbaru, tren teknologi, medis, atau data yang butuh akurasi tinggi, Wajib gunakan tool 'cari_di_internet'.

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

    if message.author == client.user:
        return

    if client.user in message.mentions:
        user_command = message.content.replace(f'<@{client.user.id}>', '').strip()

        async with message.channel.typing():
            try:
                response = await chat_session.send_message_async(user_command)
                await kirim_pesan_panjang(response.text, message.channel)

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