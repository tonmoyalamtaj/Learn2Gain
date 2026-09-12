import csv
import os
from flask import Flask, render_template,session,request,redirect,url_for
from dotenv import load_dotenv
from groq import Groq


app = Flask(__name__)
app.secret_key = "Tonmoy_alam_taj_harvard_university_computer_science_final_project_secret_key"

@app.route("/")
@app.route("/freecoursewithcertificate")
def freecoursewithcertificate():
    courses = []
    
    csv_path = os.path.join(os.path.dirname(__file__), "data_base.csv")

    with open(csv_path, mode="r", encoding="utf-8-sig") as file:
        csv_reader = csv.DictReader(file)
        for i in csv_reader:
            courses.append(i)

    return render_template("freecoursewithcertificate.html", courses=courses)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html")

@app.route("/showcase")
def showcase():
    return render_template("showcase.html")

@app.route("/ai_assitant",methods=["GET", "POST"])
def ai_assitant():

    if "messege" not in session:
        session['messege'] = []

    if request.method == "POST":
        user_question = request.form.get("messege","").strip()

        if user_question:
            info_of_project = os.path.join(os.path.dirname(__file__), "project_context.txt")
            with open(file=info_of_project,mode='r') as file:
               PROJECT_CONTEXT = file.read()

            chat_history = session["messege"]
            chat_history.append({"role":"user","content":user_question})

            load_dotenv()
            
            api = os.getenv("ai_api")
            
            client = Groq(api_key=api)

            response = client.chat.completions.create(
            messages=[
            {"role": "system", "content": PROJECT_CONTEXT},
            {"role": "user", "content": user_question}
            ],
            model="openai/gpt-oss-120b"  
            )
            ai_ans = response.choices[0].message.content

            chat_history.append({"role": "assistant", "content": ai_ans})
            session["messege"] = chat_history
            session.modified = True

            return redirect(url_for("ai_assitant"))

    return render_template("ai_assitant.html",messege=session.get("messege", []))

@app.route("/clear_chat")
def clear_chat():
    session.pop("messege", None)  
    return redirect(url_for("ai_assitant"))

if __name__ == '__main__':
    app.run(debug=True)


