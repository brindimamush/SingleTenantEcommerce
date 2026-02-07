from collections import defaultdict

# telegram_user_id -> {product_id: quantity}
cart_store = defaultdict(dict)
