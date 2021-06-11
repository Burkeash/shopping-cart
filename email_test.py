import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDER_ADDRESS = os.environ.get("SENDER_ADDRESS", "OOPS, please set env var called 'SENDER_ADDRESS'")

client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
print("CLIENT:", type(client))

subject = "Your Receipt from Burke's Grocery Store"

html_content = "Hello World"
#
#  ...OR MAYBE START TO USE SOME HTML FORMATTING...
#
# html_content = "Hello <strong>World</strong>"
#
#  ...OR MAYBE ASSEMBLE AN ENTIRE PAGE OF HTML INTO A SINGLE STRING...
#
# html_list_items = "<li>You ordered: Product 1</li>"
# html_list_items += "<li>You ordered: Product 2</li>"
# html_list_items += "<li>You ordered: Product 3</li>"
# html_content = f"""
# <h3>Hello this is your receipt</h3>
# <p>Date: ____________</p>
# <ol>
#     {html_list_items}
# </ol>
# """
#
print("HTML:", html_content)

message = Mail(from_email=SENDER_ADDRESS, to_emails=SENDER_ADDRESS, subject=subject, html_content=html_content)

try:
    response = client.send(message)

    print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
    print(response.status_code) #> 202 indicates SUCCESS
    print(response.body)
    print(response.headers)

except Exception as err:
    print("OOPS")
    print(type(err))
    print(err)
