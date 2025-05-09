from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your actual bot token
TOKEN: final = "Enter_your_token"
BOT_USERNAME: final = "Enter_your_bot_username"


# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm Dummy Bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type something and I will try to respond!")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command.")


# Text response logic
def handle_response(text: str) -> str:
    processed = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    if any(greet in processed for greet in ['hi', 'hii', 'hie']):
        return 'Hello there!'
    if 'Who are you' in processed:
        return 'I am a dummy bot.'
    if any(bye in processed for bye in ['bye', 'byee']):
        return "Bye, take care!"

    return "I don't understand what you're saying!"


# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_type = update.message.chat.type

    print(f'User({update.message.chat.id}) in {chat_type}: "{text}"')

    if chat_type in ['group', 'supergroup']:
        if BOT_USERNAME in text:
            # Remove bot mention and process the remaining text
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            return  # Ignore messages not mentioning the bot
    else:
        response = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error: {context.error}")


# Main function to run the bot
if __name__ == '__main__':
    print("Starting the bot...")
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    app.add_error_handler(error_handler)

    # Run the bot
    print("Bot is polling...")
    app.run_polling(poll_interval=3)

