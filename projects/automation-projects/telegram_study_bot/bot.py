from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from datetime import datetime

from dotenv import load_dotenv
import os
import json


#Load environment variables 
load_dotenv()

#Get bot token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

#load_task 

def load_tasks():
    try:
        with open("data/tasks.json","r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    


def load_user_stats():
    try:
        with open("data/user_stats.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
tasks = load_tasks()
user_stats = load_user_stats()

#Save task to json file

def save_tasks():

    with open("data/tasks.json","w") as file:
        json.dump(tasks, file, indent=4)


def save_user_stats():
    with open("data/user_stats.json", "w") as file:
        json.dump(user_stats, file, indent=4)


#/START COMMAND

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! FocusFlow Bot is running now  🚀"

    )

#/HELP COMMAND

async def help_command(update: Update, context : ContextTypes.DEFAULT_TYPE):   

    help_text = """
/start - Start the bot
/help - Show commands
/addtask - Add a new task
/tasks - View all tasks
"""
    await update.message.reply_text(help_text)

#ADDTASK COMMAND

async def add_task(update: Update, context : ContextTypes.DEFAULT_TYPE):

    #Get task set
    task = " ".join(context.args)

    #Check if task is empty:
    if not task:
        await update.message.reply_text(
            "Please provide a task.\nExample: /addtask Study Python"
        )
        return
    
    #User id for differnet users
    user_id = str(update.effective_user.id)
    if user_id not in tasks:
        tasks[user_id] = []

    #Current time 
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    #task data
    task_data = {
        "task":task,
        "priority":"Medium",
        "created_at":current_time,
        "due_date":None,
        "reminded": False
    }

    #Add task to list 
    tasks[user_id].append(task_data)

    #save tasks
    save_tasks()

    await update.message.reply_text(
        f"Task added successfully ✅\nTask: {task}"
    )

#/TASKS COMMAND

async def show_tasks(update: Update, context : ContextTypes.DEFAULT_TYPE):
    
    user_id = str(update.effective_user.id)
    if user_id not in tasks:
        await update.message.reply_text(
            "No tasks available."
    )
        return

    #Check if no tasks exist
    if not tasks:
        await update.message.reply_text(
            "No tasks availaible."
        )
        return
    
    #Create tasks list

    task_list = "\n\n".join(
    [
        f"{i+1}. {task['task']}\n"
        f"   Priority: {task['priority']}\n"
        f"   Added: {task['created_at']}\n"
        f"   Due: {'Not Set' if task['due_date'] is None else task['due_date']}"
        for i, task in enumerate(tasks[user_id])
    ]
)

    await update.message.reply_text(
        f"Your Tasks:\n\n{task_list}"
        )
    
# /done command
async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_id = str(update.effective_user.id)
    if user_id not in tasks:
        await update.message.reply_text(
            "No tasks available."
    )
        return

    # Check if user provided task number
    if not context.args:
        await update.message.reply_text(
            "Please provide task number.\nExample: /done 1"
        )
        return

    try:
        # Convert input to integer
        task_number = int(context.args[0])

        # Check valid range
        if task_number < 1 or task_number > len(tasks[user_id]):
            await update.message.reply_text(
                "Invalid task number."
            )
            return
        
        if user_id not in user_stats:
            user_stats[user_id] = {
                "streak": 0,
                "last_completed_date": None
            }

        today = datetime.now().date()

        last_date = user_stats[user_id]["last_completed_date"]

        if last_date is None:

            user_stats[user_id]["streak"] = 1

        else:

            last_date = datetime.strptime(
                last_date,
                "%Y-%m-%d"
            ).date()

            difference = (today - last_date).days

            if difference == 0:
                pass

            elif difference == 1:
                user_stats[user_id]["streak"] += 1

            else:
                user_stats[user_id]["streak"] = 1

        user_stats[user_id]["last_completed_date"] = str(today)

        save_user_stats()

        # Remove task
        removed_task = tasks[user_id].pop(task_number - 1)

        # Save tasks
        save_tasks()

        await update.message.reply_text(
            f"✅ Task completed: {removed_task['task']}\n\n"
            f"🔥 Current Streak: {user_stats[user_id]['streak']} day(s)"
        )


    except ValueError:
        await update.message.reply_text(
            "Please enter a valid number."
        )

# /set priority 
async def set_priority(update, context):

    user_id = str(update.effective_user.id)

    if user_id not in tasks:
        await update.message.reply_text(
            "No tasks available."
        )
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage: /setpriority <task_number> <High|Medium|Low>"
        )
        return

    try:
        task_number = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Task number must be a valid number."
        )
        return

    priority = context.args[1].capitalize()

    if priority not in ["High", "Medium", "Low"]:
        await update.message.reply_text(
            "Priority must be High, Medium, or Low."
        )
        return

    if task_number < 1 or task_number > len(tasks[user_id]):
        await update.message.reply_text(
            "Invalid task number."
        )
        return

    tasks[user_id][task_number - 1]["priority"] = priority

    save_tasks()

    await update.message.reply_text(
        f"✅ Priority updated to {priority}"
    )

