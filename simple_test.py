import os
os.environ["BOT_TOKEN"] = "test"
os.environ["CHANNEL_ID"] = "test"

from bot import WorkBot

print("Инициализация бота...")
bot = WorkBot()

print("\n=== ТЕСТ 1: Генерация обычных сообщений ===")
for i in range(5):
    msg = bot.generate_message()
    print(f"{i+1}. {msg}")

print("\n=== ТЕСТ 2: Генерация голосовых текстов ===")
for i in range(3):
    msg = bot.generate_message()
    voice = bot.convert_to_personal_voice_style(msg)
    print(f"{i+1}. {voice}")

print("\n=== ТЕСТ 3: Ответные сообщения ===")
for i in range(3):
    comp = bot.generate_completion_message()
    print(f"{i+1}. {comp}")

print("\n✅ Все тесты пройдены!")

