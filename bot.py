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

class WorkBot:
    def __init__(self):
        # Настройка HTTP клиента с увеличенными лимитами
        request = HTTPXRequest(
            connection_pool_size=20,
            pool_timeout=30,
            read_timeout=30,
            write_timeout=30,
            connect_timeout=30
        )
        self.bot = Bot(token=BOT_TOKEN, request=request)
        self.last_keywords = []
        
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
        """Выделяет 1-3 ключевых слова из исходной фразы работы (без опечаток)."""
        try:
            text = work.lower()
            # Удаляем запятые/лишние символы
            for ch in [",", ".", "!", "?", ":", ";"]:
                text = text.replace(ch, " ")
            tokens = [t for t in text.split() if t]
            # Стоп-слова (минимум, чтобы не тащить лишние)
            stop = {
                "в", "во", "на", "над", "под", "из", "от", "до", "за", "по", "для",
                "и", "или", "к", "с", "у", "о", "об", "про", "что", "как",
                "дня", "утра", "вечера", "ночью", "ночь", "днем", "день", "дома"
            }
            # Пробуем отобрать содержательные слова: сперва объект/существительные из известного списка
            known_objects = set(w.lower() for w in self.work_objects)
            keywords = []
            # Берем первое совпадение из объектов
            for tok in tokens:
                if tok in known_objects and tok not in keywords:
                    keywords.append(tok)
                    break
            # Добавим еще одно слово (условие/глагол), если есть
            for tok in tokens:
                if tok not in stop and tok not in keywords and tok.isalpha():
                    keywords.append(tok)
                    if len(keywords) >= 3:
                        break
            if not keywords:
                # Фоллбек: любые 1-2 значимых токена
                for tok in tokens:
                    if tok not in stop and tok.isalpha():
                        keywords.append(tok)
                        if len(keywords) >= 2:
                            break
            return keywords[:3]
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

    def search_churka_image(self):
        """Фоллбек: изображения с таджиками/узбеками из готовых URL."""
        try:
            # Готовые URL изображений с таджиками/узбеками/хачами
            central_asian_image_urls = [
                # Unsplash - бесплатные изображения
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
                "https://picsum.photos/400/400?random=100",
                "https://picsum.photos/400/400?random=101", 
                "https://picsum.photos/400/400?random=102",
                "https://picsum.photos/400/400?random=103",
                "https://picsum.photos/400/400?random=104",
                "https://picsum.photos/400/400?random=105",
                "https://picsum.photos/400/400?random=106",
                "https://picsum.photos/400/400?random=107",
                "https://picsum.photos/400/400?random=108",
                "https://picsum.photos/400/400?random=109",
                "https://picsum.photos/400/400?random=110"
            ]
            
            selected_url = random.choice(central_asian_image_urls)
            logger.info(f"Выбрано изображение (fallback с таджиком/узбеком): {selected_url}")
            return selected_url
        except Exception as e:
            logger.error(f"Ошибка при выборе изображения: {e}")
            return None

    def fetch_pixabay_image(self, keywords):
        """Ищет фото с таджиками/узбеками/хачами на Pixabay."""
        try:
            if not PIXABAY_API_KEY:
                return None
            
            # Специальные запросы для поиска изображений с таджиками/узбеками/хачами
            central_asian_queries = [
                "tajik+worker", "uzbek+worker", "central+asian+man", "tajik+man", "uzbek+man",
                "migrant+worker", "construction+worker", "laborer", "tajik+construction", 
                "uzbek+construction", "central+asian+construction", "tajik+labor", "uzbek+labor",
                "migrant+labor", "tajik+worker+construction", "uzbek+worker+construction",
                "central+asian+worker", "tajik+man+work", "uzbek+man+work", "migrant+man",
                "tajik+person", "uzbek+person", "central+asian+person", "tajik+people",
                "uzbek+people", "central+asian+people", "tajik+team", "uzbek+team"
            ]
            
            # Пробуем разные запросы
            for query in central_asian_queries:
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
                            logger.info(f"Найдено изображение с таджиком/узбеком по запросу '{query}': {image_url}")
                            return image_url
                except Exception as e:
                    logger.warning(f"Ошибка поиска по запросу '{query}': {e}")
                    continue
            
            logger.warning("Не найдено подходящих изображений с таджиками/узбеками")
            return None
            
        except Exception as e:
            logger.warning(f"Pixabay недоступен или вернул ошибку: {e}")
            return None

    def get_image_for_message(self):
        """Возвращает URL изображения с таджиками/узбеками/хачами."""
        # Сначала пробуем Pixabay для поиска релевантных изображений с таджиками/узбеками
        url = self.fetch_pixabay_image(self.last_keywords)
        if url:
            logger.info(f"Найдено релевантное изображение с таджиком/узбеком по ключевым словам {self.last_keywords}: {url}")
            return url
        
        # Фоллбек: всегда изображения с таджиками/узбеками
        fallback_url = self.search_churka_image()
        if fallback_url:
            logger.info(f"Используется fallback изображение с таджиком/узбеком: {fallback_url}")
            return fallback_url
        
        # Последний резерв - случайное изображение
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
        """Отправляет сообщение с изображением в канал с повторными попытками"""
        message = self.generate_message()
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Получаем URL изображения: ассоциативный выбор с fallback
                image_url = self.get_image_for_message()
                
                # Пытаемся отправить с изображением
                try:
                    await self.bot.send_photo(
                        chat_id=CHANNEL_ID,
                        photo=image_url,
                        caption=message
                    )
                    logger.info(f"✅ Сообщение с изображением отправлено: {message}")
                    return
                    
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка при отправке фото (попытка {attempt + 1}): {e}")
                    # Если не получилось с фото, отправляем только текст
                    await self.bot.send_message(chat_id=CHANNEL_ID, text=message)
                    logger.info(f"📝 Сообщение без изображения отправлено: {message}")
                    return
                    
            except Exception as e:
                logger.error(f"❌ Ошибка отправки (попытка {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Экспоненциальная задержка
                else:
                    logger.error(f"💀 Не удалось отправить сообщение после {max_retries} попыток: {message}")
                    # Последняя попытка - только текст
                    try:
                        await self.bot.send_message(chat_id=CHANNEL_ID, text=message)
                        logger.info(f"🆘 Резервное сообщение отправлено: {message}")
                    except Exception as final_e:
                        logger.error(f"💀 Финальная ошибка: {final_e}")

    def send_message_sync(self):
        """Синхронная обертка для отправки сообщения"""
        try:
            # Создаем новый event loop для каждого вызова
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.send_message_to_channel())
            finally:
                loop.close()
        except Exception as e:
            logger.error(f"❌ Ошибка в send_message_sync: {e}")
            # Попытка с новым loop
            try:
                asyncio.run(self.send_message_to_channel())
            except Exception as e2:
                logger.error(f"❌ Критическая ошибка в send_message_sync: {e2}")

    def schedule_messages(self):
        """Планирует отправку сообщений 10 раз в день"""
        # 7:00 утра
        schedule.every().day.at("07:00").do(self.send_message_sync)
        # 9:00 утра
        schedule.every().day.at("09:00").do(self.send_message_sync)
        # 11:00 утра
        schedule.every().day.at("11:00").do(self.send_message_sync)
        # 13:00 дня
        schedule.every().day.at("13:00").do(self.send_message_sync)
        # 15:00 дня
        schedule.every().day.at("15:00").do(self.send_message_sync)
        # 17:00 дня
        schedule.every().day.at("17:00").do(self.send_message_sync)
        # 19:00 вечера
        schedule.every().day.at("19:00").do(self.send_message_sync)
        # 21:00 вечера
        schedule.every().day.at("21:00").do(self.send_message_sync)
        # 23:00 вечера
        schedule.every().day.at("23:00").do(self.send_message_sync)
        # 1:00 ночи
        schedule.every().day.at("01:00").do(self.send_message_sync)
        
        logger.info("Расписание сообщений настроено: 07:00, 09:00, 11:00, 13:00, 15:00, 17:00, 19:00, 21:00, 23:00, 01:00")

    def run_scheduler(self):
        """Запускает планировщик в отдельном потоке"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту

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
                logger.info("✅ Тестовое сообщение 1 отправлено")
            except Exception as e:
                logger.error(f"❌ Ошибка тестового сообщения 1: {e}")
            
            await asyncio.sleep(5)
            
            try:
                await self.send_message_to_channel()
                logger.info("✅ Тестовое сообщение 2 отправлено")
            except Exception as e:
                logger.error(f"❌ Ошибка тестового сообщения 2: {e}")
            
            await asyncio.sleep(5)
            
            try:
                await self.send_message_to_channel()
                logger.info("✅ Тестовое сообщение 3 отправлено")
            except Exception as e:
                logger.error(f"❌ Ошибка тестового сообщения 3: {e}")
            
            # Держим бота активным
            while True:
                await asyncio.sleep(3600)  # Спим час
                
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            raise

def main():
    """Главная функция"""
    bot = WorkBot()
    
    try:
        asyncio.run(bot.start_bot())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
