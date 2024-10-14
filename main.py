import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

current_question = None
current_answer = None
score = 0

def generate_question():
    operations = ['+', '-', '*', '/']
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(operations)

    if operation == '/':
        num1 *= num2

    question = f"{num1} {operation} {num2}"
    answer = eval(question)
    return question, round(answer, 2)

async def start(update: Update, context):
    global score
    score = 0
    await update.message.reply_text("Привет! Давай решать мат задачки")
    await send_new_question(update)

async def send_new_question(update: Update):
    global current_question, current_answer
    current_question, current_answer = generate_question()
    await update.message.reply_text(f"{current_question} = ")

async def handle_message(update: Update, context):
    global score

    try:
        user_answer = float(update.message.text)
    except ValueError:
        await update.message.reply_text("Пожалуйста, напиши свой ответ")
        return

    if user_answer == current_answer:
        score += 1
        await update.message.reply_text(f"Молодец, все правильно! Текущий счет: {score}.")
    else:
        await update.message.reply_text(f"Неправильно, думаю тебе стоит подтянуть свои знания. Правильный ответ был {current_answer}. Текущий счет: {score}.")

    await send_new_question(update)

async def finish(update: Update, context):
    global score
    await update.message.reply_text(f"Викторина завершена! Твой счет: {score}. Призов нет, извини))")
    score = 0

async def main():
    token = 'тг токен закиньте сюда'

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("finish", finish))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.start()
    await application.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
