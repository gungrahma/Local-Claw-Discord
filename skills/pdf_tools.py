from fpdf import FPDF
import datetime
import os

def buat_pdf_dari_teks(judul: str, isi_konten: str) -> str:
    """Skill untuk mengubah teks atau ringkasan riset menjadi file PDF.
    Gunakan ini jika user meminta untuk 'simpas sebagai PDF', 'buatkan dokumen', atau 
    'ekspor hasil riset ke PDF'.
    """

    try:
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Times", 'B', 16)
        pdf.cell(0, 10, judul, ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Times", size=12)
        pdf.multi_cell(0, 10, isi_konten)

        pdf.ln(10)
        pdf.set_font("Times", 'I', 8)
        waktu_sekarang = datetime.datetime.now().strftime("%Y-%M-%D %H:%M")
        pdf.cell(0, 10, f"DIbuat secara otomatis oleh Local Claw pada: {waktu_sekarang}", align='R')

        nama_file = f"Dokumen_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
        pdf.output(nama_file)

        return f"Berhasil! Dokumen PDF telah dibuat dengan nama: {nama_file}"
    except Exception as e:
        return f"Gagal membuat PDF: {str(e)}"