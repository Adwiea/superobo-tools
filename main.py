from telethon import TelegramClient
import asyncio
import random
import json
import os
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.live import Live

console = Console()

# ================= API =================
def load_api():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
        return config["api_id"], config["api_hash"]
    else:
        api_id = int(Prompt.ask("[cyan]Masukkan API ID[/cyan]"))
        api_hash = Prompt.ask("[cyan]Masukkan API HASH[/cyan]")

        with open("config.json", "w") as f:
            json.dump({"api_id": api_id, "api_hash": api_hash}, f)

        return api_id, api_hash

# ================= MESSAGE SYSTEM =================
def load_messages():
    if os.path.exists("messages.json"):
        with open("messages.json", "r") as f:
            return json.load(f)
    else:
        default = [
            "Halo 👋",
            "Lagi apa?",
            "Ngopi dulu ☕",
            "Santai 😄"
        ]
        with open("messages.json", "w") as f:
            json.dump(default, f)
        return default

def save_messages(messages):
    with open("messages.json", "w") as f:
        json.dump(messages, f)

def message_manager():
    messages = load_messages()

    while True:
        console.clear()
        console.print("[bold cyan]📩 MESSAGE MANAGER[/bold cyan]\n")

        for i, msg in enumerate(messages, 1):
            console.print(f"{i}. {msg}")

        console.print("\n[a] Tambah pesan")
        console.print("[d] Hapus pesan")
        console.print("[0] Kembali")

        choice = Prompt.ask("\nPilih")

        if choice == "a":
            new_msg = Prompt.ask("Tulis pesan baru")
            messages.append(new_msg)
            save_messages(messages)

        elif choice == "d":
            idx = int(Prompt.ask("Nomor pesan"))
            if 0 < idx <= len(messages):
                messages.pop(idx - 1)
                save_messages(messages)

        elif choice == "0":
            break

# ================= DASHBOARD =================
def make_layout():
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    layout["body"].split_row(
        Layout(name="menu"),
        Layout(name="info")
    )
    return layout

def header():
    return Panel(Align.center("[bold cyan]🚀 SUPEROBO TOOLS V2 🚀[/bold cyan]"), style="blue")

def menu():
    table = Table(title="MENU", expand=True)
    table.add_column("No", justify="center")
    table.add_column("Fitur")

    table.add_row("1", "Auto Sender Telegram")
    table.add_row("2", "Message Manager")
    table.add_row("0", "Exit")

    return Panel(table, border_style="green")

def info():
    return Panel(
        "[yellow]Status:[/yellow] Ready\n"
        "[cyan]Version:[/cyan] 2.0\n"
        "[magenta]Mode:[/magenta] CLI Tools\n\n"
        "[white]All-in-One Tools 🚀[/white]",
        title="INFO",
        border_style="magenta"
    )

def footer():
    return Panel(Align.center("Pilih menu dengan angka"), style="bold")

# ================= AUTO SENDER =================
async def auto_sender():
    api_id, api_hash = load_api()

    target = Prompt.ask("[cyan]Target (username/grup/ID)[/cyan]")

    confirm = Prompt.ask("Mulai? (y/n)", choices=["y","n"], default="n")
    if confirm != "y":
        return

    msg_list = load_messages()
    random.shuffle(msg_list)

    index = 0
    total = 0

    async with TelegramClient("session", api_id, api_hash) as client:
        me = await client.get_me()

        def panel(msg, countdown):
            table = Table.grid()
            table.add_row(f"User: {me.first_name}")
            table.add_row(f"Phone: {me.phone}")
            table.add_row(f"Last: {msg}")
            table.add_row(f"Next: {countdown}s")
            table.add_row(f"Total: {total}")
            return Panel(table, title="AUTO SENDER", border_style="blue")

        with Live(refresh_per_second=4) as live:
            while True:
                msg = msg_list[index]
                index += 1

                if index >= len(msg_list):
                    random.shuffle(msg_list)
                    index = 0

                await client.send_message(target, msg)
                total += 1

                delay = random.randint(60, 120)

                for i in range(delay, 0, -1):
                    live.update(panel(msg, i))
                    await asyncio.sleep(1)

# ================= MAIN =================
def dashboard():
    while True:
        console.clear()

        layout = make_layout()
        layout["header"].update(header())
        layout["menu"].update(menu())
        layout["info"].update(info())
        layout["footer"].update(footer())

        console.print(layout)

        choice = Prompt.ask("\n[cyan]Pilih menu[/cyan]")

        if choice == "1":
            asyncio.run(auto_sender())

        elif choice == "2":
            message_manager()

        elif choice == "0":
            console.print("[red]Keluar...[/red]")
            break

        else:
            console.print("[yellow]Pilihan tidak valid[/yellow]")
            input("Enter...")

# ================= RUN =================
if __name__ == "__main__":
    dashboard()