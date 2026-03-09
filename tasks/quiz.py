"""
Kite AI Bot — Daily quiz auto-completion.
"""
import logging
import requests

logger = logging.getLogger("kiteai.tasks.quiz")


def complete_quiz(account, config: dict) -> None:
    """Fetch the daily quiz and submit answers automatically."""
    api_base = config.get("api_base", "https://testnet-router.kiteai.top")
    proxy = {"http": account.proxy, "https": account.proxy} if account.proxy else None

    try:
        quiz_resp = requests.get(
            f"{api_base}/api/quiz/daily",
            params={"address": account.address},
            proxies=proxy,
            timeout=20,
        )
        quiz_resp.raise_for_status()
        quiz_data = quiz_resp.json()

        if quiz_data.get("already_completed"):
            logger.info("Quiz already completed today for %s", account.short_addr())
            return

        questions = quiz_data.get("questions", [])
        answers = []
        for q in questions:
            options = q.get("options", [])
            correct = q.get("correct_index", 0)
            answers.append({"question_id": q["id"], "answer_index": correct})

        submit_resp = requests.post(
            f"{api_base}/api/quiz/submit",
            json={"address": account.address, "answers": answers},
            proxies=proxy,
            timeout=20,
        )
        submit_resp.raise_for_status()
        result = submit_resp.json()
        logger.info(
            "Quiz completed for %s — score: %s/%s",
            account.short_addr(), result.get("correct", 0), result.get("total", 0),
        )
    except Exception as exc:
        logger.error("Quiz failed for %s: %s", account.short_addr(), exc)
        raise
