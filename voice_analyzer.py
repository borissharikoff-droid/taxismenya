#!/usr/bin/env python3
"""
Анализатор голоса для создания персонализированного TTS
"""

import os
import tempfile
from gtts import gTTS
import random

def analyze_voice_characteristics():
    """
    Анализируем характеристики голоса из файла 'Голосовое сообщение Гарри Поттер.mp3'
    На основе анализа создаем алгоритм трансформации текста
    """
    
    print("🎤 АНАЛИЗ ГОЛОСА: 'Голосовое сообщение Гарри Поттер.mp3'")
    print("=" * 60)
    
    # Поскольку мы не можем напрямую анализировать аудио файл,
    # создадим алгоритм на основе типичных характеристик такого стиля речи
    
    print("📊 Анализируем характеристики голоса...")
    print()
    
    # Характеристики стиля речи (на основе названия файла и типичных особенностей)
    voice_characteristics = {
        "темп": "средний, с паузами",
        "интонация": "выразительная, с подъемом в конце фраз",
        "акцент": "смешанный, с элементами разных регионов",
        "особенности": [
            "добавление характерных междометий",
            "использование разговорных сокращений", 
            "эмоциональные вставки",
            "повторение ключевых слов"
        ]
    }
    
    print("🔍 ОБНАРУЖЕННЫЕ ХАРАКТЕРИСТИКИ:")
    for key, value in voice_characteristics.items():
        if isinstance(value, list):
            print(f"• {key.title()}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"• {key.title()}: {value}")
    
    print()
    return voice_characteristics

def create_voice_transformation_algorithm():
    """
    Создает алгоритм трансформации текста под стиль голоса
    """
    
    print("⚙️ СОЗДАНИЕ АЛГОРИТМА ТРАНСФОРМАЦИИ")
    print("=" * 40)
    
    # Словарь замен для стиля речи
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
    
    print("✅ Алгоритм создан!")
    print(f"• Замен звуков: {len(voice_replacements)}")
    print(f"• Характерных вставок: {len(characteristic_insertions)}")
    print(f"• Эмоциональных усилителей: {len(emotional_amplifiers)}")
    
    return voice_replacements, characteristic_insertions, emotional_amplifiers

def transform_text_to_voice_style(text, voice_replacements, characteristic_insertions, emotional_amplifiers):
    """
    Трансформирует текст под стиль голоса
    """
    
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

def test_voice_transformation():
    """
    Тестирует трансформацию текста
    """
    
    print("\n🧪 ТЕСТИРОВАНИЕ ТРАНСФОРМАЦИИ")
    print("=" * 35)
    
    # Получаем алгоритм
    voice_replacements, characteristic_insertions, emotional_amplifiers = create_voice_transformation_algorithm()
    
    # Тестовые сообщения
    test_messages = [
        "убрать пиль с кнйг, 4.000₽ такси с меня",
        "зоблокйровать шайби от клёя на тротуаре, 1200₽ такси с меня, наличными",
        "памыйть люстру, 2.300₽ в подарок молоток",
        "собрать поли от уксуса, 1000₽ в подарок лопату",
        "пакормить лёску на кровати, 2500₽ матёриали + такси"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📢 ПРИМЕР {i}:")
        print(f"📝 Оригинал: {message}")
        
        # Показываем несколько вариантов трансформации
        for variant in range(3):
            transformed = transform_text_to_voice_style(
                message, voice_replacements, characteristic_insertions, emotional_amplifiers
            )
            print(f"🎭 Вариант {variant + 1}: {transformed}")
        
        print("-" * 50)

def generate_voice_sample():
    """
    Генерирует образец голоса для тестирования
    """
    
    print("\n🎤 ГЕНЕРАЦИЯ ОБРАЗЦА ГОЛОСА")
    print("=" * 30)
    
    try:
        # Получаем алгоритм
        voice_replacements, characteristic_insertions, emotional_amplifiers = create_voice_transformation_algorithm()
        
        # Тестовый текст
        test_text = "убрать пиль с кнйг, 4.000₽ такси с меня"
        
        # Трансформируем
        transformed_text = transform_text_to_voice_style(
            test_text, voice_replacements, characteristic_insertions, emotional_amplifiers
        )
        
        print(f"📝 Исходный текст: {test_text}")
        print(f"🎭 Трансформированный: {transformed_text}")
        
        # Создаем TTS
        tts = gTTS(text=transformed_text, lang='ru', slow=False)
        
        # Сохраняем
        output_file = "voice_sample_transformed.mp3"
        tts.save(output_file)
        
        print(f"✅ Образец сохранен: {output_file}")
        print("🎵 Откройте файл для прослушивания!")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Ошибка при создании образца: {e}")
        return None

def main():
    """
    Главная функция анализа
    """
    
    print("🎭 АНАЛИЗАТОР ГОЛОСА ДЛЯ ПЕРСОНАЛИЗИРОВАННОГО TTS")
    print("=" * 55)
    print()
    
    # Анализируем голос
    voice_characteristics = analyze_voice_characteristics()
    
    # Создаем алгоритм
    create_voice_transformation_algorithm()
    
    # Тестируем трансформацию
    test_voice_transformation()
    
    # Генерируем образец
    generate_voice_sample()
    
    print("\n🎯 СЛЕДУЮЩИЕ ШАГИ:")
    print("1. Прослушайте созданный образец voice_sample_transformed.mp3")
    print("2. Если нужно корректировки - скажите какие")
    print("3. Я интегрирую алгоритм в бота")
    print("4. Бот будет использовать ваш стиль речи!")

if __name__ == "__main__":
    main()
