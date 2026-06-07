from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from datetime import datetime

from dotenv import load_dotenv
import os
import sqlite3


# Load environment variables
load_dotenv()

# Get bot token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

conn = sqlite3.connect(
    "focusflow.db",
    check_same_thread=False
)
conn.row_factory = sqlite3.Row

# Use a single setup cursor just for table creation, then discard it
_setup = conn.cursor()
_setup.executescript("""
CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT    NOT NULL,
    task        TEXT    NOT NULL,
    priority    TEXT    NOT NULL DEFAULT 'Medium',
    created_at  TEXT    NOT NULL,
    due_date    TEXT,
    reminded    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_stats (
    user_id               TEXT PRIMARY KEY,
    streak                INTEGER NOT NULL DEFAULT 0,
    last_completed_date   TEXT,
    pomodoros_completed   INTEGER NOT NULL DEFAULT 0
);
""")
conn.commit()
del _setup

# In-memory store for active pomodoro jobs (not persisted – lives only while
# the bot process is running, which is fine for scheduled jobs).
active_pomodoros = {}

# ---------------------------------------------------------------------------
# DB helper functions
# ---------------------------------------------------------------------------

def db_get_tasks(user_id: str) -> list:
    """Return all tasks for a user as a list of sqlite3.Row objects."""
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY id",
        (user_id,)
    )
    return cur.fetchall()


def db_get_task_by_index(user_id: str, index: int):
    """Return a single task by its 1-based display index (or None)."""
    rows = db_get_tasks(user_id)
    if index < 1 or index > len(rows):
        return None
    return rows[index - 1]


def db_add_task(user_id, task, priority, created_at, due_date, reminded):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO tasks (user_id, task, priority, created_at, due_date, reminded)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, task, priority, created_at, due_date, reminded)
    )
    conn.commit()


def db_delete_task(task_id: int):
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()


def db_update_priority(task_id: int, priority: str):
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET priority = ? WHERE id = ?",
        (priority, task_id)
    )
    conn.commit()


def db_update_due_date(task_id: int, due_date: str):
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET due_date = ?, reminded = 0 WHERE id = ?",
        (due_date, task_id)
    )
    conn.commit()


def db_mark_reminded(task_id: int):
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET reminded = 1 WHERE id = ?",
        (task_id,)
    )
    conn.commit()


def db_get_stats(user_id: str):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM user_stats WHERE user_id = ?",
        (user_id,)
    )
    return cur.fetchone()


def db_ensure_stats(user_id: str):
    """Insert a default stats row if one doesn't exist yet."""
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO user_stats (user_id) VALUES (?)",
        (user_id,)
    )
    conn.commit()


def db_update_streak(user_id: str, streak: int, last_date: str):
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE user_stats
        SET streak = ?, last_completed_date = ?
        WHERE user_id = ?
        """,
        (streak, last_date, user_id)
    )
    conn.commit()


def db_increment_pomodoros(user_id: str):
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE user_stats
        SET pomodoros_completed = pomodoros_completed + 1
        WHERE user_id = ?
        """,
        (user_id,)
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Bot command handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! FocusFlow Bot is running now  🚀"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🚀 FocusFlow Commands

📋 Task Management
/addtask <task> - Add a new task
/tasks - View all tasks
/done <task_number> - Complete a task

🔥 Priority Management
/setpriority <task_number> <High|Medium|Low>
/highpriority - View high-priority tasks

⏰ Due Dates & Reminders
/setdue <task_number> <YYYY-MM-DD>
/setdue <task_number> <YYYY-MM-DD HH:MM>
/upcoming - View upcoming tasks
/overdue - View overdue tasks

📈 Productivity
/stats - Task statistics
/streak - View study streak
/analytics - Productivity dashboard

🍅 Focus Tools
/pomodoro <minutes> - Start a Pomodoro session
/cancelpomodoro - Cancel active Pomodoro
/pomodorostats - View completed Pomodoros

