"""
Kite AI Bot — Token staking operations.
"""
import logging
import requests

logger = logging.getLogger("kiteai.tasks.staking")


def stake_tokens(account, config: dict) -> None:
    """Stake available KITE tokens on the network."""
    api_base = config.get("api_base", "https://testnet-router.kiteai.top")
    proxy = {"http": account.proxy, "https": account.proxy} if account.proxy else None

    try:
        bal_resp = requests.get(
            f"{api_base}/api/account/{account.address}/balance",
            proxies=proxy,
            timeout=20,
        )
        bal_resp.raise_for_status()
        balance = float(bal_resp.json().get("available", 0))

        if balance < 1.0:
            logger.info("Insufficient balance for staking on %s (%.4f KITE)", account.short_addr(), balance)
            return

        stake_amount = balance * 0.8
        resp = requests.post(
            f"{api_base}/api/staking/stake",
            json={"address": account.address, "amount": str(stake_amount)},
            proxies=proxy,
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()
        logger.info("Staked %.4f KITE for %s — tx: %s", stake_amount, account.short_addr(), result.get("tx_hash", "N/A"))
    except Exception as exc:
        logger.error("Staking failed for %s: %s", account.short_addr(), exc)
        raise
