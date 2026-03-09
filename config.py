"""
Kite AI Bot — Configuration management.
"""
import json
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

CONFIG_FILE = Path(__file__).parent / "config.json"
console = Console(force_terminal=True)

DEFAULTS = {
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


def load() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return dict(DEFAULTS)


def save(cfg: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def interactive_setup() -> None:
    cfg = load()
    console.print("\n[bold yellow]Bot Configuration[/bold yellow]\n")

    cfg["rpc_url"] = Prompt.ask("RPC URL", default=cfg.get("rpc_url", DEFAULTS["rpc_url"]))
    cfg["chain_id"] = int(Prompt.ask("Chain ID", default=str(cfg.get("chain_id", DEFAULTS["chain_id"]))))
    cfg["api_base"] = Prompt.ask("API base URL", default=cfg.get("api_base", DEFAULTS["api_base"]))
    cfg["max_concurrent"] = int(Prompt.ask("Max concurrent workers", default=str(cfg.get("max_concurrent", 5))))
    cfg["task_delay_min"] = int(Prompt.ask("Min delay between tasks (sec)", default=str(cfg.get("task_delay_min", 3))))
    cfg["task_delay_max"] = int(Prompt.ask("Max delay between tasks (sec)", default=str(cfg.get("task_delay_max", 10))))

    console.print("\n[bold]Task toggles:[/bold]")
    cfg["auto_claim_faucet"] = Confirm.ask("  Auto claim faucet?", default=cfg.get("auto_claim_faucet", True))
    cfg["auto_stake"] = Confirm.ask("  Auto stake tokens?", default=cfg.get("auto_stake", True))
    cfg["auto_swap"] = Confirm.ask("  Auto swap tokens?", default=cfg.get("auto_swap", True))
    cfg["auto_quiz"] = Confirm.ask("  Auto complete daily quiz?", default=cfg.get("auto_quiz", True))
    cfg["auto_bridge"] = Confirm.ask("  Auto bridge tokens?", default=cfg.get("auto_bridge", True))

    save(cfg)
    console.print("\n[green]Configuration saved to config.json[/green]")
