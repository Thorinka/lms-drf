import os
import stripe


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def create_session(payment):
    product = stripe.Product.create(name="Gold Special")
    price = stripe.Price.create(
        unit_amount=int(f"{str(payment.amount)}"+"00"),
        currency="usd",
        product=product["id"],
    )

    payment = stripe.checkout.Session.create(
        success_url='https://example.com/success',
        line_items=[
            {
                "price": price["id"],
                "quantity": 1,
            },
        ],
        mode="payment",
    )
    return payment['url']
