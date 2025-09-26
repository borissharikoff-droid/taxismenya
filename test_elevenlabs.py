#!/usr/bin/env python3
"""
Тест интеграции ElevenLabs для голосовых сообщений
"""

import os
import tempfile
from elevenlabs.client import ElevenLabs

def test_elevenlabs_connection():
    """Тестирует подключение к ElevenLabs"""
    
    print("🎤 ТЕСТ ПОДКЛЮЧЕНИЯ К ELEVENLABS")
    print("=" * 40)
    
    # Получаем API ключ
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")
    
    if not api_key:
        print("❌ ELEVENLABS_API_KEY не найден в переменных окружения")
        print("💡 Добавьте ваш API ключ в переменные окружения")
        return False
    
    if not voice_id:
        print("❌ ELEVENLABS_VOICE_ID не найден в переменных окружения")
        print("💡 Добавьте ID вашего клонированного голоса")
        return False
    
    try:
        # Инициализируем клиент
        client = ElevenLabs(api_key=api_key)
        print("✅ ElevenLabs клиент инициализирован")
        
        # Тестируем генерацию голоса
        test_text = "Привет, это тест моего голоса через ElevenLabs"
        print(f"📝 Тестовый текст: {test_text}")
        
        # Генерируем аудио
        audio = client.text_to_speech.convert(
            text=test_text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        # Сохраняем тестовый файл
        test_file = "elevenlabs_test.mp3"
        with open(test_file, "wb") as f:
            f.write(audio)
        
        print(f"✅ Тестовый голос создан: {test_file}")
        print("🎧 Откройте файл для прослушивания!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании ElevenLabs: {e}")
        return False

def list_available_voices():
    """Показывает доступные голоса"""
    
    print("\n🎭 ДОСТУПНЫЕ ГОЛОСА")
    print("=" * 25)
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ API ключ не найден")
        return
    
    try:
        client = ElevenLabs(api_key=api_key)
        
        # Получаем список голосов
        response = client.voices.search()
        
        print(f"📊 Найдено голосов: {len(response.voices)}")
        print()
        
        for i, voice in enumerate(response.voices[:10], 1):  # Показываем первые 10
            print(f"{i}. {voice.name}")
            print(f"   ID: {voice.voice_id}")
            print(f"   Категория: {voice.category}")
            if hasattr(voice, 'description') and voice.description:
                print(f"   Описание: {voice.description}")
            print()
        
        if len(response.voices) > 10:
            print(f"... и еще {len(response.voices) - 10} голосов")
            
    except Exception as e:
        print(f"❌ Ошибка при получении списка голосов: {e}")

def main():
    """Главная функция тестирования"""
    
    print("🎤 ТЕСТИРОВАНИЕ ELEVENLABS ИНТЕГРАЦИИ")
    print("=" * 45)
    print()
    
    # Тестируем подключение
    success = test_elevenlabs_connection()
    
    if success:
        # Показываем доступные голоса
        list_available_voices()
        
        print("\n🎯 СЛЕДУЮЩИЕ ШАГИ:")
        print("1. Прослушайте созданный тестовый файл")
        print("2. Если голос подходит - настройте переменные окружения в Railway")
        print("3. Бот будет использовать ваш клонированный голос!")
    else:
        print("\n🔧 НАСТРОЙКА:")
        print("1. Получите API ключ на elevenlabs.io")
        print("2. Создайте клон вашего голоса")
        print("3. Добавьте переменные окружения:")
        print("   - ELEVENLABS_API_KEY=ваш_ключ")
        print("   - ELEVENLABS_VOICE_ID=id_вашего_голоса")

if __name__ == "__main__":
    main()
