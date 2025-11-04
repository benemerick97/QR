from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
import os

app = FastAPI(title="Simple Dynamic QR Redirect")

# ─────────────────────────────────────────────
# ✏️ Change this URL anytime you want to redirect the QR elsewhere
REDIRECT_URL = "https://mitilabs-46899750.hubspotpagebuilder.com/watch-give-away"

# ─────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <h2>Simple QR Redirect</h2>
    <p>Current redirect target:</p>
    <p><a href="{REDIRECT_URL}" target="_blank">{REDIRECT_URL}</a></p>
    <p>QR link to share or embed: <code>/r</code></p>
    <p><a href="/r" target="_blank">Test Redirect</a></p>
    <hr>
    <p>To change the destination, edit <b>REDIRECT_URL</b> in <code>main.py</code> and redeploy.</p>
    """

@app.get("/mitilabs")
def redirect():
    return RedirectResponse(REDIRECT_URL)

# optional Railway health check
@app.get("/health")
def health():
    return {"status": "ok", "redirect": REDIRECT_URL}
