#!/usr/bin/env python3
"""
Kite AI Bot — Automated multi-account interaction tool
for the Kite AI decentralized payment network.
"""
import os
import sys
import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box

from utils import ensure_env

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_FILE = PROJECT_ROOT / "config.json"

console = Console(force_terminal=True)

LOGO = r"""
 _  ___ _         _    ___   ____        _   
| |/ (_) |_ ___  / \  |_ _| | __ )  ___ | |_ 
| ' /| | __/ _ \/ _ \  | |  |  _ \ / _ \| __|
| . \| | ||  __/ ___ \ | |  | |_) | (_) | |_ 
|_|\_\_|\__\___/_/   \_\___| |____/ \___/ \__|
"""


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "rpc_url": "https://rpc.kiteai.top",
        "chain_id": 2368,
        "api_base": "https://testnet-router.kiteai.top",
        "max_concurrent": 5,
        "task_delay_min": 3,
        "task_delay_max": 10,
        "proxy_mode": "rotating",
        "auto_claim_faucet": True,
        "auto_stake": True,
        "auto_swap": True,
        "auto_quiz": True,
        "auto_bridge": True,
    }


def save_config(cfg: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def show_banner() -> None:
    console.print(Text(LOGO, style="bold cyan"))
    console.print(
        Panel(
            "[bold]Kite AI Bot[/bold] — Multi-account automation for Kite AI Network\n"
            "Testnet faucet, staking, swaps, quizzes, bridge & AI agent interaction",
            border_style="cyan",
        )
    )


def menu_install_deps() -> None:
    console.print("\n[bold yellow]Installing dependencies...[/bold yellow]\n")
    req = PROJECT_ROOT / "requirements.txt"
    if not req.exists():
        console.print("[red]requirements.txt not found.[/red]")
        return
    os.system(f'"{sys.executable}" -m pip install -r "{req}"')
    console.print("\n[green]Dependencies installed successfully.[/green]")


def menu_configure() -> None:
    from config import interactive_setup
    interactive_setup()


def menu_accounts() -> None:
    acct_file = PROJECT_ROOT / "accounts.txt"
    console.print("\n[bold yellow]Account Management[/bold yellow]\n")

    if acct_file.exists():
        lines = [l.strip() for l in acct_file.read_text().splitlines() if l.strip()]
        console.print(f"[cyan]Currently loaded:[/cyan] {len(lines)} account(s)")
    else:
        console.print("[dim]No accounts file found.[/dim]")

    if Confirm.ask("Edit accounts now?", default=False):
        console.print("Enter private keys, one per line. Empty line to finish.")
        keys = []
        while True:
            key = Prompt.ask("[cyan]privkey[/cyan]", default="")
            if not key:
                break
            keys.append(key)
        acct_file.write_text("\n".join(keys) + "\n", encoding="utf-8")
        console.print(f"[green]Saved {len(keys)} account(s) to accounts.txt[/green]")


def menu_proxy() -> None:
    proxy_file = PROJECT_ROOT / "proxy.txt"
    console.print("\n[bold yellow]Proxy Configuration[/bold yellow]\n")
    console.print("Supported formats:")
    console.print("  [dim]ip:port | http://ip:port | user:pass@ip:port[/dim]\n")

    if proxy_file.exists():
        lines = [l.strip() for l in proxy_file.read_text().splitlines() if l.strip()]
        console.print(f"[cyan]Loaded proxies:[/cyan] {len(lines)}")

    if Confirm.ask("Edit proxy list?", default=False):
        proxies = []
        while True:
            p = Prompt.ask("[cyan]proxy[/cyan]", default="")
            if not p:
                break
            proxies.append(p)
        proxy_file.write_text("\n".join(proxies) + "\n", encoding="utf-8")
        console.print(f"[green]Saved {len(proxies)} proxies.[/green]")


def menu_run_bot() -> None:
    from bot import KiteBot
    cfg = load_config()
    try:
        bot = KiteBot(cfg)
        bot.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Bot stopped by user.[/yellow]")
    except Exception as exc:
        console.print(f"[red]Bot error: {exc}[/red]")


def menu_status() -> None:
    cfg = load_config()
    table = Table(title="Current Configuration", box=box.ROUNDED)
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    for k, v in cfg.items():
        table.add_row(k, str(v))
    console.print(table)

    acct_file = PROJECT_ROOT / "accounts.txt"
    proxy_file = PROJECT_ROOT / "proxy.txt"
    accts = len([l for l in acct_file.read_text().splitlines() if l.strip()]) if acct_file.exists() else 0
    proxies = len([l for l in proxy_file.read_text().splitlines() if l.strip()]) if proxy_file.exists() else 0
    console.print(f"\n  Accounts loaded: [bold]{accts}[/bold]")
    console.print(f"  Proxies loaded:  [bold]{proxies}[/bold]")


def menu_about() -> None:
    console.print(Panel(
        "[bold]Kite AI Bot[/bold]\n\n"
        "An open-source automation tool for interacting with the Kite AI\n"
        "decentralized payment network testnet.\n\n"
        "[cyan]Features:[/cyan]\n"
        "  • Multi-account management with proxy rotation\n"
        "  • Automated faucet claims and token staking\n"
        "  • DEX swap and cross-chain bridge execution\n"
        "  • Daily quiz auto-completion\n"
        "  • AI agent interaction and reward collection\n"
        "  • Configurable delays and concurrent workers\n\n"
        "[dim]github.com/vonssy/KiteAi-BOT[/dim]",
        title="About",
        border_style="cyan",
    ))


@ensure_env
def main() -> None:
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        show_banner()

        console.print("[bold cyan]  Main Menu[/bold cyan]\n")
        console.print("  [cyan][1][/cyan] Install dependencies")
        console.print("  [cyan][2][/cyan] Configure bot settings")
        console.print("  [cyan][3][/cyan] Manage accounts")
        console.print("  [cyan][4][/cyan] Manage proxies")
        console.print("  [cyan][5][/cyan] Run bot")
        console.print("  [cyan][6][/cyan] View status")
        console.print("  [cyan][7][/cyan] About")
        console.print("  [cyan][0][/cyan] Exit\n")

        choice = Prompt.ask("Select option", choices=["0","1","2","3","4","5","6","7"], default="0")

        if choice == "1":
            menu_install_deps()
        elif choice == "2":
            menu_configure()
        elif choice == "3":
            menu_accounts()
        elif choice == "4":
            menu_proxy()
        elif choice == "5":
            menu_run_bot()
        elif choice == "6":
            menu_status()
        elif choice == "7":
            menu_about()
        elif choice == "0":
            console.print("[bold cyan]Exiting Kite AI Bot. Goodbye![/bold cyan]")
            break

        Prompt.ask("\n[dim]Press Enter to continue...[/dim]", default="")


if __name__ == "__main__":
    main()
