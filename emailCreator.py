import json
from email.message import EmailMessage
from constants import *
import smtplib
from jinja2 import Environment, PackageLoader, select_autoescape
from bs4 import BeautifulSoup


class Email:

    def __init__(self, giver_email, giver_name, receiver_name):
        self.giver_name = giver_name
        self.giver_email = giver_email
        self.receiver_name = receiver_name

        # get credentials from JSON file with try-except block
        try:
            with open("credentials.json", "r", encoding="utf-8") as f:
                self.sender_credentials = json.load(f)
        except FileNotFoundError:
            print("Error: File not found!")
            self.sender_credentials = None

    def create_email(self):
        env = Environment(
            loader=PackageLoader("emailCreator", "."),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template("emailTemplate.html")
        content = {
            "subject": f"{SUBJECT_EMOJI} {SUBJECT} {SUBJECT_EMOJI}",
            "giver": self.giver_name,
            "receiver": self.receiver_name,
            "min": MIN_AMOUNT,
            "max": MAX_AMOUNT,
            "date": DATE,
            "month": MONTH,
            "time": TIME,
            "place": PLACE,
            "address": ADDRESS,
        }

        html = template.render(content=content)

        def extract_text_from_html(html_content):
            soup = BeautifulSoup(html_content, "html.parser")
            return soup.get_text()

        text = extract_text_from_html(html)

        return {"text": text, "html": html}

    def send_email(self):
        # build email message
        msg = EmailMessage()
        msg["Subject"] = SUBJECT
        msg["From"] = self.sender_credentials["email"]
        msg["To"] = self.giver_email

        # add Plaintext and HTML content
        msg_body = self.create_email()
        msg.set_content(msg_body["text"])
        msg.add_alternative(msg_body["html"], subtype="html")

        # Send the email using Outlook SMTP server
        try:
            # Connect to the Outlook SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  # Upgrade the connection to secure
            server.login(
                self.sender_credentials["email"], self.sender_credentials["password"]
            )  # Log in with email and App Password
            server.send_message(msg)
            print("Email sent successfully to", self.giver_email, "!")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()  # Close the connection


if __name__ == "__main__":
    email = Email("someone@gmail.com", "María", "Nadie")

    ##### test format_message() #####
    print("\nTesting email body generation...")
    message = email.create_email()
    email.send_email()

    # print Plaintext and HTML messages
    print("\nPlaintext email body is...")
    print(message["text"])
    print("\n------------------------------------------------------------")
    print("\nHTML email body is...")
    print(message["html"])

    # save Plaintext and HTML messages to file
    with open("message_text.txt", "w", encoding="utf-8") as f:
        f.write(message["text"])
    with open("message_html.html", "w", encoding="utf-8") as f:
        f.write(message["html"])
