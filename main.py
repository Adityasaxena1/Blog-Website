from flask import Flask, render_template, request
import requests
import smtplib


posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
MAIL_ID = "YOUR_MAIL_ID"
PASSWORD = "YOUR_PASSWORD"


app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")




@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=['GET', 'POST'])
def receive_data():
    if request.method == 'POST':
        name = request.form["name"]
        email= request.form["email"]
        phone=request.form["phone"]
        message = request.form["message"]
        send_mail(name, email, phone, message)
        print(f"{name}\n{email}\n{phone}\n{message}")
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_mail(name, email, number, message):
    email_message = f"Subject: New Message\n\n Name:{name}\nEmail: {email}\n Number: {number}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MAIL_ID, password=PASSWORD)
        connection.sendmail(from_addr=MAIL_ID, to_addrs=MAIL_ID, msg=email_message)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
