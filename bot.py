from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import random
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
WORKS_FOLDER = "works"

# Переводы
LANGUAGES = {
    "ru": {
        "start": "Привет! Я — little.helper 👋 я помогу тебе узнать подробности моего хозяена\nВыбери, что хочешь узнать:",
        "about": """👋 Привет! Я Артём — увлечённый 3D-художник, дизайнер и разработчик.
🔧 Создаю крутых ботов на Python, JavaScript, Discord.js и через Telegram API.
🎨 Работаю в Blender, проектируя стильные 3D-модели и анимации.
💻 Владею After Effects, Photoshop, Illustrator, Premiere Pro и другими инструментами из Creative Cloud — от монтажа до motion-дизайна.
🧠 Постоянно учусь новому, совмещая код с креативом и превращая идеи в живые проекты.""",
        "contacts": "Discord: arty4509",
        "choose_category": "Выбери категорию работ:",
        "no_works": "Пока нет добавленных работ 😢",
        "back_to_main": "Главное меню:",
        "unknown_command": "Не понимаю 🧐",
        "more_works": "Просто нажми нужную категорию, чтобы увидеть больше 😉",
        "choose_language": "Выберите язык:",
        "about_btn": "👤 О моём хозяине",
        "works_btn": "🎨 Мои работы",
        "contacts_btn": "📬 Контакты",
        "lang_btn": "🌐 Выбрать язык",
        "back_btn": "🔙 Назад",
        "category_buttons": ["🧊 3D", "🎨 Дизайн", "🎥 After Effects"]
    },
    "en": {
        "start": "Hi! I'm little.helper 👋 I’ll help you learn more about my creator.\nChoose what you want to know:",
        "about": """👋 Hi! I'm Artem — a passionate 3D artist, designer, and developer.
🔧 I create powerful bots using Python, JavaScript, Discord.js, and the Telegram API.
🎨 I work in Blender, crafting stylish 3D models and animations.
💻 Skilled in After Effects, Photoshop, Illustrator, Premiere Pro, and other Creative Cloud tools — from editing to motion design.
🧠 Always learning, I combine code with creativity to bring ideas to life.""",
        "contacts": "Discord: arty4509",
        "choose_category": "Choose a category of works:",
        "no_works": "No works added yet 😢",
        "back_to_main": "Main menu:",
        "unknown_command": "I don't understand 🧐",
        "more_works": "Just click the category again to see more 😉",
        "choose_language": "Choose a language:",
        "about_btn": "👤 About my master",
        "works_btn": "🎨 My works",
        "contacts_btn": "📬 Contacts",
        "lang_btn": "🌐 Choose language",
        "back_btn": "🔙 Back",
        "category_buttons": ["🧊 3D", "🎨 Design", "🎥 After Effects"]
    },
    "pl": {
        "start": "Cześć! Jestem little.helper 👋 pomogę ci poznać mojego właściciela\nWybierz, co chcesz wiedzieć:",
        "about": """👋 Cześć! Jestem Artem — pasjonat 3D, projektant i programista.
🔧 Tworzę boty w Pythonie, JavaScript, Discord.js oraz przez Telegram API.
🎨 Pracuję w Blenderze, tworząc stylowe modele 3D i animacje.
💻 Znam After Effects, Photoshop, Illustrator, Premiere Pro i inne narzędzia Creative Cloud — od montażu po motion design.
🧠 Ciągle się uczę, łączę kod z kreatywnością i zamieniam pomysły w żywe projekty.""",
        "contacts": "Discord: arty4509",
        "choose_category": "Wybierz kategorię prac:",
        "no_works": "Brak dodanych prac 😢",
        "back_to_main": "Główne menu:",
        "unknown_command": "Nie rozumiem 🧐",
        "more_works": "Po prostu kliknij kategorię ponownie, aby zobaczyć więcej 😉",
        "choose_language": "Wybierz język:",
        "about_btn": "👤 O moim mistrzu",
        "works_btn": "🎨 Moje prace",
        "contacts_btn": "📬 Kontakty",
        "lang_btn": "🌐 Wybierz język",
        "back_btn": "🔙 Wstecz",
        "category_buttons": ["🧊 3D", "🎨 Design", "🎥 After Effects"]
    }
}

