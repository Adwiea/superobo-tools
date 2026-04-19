# 🚀 SUPEROBO TOOLS V5.1 FINAL

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Telethon](https://img.shields.io/badge/Library-Telethon-orange.svg)
![Rich](https://img.shields.io/badge/UI-Rich-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Superobo Tools** adalah CLI (Command Line Interface) berbasis Python yang dirancang untuk otomatisasi pengiriman pesan di Telegram dengan antarmuka terminal yang modern dan interaktif.

---

## ✨ Fitur Utama

* 🤖 **Auto Sender Telegram**: Kirim pesan otomatis ke banyak target sekaligus.
* 🔄 **Multi Account Rotate**: Mendukung penggunaan banyak akun secara bergantian (rotasi) untuk menghindari limit.
* 📩 **Message Manager**: Kelola daftar pesan langsung dari aplikasi (Tambah, Edit, Hapus, Hapus Masal).
* 📄 **TXT File Support**: Impor pesan secara masal dari file `.txt`.
* 📊 **Live Dashboard**: Pantau progres pengiriman secara real-time dengan tabel dan countdown delay yang estetik.
* 🛡️ **Smart Delay**: Pengaturan jeda waktu (min/max) yang fleksibel untuk meminimalisir risiko ban.

---

## 📦 Instalasi

Pastikan kamu sudah menginstal Python di perangkatmu (Termux/PC).

```bash
pkg update && pkg upgrade -y
termux-setup-storage
pkg install python git -y
git clone https://github.com/Adwiea/superobo-tools.git
cd superobo-tools
pip install -r requirements.txt
python main.py
```

⚙️ Cara Penggunaan
Dapatkan API ID dan API HASH dari my.telegram.org.
Siapkan file session Telegram (letakkan di folder yang sama dengan format nama session_namaanda.session).
Jalankan program dan masukkan API ID & Hash saat diminta (hanya sekali, akan tersimpan di config.json).
Gunakan Message Manager untuk mengatur pesan kamu.
Pilih Auto Sender dan ikuti instruksi di layar.

⚠️ Disclaimer
Aplikasi ini dibuat untuk tujuan edukasi dan produktivitas pribadi. Penggunaan bot untuk aktivitas SPAM dapat menyebabkan akun Telegram kamu diblokir. Gunakan dengan bijak dan patuhi TOS Telegram.

👨‍💻 Author
Superobo Don't forget to give a ⭐ if you like this project!
