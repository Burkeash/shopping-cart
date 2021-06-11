# shopping_cart.py

import datetime
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", default="OOPS, please set env var called 'EMAIL_ADDRESS'")

TAX_RATE = 0.08875


def to_usd(my_price):
  
    return f"${my_price:,.2f}"

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017


timestamp = datetime.datetime.now()
human_friendly_timestamp = timestamp.strftime("%Y-%m-%d %H:%M")

print(len(products))

#1 capture product IDs until we're finished
#(use infinite while loop)

selected_products = []

while True:
    selected_id = input("Please input a product id, or 'DONE': " )

    if selected_id.upper() == "DONE":
        break # (breaking  out of while loop)
    else:
        try:
            matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
            matching_product = matching_products[0]
            selected_products.append(matching_product)
        except IndexError as e:
            print("Oh, product not found. Please try again...")
            

if not selected_products:
    print("You haven't selected any products. Please try again.")
    exit()


subtotal = sum([float(p["price"]) for p in selected_products])
tax = subtotal * TAX_RATE
total = subtotal + tax



print("---------------------------")
print("WELCOME TO BURKE'S GROCERY STORE!")
print("CHECKOUT AT:", human_friendly_timestamp)
print("---------------------------")
print("SELECTED PRODUCTS:")
for p in selected_products:
    print(f"... {p['name']} {to_usd(p['price'])}")


# Adapted from Professor's code!

print("---------------------------")
print("SUBTOTAL:", to_usd(subtotal))
print("TAX:", to_usd(tax))
print("TOTAL:", to_usd(total))

#Receipt Section

print("Would you like a receipt?")
user_email_address = input("Please input your email address, or 'N' to opt-out: ")

if user_email_address.upper() == "Y":
    print(f"Hello! Using your default email address {EMAIL_ADDRESS} :-D")
    user_email_address = EMAIL_ADDRESS

if user_email_address.upper() in ["N", "NO", "N/A"]:
    print("You've elected to not receive a receipt via email.")
elif "@" not in user_email_address:
    print("Oh, detected invalid email address.")
else:
    print("Sending receipt via email...")

    # format all product prices as we'd like them to appear in the email...
    formatted_products = []
    for p in selected_products:
        formatted_product = p
        if not isinstance(formatted_product["price"], str): #Adapted from professor's code
            formatted_product["price"] = to_usd(p["price"])
        formatted_products.append(formatted_product)

    receipt = {
        "subtotal_price_usd": to_usd(subtotal),
        "tax_price_usd": to_usd(tax),
        "total_price_usd": to_usd(total),
        "human_friendly_timestamp": human_friendly_timestamp,
        "products": formatted_products
    }
    

    client = SendGridAPIClient(SENDGRID_API_KEY)

    message = Mail(from_email=user_email_address, to_emails=user_email_address)
    message.template_id = SENDGRID_TEMPLATE_ID
    message.dynamic_template_data = receipt

    response = client.send(message)

    if str(response.status_code) == "202":
        print("Email sent successfully!")
    else:
        print("Oh, something went wrong with sending the email.")
        print(response.status_code)
        print(response.body)

print("Thanks for shopping!")

for selected_id in selected_ids:
    #print(selected_id)
    # lookup the corresponding product!
    # ... and display the selected product's name and price
    matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
    # FYI the result of our list comprehension will be a list!
    matching_product = matching_products[0] # ... so we'll need to access its first item using [0]
    total_price = total_price + matching_product["price"]
    print("SELECTED PRODUCT: " + matching_product["name"] + " " + str(matching_product["price"]))




print("TOTAL PRICE: " + str(total_price)) #put in USD


