from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from dotenv import load_dotenv
import os

#Load environment variables 
load_dotenv()

#Get bot token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

tasks = []

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
    
    #Add task to list 
    tasks.append(task)

    await update.message.reply_text(
        f"Task added successfully ✅\nTask: {task}"
    )

#/TASKS COMMAND

async def show_tasks(update: Update, context : ContextTypes.DEFAULT_TYPE):

    #Check if no tasks exist
    if not tasks:
        await update.message.reply_text(
            "No tasks availaible."
        )
        return
    
    #Create tasks list

    task_list = "\n".join(
         [f"{i+1}. {task}" for i, task in enumerate(tasks)]

    )

    await update.message.reply_text(
        f"Your Tasks:\n\n{task_list}"
        )
    
# /done command
async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
        if task_number < 1 or task_number > len(tasks):
            await update.message.reply_text(
                "Invalid task number."
            )
            return

        # Remove task
        removed_task = tasks.pop(task_number - 1)

        await update.message.reply_text(
            f"Task completed ✅\nRemoved: {removed_task}"
        )

    except ValueError:
        await update.message.reply_text(
            "Please enter a valid number."
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

    #Run bot
    print("Bot is running...")
    app.run_polling()

if __name__=="__main__":
    main()
