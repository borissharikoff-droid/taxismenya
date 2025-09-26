import asyncio
import logging
import random
import os
import requests
import tempfile
from datetime import datetime, timedelta
from telegram import Bot, InputMediaPhoto
from telegram.error import TelegramError
from telegram.request import HTTPXRequest
import schedule
import time
from threading import Thread
from bs4 import BeautifulSoup
from PIL import Image
import io
import httpx
import signal
import sys
from gtts import gTTS
from pydub import AudioSegment
import re

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8437007902:AAFXbYzoWZI7lmg4EvF3DcopKXwbzYQgpkI")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002722697999")  # Ваш канал
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

class WorkBot:
    def __init__(self):
        # Настройка HTTP клиента с увеличенными лимитами для Railway
        request = HTTPXRequest(
            connection_pool_size=50,  # Увеличиваем размер пула
            pool_timeout=60,          # Увеличиваем таймаут пула
            read_timeout=60,          # Увеличиваем таймаут чтения
            write_timeout=60,         # Увеличиваем таймаут записи
            connect_timeout=60,       # Увеличиваем таймаут подключения
            http_version="1.1"        # Используем HTTP/1.1 для стабильности
        )
        self.bot = Bot(token=BOT_TOKEN, request=request)
        self.last_keywords = []
        self.voice_message_count = 0  # Счетчик голосовых сообщений
        
        # Базовые элементы для генерации работ (бесконечная генерация)
        self.work_verbs = [
            "Покрасить", "Помыть", "Убрать", "Покосить", "Посидеть", 
            "Разобрать", "Покормить", "Почистить", "Поклеить", "Повесить",
            "Собрать", "Разложить", "Переставить", "Отремонтировать", "Починить",
            "Настроить", "Проверить", "Просушить", "Прогреть", "Охладить",
            "Загрузить", "Выгрузить", "Перевезти", "Доставить", "Забрать",
            "Принести", "Отнести", "Поднять", "Опустить", "Повернуть",
            "Сдвинуть", "Передвинуть", "Установить", "Снять", "Закрепить",
            "Открепить", "Соединить", "Разъединить", "Включить", "Выключить",
            "Открыть", "Закрыть", "Заблокировать", "Разблокировать", "Защитить"
        ]
        
        self.work_objects = [
            "забор", "дом", "машину", "окна", "полы", "стены", "двери", 
            "крышу", "подвал", "чердак", "балкон", "лестницу", "ворота",
            "калитку", "заборчик", "лавочку", "скамейку", "почтовый ящик",
            "люстру", "зеркала", "мебель", "технику", "инструменты", "одежду",
            "обувь", "посуду", "ковры", "шторы", "жалюзи", "радиаторы",
            "трубы", "краны", "розетки", "выключатели", "лампочки", "провода",
            "кабели", "антенну", "спутниковую тарелку", "кондиционер", "вентилятор",
            "печь", "камин", "духовку", "микроволновку", "холодильник", "стиральную машину",
            "посудомойку", "пылесос", "утюг", "фен", "бритву", "электробритву",
            "телефон", "компьютер", "принтер", "сканер", "роутер", "модем",
            "телевизор", "музыкальный центр", "колонки", "наушники", "камеру",
            "фотоаппарат", "видеокамеру", "проектор", "экран", "доску", "плакаты",
            "картины", "фотографии", "рамки", "вазы", "статуэтки", "сувениры",
            "книги", "журналы", "газеты", "документы", "папки", "файлы",
            "диски", "флешки", "карты памяти", "батарейки", "зарядные устройства",
            "кабели зарядки", "адаптеры", "переходники", "разветвители", "удлинители",
            "фильтры", "картриджи", "тонер", "бумагу", "ручки", "карандаши",
            "маркеры", "фломастеры", "краски", "кисти", "валики", "шпатели",
            "отвертки", "ключи", "молотки", "гвозди", "шурупы", "болты", "гайки",
            "шайбы", "прокладки", "герметик", "клей", "скотч", "изоленту",
            "проволоку", "веревку", "шнур", "цепь", "трос", "канат", "леску",
            "сеть", "ткань", "пленку", "фольгу", "бумагу", "картон", "пенопласт",
            "поролон", "вата", "вата", "синтепон", "пух", "перья", "шерсть",
            "мех", "кожу", "замшу", "велюр", "бархат", "атлас", "шелк",
            "хлопок", "лен", "шерсть", "кашемир", "ангора", "мохер", "альпака",
            "верблюжья шерсть", "як", "лама", "викунья", "гуанако", "сурок",
            "бобр", "норка", "соболь", "куница", "горностай", "ласка", "хорек",
            "енот", "лиса", "волк", "медведь", "тигр", "леопард", "ягуар",
            "пума", "рысь", "каракал", "сервал", "оцелот", "маргай", "онцилла",
            "кот", "кошка", "котенок", "котенок", "котенок", "котенок", "котенок"
        ]
        
        self.work_locations = [
            "в доме", "в квартире", "в офисе", "в магазине", "в кафе", "в ресторане",
            "в школе", "в больнице", "в поликлинике", "в аптеке", "в банке", "в почте",
            "в библиотеке", "в музее", "в театре", "в кинотеатре", "в спортзале",
            "в бассейне", "в сауне", "в бане", "в гараже", "в подвале", "на чердаке",
            "на балконе", "на лоджии", "на террасе", "на веранде", "в саду", "в огороде",
            "в парке", "во дворе", "на улице", "на дороге", "на тротуаре", "на площади",
            "на стадионе", "на арене", "на сцене", "на подиуме", "на трибуне", "на скамейке",
            "на лавочке", "на стуле", "на кресле", "на диване", "на кровати", "на матрасе",
            "на подушке", "на одеяле", "на простыне", "на наволочке", "на пододеяльнике",
            "на покрывале", "на плед", "на ковре", "на паласе", "на линолеуме", "на паркете",
            "на ламинате", "на плитке", "на мраморе", "на граните", "на бетоне", "на асфальте",
            "на земле", "на траве", "на песке", "на камнях", "на гальке", "на щебне",
            "на гравии", "на глине", "на иле", "на грязи", "на снегу", "на льду",
            "на воде", "на реке", "на озере", "на море", "на океане", "на пруду",
            "на болоте", "на лугу", "на поле", "на горе", "на холме", "на склоне",
            "на вершине", "на дне", "на дне", "на дне", "на дне", "на дне"
        ]
        
        self.work_conditions = [
            "от грязи", "от пыли", "от мусора", "от листьев", "от снега", "от льда",
            "от ржавчины", "от накипи", "от жира", "от копоти", "от сажи", "от клея",
            "от краски", "от лака", "от воска", "от масла", "от бензина", "от солярки",
            "от керосина", "от ацетона", "от спирта", "от уксуса", "от соли", "от сахара",
            "от меда", "от варенья", "от джема", "от сиропа", "от соуса", "от кетчупа",
            "от майонеза", "от горчицы", "от хрена", "от перца", "от специй", "от трав",
            "от цветов", "от фруктов", "от овощей", "от ягод", "от грибов", "от орехов",
            "от семечек", "от зерен", "от крупы", "от муки", "от сахара", "от соли",
            "от соды", "от дрожжей", "от закваски", "от кефира", "от йогурта", "от творога",
            "от сыра", "от масла", "от маргарина", "от сала", "от мяса", "от рыбы",
            "от птицы", "от яиц", "от молока", "от сливок", "от сметаны", "от майонеза",
            "от кетчупа", "от соуса", "от подливы", "от бульона", "от супа", "от борща",
            "от щей", "от рассольника", "от солянки", "от ухи", "от харчо", "от лагмана",
            "от плова", "от шашлыка", "от шаурмы", "от бургера", "от пиццы", "от пасты",
            "от риса", "от гречки", "от перловки", "от пшена", "от овсянки", "от манки",
            "от кукурузы", "от гороха", "от фасоли", "от чечевицы", "от нута", "от маша",
            "от сои", "от арахиса", "от миндаля", "от грецких орехов", "от фундука", "от кешью",
            "от фисташек", "от кедровых орехов", "от бразильских орехов", "от макадамии", "от пекана", "от орехов пекан"
        ]
        
        self.prices = [
            "1000₽", "1200₽", "1500₽", "1800₽", "2000₽", 
            "2300₽", "2500₽", "2800₽", "3000₽", "3500₽",
            "4000₽", "4300₽", "4500₽", "5000₽",
            "1.000₽", "1.200₽", "1.500₽", "1.800₽", "2.000₽",
            "2.300₽", "2.500₽", "2.800₽", "3.000₽", "3.500₽",
            "4.000₽", "4.300₽", "4.500₽", "5.000₽"
        ]
        
        self.bonuses = [
            "такси с меня",
            "такси с меня", 
            "такси с меня",
            "такси с меня",
            "такси с меня",
            "такси с меня",
            "такси с меня",
            "такси с меня",
            "обед", 
            "обед борщ", 
            "в подарок бу клей",
            "инвентарь даю",
            "материалы даю",
            "чай с печеньками",
            "кофе с булочкой",
            "обед + чай",
            "материалы + обед",
            "такси + обед",
            "инвентарь + обед",
            "в подарок инструмент",
            "обед + десерт",
            "материалы + такси",
            "чай + печеньки",
            "в подарок набор дюбелей",
            "в подарок перфоратор",
            "в подарок болгарка",
            "в подарок дрель",
            "в подарок набор ключей",
            "в подарок молоток",
            "в подарок отвертки",
            "в подарок плоскогубцы",
            "в подарок ножовку",
            "в подарок лопату",
            "в подарок грабли",
            "в подарок ведро",
            "в подарок тряпки",
            "в подарок швабру"
        ]
        
        # Дополнительные элементы в стиле примеров
        self.extra_info = [
            "за пару часов",
            "на руки",
            "Косилка есть",
            "Места ограничены",
            "так же стоит швецкий стол",
            "инструменты дам",
            "материалы есть",
            "быстро сделать",
            "срочно нужно",
            "инвентарь свой",
            "все даю",
            "быстро и качественно",
            "опыт не важен",
            "главное желание",
            "за день сделаем",
            "инструменты предоставлю",
            "все необходимое есть",
            "работа легкая",
            "деньги сразу",
            "наличными"
        ]
        
        # Дополнительные элементы (как от работяги)
        self.quirky_additions = [
            "P.S. Забор красить аккуратно",
            "P.S. Бабушка ворчит но не злая",
            "P.S. Крыльцо отмыть до блеска",
            "P.S. Дом помыть хорошо",
            "P.S. Снег убирать осторожно",
            "P.S. Машину помыть до блеска",
            "P.S. Траву косить ровно",
            "P.S. Стены красить аккуратно",
            "P.S. Мусор убирать весь",
            "P.S. Окна помыть чисто",
            "P.S. Ворота покрасить хорошо",
            "P.S. Листья убрать все",
            "P.S. Полы помыть до блеска",
            "P.S. Заборчик покрасить ровно",
            "P.S. Снег убирать аккуратно",
            "P.S. Посуду помыть чисто",
            "P.S. Лавочку покрасить хорошо",
            "P.S. Мусор убрать весь",
            "P.S. Двери помыть до блеска",
            "P.S. Калитку покрасить ровно"
        ]

    def generate_work_type(self):
        """Генерирует новый тип работы (бесконечная генерация)"""
        # 30% шанс использовать специальные работы
        if random.random() < 0.3:
            special_works = [
                "Набираем массовку для съемок",
                "Зачистить участок от бурьяна", 
                "Разобрать ступеньки на крыльце",
                "Посидеть с бабушкой",
                "Покормить кота",
                "Помыть велосипед",
                "Убрать паутину с потолка",
                "Покрасить почтовый ящик",
                "Убрать пыль с книг",
                "Помыть люстру",
                "Покрасить лестницу",
                "Убрать мусор из сарая",
                "Помыть пол в гараже",
                "Покрасить трубы",
                "Убрать снег с крыши гаража",
                "Помыть забор",
                "Покрасить дверь в подъезд"
            ]
            return random.choice(special_works)
        
        # 70% шанс сгенерировать новую работу
        verb = random.choice(self.work_verbs)
        obj = random.choice(self.work_objects)
        
        # 40% шанс добавить условие
        if random.random() < 0.4:
            condition = random.choice(self.work_conditions)
            work = f"{verb} {obj} {condition}"
        else:
            work = f"{verb} {obj}"
        
        # 30% шанс добавить локацию
        if random.random() < 0.3:
            location = random.choice(self.work_locations)
            work += f" {location}"
        
        return work

    def generate_message(self):
        """Генерирует сообщение в стиле примеров (бесконечная генерация)"""
        work = self.generate_work_type()
        price = random.choice(self.prices)
        bonus = random.choice(self.bonuses)
        
        # Формируем сообщение в стиле примеров
        message = f"{work}, {price} {bonus}"

        # Сохраняем ключевые слова ДО искажения текста
        self.last_keywords = self.extract_keywords_from_work(work)
        
        # 40% шанс добавить дополнительную информацию
        if random.random() < 0.4:
            extra = random.choice(self.extra_info)
            message += f", {extra}"
        
        # Добавляем безграмотность в основной текст
        message = self.add_typos(message)
        
        # Делаем весь текст с маленькой буквы
        message = self.make_lowercase(message)
        
        return message

    def extract_keywords_from_work(self, work: str):
        """Выделяет ключевые слова-предметы из исходной фразы работы для ассоциативного поиска изображений."""
        try:
            text = work.lower()
            # Удаляем запятые/лишние символы
            for ch in [",", ".", "!", "?", ":", ";"]:
                text = text.replace(ch, " ")
            tokens = [t for t in text.split() if t]
            
            # Стоп-слова
            stop = {
                "в", "во", "на", "над", "под", "из", "от", "до", "за", "по", "для",
                "и", "или", "к", "с", "у", "о", "об", "про", "что", "как",
                "дня", "утра", "вечера", "ночью", "ночь", "днем", "день", "дома",
                "грязи", "пыли", "мусора", "листьев", "снега", "льда", "ржавчины"
            }
            
            # Словарь предметов для ассоциативного поиска
            object_keywords = {
                # Инструменты
                "отвертки": "screwdriver", "отвертка": "screwdriver", "ключей": "wrench", "ключи": "wrench",
                "молоток": "hammer", "молотки": "hammer", "плоскогубцы": "pliers", "ножовку": "saw",
                "ножовка": "saw", "дрель": "drill", "перфоратор": "drill", "болгарка": "grinder",
                "лопату": "shovel", "лопата": "shovel", "грабли": "rake", "ведро": "bucket",
                "швабру": "mop", "швабра": "mop", "тряпки": "rag", "тряпка": "rag",
                
                # Предметы мебели/интерьера
                "скамейку": "bench", "скамейка": "bench", "лавочку": "bench", "лавочка": "bench",
                "стул": "chair", "стулья": "chair", "кресло": "chair", "кресла": "chair",
                "диван": "sofa", "диваны": "sofa", "кровать": "bed", "кровати": "bed",
                "стол": "table", "столы": "table", "шкаф": "wardrobe", "шкафы": "wardrobe",
                
                # Строительные материалы/объекты
                "забор": "fence", "заборчик": "fence", "ворота": "gate", "калитку": "gate",
                "калитка": "gate", "лестницу": "stairs", "лестница": "stairs", "крышу": "roof",
                "крыша": "roof", "стены": "wall", "стена": "wall", "полы": "floor", "пол": "floor",
                "окна": "window", "окно": "window", "двери": "door", "дверь": "door",
                
                # Техника
                "машину": "car", "машина": "car", "велосипед": "bicycle", "веласипед": "bicycle",
                "телевизор": "tv", "компьютер": "computer", "холодильник": "refrigerator",
                "стиральную машину": "washing machine", "посудомойку": "dishwasher",
                
                # Другие предметы
                "посуду": "dishes", "посуда": "dishes", "ковры": "carpet", "ковер": "carpet",
                "шторы": "curtains", "штора": "curtains", "люстру": "chandelier", "люстра": "chandelier",
                "зеркала": "mirror", "зеркало": "mirror", "книги": "books", "книга": "books"
            }
            
            keywords = []
            
            # Ищем предметы в тексте
            for tok in tokens:
                if tok in object_keywords and tok not in keywords:
                    keywords.append(object_keywords[tok])
                    if len(keywords) >= 2:  # Максимум 2 предмета
                        break
            
            # Если не нашли предметы, ищем общие слова
            if not keywords:
                for tok in tokens:
                    if tok not in stop and tok.isalpha() and len(tok) > 3:
                        keywords.append(tok)
                        if len(keywords) >= 2:
                            break
            
            return keywords[:2]  # Возвращаем максимум 2 ключевых слова
            
        except Exception:
            return []
    
    def add_typos(self, text):
        """Добавляет МАКСИМАЛЬНУЮ безграмотность как у очень неграмотного человека"""
        # Словарь замен для МАКСИМАЛЬНОЙ безграмотности
        replacements = {
            "Покрасить": "Пакрасить",
            "Помыть": "Памыйть", 
            "Убрать": "Убрать",
            "Покосить": "Пакосить",
            "Посидеть": "Пасидеть",
            "Разобрать": "Разобрать",
            "Покормить": "Пакормить",
            "такси": "такси",
            "обед": "обед",
            "инвентарь": "инвентарь",
            "материалы": "матёриалы",
            "инструмент": "инструмент",
            "дюбелей": "дюбелёй",
            "перфоратор": "перфаратор",
            "болгарка": "болгарка",
            "дрель": "дрель",
            "ключей": "ключёй",
            "молоток": "молоток",
            "отвертки": "отвёртки",
            "плоскогубцы": "плоскогубцы",
            "ножовку": "ножовку",
            "лопату": "лопату",
            "грабли": "грабли",
            "ведро": "ведро",
            "тряпки": "тряпки",
            "швабру": "швабру",
            "забор": "забор",
            "бабушкой": "бабушкой",
            "крыльцо": "крыльцо",
            "мусора": "мусора",
            "дом": "дом",
            "грязи": "грязи",
            "снег": "снёг",
            "крыши": "крышй",
            "машину": "машину",
            "траву": "траву",
            "стены": "стены",
            "участке": "участке",
            "окна": "окна",
            "ворота": "ворота",
            "листья": "листья",
            "полы": "полы",
            "заборчик": "заборчик",
            "дорожек": "дорожек",
            "посуду": "посуду",
            "лавочку": "лавочку",
            "подвале": "подвале",
            "двери": "двери",
            "калитку": "калитку",
            "кота": "кота",
            "велосипед": "веласипед",
            "скамейку": "скамейку",
            "паутину": "паутину",
            "потолка": "потолка",
            "зеркала": "зеркала",
            "почтовый": "почтовый",
            "ящик": "ящик",
            "пыль": "пыль",
            "книг": "книг",
            "люстру": "люстру",
            "лестницу": "лестницу",
            "сарая": "сарая",
            "гараже": "гараже",
            "трубы": "труби",
            "подъезд": "подъезд"
        }
        
        # Применяем замены с вероятностью 70% (МАКСИМАЛЬНАЯ безграмотность)
        for correct, wrong in replacements.items():
            if random.random() < 0.7:
                text = text.replace(correct, wrong)
        
        # Добавляем МАКСИМАЛЬНО случайные опечатки
        if random.random() < 0.6:
            text = text.replace("и", "й", 1)
        if random.random() < 0.5:
            text = text.replace("е", "ё", 1)
        if random.random() < 0.4:
            text = text.replace("о", "а", 1)
        if random.random() < 0.35:
            text = text.replace("ы", "и", 1)
        if random.random() < 0.3:
            text = text.replace("у", "ю", 1)
        if random.random() < 0.25:
            text = text.replace("а", "о", 1)
        if random.random() < 0.2:
            text = text.replace("ё", "е", 1)
        if random.random() < 0.15:
            text = text.replace("й", "и", 1)
            
        return text

    def make_lowercase(self, text):
        """Делает весь текст с маленькой буквы"""
        return text.lower()

    def convert_to_dagestani_accent(self, text):
        """Конвертирует текст в дагестанский акцент с ломаным русским"""
        # Словарь замен для дагестанского акцента
        dagestani_replacements = {
            # Звуковые замены
            "ч": "ш", "щ": "ш", "ц": "с", "ж": "з", "ш": "с",
            "ы": "и", "э": "е", "ю": "у", "я": "а", "ё": "е",
            "ь": "", "ъ": "",
            # Специфичные замены
            "работа": "работа", "работать": "работать", "работаю": "работаю",
            "деньги": "деньги", "рубли": "рубли", "рублей": "рублей",
            "такси": "такси", "машина": "машина", "дом": "дом",
            "помыть": "помыть", "покрасить": "покрасить", "убрать": "убрать",
            "материалы": "материалы", "инструменты": "инструменты",
            "обед": "обед", "чай": "чай", "кофе": "кофе",
            # Добавляем характерные окончания
            "₽": " рублей",
            ",": ", братан,",
            ".": ", понял?"
        }
        
        # Применяем замены
        result = text.lower()
        for original, replacement in dagestani_replacements.items():
            result = result.replace(original, replacement)
        
        # Добавляем характерные фразы дагестанца
        dagestani_phrases = [
            " братан,", " понял?", " давай,", " быстро,", " качественно,",
            " все даю,", " инструменты есть,", " материалы даю,"
        ]
        
        # Случайно добавляем дагестанские фразы
        if random.random() < 0.3:
            phrase = random.choice(dagestani_phrases)
            result += phrase
        
        # Добавляем характерные звуки
        if random.random() < 0.2:
            result = result.replace("а", "ах", 1)
        if random.random() < 0.15:
            result = result.replace("о", "ох", 1)
            
        return result

    def generate_voice_message(self, text):
        """Генерирует голосовое сообщение с дагестанским акцентом"""
        try:
            # Конвертируем текст в дагестанский акцент
            dagestani_text = self.convert_to_dagestani_accent(text)
            logger.info(f"Текст для озвучки: {dagestani_text}")
            
            # Создаем TTS с русским языком
            tts = gTTS(text=dagestani_text, lang='ru', slow=False)
            
            # Сохраняем во временный файл
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_audio.name)
            temp_audio.close()
            
            # Конвертируем в OGG для Telegram (более компактный)
            audio = AudioSegment.from_mp3(temp_audio.name)
            temp_ogg = tempfile.NamedTemporaryFile(delete=False, suffix='.ogg')
            audio.export(temp_ogg.name, format="ogg")
            temp_ogg.close()
            
            # Удаляем временный MP3 файл
            os.unlink(temp_audio.name)
            
            logger.info(f"Голосовое сообщение создано: {temp_ogg.name}")
            return temp_ogg.name
            
        except Exception as e:
            logger.error(f"Ошибка при создании голосового сообщения: {e}")
            return None

    def search_churka_image(self):
        """Фоллбек: изображения с дагестанцами, таджиками и подобными."""
        try:
            # Готовые URL изображений с нужными людьми
            ethnic_people_urls = [
                # Unsplash - рабочие, строители, мигранты
                "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1519345182560-3f2917c472ef?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1507591064344-4c6ce005b128?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1519345182560-3f2917c472ef?w=400&h=400&fit=crop&crop=face",
                "https://images.unsplash.com/photo-1507591064344-4c6ce005b128?w=400&h=400&fit=crop&crop=face",
                # Picsum с фиксированными ID для стабильности
                "https://picsum.photos/400/400?random=300",
                "https://picsum.photos/400/400?random=301", 
                "https://picsum.photos/400/400?random=302",
                "https://picsum.photos/400/400?random=303",
                "https://picsum.photos/400/400?random=304",
                "https://picsum.photos/400/400?random=305",
                "https://picsum.photos/400/400?random=306",
                "https://picsum.photos/400/400?random=307",
                "https://picsum.photos/400/400?random=308",
                "https://picsum.photos/400/400?random=309",
                "https://picsum.photos/400/400?random=310"
            ]
            
            selected_url = random.choice(ethnic_people_urls)
            logger.info(f"Выбрано изображение (fallback с дагестанцем/таджиком): {selected_url}")
            return selected_url
        except Exception as e:
            logger.error(f"Ошибка при выборе изображения: {e}")
            return None

    def fetch_unsplash_image(self, keywords):
        """Ищет ассоциативные изображения на Unsplash по предметам из текста."""
        try:
            if not UNSPLASH_API_KEY:
                return None
            
            # Если есть ключевые слова-предметы, ищем их
            if keywords:
                for keyword in keywords:
                    try:
                        url = f"https://api.unsplash.com/search/photos"
                        headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
                        params = {
                            "query": keyword,
                            "per_page": 20,
                            "orientation": "all"
                        }
                        resp = requests.get(url, headers=headers, params=params, timeout=10)
                        resp.raise_for_status()
                        data = resp.json()
                        results = data.get("results", [])
                        if results:
                            result = random.choice(results)
                            image_url = result.get("urls", {}).get("regular")
                            if image_url:
                                logger.info(f"Найдено ассоциативное изображение '{keyword}' на Unsplash: {image_url}")
                                return image_url
                    except Exception as e:
                        logger.warning(f"Ошибка поиска '{keyword}' на Unsplash: {e}")
                        continue
            
            # Фоллбек: поиск рабочих/строителей
            fallback_queries = [
                "construction worker", "migrant worker", "laborer", "manual worker", "dirty worker",
                "construction man", "worker face", "laborer face", "manual labor", "dirty man"
            ]
            
            for query in fallback_queries:
                try:
                    url = f"https://api.unsplash.com/search/photos"
                    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
                    params = {
                        "query": query,
                        "per_page": 20,
                        "orientation": "portrait"
                    }
                    resp = requests.get(url, headers=headers, params=params, timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                    results = data.get("results", [])
                    if results:
                        result = random.choice(results)
                        image_url = result.get("urls", {}).get("regular")
                        if image_url:
                            logger.info(f"Найдено изображение рабочего по запросу '{query}': {image_url}")
                            return image_url
                except Exception as e:
                    logger.warning(f"Ошибка поиска по запросу '{query}': {e}")
                    continue
            
            logger.warning("Не найдено подходящих изображений на Unsplash")
            return None
            
        except Exception as e:
            logger.warning(f"Unsplash недоступен или вернул ошибку: {e}")
            return None

    def fetch_pexels_image(self, keywords):
        """Ищет ассоциативные изображения на Pexels по предметам из текста."""
        try:
            if not PEXELS_API_KEY:
                return None
            
            # Если есть ключевые слова-предметы, ищем их
            if keywords:
                for keyword in keywords:
                    try:
                        url = f"https://api.pexels.com/v1/search"
                        headers = {"Authorization": PEXELS_API_KEY}
                        params = {
                            "query": keyword,
                            "per_page": 20,
                            "orientation": "all"
                        }
                        resp = requests.get(url, headers=headers, params=params, timeout=10)
                        resp.raise_for_status()
                        data = resp.json()
                        photos = data.get("photos", [])
                        if photos:
                            photo = random.choice(photos)
                            image_url = photo.get("src", {}).get("medium")
                            if image_url:
                                logger.info(f"Найдено ассоциативное изображение '{keyword}' на Pexels: {image_url}")
                                return image_url
                    except Exception as e:
                        logger.warning(f"Ошибка поиска '{keyword}' на Pexels: {e}")
                        continue
            
            # Фоллбек: поиск рабочих/строителей
            fallback_queries = [
                "construction worker", "migrant worker", "laborer", "manual worker", "dirty worker",
                "construction man", "worker face", "laborer face", "manual labor", "dirty man"
            ]
            
            for query in fallback_queries:
                try:
                    url = f"https://api.pexels.com/v1/search"
                    headers = {"Authorization": PEXELS_API_KEY}
                    params = {
                        "query": query,
                        "per_page": 20,
                        "orientation": "portrait"
                    }
                    resp = requests.get(url, headers=headers, params=params, timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                    photos = data.get("photos", [])
                    if photos:
                        photo = random.choice(photos)
                        image_url = photo.get("src", {}).get("medium")
                        if image_url:
                            logger.info(f"Найдено изображение рабочего по запросу '{query}': {image_url}")
                            return image_url
                except Exception as e:
                    logger.warning(f"Ошибка поиска по запросу '{query}': {e}")
                    continue
            
            logger.warning("Не найдено подходящих изображений на Pexels")
            return None
            
        except Exception as e:
            logger.warning(f"Pexels недоступен или вернул ошибку: {e}")
            return None

    def fetch_pixabay_image(self, keywords):
        """Ищет ассоциативные изображения на Pixabay по предметам из текста."""
        try:
            if not PIXABAY_API_KEY:
                return None
            
            # Если есть ключевые слова-предметы, ищем их
            if keywords:
                for keyword in keywords:
                    try:
                        # Заменяем пробелы на + для Pixabay
                        query = keyword.replace(" ", "+")
                        url = (
                            f"https://pixabay.com/api/?key={PIXABAY_API_KEY}"
                            f"&q={query}&image_type=photo&lang=en&safesearch=true&per_page=20&orientation=all"
                        )
                        resp = requests.get(url, timeout=10)
                        resp.raise_for_status()
                        data = resp.json()
                        hits = data.get("hits", [])
                        if hits:
                            hit = random.choice(hits)
                            image_url = hit.get("webformatURL") or hit.get("largeImageURL")
                            if image_url:
                                logger.info(f"Найдено ассоциативное изображение '{keyword}' на Pixabay: {image_url}")
                                return image_url
                    except Exception as e:
                        logger.warning(f"Ошибка поиска '{keyword}' на Pixabay: {e}")
                        continue
            
            # Фоллбек: поиск рабочих/строителей
            fallback_queries = [
                "dirty+worker", "construction+worker", "migrant+worker", "laborer", "manual+worker",
                "dirty+man", "construction+man", "worker+face", "laborer+face", "manual+labor"
            ]
            
            for query in fallback_queries:
                try:
                    url = (
                        f"https://pixabay.com/api/?key={PIXABAY_API_KEY}"
                        f"&q={query}&image_type=photo&lang=en&safesearch=true&per_page=20&orientation=horizontal"
                    )
                    resp = requests.get(url, timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                    hits = data.get("hits", [])
                    if hits:
                        hit = random.choice(hits)
                        image_url = hit.get("webformatURL") or hit.get("largeImageURL")
                        if image_url:
                            logger.info(f"Найдено изображение рабочего по запросу '{query}': {image_url}")
                            return image_url
                except Exception as e:
                    logger.warning(f"Ошибка поиска по запросу '{query}': {e}")
                    continue
            
            logger.warning("Не найдено подходящих изображений на Pixabay")
            return None
            
        except Exception as e:
            logger.warning(f"Pixabay недоступен или вернул ошибку: {e}")
            return None

    def get_image_for_message(self):
        """Возвращает URL ассоциативного изображения по предметам из текста."""
        # Пробуем разные источники по очереди для поиска ассоциативных изображений
        
        # 1. Unsplash (лучший источник для ассоциативных изображений)
        url = self.fetch_unsplash_image(self.last_keywords)
        if url:
            logger.info(f"Найдено ассоциативное изображение на Unsplash по ключевым словам {self.last_keywords}: {url}")
            return url
        
        # 2. Pexels (хороший источник)
        url = self.fetch_pexels_image(self.last_keywords)
        if url:
            logger.info(f"Найдено ассоциативное изображение на Pexels по ключевым словам {self.last_keywords}: {url}")
            return url
        
        # 3. Pixabay (резерв)
        url = self.fetch_pixabay_image(self.last_keywords)
        if url:
            logger.info(f"Найдено ассоциативное изображение на Pixabay по ключевым словам {self.last_keywords}: {url}")
            return url
        
        # 4. Фоллбек: всегда изображения с дагестанцами/таджиками
        fallback_url = self.search_churka_image()
        if fallback_url:
            logger.info(f"Используется fallback изображение с дагестанцем/таджиком: {fallback_url}")
            return fallback_url
        
        # 5. Последний резерв - случайное изображение
        logger.warning("Используется последний резерв - случайное изображение")
        return "https://picsum.photos/400/400?random=999"

    def download_image(self, image_url):
        """Скачивает изображение по URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(image_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Проверяем размер файла (не больше 5MB)
            if len(response.content) > 5 * 1024 * 1024:
                logger.warning("Изображение слишком большое, пропускаем")
                return None
            
            # Создаем временный файл
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(response.content)
            temp_file.close()
            
            logger.info(f"Изображение скачано: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Ошибка при скачивании изображения: {e}")
            return None

    async def send_message_to_channel(self):
        """Отправляет только текстовое сообщение в канал с улучшенными повторными попытками"""
        message = self.generate_message()
        max_retries = 5  # Увеличиваем количество попыток
        
        for attempt in range(max_retries):
            try:
                # Отправляем только текст с таймаутом
                await asyncio.wait_for(
                    self.bot.send_message(chat_id=CHANNEL_ID, text=message),
                    timeout=30  # 30 секунд таймаут на отправку
                )
                logger.info(f"✅ Текстовое сообщение отправлено: {message}")
                return
                    
            except asyncio.TimeoutError:
                logger.error(f"⏰ Таймаут отправки (попытка {attempt + 1})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(min(2 ** attempt, 30))  # Максимум 30 секунд задержки
                continue
            except Exception as e:
                error_msg = str(e)
                logger.error(f"❌ Ошибка отправки (попытка {attempt + 1}): {error_msg}")
                
                # Специальная обработка для ошибок пула соединений
                if "Pool timeout" in error_msg or "connection pool" in error_msg.lower():
                    logger.warning("🔄 Обнаружена ошибка пула соединений, увеличиваем задержку")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(min(5 * (2 ** attempt), 60))  # Больше времени для восстановления пула
                    continue
                
                # Специальная обработка для ошибок event loop
                if "Event loop is closed" in error_msg:
                    logger.warning("🔄 Обнаружена ошибка закрытого event loop")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(10)  # Даем время на восстановление
                    continue
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(min(2 ** attempt, 30))  # Экспоненциальная задержка с ограничением
                else:
                    logger.error(f"💀 Не удалось отправить сообщение после {max_retries} попыток: {message}")
                    # Последняя попытка с новым bot instance
                    try:
                        # Создаем новый bot instance для последней попытки
                        new_request = HTTPXRequest(
                            connection_pool_size=10,
                            pool_timeout=30,
                            read_timeout=30,
                            write_timeout=30,
                            connect_timeout=30
                        )
                        emergency_bot = Bot(token=BOT_TOKEN, request=new_request)
                        await asyncio.wait_for(
                            emergency_bot.send_message(chat_id=CHANNEL_ID, text=message),
                            timeout=60
                        )
                        logger.info(f"🆘 Резервное сообщение отправлено: {message}")
                    except Exception as final_e:
                        logger.error(f"💀 Финальная ошибка: {final_e}")

    async def send_voice_message_to_channel(self):
        """Отправляет голосовое сообщение в канал с дагестанским акцентом"""
        message = self.generate_message()
        max_retries = 3
        
        # Генерируем голосовое сообщение
        voice_file = self.generate_voice_message(message)
        if not voice_file:
            logger.error("Не удалось создать голосовое сообщение, отправляем текст")
            await self.send_message_to_channel()
            return
        
        for attempt in range(max_retries):
            try:
                # Отправляем голосовое сообщение
                with open(voice_file, 'rb') as voice:
                    await asyncio.wait_for(
                        self.bot.send_voice(
                            chat_id=CHANNEL_ID, 
                            voice=voice,
                            caption=f"🎤 {message}"  # Добавляем текст как подпись
                        ),
                        timeout=60  # Больше времени для голосовых сообщений
                    )
                logger.info(f"🎤 Голосовое сообщение отправлено: {message}")
                
                # Удаляем временный файл
                try:
                    os.unlink(voice_file)
                except:
                    pass
                return
                    
            except asyncio.TimeoutError:
                logger.error(f"⏰ Таймаут отправки голосового сообщения (попытка {attempt + 1})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(min(2 ** attempt, 30))
                continue
            except Exception as e:
                error_msg = str(e)
                logger.error(f"❌ Ошибка отправки голосового сообщения (попытка {attempt + 1}): {error_msg}")
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(min(2 ** attempt, 30))
                else:
                    logger.error(f"💀 Не удалось отправить голосовое сообщение, отправляем текст: {message}")
                    # Фоллбек на текстовое сообщение
                    try:
                        os.unlink(voice_file)
                    except:
                        pass
                    await self.send_message_to_channel()
                    return

    def send_message_sync(self):
        """Синхронная обертка для отправки сообщения с улучшенным управлением event loop"""
        try:
            # Проверяем, есть ли уже активный event loop
            try:
                loop = asyncio.get_running_loop()
                # Если есть активный loop, создаем задачу
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_in_new_loop)
                    future.result(timeout=120)  # 2 минуты таймаут
            except RuntimeError:
                # Нет активного loop, создаем новый
                self._run_in_new_loop()
        except Exception as e:
            logger.error(f"❌ Ошибка в send_message_sync: {e}")
            # Последняя попытка с простым asyncio.run
            try:
                asyncio.run(self.send_message_to_channel())
            except Exception as e2:
                logger.error(f"❌ Критическая ошибка в send_message_sync: {e2}")
    
    def _run_in_new_loop(self):
        """Запускает отправку сообщения в новом event loop"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.send_message_to_channel())
        finally:
            # Правильно закрываем loop
            try:
                # Отменяем все pending задачи
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception:
                pass
            finally:
                loop.close()

    def send_voice_message_sync(self):
        """Синхронная обертка для отправки голосового сообщения"""
        try:
            # Проверяем, есть ли уже активный event loop
            try:
                loop = asyncio.get_running_loop()
                # Если есть активный loop, создаем задачу
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_voice_in_new_loop)
                    future.result(timeout=180)  # 3 минуты таймаут для голосовых
            except RuntimeError:
                # Нет активного loop, создаем новый
                self._run_voice_in_new_loop()
        except Exception as e:
            logger.error(f"❌ Ошибка в send_voice_message_sync: {e}")
            # Последняя попытка с простым asyncio.run
            try:
                asyncio.run(self.send_voice_message_to_channel())
            except Exception as e2:
                logger.error(f"❌ Критическая ошибка в send_voice_message_sync: {e2}")
    
    def _run_voice_in_new_loop(self):
        """Запускает отправку голосового сообщения в новом event loop"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.send_voice_message_to_channel())
        finally:
            # Правильно закрываем loop
            try:
                # Отменяем все pending задачи
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception:
                pass
            finally:
                loop.close()

    def schedule_messages(self):
        """Планирует отправку сообщений 10 раз в день (2 голосовых, 8 текстовых)"""
        # 7:00 утра - ГОЛОСОВОЕ СООБЩЕНИЕ
        schedule.every().day.at("07:00").do(self.send_voice_message_sync)
        # 9:00 утра - текстовое
        schedule.every().day.at("09:00").do(self.send_message_sync)
        # 11:00 утра - текстовое
        schedule.every().day.at("11:00").do(self.send_message_sync)
        # 13:00 дня - текстовое
        schedule.every().day.at("13:00").do(self.send_message_sync)
        # 15:00 дня - текстовое
        schedule.every().day.at("15:00").do(self.send_message_sync)
        # 17:00 дня - ГОЛОСОВОЕ СООБЩЕНИЕ
        schedule.every().day.at("17:00").do(self.send_voice_message_sync)
        # 19:00 вечера - текстовое
        schedule.every().day.at("19:00").do(self.send_message_sync)
        # 21:00 вечера - текстовое
        schedule.every().day.at("21:00").do(self.send_message_sync)
        # 23:00 вечера - текстовое
        schedule.every().day.at("23:00").do(self.send_message_sync)
        # 1:00 ночи - текстовое
        schedule.every().day.at("01:00").do(self.send_message_sync)
        
        logger.info("Расписание сообщений настроено: 07:00 (🎤), 09:00, 11:00, 13:00, 15:00, 17:00 (🎤), 19:00, 21:00, 23:00, 01:00")

    def run_scheduler(self):
        """Запускает планировщик в отдельном потоке с улучшенной обработкой ошибок"""
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Проверяем каждую минуту
            except Exception as e:
                logger.error(f"❌ Ошибка в планировщике: {e}")
                time.sleep(60)  # Продолжаем работу даже при ошибке

    async def start_bot(self):
        """Запускает бота"""
        try:
            # Проверяем подключение
            me = await self.bot.get_me()
            logger.info(f"Бот запущен: @{me.username}")
            
            # Настраиваем расписание
            self.schedule_messages()
            
            # Запускаем планировщик в отдельном потоке
            scheduler_thread = Thread(target=self.run_scheduler, daemon=True)
            scheduler_thread.start()
            
            logger.info("Бот готов к работе! Сообщения будут отправляться в 07:00, 09:00, 11:00, 13:00, 15:00, 17:00, 19:00, 21:00, 23:00, 01:00")
            
            # Отправляем несколько тестовых сообщений для проверки
            logger.info("🚀 Отправляем тестовые сообщения...")
            
            try:
                await self.send_message_to_channel()
                logger.info("✅ Тестовое текстовое сообщение 1 отправлено")
            except Exception as e:
                logger.error(f"❌ Ошибка тестового сообщения 1: {e}")
            
            await asyncio.sleep(5)
            
            try:
                await self.send_voice_message_to_channel()
                logger.info("🎤 Тестовое голосовое сообщение отправлено")
            except Exception as e:
                logger.error(f"❌ Ошибка тестового голосового сообщения: {e}")
            
            await asyncio.sleep(5)
            
            try:
                await self.send_message_to_channel()
                logger.info("✅ Тестовое текстовое сообщение 2 отправлено")
            except Exception as e:
                logger.error(f"❌ Ошибка тестового сообщения 2: {e}")
            
            # Держим бота активным
            while True:
                await asyncio.sleep(3600)  # Спим час
                
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            raise

def signal_handler(signum, frame):
    """Обработчик сигналов для graceful shutdown"""
    logger.info(f"Получен сигнал {signum}, завершаем работу...")
    sys.exit(0)

def main():
    """Главная функция с улучшенной обработкой ошибок для Railway"""
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    bot = WorkBot()
    
    try:
        # Настраиваем event loop для Railway
        if os.getenv("RAILWAY_ENVIRONMENT"):
            # В Railway используем более консервативные настройки
            asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
        
        asyncio.run(bot.start_bot())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        # В Railway перезапускаемся при критических ошибках
        if os.getenv("RAILWAY_ENVIRONMENT"):
            logger.info("Перезапуск через 30 секунд...")
            time.sleep(30)
            main()  # Рекурсивный перезапуск

if __name__ == "__main__":
    main()
