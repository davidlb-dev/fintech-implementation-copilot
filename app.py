from datetime import datetime
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from openai import OpenAI

app = Flask(__name__)

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

print(
    "Flask startup:",
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "| API key loaded:",
    api_key is not None
)

@app.route("/", methods=["GET", "POST"])
def home():
   
   print(request.method)

   meeting_notes = ""
   
   analysis = ""
   
   if request.method == "POST":

      meeting_notes = request.form["meeting_notes"]

   #  print(meeting_notes)

      print("Meeting notes:", meeting_notes)
      print("Meeting notes length:", len(meeting_notes))

      response = client.responses.create(
      model="gpt-5",
      input=meeting_notes
   )

      analysis = response.output_text

   return render_template(
      "index.html",
      meeting_notes=meeting_notes,
      analysis=analysis
   )

if __name__ == "__main__":
    app.run(debug=True)