from __future__ import annotations

import hmac
import os
import time
from hashlib import sha256

import requests
from flask import Flask, abort, request

app = Flask(__name__)

SLACK_SIGNATURE_HEADER = "X-Slack-Signature"
SLACK_TIMESTAMP_HEADER = "X-Slack-Request-Timestamp"


def _verify_slack_signature() -> None:
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
    if not signing_secret:
        return

    signature = request.headers.get(SLACK_SIGNATURE_HEADER, "")
    timestamp = request.headers.get(SLACK_TIMESTAMP_HEADER, "")
    if not signature or not timestamp:
        abort(401)

    try:
        request_ts = int(timestamp)
    except ValueError:
        abort(401)

    tolerance_seconds = int(os.environ.get("SLACK_TOLERANCE_SECONDS", "300"))
    if abs(int(time.time()) - request_ts) > tolerance_seconds:
        abort(401)

    body = request.get_data(cache=True, as_text=False) or b""
    base_string = f"v0:{timestamp}:".encode() + body
    expected = (
        "v0="
        + hmac.new(signing_secret.encode(), base_string, sha256).hexdigest()
    )
    if not hmac.compare_digest(expected, signature):
        abort(401)


def _ai_studio_status() -> str:
    url = os.environ.get("AI_STUDIO_HEALTH_URL")
    if not url:
        return "AI Studio is running"

    try:
        resp = requests.get(url, timeout=5)
        if resp.ok:
            return "AI Studio is running"
        return f"AI Studio check failed (HTTP {resp.status_code})"
    except requests.RequestException as exc:
        return f"AI Studio check error: {exc}"


@app.route("/slack", methods=["POST"])
def slack_bot() -> str:
    _verify_slack_signature()

    text = (request.form.get("text") or "").strip().lower()

    if "status" in text:
        return _ai_studio_status()

    if "pods" in text:
        return "Check Kubernetes pods using kubectl"

    if "search" in text:
        return "Search feature coming soon 🔍"

    return "Unknown command"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
