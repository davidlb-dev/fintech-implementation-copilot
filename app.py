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
         input=f"""
      You are a fintech implementation analyst.

      Analyze the meeting notes and provide the following sections.

      Executive Summary
      
      Risks
      
      Blockers
      
      Dependencies
      
      Action Items

      Format your response exactly as follows:

      Executive Summary:
      <summary>

      Risks:
      - risk 1
      - risk 2

      Blockers:
      - blocker 1
      - blocker 2

      Dependencies:
      - dependency 1
      - dependency 2

      Action Items:
      - owner: action item 1
      - owner: action item 2

      If a category has no items, write "None identified."
      
      Meeting Notes:

      {meeting_notes}
     """
   )

      analysis = response.output_text

   return render_template(
      "index.html",
      meeting_notes=meeting_notes,
      analysis=analysis
   )

if __name__ == "__main__":
    app.run(debug=True)