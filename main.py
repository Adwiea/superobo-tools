from telethon import TelegramClient
import asyncio, random, json, os, time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live

console = Console()

# ================= LOAD CONFIG =================
def load_api():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    api_id = int(Prompt.ask("Masukkan API ID"))
    api_hash = Prompt.ask("Masukkan API HASH")
    data = {"api_id": api_id, "api_hash": api_hash}
    with open("config.json", "w") as f:
        json.dump(data, f)
    return data

def load_messages():
    if os.path.exists("messages.json"):
        with open("messages.json", "r") as f:
            return json.load(f)
    default = ["Halo 👋", "Lagi apa?", "Ngopi dulu ☕"]
    with open("messages.json", "w") as f:
        json.dump(default, f)
    return default

def save_messages(m):
    with open("messages.json", "w") as f:
        json.dump(m, f)

def get_sessions():
    # Mengambil semua file yang berakhiran .session
    return [f.replace(".session", "") for f in os.listdir() if f.endswith(".session")]

# ================= MESSAGE MANAGER =================
def message_manager():
    while True:
        m = load_messages()
        console.clear()
        console.print("[bold cyan]📩 MESSAGE MANAGER[/bold cyan]\n")
        if not m:
            console.print("[yellow]Daftar pesan kosong.[/yellow]")
        else:
            for i, x in enumerate(m, 1):
                console.print(f"{i}. {x}")

        console.print("\n[1] Tambah [2] Edit [3] Hapus [4] Import TXT [5] Hapus Semua [0] Kembali")
        c = Prompt.ask("Pilih")

        if c == "1":
            msg = Prompt.ask("Pesan baru")
            if msg.strip(): 
                m.append(msg)
                save_messages(m)
        elif c == "2":
            i = int(Prompt.ask("Nomor pesan")) - 1
            if 0 <= i < len(m): 
                m[i] = Prompt.ask("Edit pesan", default=m[i])
                save_messages(m)
        elif c == "3":
            i = int(Prompt.ask("Nomor pesan")) - 1
            if 0 <= i < len(m): 
                m.pop(i)
                save_messages(m)
        elif c == "4":
            filename = Prompt.ask("Nama file .txt", default="pesan.txt")
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    new_msgs = [line.strip() for line in f if line.strip()]
                    m.extend(new_msgs)
                save_messages(m)
                console.print(f"[green]✅ Berhasil impor![/green]")
            else:
                console.print("[red]❌ File tidak ditemukan![/red]")
            time.sleep(1)
        elif c == "5":
            if Prompt.ask("Hapus semua? (y/n)", choices=["y", "n"]) == "y":
                save_messages([])
                console.print("[red]🗑️ Semua pesan dihapus![/red]")
                time.sleep(1)
        elif c == "0":
            break

# ================= AUTO SENDER CORE =================
async def auto_sender():
    try:
        cfg = load_api()
        sessions = get_sessions()
        
        # JIKA TIDAK ADA SESSION, BUAT BARU
        if not sessions:
            console.print("[yellow]⚠️ Tidak ada session. Ayo login dulu untuk buat session baru.[/yellow]")
            session_name = Prompt.ask("Mau kasih nama session apa? (bebas, contoh: akun1)")
            # Pastikan nama file diawali session_ agar sesuai filter kita
            full_name = f"session_{session_name}"
            
            client = TelegramClient(full_name, cfg["api_id"], cfg["api_hash"])
            await client.start() # Ini akan otomatis minta No HP & Kode OTP di terminal
            console.print(f"[green]✅ Berhasil login! File {full_name}.session dibuat.[/green]")
            await client.disconnect()
            sessions = [full_name]
            time.sleep(1)

        console.print("\nMode: [1] Single [2] Multi Rotate")
        mode = Prompt.ask("Pilih", choices=["1", "2"])

        if mode == "1":
            for i, s in enumerate(sessions, 1):
                console.print(f"{i}. {s}")
            idx = int(Prompt.ask("Pilih nomor akun")) - 1
            sessions = [sessions[idx]]

        targets = [t.strip() for t in Prompt.ask("Target (Username, pisah koma)").split(",")]
        min_d = int(Prompt.ask("Min delay", default="30"))
        max_d = int(Prompt.ask("Max delay", default="90"))
        limit = int(Prompt.ask("Total kirim", default="20"))

        msgs = load_messages()
        clients = []
        for s in sessions:
            client = TelegramClient(s, cfg["api_id"], cfg["api_hash"])
            await client.start()
            clients.append(client)

        total = 0
        msg_idx = 0
        client_idx = 0

        with Live(refresh_per_second=1) as live:
            while total < limit:
                client = clients[client_idx]
                current_msg = msgs[msg_idx]
                
                try:
                    for target in targets:
                        await client.send_message(target, current_msg)
                        if len(targets) > 1: await asyncio.sleep(1)
                    total += 1
                except Exception as e:
                    console.print(f"\n[red]Error: {e}[/red]")

                msg_idx = (msg_idx + 1) % len(msgs)
                client_idx = (client_idx + 1) % len(clients)

                if total < limit:
                    delay = random.randint(min_d, max_d)
                    for i in range(delay, 0, -1):
                        t = Table.grid()
                        t.add_row(f"Status: [bold green]Running[/bold green]")
                        t.add_row(f"Total: {total}/{limit}")
                        t.add_row(f"Next Delay: {i}s")
                        live.update(Panel(t, title="SENDER ACTIVE"))
                        await asyncio.sleep(1)

        for c in clients: await c.disconnect()
        console.print("\n[bold green]✅ Tugas Selesai![/bold green]")
        time.sleep(2)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        time.sleep(3)

# ================= MAIN MENU =================
async def main():
    while True:
        console.clear()
        table = Table(title="🚀 SUPEROBO TOOLS V5.1", show_header=False)
        table.add_row("[1] Auto Sender")
        table.add_row("[2] Message Manager")
        table.add_row("[0] Exit")
        console.print(Panel(table, title="Main Menu", border_style="blue"))

        c = Prompt.ask("Pilih")
        if c == "1":
            await auto_sender()
        elif c == "2":
            message_manager()
        elif c == "0":
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
                