def get_main_menu(lang):
    t = LANGUAGES[lang]
    return ReplyKeyboardMarkup([
        [KeyboardButton(t["about_btn"])],
        [KeyboardButton(t["works_btn"])],
        [KeyboardButton(t["contacts_btn"])],
        [KeyboardButton(t["lang_btn"])]
    ], resize_keyboard=True)

def get_works_menu(lang):
    t = LANGUAGES[lang]
    return ReplyKeyboardMarkup([
        [KeyboardButton(t["category_buttons"][0]), KeyboardButton(t["category_buttons"][1])],
        [KeyboardButton(t["category_buttons"][2]), KeyboardButton("💾 Code")],
        [KeyboardButton(t["back_btn"])]
    ], resize_keyboard=True)

language_menu = ReplyKeyboardMarkup(
    [[KeyboardButton("🇷🇺 Русский")], [KeyboardButton("🇬🇧 English")], [KeyboardButton("🇵🇱 Polski")]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "ru")
    await update.message.reply_text(LANGUAGES[lang]["start"], reply_markup=get_main_menu(lang))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    lang = context.user_data.get("lang", "ru")
    t = LANGUAGES[lang]

    if msg == t["about_btn"]:
        await update.message.reply_text(t["about"])
    elif msg == t["contacts_btn"]:
        await update.message.reply_text(t["contacts"])
    elif msg == t["works_btn"]:
        await update.message.reply_text(t["choose_category"], reply_markup=get_works_menu(lang))
    elif msg in t["category_buttons"] or msg == "💾 Code":
        if msg == "💾 Code":
            await update.message.reply_text("📂 GitHub: https://github.com/Gerther?tab=overview&from=2025-04-01&to=2025-04-20")
            return

        category = get_category_from_button(msg)
        path = os.path.join(WORKS_FOLDER, category)
        file_path = get_random_file(path)

        if not file_path:
            await update.message.reply_text(t["no_works"])
            return

        ext = file_path.lower().split('.')[-1]
        with open(file_path, "rb") as f:
            if ext in ["jpg", "jpeg", "png", "webp"]:
                await update.message.reply_photo(photo=f)
            elif ext in ["mp4", "mov", "mkv"]:
                await update.message.reply_video(video=f)

        await update.message.reply_text(t["more_works"])
    elif msg == t["back_btn"]:
        await update.message.reply_text(t["back_to_main"], reply_markup=get_main_menu(lang))
    elif msg in ["🌐 Выбрать язык", "🌐 Choose language", "🌐 Wybierz język"]:
        await update.message.reply_text(t["choose_language"], reply_markup=language_menu)
    elif msg == "🇷🇺 Русский":
        context.user_data["lang"] = "ru"
        await update.message.reply_text("Язык изменён на русский.", reply_markup=get_main_menu("ru"))
    elif msg == "🇬🇧 English":
        context.user_data["lang"] = "en"
        await update.message.reply_text("Language changed to English.", reply_markup=get_main_menu("en"))
    elif msg == "🇵🇱 Polski":
        context.user_data["lang"] = "pl"
        await update.message.reply_text("Język zmieniony na polski.", reply_markup=get_main_menu("pl"))
    else:
        await update.message.reply_text(t["unknown_command"], reply_markup=get_main_menu(lang))

def get_category_from_button(button_text):
    mapping = {
        "🧊 3D": "3d",
        "🎨 Дизайн": "design", "🎨 Design": "design", "🎨 Projektowanie": "design",
        "🎥 After Effects": "ae"
    }
    return mapping.get(button_text)

def get_random_file(folder):
    allowed = ('.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mov', '.mkv')
    if not os.path.exists(folder):
        return None
    files = [f for f in os.listdir(folder) if f.lower().endswith(allowed)]
    if not files:
        return None
    return os.path.join(folder, random.choice(files))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