ℹ️ General
/start - Start the bot
/help - Show this help menu
"""
    await update.message.reply_text(help_text)


async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = " ".join(context.args)
    if not task:
        await update.message.reply_text(
            "Please provide a task.\nExample: /addtask Study Python"
        )
        return

    user_id = str(update.effective_user.id)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    db_add_task(user_id, task, "Medium", current_time, None, 0)

    await update.message.reply_text(
        f"Task added successfully ✅\nTask: {task}"
    )


async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    rows = db_get_tasks(user_id)

    if not rows:
        await update.message.reply_text("No tasks available.")
        return

    task_list = "\n\n".join(
        f"{i + 1}. {row['task']}\n"
        f"   Priority: {row['priority']}\n"
        f"   Added: {row['created_at']}\n"
        f"   Due: {'Not Set' if row['due_date'] is None else row['due_date']}"
        for i, row in enumerate(rows)
    )

    await update.message.reply_text(f"Your Tasks:\n\n{task_list}")


async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    rows = db_get_tasks(user_id)

    if not rows:
        await update.message.reply_text("No tasks available.")
        return

    if not context.args:
        await update.message.reply_text(
            "Please provide task number.\nExample: /done 1"
        )
        return

    try:
        task_number = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return

    if task_number < 1 or task_number > len(rows):
        await update.message.reply_text("Invalid task number.")
        return

    task_row = rows[task_number - 1]

    # Update streak
    db_ensure_stats(user_id)
    stats_row = db_get_stats(user_id)

    today = datetime.now().date()
    last_date_str = stats_row["last_completed_date"]
    streak = stats_row["streak"]

    if last_date_str is None:
        streak = 1
    else:
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
        difference = (today - last_date).days
        if difference == 0:
            pass
        elif difference == 1:
            streak += 1
        else:
            streak = 1

    db_update_streak(user_id, streak, str(today))

    # Remove task
    db_delete_task(task_row["id"])

    await update.message.reply_text(
        f"✅ Task completed: {task_row['task']}\n\n"
        f"🔥 Current Streak: {streak} day(s)"
    )


async def set_priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage: /setpriority <task_number> <High|Medium|Low>"
        )
        return

    try:
        task_number = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Task number must be a valid number.")
        return

    priority = context.args[1].capitalize()
    if priority not in ["High", "Medium", "Low"]:
        await update.message.reply_text("Priority must be High, Medium, or Low.")
        return

    task_row = db_get_task_by_index(user_id, task_number)
    if task_row is None:
        await update.message.reply_text("Invalid task number.")
        return

    db_update_priority(task_row["id"], priority)

    await update.message.reply_text(f"✅ Priority updated to {priority}")


async def high_priority_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    all_rows = db_get_tasks(user_id)
    if not all_rows:
        await update.message.reply_text("You have no tasks yet. Use /addtask to add one!")
        return

    rows = [r for r in all_rows if r["priority"] == "High"]

    if not rows:
        await update.message.reply_text("No high-priority tasks found.")
        return

    task_list = "\n".join(
        f"{i + 1}. {row['task']}" for i, row in enumerate(rows)
    )

    await update.message.reply_text(f"🔥 High Priority Tasks\n\n{task_list}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    rows = db_get_tasks(user_id)

    if not rows:
        await update.message.reply_text("You have no tasks yet. Use /addtask to add one!")
        return

    total_tasks = len(rows)
    high_count = sum(1 for r in rows if r["priority"] == "High")
    medium_count = sum(1 for r in rows if r["priority"] == "Medium")
    low_count = sum(1 for r in rows if r["priority"] == "Low")

    await update.message.reply_text(
        f"📊 Task Statistics\n\n"
        f"Total Tasks: {total_tasks}\n"
        f"High Priority: {high_count}\n"
        f"Medium Priority: {medium_count}\n"
        f"Low Priority: {low_count}"
    )


async def set_due(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if len(context.args) not in [2, 3]:
        await update.message.reply_text(
            "Usage:\n/setdue <task_number> <YYYY-MM-DD>\nOR\n/setdue <task_number> <YYYY-MM-DD HH:MM>"
        )
        return

    try:
        task_number = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Task number must be a valid number.")
        return

    due_date = context.args[1] if len(context.args) == 2 else context.args[1] + " " + context.args[2]

    try:
        try:
            datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        except ValueError:
            datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(
            "Invalid format.\nUse:\nYYYY-MM-DD\nor\nYYYY-MM-DD HH:MM"
        )
        return

    task_row = db_get_task_by_index(user_id, task_number)
    if task_row is None:
        await update.message.reply_text("Invalid task number.")
        return

    db_update_due_date(task_row["id"], due_date)

    await update.message.reply_text(
        f"⏰ Due date for task {task_number} set to {due_date}"
    )


async def upcoming_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    rows = db_get_tasks(user_id)

    if not rows:
        await update.message.reply_text("No tasks available.")
        return

    upcoming = []
    now = datetime.now()
    for row in rows:
        due_date = row["due_date"]
        if due_date is None:
            continue
        try:
            try:
                due_obj = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            except ValueError:
                due_obj = datetime.strptime(due_date, "%Y-%m-%d")
            if due_obj >= now:  # Bug 2 fix: only future tasks
                upcoming.append((row, due_obj))
        except ValueError:
            continue

    if not upcoming:
        await update.message.reply_text("No upcoming tasks.")
        return

    upcoming.sort(key=lambda x: x[1])

    task_list = "\n\n".join(
        f"{i + 1}. {row['task']}\n"
        f"   Priority: {row['priority']}\n"
        f"   Due: {row['due_date']}"
        for i, (row, _) in enumerate(upcoming)
    )

    await update.message.reply_text(f"📅 Upcoming Tasks:\n\n{task_list}")


async def overdue_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    rows = db_get_tasks(user_id)

    if not rows:
        await update.message.reply_text("No tasks available.")
        return

    current_time = datetime.now()
    overdue = []

    for row in rows:
        due_date = row["due_date"]
        if due_date is None:
            continue
        try:
            try:
                due_obj = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            except ValueError:
                due_obj = datetime.strptime(due_date, "%Y-%m-%d")
            if due_obj < current_time:
                overdue.append((row, due_obj))
        except ValueError:
            continue

    if not overdue:
        await update.message.reply_text("🎉 No overdue tasks.")
        return

    overdue.sort(key=lambda x: x[1])

    task_list = "\n\n".join(
        f"{i + 1}. {row['task']}\n"
        f"   Priority: {row['priority']}\n"
        f"   Due: {row['due_date']}"
        for i, (row, _) in enumerate(overdue)
    )

    await update.message.reply_text(f"⚠️ Overdue Tasks:\n\n{task_list}")


async def reminder_checker(context):
    current_time = datetime.now()

    cur = conn.cursor()  # Bug 1 fix: local cursor
    cur.execute(
        "SELECT * FROM tasks WHERE due_date IS NOT NULL AND reminded = 0"
    )
    rows = cur.fetchall()

    for row in rows:
        due_date = row["due_date"]
        try:
            due_time = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        except ValueError:
            continue

        time_left = due_time - current_time
        if 0 < time_left.total_seconds() <= 3600:
            try:  # Bug 4 fix: don't let a failed send kill the whole loop
                await context.bot.send_message(
                    chat_id=int(row["user_id"]),
                    text=(
                        f"🔔 Reminder!\n\n"
                        f"Task: {row['task']}\n"
                        f"Due: {due_date}"
                    )
                )
                db_mark_reminded(row["id"])
            except Exception:
                pass


async def streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    stats_row = db_get_stats(user_id)
    current_streak = stats_row["streak"] if stats_row else 0

    await update.message.reply_text(f"🔥 Current Streak: {current_streak} day(s)")


async def pomodoro_complete(context):
    job = context.job
    user_id = str(job.data)

    if user_id in active_pomodoros:
        del active_pomodoros[user_id]

    db_ensure_stats(user_id)
    db_increment_pomodoros(user_id)

    stats_row = db_get_stats(user_id)
    completed = stats_row["pomodoros_completed"]

    await context.bot.send_message(
        chat_id=int(user_id),
        text=(
            f"🎉 Pomodoro Complete!\n\n"
            f"Great work! Take a short break.\n\n"
            f"🍅 Total Pomodoros: {completed}"
        )
    )


async def pomodoro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id in active_pomodoros:
        await update.message.reply_text(
            "⚠️ You already have an active Pomodoro session."
        )
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /pomodoro <minutes>")
        return

    try:
        minutes = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Minutes must be a number.")
        return

    if minutes <= 0:  # Bug 3 fix: reject non-positive values
        await update.message.reply_text("Please enter a positive number of minutes.")
        return

    job = context.job_queue.run_once(
        pomodoro_complete,
        when=minutes * 60,
        data=user_id
    )

    active_pomodoros[user_id] = job

    await update.message.reply_text(
        f"🍅 Pomodoro started!\n\n"
        f"Focus for {minutes} minute(s)."
    )


async def pomodoro_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    stats_row = db_get_stats(user_id)
    completed = stats_row["pomodoros_completed"] if stats_row else 0

    await update.message.reply_text(f"🍅 Pomodoros Completed: {completed}")


async def cancel_pomodoro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    job = active_pomodoros.get(user_id)

    if not job:
        await update.message.reply_text("❌ No active Pomodoro session found.")
        return

    job.schedule_removal()
    del active_pomodoros[user_id]

    await update.message.reply_text("🛑 Pomodoro session cancelled.")


async def analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    stats_row = db_get_stats(user_id)
    streak_val = stats_row["streak"] if stats_row else 0
    pomodoros = stats_row["pomodoros_completed"] if stats_row else 0

    rows = db_get_tasks(user_id)
    total_tasks = len(rows)
    high_priority = sum(1 for r in rows if r["priority"] == "High")
    due_dates = sum(1 for r in rows if r["due_date"] is not None)

    await update.message.reply_text(
        f"📊 FocusFlow Analytics\n\n"
        f"🔥 Current Streak: {streak_val} day(s)\n\n"
        f"🍅 Pomodoros Completed: {pomodoros}\n\n"
        f"📋 Active Tasks: {total_tasks}\n\n"
        f"🚨 High Priority Tasks: {high_priority}\n\n"
        f"⏰ Tasks With Due Dates: {due_dates}"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("addtask", add_task))
    app.add_handler(CommandHandler("tasks", show_tasks))
    app.add_handler(CommandHandler("done", done_task))
    app.add_handler(CommandHandler("setpriority", set_priority))
    app.add_handler(CommandHandler("highpriority", high_priority_tasks))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("setdue", set_due))
    app.add_handler(CommandHandler("upcoming", upcoming_tasks))
    app.add_handler(CommandHandler("overdue", overdue_tasks))
    app.add_handler(CommandHandler("streak", streak))
    app.add_handler(CommandHandler("pomodoro", pomodoro))
    app.add_handler(CommandHandler("analytics", analytics))
    app.add_handler(CommandHandler("pomodorostats", pomodoro_stats))
    app.add_handler(CommandHandler("cancelpomodoro", cancel_pomodoro))

    job_queue = app.job_queue
    job_queue.run_repeating(reminder_checker, interval=60, first=10)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
