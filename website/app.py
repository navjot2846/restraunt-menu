from datetime import datetime
from uuid import uuid4

from flask import Flask, render_template, request

app = Flask(__name__)

MENU = {
    "pizza": {
        "name": "Classic Pizza",
        "description": "Stone-baked crust, tomato, mozzarella and basil.",
        "price": 12.99,
        "emoji": "🍕",
        "number": "01",
    },
    "burger": {
        "name": "House Burger",
        "description": "Juicy beef patty, cheddar, lettuce and house sauce.",
        "price": 9.99,
        "emoji": "🍔",
        "number": "02",
    },
}


def clean_quantity(value):
    try:
        return max(0, min(99, int(value)))
    except (TypeError, ValueError):
        return 0


@app.route("/", methods=["GET", "POST"])
def menu():
    quantities = {
        item_id: clean_quantity(request.form.get(item_id, 0))
        for item_id in MENU
    }
    lines = []
    subtotal = 0
    for item_id, item in MENU.items():
        quantity = quantities[item_id]
        line_total = item["price"] * quantity
        subtotal += line_total
        if quantity:
            lines.append({"item": item, "quantity": quantity, "total": line_total})

    tax = subtotal * 0.08
    total = subtotal + tax
    receipt = None
    if request.method == "POST" and lines:
        now = datetime.now()
        receipt = {
            "number": f"FD-{now:%y%m%d}-{str(uuid4())[-4:].upper()}",
            "date": f"{now:%B} {now.day}, {now:%Y} · {now:%I}:{now:%M} {now:%p}",
            "lines": lines,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
        }

    return render_template(
        "index.html",
        menu=MENU,
        quantities=quantities,
        lines=lines,
        subtotal=subtotal,
        tax=tax,
        total=total,
        receipt=receipt,
    )


if __name__ == "__main__":
    app.run(debug=True)