"""
Kite AI Bot — Cross-chain bridge operations.
"""
import random
import logging
import requests

logger = logging.getLogger("kiteai.tasks.bridge")

BRIDGE_TARGETS = ["ethereum", "arbitrum", "base"]


def bridge_tokens(account, config: dict) -> None:
    """Bridge KITE tokens to a random supported chain."""
    api_base = config.get("api_base", "https://testnet-router.kiteai.top")
    proxy = {"http": account.proxy, "https": account.proxy} if account.proxy else None

    target_chain = random.choice(BRIDGE_TARGETS)
    amount = round(random.uniform(0.01, 0.1), 4)

    try:
        resp = requests.post(
            f"{api_base}/api/bridge/initiate",
            json={
                "address": account.address,
                "target_chain": target_chain,
                "token": "KITE",
                "amount": str(amount),
            },
            proxies=proxy,
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json()
        logger.info(
            "Bridged %.4f KITE to %s for %s — tx: %s",
            amount, target_chain, account.short_addr(), result.get("tx_hash", "N/A"),
        )
    except Exception as exc:
        logger.error("Bridge failed for %s: %s", account.short_addr(), exc)
        raise
