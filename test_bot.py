"""
Тестовый скрипт для проверки генерации сообщений бота
"""
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Устанавливаем фейковые токены для теста
os.environ["BOT_TOKEN"] = "test_token"
os.environ["CHANNEL_ID"] = "test_channel"

from bot import WorkBot

def test_message_generation():
    """Тестирует генерацию сообщений"""
    print("🧪 Тестирование генерации сообщений...\n")
    
    bot = WorkBot()
    
    # Генерируем 10 обычных сообщений
    print("📝 Обычные сообщения о работе:")
    print("=" * 80)
    for i in range(10):
        message = bot.generate_message()
        print(f"{i+1}. {message}")
    
    print("\n" + "=" * 80)
    
    # Генерируем 5 голосовых текстов
    print("\n🎤 Тексты для голосовых сообщений:")
    print("=" * 80)
    for i in range(5):
        message = bot.generate_message()
        voice_text = bot.convert_to_personal_voice_style(message)
        print(f"{i+1}. Оригинал: {message}")
        print(f"   Голос: {voice_text}\n")
    
    print("=" * 80)
    
    # Генерируем 5 ответных сообщений
    print("\n✅ Ответные сообщения (работа выполнена):")
    print("=" * 80)
    for i in range(5):
        completion = bot.generate_completion_message()
        print(f"{i+1}. {completion}")
    
    print("\n" + "=" * 80)
    print("\n✅ Тест завершен успешно!")

def test_uniqueness():
    """Тестирует уникальность сообщений"""
    print("\n🔍 Тестирование уникальности сообщений...\n")
    
    bot = WorkBot()
    messages = []
    
    # Генерируем 50 сообщений
    for _ in range(50):
        message = bot.generate_message()
        messages.append(message)
    
    # Проверяем уникальность
    unique_messages = set(messages)
    duplicates = len(messages) - len(unique_messages)
    
    print(f"Всего сгенерировано: {len(messages)}")
    print(f"Уникальных: {len(unique_messages)}")
    print(f"Дубликатов: {duplicates}")
    print(f"Процент уникальности: {len(unique_messages) / len(messages) * 100:.1f}%")
    
    if duplicates > 0:
        print(f"\n⚠️ Найдено {duplicates} дубликатов")
    else:
        print("\n✅ Все сообщения уникальны!")

def show_funny_examples():
    """Показывает примеры смешных элементов"""
    print("\n😂 Примеры смешных элементов:\n")
    
    bot = WorkBot()
    
    print("🎁 Абсурдные подарки:")
    print("=" * 80)
    funny_bonuses = [b for b in bot.bonuses if "в подарок" in b]
    for i, bonus in enumerate(funny_bonuses[:15], 1):
        print(f"{i}. {bonus}")
    
    print("\n📋 Смешные условия:")
    print("=" * 80)
    funny_extras = [e for e in bot.extra_info if any(word in e for word in ["собака", "бабушка", "сосед", "туалет", "трусах"])]
    for i, extra in enumerate(funny_extras[:10], 1):
        print(f"{i}. {extra}")
    
    print("\n💬 Угарные дополнения:")
    print("=" * 80)
    funny_quirky = [q for q in bot.quirky_additions if any(word in q for word in ["жена", "кот", "крыса", "тесть", "теща"])]
    for i, quirky in enumerate(funny_quirky[:10], 1):
        print(f"{i}. {quirky}")
    
    print("\n🎉 Подарки за выполненную работу:")
    print("=" * 80)
    funny_completion = [c for c in bot.completion_details if any(word in c for word in ["сигарет", "самогон", "шаурм", "пиво", "сало"])]
    for i, detail in enumerate(funny_completion[:10], 1):
        print(f"{i}. {detail}")

if __name__ == "__main__":
    print("\n" + "🤖 ТЕСТИРОВАНИЕ БОТА ".center(80, "="))
    print()
    
    try:
        test_message_generation()
        test_uniqueness()
        show_funny_examples()
        
        print("\n" + "=" * 80)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!".center(80))
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

