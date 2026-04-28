import discord
import google.generativeai as genai
import os

from skills.system_tools import execute_terminal_command, baca_isi_file
from skills.dev_tools import cek_status_server_lokal
from skills.automation_tools import cari_folder_klien

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

list_semua_skill = [
    execute_terminal_command, 
    baca_isi_file, 
    cek_status_server_lokal, 
    cari_folder_klien
]

agent_model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=list_semua_skill,
    system_instruction="""
    Kamu adalah Local Claw, asisten AI canggih milik Agung yang berjalan di Docker.
    Kamu punya akses ke terminal, sistem file, dan pengecekan server lokal.
    Gunakan 'cek_status_server_lokal' jika user bertanya tentang status port atau backend.
    Gunakan 'cari_folder_klien' jika ditanya soal lokasi aset proyek.
    Selalu bekerja selangkah demi selangkah. Jawab dengan santai dan solutif.
    """
)

chat_session = agent_model.start_chat(enable_automatic_function_calling = True)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Local Claw berhasil login ke Discord sebagai {client.user}')
    print('Container siap menerima perintah!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        user_command = message.content.replace(f'<@{client.user.id}>', '').strip()

        async with message.channel.typing():
            try:
                response = await chat_session.send_message_async(user_command)

                if len(response.text) > 2000:
                    await message.channel.send(response.text[:1998] + "....\n*(Text kepanjangan, terpotong)*")
                else:
                    await message.channel.send(response.text)
            except Exception as e:
                await message.channel.send(f"Terjadi kesalahan sistem Claw: {str(e)}")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("CRITICAL ERROR: DISCORD_TOKEN tidak ditemukan di env!")
    else:
        client.run(DISCORD_TOKEN)