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
import json
from app.bot.cart import cart_store
from app.core.database import SessionLocal
from app.db.models.product import Product
from app.db.models.order import Order

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
    if query is None or query.data is None:
        return

    await query.answer()
    user_id = query.from_user.id

    # BROWSE PRODUCTS
    if query.data == "browse":
        db = SessionLocal()
        products = db.query(Product).all()
        db.close()

        keyboard = [
            [InlineKeyboardButton(
                f"{p.name} - ${p.price}",
                callback_data=f"add_{p.id}"
            )]
            for p in products
        ]

        keyboard.append(
            [InlineKeyboardButton("🛍 View Cart", callback_data="view_cart")]
        )

        await query.edit_message_text(
            text="🛒 Available Products:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ADD TO CART
    elif query.data.startswith("add_"):
        product_id = int(query.data.split("_")[1])
        cart = cart_store[user_id]
        cart[product_id] = cart.get(product_id, 0) + 1
        keyboard = [
        [InlineKeyboardButton("➕ Add More", callback_data="browse")],
        [InlineKeyboardButton("🛍 View Cart", callback_data="view_cart")],
        ]

        await query.edit_message_text(
        text="✅ Added to cart",
        reply_markup=InlineKeyboardMarkup(keyboard),
        )
    # VIEW CART
    elif query.data == "view_cart":
        cart = cart_store.get(user_id, {})
        if not cart:
            await query.edit_message_text("🛒 Your cart is empty")
            return

        db = SessionLocal()
        total = 0
        lines = []

        for pid, qty in cart.items():
            product = db.get(Product, pid)
            if product:
                subtotal = product.price * qty
                total += subtotal
                lines.append(f"{product.name} x{qty} = ${subtotal}")

        db.close()

        text = "\n".join(lines) + f"\n\nTotal: ${total}"

        keyboard = [
            [InlineKeyboardButton("✅ Place Order", callback_data="place_order")],
        ]

        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # PLACE ORDER
    elif query.data == "place_order":
        cart = cart_store.get(user_id)
        if not cart:
            await query.edit_message_text("Cart is empty")
            return

        db = SessionLocal()
        total = 0
        items = []

        for pid, qty in cart.items():
            product = db.get(Product, pid)
            if product:
                total += product.price * qty
                items.append({
                    "product_id": pid,
                    "name": product.name,
                    "qty": qty,
                    "price": product.price,
                })

        order = Order(
            telegram_user_id=user_id,
            items=json.dumps(items),
            total_amount=total,
        )

        db.add(order)
        db.commit()
        db.close()

        cart_store.pop(user_id, None)

        await query.edit_message_text(
            "🎉 Order placed successfully!\nWe will contact you soon."
        )

def register_handlers(app) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_callback))
