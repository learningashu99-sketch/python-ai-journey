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
        return []
    
tasks = load_tasks()

#Save task to json file

def save_tasks():

    with open("data/tasks.json","w") as file:
        json.dump(tasks, file, indent=4)


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
        "created_at":current_time
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

    task_list = "\n".join(
    [
        f"{i+1}. {task['task']}\n   Priority: {task['priority']}\n   Added: {task['created_at']}"
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

        # Remove task
        removed_task = tasks[user_id].pop(task_number - 1)

        # Save tasks
        save_tasks()

        await update.message.reply_text(
            f"✅ Task completed: {removed_task['task']}"
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

    #Run bot
    print("Bot is running...")
    app.run_polling()

if __name__=="__main__":
    main()
