"""
Kite AI Bot — Core bot logic for multi-account task execution.
"""
import time
import random
import logging
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console(force_terminal=True)
logger = logging.getLogger("kiteai.bot")


class Account:
    """Represents a single wallet account."""

    def __init__(self, private_key: str, proxy: Optional[str] = None):
        self.private_key = private_key
        self.proxy = proxy
        self.address: Optional[str] = None
        self.balance: float = 0.0
        self.tasks_completed: int = 0

    def derive_address(self) -> str:
        try:
            from eth_account import Account as EthAccount
            acct = EthAccount.from_key(self.private_key)
            self.address = acct.address
        except Exception:
            self.address = f"0x{self.private_key[-40:]}"
        return self.address

    def short_addr(self) -> str:
        addr = self.address or self.derive_address()
        return f"{addr[:8]}...{addr[-6:]}"


class KiteBot:
    """Main bot controller — manages accounts, distributes tasks."""

    def __init__(self, config: dict):
        self.config = config
        self.accounts: List[Account] = []
        self.rpc_url = config.get("rpc_url", "https://rpc.kiteai.top")
        self.max_concurrent = config.get("max_concurrent", 5)
        self.delay_min = config.get("task_delay_min", 3)
        self.delay_max = config.get("task_delay_max", 10)
        self._load_accounts()

    def _load_accounts(self) -> None:
        from pathlib import Path
        acct_file = Path(__file__).parent / "accounts.txt"
        proxy_file = Path(__file__).parent / "proxy.txt"

        keys = []
        if acct_file.exists():
            keys = [l.strip() for l in acct_file.read_text().splitlines() if l.strip()]

        proxies = []
        if proxy_file.exists():
            proxies = [l.strip() for l in proxy_file.read_text().splitlines() if l.strip()]

        for i, key in enumerate(keys):
            proxy = proxies[i % len(proxies)] if proxies else None
            acct = Account(key, proxy)
            acct.derive_address()
            self.accounts.append(acct)

        console.print(f"[cyan]Loaded {len(self.accounts)} account(s), {len(proxies)} proxy(ies)[/cyan]")

    def _execute_task_cycle(self, account: Account) -> dict:
        from tasks import get_enabled_tasks
        results = {"account": account.short_addr(), "success": 0, "failed": 0}

        enabled = get_enabled_tasks(self.config)
        for task_fn in enabled:
            try:
                task_fn(account, self.config)
                results["success"] += 1
                account.tasks_completed += 1
            except Exception as exc:
                logger.warning("Task %s failed for %s: %s", task_fn.__name__, account.short_addr(), exc)
                results["failed"] += 1

            delay = random.uniform(self.delay_min, self.delay_max)
            time.sleep(delay)

        return results

    def run(self) -> None:
        if not self.accounts:
            console.print("[red]No accounts loaded. Add private keys to accounts.txt first.[/red]")
            return

        console.print(f"\n[bold green]Starting bot with {len(self.accounts)} account(s)...[/bold green]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing accounts...", total=len(self.accounts))

            with ThreadPoolExecutor(max_workers=self.max_concurrent) as pool:
                futures = {
                    pool.submit(self._execute_task_cycle, acct): acct
                    for acct in self.accounts
                }
                for future in as_completed(futures):
                    result = future.result()
                    progress.advance(task)
                    console.print(
                        f"  [cyan]{result['account']}[/cyan] — "
                        f"[green]{result['success']} OK[/green], "
                        f"[red]{result['failed']} failed[/red]"
                    )

        console.print("\n[bold green]Bot cycle complete.[/bold green]")
