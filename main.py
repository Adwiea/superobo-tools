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
    return [f.replace(".session", "") for f in os.listdir() if f.endswith(".session") and f.startswith("session_")]

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
                console.print(f"[green]✅ {len(new_msgs)} pesan ditambahkan![/green]")
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

# ================= AUTO SENDER core =================
async def auto_sender():
    try:
        cfg = load_api()
        sessions = get_sessions()
        
        if not sessions:
            console.print("[red]❌ Tidak ada file session (session_name.session)[/red]")
            time.sleep(2)
            return

        console.print("\nMode: [1] Single [2] Multi Rotate")
        mode = Prompt.ask("Pilih", choices=["1", "2"])

        if mode == "1":
            for i, s in enumerate(sessions, 1):
                console.print(f"{i}. {s}")
            idx = int(Prompt.ask("Pilih nomor akun")) - 1
            sessions = [sessions[idx]]

        targets = [t.strip() for t in Prompt.ask("Target (Username/ID, pisah koma)").split(",")]
        min_d = int(Prompt.ask("Min delay", default="30"))
        max_d = int(Prompt.ask("Max delay", default="90"))
        limit = int(Prompt.ask("Total kirim", default="20"))

        msgs = load_messages()
        if not msgs:
            console.print("[red]❌ Pesan kosong![/red]")
            time.sleep(2)
            return

        clients = []
        console.print("[yellow]🔄 Menghubungkan ke Telegram...[/yellow]")
        for s in sessions:
            client = TelegramClient(s, cfg["api_id"], cfg["api_hash"])
            await client.start()
            clients.append(client)

        total = 0
        msg_idx = 0
        client_idx = 0

        def get_panel(last_msg, cd, count):
            t = Table.grid()
            t.add_row(f"[bold green]Status:[/bold green] Aktif")
            t.add_row(f"[bold blue]Pesan:[/bold blue] {last_msg[:25]}...")
            t.add_row(f"[bold yellow]Progress:[/bold yellow] {count}/{limit}")
            t.add_row(f"[bold cyan]Jeda:[/bold cyan] {cd}s")
            return Panel(t, title="🚀 SENDER ACTIVE", border_style="green")

        with Live(get_panel("-", 0, 0), refresh_per_second=1) as live:
            while total < limit:
                client = clients[client_idx]
                current_msg = msgs[msg_idx]
                
                try:
                    for target in targets:
                        await client.send_message(target, current_msg)
                        if len(targets) > 1: await asyncio.sleep(1)
                    total += 1
                except Exception as e:
                    console.print(f"\n[red]Gagal kirim: {e}[/red]")

                msg_idx = (msg_idx + 1) % len(msgs)
                client_idx = (client_idx + 1) % len(clients)

                if total < limit:
                    delay = random.randint(min_d, max_d)
                    for i in range(delay, 0, -1):
                        live.update(get_panel(current_msg, i, total))
                        await asyncio.sleep(1)

        for c in clients: await c.disconnect()
        console.print("\n[bold green]✅ Selesai![/bold green]")
        time.sleep(2)

    except Exception as e:
        console.print(f"[red]Fatal Error: {e}[/red]")
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
            await auto_sender() # Gunakan await, jangan asyncio.run() lagi
        elif c == "2":
            message_manager()
        elif c == "0":
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
        
