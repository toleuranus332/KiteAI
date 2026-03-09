"""
Kite AI Bot — Testnet faucet claim task.
"""
import time
import logging
import requests

logger = logging.getLogger("kiteai.tasks.faucet")


def claim_faucet(account, config: dict) -> None:
    """Request testnet KITE tokens from the faucet endpoint."""
    api_base = config.get("api_base", "https://testnet-router.kiteai.top")
    proxy = {"http": account.proxy, "https": account.proxy} if account.proxy else None

    payload = {
        "address": account.address,
        "chain_id": config.get("chain_id", 2368),
    }

    try:
        resp = requests.post(
            f"{api_base}/api/faucet/claim",
            json=payload,
            proxies=proxy,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            logger.info("Faucet claimed for %s — tx: %s", account.short_addr(), data.get("tx_hash", "N/A"))
        else:
            logger.warning("Faucet claim rejected for %s: %s", account.short_addr(), data.get("message", "unknown"))
    except requests.exceptions.RequestException as exc:
        logger.error("Faucet request failed for %s: %s", account.short_addr(), exc)
        raise
