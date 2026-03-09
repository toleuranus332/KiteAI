"""
Kite AI Bot — DEX token swap execution.
"""
import random
import logging
import requests

logger = logging.getLogger("kiteai.tasks.swap")

SWAP_PAIRS = [
    ("KITE", "USDT"),
    ("KITE", "ETH"),
    ("USDT", "KITE"),
]


def execute_swap(account, config: dict) -> None:
    """Execute a random token swap on the Kite AI DEX."""
    api_base = config.get("api_base", "https://testnet-router.kiteai.top")
    proxy = {"http": account.proxy, "https": account.proxy} if account.proxy else None

    token_in, token_out = random.choice(SWAP_PAIRS)
    amount = round(random.uniform(0.01, 0.5), 4)

    try:
        resp = requests.post(
            f"{api_base}/api/swap/execute",
            json={
                "address": account.address,
                "token_in": token_in,
                "token_out": token_out,
                "amount_in": str(amount),
                "slippage": 0.5,
            },
            proxies=proxy,
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()
        logger.info(
            "Swapped %.4f %s -> %s for %s — tx: %s",
            amount, token_in, token_out, account.short_addr(), result.get("tx_hash", "N/A"),
        )
    except Exception as exc:
        logger.error("Swap failed for %s: %s", account.short_addr(), exc)
        raise
