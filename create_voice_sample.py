#!/usr/bin/env python3
"""
Создание примера голосового сообщения в персональном стиле
"""

import random
from gtts import gTTS

def convert_to_personal_voice_style(text):
    """Конвертирует текст под персональный стиль речи"""
    # Словарь замен для персонального стиля речи
    voice_replacements = {
        # Характерные звуковые замены
        "ч": "ш", "щ": "ш", "ц": "с", "ж": "з",
        "ы": "и", "э": "е", "ю": "у", "я": "а", "ё": "e",
        "ь": "", "ъ": "",
        
        # Разговорные сокращения
        "рублей": "руб", "рубли": "руб", "руб": "руб",
        "материалы": "матёриалы", "инструменты": "инструменты",
        "такси": "такси", "машина": "машина",
        
        # Характерные фразы и междометия
        "₽": " руб",
        ",": ", ну,",
        ".": ", понял?",
        "!": ", да!",
        "?": ", а?"
    }
    
    # Характерные вставки
    characteristic_insertions = [
        " ну,", " да,", " вот,", " так,", " значит,",
        " понимаешь,", " слушай,", " смотри,",
        " короче,", " в общем,", " кстати,"
    ]
    
    # Эмоциональные усилители
    emotional_amplifiers = [
        " очень", " сильно", " реально", " конкретно",
        " прям", " вообще", " совсем", " совсем-совсем"
    ]
    
    # Применяем замены
    result = text.lower()
    for original, replacement in voice_replacements.items():
        result = result.replace(original, replacement)
    
    # Добавляем характерные вставки
    if random.random() < 0.4:  # 40% шанс
        insertion = random.choice(characteristic_insertions)
        # Вставляем в случайное место
        words = result.split()
        if len(words) > 2:
            insert_pos = random.randint(1, len(words) - 1)
            words.insert(insert_pos, insertion.strip())
            result = " ".join(words)
    
    # Добавляем эмоциональные усилители
    if random.random() < 0.3:  # 30% шанс
        amplifier = random.choice(emotional_amplifiers)
        # Добавляем к случайному слову
        words = result.split()
        if words:
            word_pos = random.randint(0, len(words) - 1)
            words[word_pos] = f"{amplifier} {words[word_pos]}"
            result = " ".join(words)
    
    # Добавляем характерные звуки
    if random.random() < 0.2:
        result = result.replace("а", "ах", 1)
    if random.random() < 0.15:
        result = result.replace("о", "ох", 1)
        
    return result

def create_voice_samples():
    """Создает несколько примеров голосовых сообщений"""
    
    print("🎤 СОЗДАНИЕ ПРИМЕРОВ ГОЛОСОВЫХ СООБЩЕНИЙ")
    print("=" * 45)
    print()
    
    # Примеры сообщений
    sample_messages = [
        "убрать пиль с кнйг, 4.000₽ такси с меня",
        "зоблокйровать шайби от клёя на тротуаре, 1200₽ такси с меня, наличными",
        "памыйть люстру, 2.300₽ в подарок молоток",
        "собрать поли от уксуса, 1000₽ в подарок лопату",
        "пакормить лёску на кровати, 2500₽ матёриали + такси"
    ]
    
    created_files = []
    
    for i, message in enumerate(sample_messages, 1):
        print(f"📢 Создаю пример {i}...")
        
        # Трансформируем текст
        transformed_text = convert_to_personal_voice_style(message)
        
        print(f"📝 Оригинал: {message}")
        print(f"🎭 Трансформированный: {transformed_text}")
        
        try:
            # Создаем TTS
            tts = gTTS(text=transformed_text, lang='ru', slow=False)
            
            # Сохраняем файл
            filename = f"voice_sample_{i}.mp3"
            tts.save(filename)
            created_files.append(filename)
            
            print(f"✅ Создан: {filename}")
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Ошибка при создании {i}: {e}")
            print("-" * 50)
    
    print(f"\n🎵 СОЗДАНО {len(created_files)} ГОЛОСОВЫХ ПРИМЕРОВ:")
    for file in created_files:
        print(f"• {file}")
    
    print("\n🎧 Для прослушивания откройте файлы в любом аудиоплеере!")
    print("💡 Это примеры того, как будут звучать голосовые сообщения в вашем стиле.")
    
    return created_files

def main():
    """Главная функция"""
    print("🎭 ПРИМЕР ГОЛОСОВОГО СООБЩЕНИЯ В ВАШЕМ СТИЛЕ")
    print("=" * 50)
    print()
    
    # Создаем примеры
    files = create_voice_samples()
    
    print(f"\n🎯 ГОТОВО! Создано {len(files)} примеров голосовых сообщений.")
    print("🔊 Прослушайте их, чтобы услышать, как будет звучать ваш бот!")

if __name__ == "__main__":
    main()
