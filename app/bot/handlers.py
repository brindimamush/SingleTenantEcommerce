from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from app.core.database import SessionLocal
from app.db.models.product import Product


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    keyboard = [
        [InlineKeyboardButton("🛒 Browse Products", callback_data="browse")],
        [InlineKeyboardButton("📦 My Orders", callback_data="orders")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="Welcome to our store! Choose an option:",
        reply_markup=reply_markup,
    )


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    if query.data == "browse":
        db = SessionLocal()
        products = db.query(Product).all()
        db.close()

        keyboard = [
            [InlineKeyboardButton(
                f"{p.name} - ${p.price}",
                callback_data=f"product_{p.id}"
            )]
            for p in products
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="🛒 Available Products:",
            reply_markup=reply_markup
        )

def register_handlers(app) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_callback))
