from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Dynamic QR Redirect")

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS redirects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/r/{code}")
def redirect(code: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url FROM redirects WHERE code=?", (code,))
    result = c.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Redirect not found")

    return RedirectResponse(result[0])

class RedirectUpdate(BaseModel):
    url: str

@app.post("/admin/{code}")
def update_redirect(code: str, data: RedirectUpdate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO redirects (id, code, url) VALUES ((SELECT id FROM redirects WHERE code=?), ?, ?)",
              (code, code, data.url))
    conn.commit()
    conn.close()
    return {"message": f"Updated redirect for '{code}' → {data.url}"}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Dynamic QR Redirect</h2>
    <form action="/admin/demo" method="post">
        <input name="url" placeholder="Enter new destination URL" style="width:300px">
        <button type="submit">Update</button>
    </form>
    <p>QR link: <a href="/r/demo">/r/demo</a></p>
    """

@app.post("/admin/demo", response_class=HTMLResponse)
def update_form(url: str = Form(...)):
    update_redirect("demo", RedirectUpdate(url=url))
    return f"<p>✅ Updated redirect to <a href='{url}'>{url}</a></p><p><a href='/r/demo'>Test Redirect</a></p>"
