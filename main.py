import sqlite3
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles




app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

init_db()


@app.get("/")
def root(request: Request):
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


@app.post("/add")
def add_task(title: str = Form(...)):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, 0))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)



@app.post("/done/{task_id}")
def done_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)