async def high_priority_tasks(update,context):
    user_id = str(update.effective_user.id)

    if user_id not in tasks:
        await update.message.reply_text(
            "No tasks available"
        )
        return
    
    high_tasks = []
    for task in tasks[user_id]:
        if task["priority"]=="High":
            high_tasks.append(task)

    if not high_tasks:
        await update.message.reply_text(
            "No high-priority tasks found."
        )
        return
    
    task_list = "\n".join(
        [
            f"{i+1}. {task['task']}"
            for i, task in enumerate(high_tasks)
        ]
    )

    await update.message.reply_text(
        f"🔥 High Priority Tasks\n\n{task_list}"
    )

async def stats(update, context):
    user_id = str(update.effective_user.id)

    if user_id not in tasks:
        await update.message.reply_text(
            "No tasks available"
        )
        return
    
    total_tasks = len(tasks[user_id])

    high_count = 0 
    low_count = 0
    medium_count = 0

    for task in tasks[user_id]:
        if task["priority"] == "High":
            high_count+=1
        elif task["priority"] == "Low":
            low_count+=1
        elif task["priority"] == "Medium":
            medium_count+=1

    await update.message.reply_text(
        f"📊 Task Statistics\n\n"
        f"Total Tasks: {total_tasks}\n"
        f"High Priority: {high_count}\n"
        f"Medium Priority: {medium_count}\n"
        f"Low Priority: {low_count}"
    )

async def set_due(update, context):

    user_id = str(update.effective_user.id)

    if user_id not in tasks:
        await update.message.reply_text(
            "No tasks available."
        )
        return

    if len(context.args) not in [2,3]:
        await update.message.reply_text(
            "Usage:\n/setdue <task_number> <YYYY-MM-DD>\nOR\n/setdue <task_number> <YYYY-MM-DD HH:MM>"
        )
        return

    try:
        task_number = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Task number must be a valid number."
        )
        return

    if len(context.args) == 2:
        due_date = context.args[1]

    else:
        due_date = context.args[1] + " " + context.args[2]

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

    if task_number < 1 or task_number > len(tasks[user_id]):
        await update.message.reply_text(
            "Invalid task number."
        )
        return

    tasks[user_id][task_number - 1]["due_date"] = due_date
    tasks[user_id][task_number - 1]["reminded"] = False

    save_tasks()

    await update.message.reply_text(
        f"⏰ Due date for task {task_number} set to {due_date}" 
    )

