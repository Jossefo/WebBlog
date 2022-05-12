import smtplib

import requests
from flask import Flask, render_template , request
from post import Post


fake_posts = requests.get('https://api.npoint.io/bdb5d42648ebfbc1f3f4').json()
fake_post_obj = []
for post in fake_posts:
    post_obj = Post(post_id=post['id'],title=post['title'],subtitle=post['subtitle'],body=post['body'])
    fake_post_obj.append(post_obj)

EMAIL_USER_NAME = "th.pt@yaho.com"
EMAIL_PASSWORD = "Yd123456"

app = Flask(__name__)

def send_mail_contact(name , email , phone_number , msg):
    with smtplib.SMTP("smtp.yahoo.com") as connection_smtp:
        connection_smtp.starttls()
        connection_smtp.login(user=EMAIL_USER_NAME , password=EMAIL_PASSWORD )
        msg_body = f"Subject: New message ! \n" \
                   f"Name : {name} \n" \
                   f"Phone : {phone_number} \n" \
                   f"Email : {email} \n" \
                   f"{msg}"
        connection_smtp.sendmail(from_addr=EMAIL_USER_NAME , to_addrs=EMAIL_USER_NAME,msg=msg_body)

@app.route('/')
def home():
    return render_template("index.html" , all_posts = fake_post_obj)

@app.route('/post/<int:index>')
def show_post(index):
    post = None
    for post_in in fake_post_obj:
        if post_in.id == index:
            post = post_in
    return render_template('post.html' , post = post)

@app.route("/about")
def show_about():
    return render_template("about.html")

@app.route("/contact" , methods=["GET" , "POST"])
def show_contact():
    if request.method == "POST":
        data = request.form
        send_mail_contact(name=data["name"],email=data["email"],phone_number=data["phone"],msg=data["message"])
        return render_template("contact.html" , msg_sent = True)
    return render_template("contact.html" , msg_sent=False)

if __name__ == "__main__":
    app.run(debug=True)
