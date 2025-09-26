#!/usr/bin/env python3
"""
Создание демо голосового сообщения
"""

import random
from gtts import gTTS

def convert_to_personal_voice_style(text):
    """Конвертирует текст под персональный стиль речи"""
    voice_replacements = {
        "ч": "ш", "щ": "ш", "ц": "с", "ж": "з",
        "ы": "и", "э": "е", "ю": "у", "я": "а", "ё": "e",
        "ь": "", "ъ": "",
        "рублей": "руб", "рубли": "руб", "руб": "руб",
        "материалы": "матёриалы", "инструменты": "инструменты",
        "такси": "такси", "машина": "машина",
        "₽": " руб", ",": ", ну,", ".": ", понял?", "!": ", да!", "?": ", а?"
    }
    
    characteristic_insertions = [
        " ну,", " да,", " вот,", " так,", " значит,",
        " понимаешь,", " слушай,", " смотри,",
        " короче,", " в общем,", " кстати,"
    ]
    
    emotional_amplifiers = [
        " очень", " сильно", " реально", " конкретно",
        " прям", " вообще", " совсем", " совсем-совсем"
    ]
    
    result = text.lower()
    for original, replacement in voice_replacements.items():
        result = result.replace(original, replacement)
    
    if random.random() < 0.4:
        insertion = random.choice(characteristic_insertions)
        words = result.split()
        if len(words) > 2:
            insert_pos = random.randint(1, len(words) - 1)
            words.insert(insert_pos, insertion.strip())
            result = " ".join(words)
    
    if random.random() < 0.3:
        amplifier = random.choice(emotional_amplifiers)
        words = result.split()
        if words:
            word_pos = random.randint(0, len(words) - 1)
            words[word_pos] = f"{amplifier} {words[word_pos]}"
            result = " ".join(words)
    
    if random.random() < 0.2:
        result = result.replace("а", "ах", 1)
    if random.random() < 0.15:
        result = result.replace("о", "ох", 1)
        
    return result

def main():
    """Создает демо голосовое сообщение"""
    
    print("🎤 СОЗДАНИЕ ДЕМО ГОЛОСОВОГО СООБЩЕНИЯ")
    print("=" * 40)
    
    # Создаем более длинное демо сообщение
    demo_text = "привет, братан, работа есть, помыть машину, 2000 рублей, такси с меня, быстро сделаем, понял?"
    
    print(f"📝 Исходный текст: {demo_text}")
    
    # Трансформируем
    transformed = convert_to_personal_voice_style(demo_text)
    print(f"🎭 Трансформированный: {transformed}")
    
    try:
        # Создаем TTS
        tts = gTTS(text=transformed, lang='ru', slow=False)
        
        # Сохраняем
        filename = "demo_voice_message.mp3"
        tts.save(filename)
        
        print(f"✅ Демо создано: {filename}")
        print("\n🎧 Откройте файл для прослушивания!")
        print("💡 Это пример того, как будет звучать ваш бот в канале.")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