async def upcoming_tasks(update, context):

    user_id = str(update.effective_user.id)

    if user_id not in tasks:
        await update.message.reply_text(
            "No tasks available."
        )
        return

    upcoming = []

    for i, task in enumerate(tasks[user_id]):

        due_date = task.get("due_date")

        if due_date is not None:

            try:
                try:
                    due_obj = datetime.strptime(
                        due_date,
                        "%Y-%m-%d %H:%M"
                    )

                except ValueError:
                    due_obj = datetime.strptime(
                        due_date,
                        "%Y-%m-%d"
                    )

                upcoming.append(
                    (i, task, due_obj)
                )

            except ValueError:
                continue

    if not upcoming:
        await update.message.reply_text(
            "No upcoming tasks."
        )
        return

    upcoming.sort(key=lambda x: x[2])

    task_list = "\n\n".join(
        [
            f"{i+1}. {task['task']}\n"
            f"   Priority: {task['priority']}\n"
            f"   Due: {task['due_date']}"
            for i, task, _ in upcoming
        ]
    )

    await update.message.reply_text(
        f"📅 Upcoming Tasks:\n\n{task_list}"
    )

async def overdue_tasks(update, context):

    user_id = str(update.effective_user.id)

    if user_id not in tasks:
        await update.message.reply_text(
            "No tasks available."
        )
        return

    overdue = []

    current_time = datetime.now()

    for i, task in enumerate(tasks[user_id]):

        due_date = task.get("due_date")

        if due_date is not None:

            try:
                try:
                    due_obj = datetime.strptime(
                        due_date,
                        "%Y-%m-%d %H:%M"
                    )

                except ValueError:
                    due_obj = datetime.strptime(
                        due_date,
                        "%Y-%m-%d"
                    )

                if due_obj < current_time:

                    overdue.append(
                        (i, task, due_obj)
                    )

            except ValueError:
                continue

    if not overdue:
        await update.message.reply_text(
            "🎉 No overdue tasks."
        )
        return

    overdue.sort(key=lambda x: x[2])

    task_list = "\n\n".join(
        [
            f"{i+1}. {task['task']}\n"
            f"   Priority: {task['priority']}\n"
            f"   Due: {task['due_date']}"
            for i, task, _ in overdue
        ]
    )

    await update.message.reply_text(
        f"⚠️ Overdue Tasks:\n\n{task_list}"
    )

async def reminder_checker(context):

    current_time = datetime.now()

    for user_id, user_tasks in tasks.items():

        for task in user_tasks:

            due_date = task.get("due_date")

            if due_date is None:
                continue

            try:

                try:
                    due_time = datetime.strptime(
                        due_date,
                        "%Y-%m-%d %H:%M"
                    )

                except ValueError:
                    continue

                time_left = due_time - current_time

                if (
                    time_left.total_seconds() <= 3600
                    and time_left.total_seconds() > 0
                    and not task.get("reminded", False)
                ):

                    await context.bot.send_message(
                        chat_id=user_id,
                        text=(
                            f"🔔 Reminder!\n\n"
                            f"Task: {task['task']}\n"
                            f"Due: {due_date}"
                        )
                    )

                    task["reminded"] = True

                    save_tasks()

            except Exception:
                continue



async def streak(update, context):

    user_id = str(update.effective_user.id)

    if user_id not in user_stats:
        await update.message.reply_text(
            "🔥 Current Streak: 0 days"
        )
        return

    current_streak = user_stats[user_id]["streak"]

    await update.message.reply_text(
        f"🔥 Current Streak: {current_streak} day(s)"
    )



#Main function

def main():
    #Application create
    app = Application.builder().token(BOT_TOKEN).build()

    #App command handler
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("addtask", add_task))
    app.add_handler(CommandHandler("tasks", show_tasks))
    app.add_handler(CommandHandler("done", done_task))
    app.add_handler(CommandHandler("setpriority", set_priority))
    app.add_handler(CommandHandler("highpriority", high_priority_tasks))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("setdue", set_due))
    app.add_handler(CommandHandler("upcoming",upcoming_tasks))
    app.add_handler(CommandHandler("overdue",overdue_tasks))
    app.add_handler(CommandHandler("streak", streak))

    # Reminder Job
    job_queue = app.job_queue

    job_queue.run_repeating(
        reminder_checker,
        interval=60,
        first=10
    )

    #Run bot
    print("Bot is running...")
    app.run_polling()

if __name__=="__main__":
    main()
