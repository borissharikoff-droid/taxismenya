#!/usr/bin/env python3
"""
Тест персонального стиля речи
"""

import random

def convert_to_personal_voice_style(text):
    """Конвертирует текст под персональный стиль речи на основе анализа голоса"""
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

def main():
    """Тестирование персонального стиля речи"""
    print("🎭 ТЕСТ ПЕРСОНАЛЬНОГО СТИЛЯ РЕЧИ")
    print("=" * 40)
    print()
    
    # Тестовые сообщения
    test_messages = [
        "убрать пиль с кнйг, 4.000₽ такси с меня",
        "зоблокйровать шайби от клёя на тротуаре, 1200₽ такси с меня, наличными",
        "памыйть люстру, 2.300₽ в подарок молоток",
        "собрать поли от уксуса, 1000₽ в подарок лопату",
        "пакормить лёску на кровати, 2500₽ матёриали + такси"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"📢 ПРИМЕР {i}:")
        print(f"📝 Оригинал: {message}")
        
        # Показываем несколько вариантов трансформации
        for variant in range(3):
            transformed = convert_to_personal_voice_style(message)
            print(f"🎭 Вариант {variant + 1}: {transformed}")
        
        print("-" * 50)
    
    print("\n🎤 ОСОБЕННОСТИ ПЕРСОНАЛЬНОГО СТИЛЯ:")
    print("• Звуковые замены: ч→ш, щ→ш, ц→с, ж→з")
    print("• Разговорные сокращения: рублей→руб")
    print("• Характерные вставки: 'ну', 'да', 'вот', 'так'")
    print("• Эмоциональные усилители: 'очень', 'сильно', 'реально'")
    print("• Междометия: 'понимаешь', 'слушай', 'смотри'")
    print("• Вопросы в конце: 'понял?', 'а?'")
    print()
    print("✅ Этот стиль теперь используется в боте!")
    print("🎯 Голосовые сообщения будут звучать в вашем стиле!")

if __name__ == "__main__":
    main()
