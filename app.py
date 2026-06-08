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

   status = ""
   
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

      Overall Status

      Executive Summary
      
      Risks
      
      Blockers
      
      Dependencies
      
      Action Items

      Determine Overall Status using these rules:

      - ON TRACK: No significant risks to timeline or delivery.
      - AT RISK: Risks or dependencies may impact timeline or delivery.
      - DELAYED: A blocker or issue has already caused a schedule delay.

      Format your response exactly as follows:

      Overall Status:
      <ON TRACK, AT RISK, or DELAYED>

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

      Do not repeat the project status in the Executive Summary. The Overall Status will be displayed separately by the application.
      
      If a category has no items, write "None identified."
      
      Meeting Notes:

      {meeting_notes}
     """
   )

      analysis = response.output_text

      print("\n=== ANALYSIS ===")
      print(analysis)
      print("=== END ANALYSIS ===\n")

      status = ""

      if "Overall Status:" in analysis:

         status = (
            analysis.split("Overall Status:")[1]
            .strip()
            .split("\n")[0]
            .strip()
         )

         analysis = analysis.replace(
            f"Overall Status:\n{status}\n\n",
            ""
         )

   executive_summary = ""

   if "Executive Summary:" in analysis:

      executive_summary = (
         analysis.split("Executive Summary:")[1]
         .split("Risks:")[0]
         .strip()
      )

   risks = ""

   if "Risks:" in analysis:

      risks = (
         analysis.split("Risks:")[1]
         .split("Blockers:")[0]
         .strip()
      )

   blockers = ""

   if "Blockers:" in analysis:

      blockers = (
         analysis.split("Blockers:")[1]
         .split("Dependencies:")[0]
         .strip()
      )

   dependencies = ""

   if "Dependencies:" in analysis:

      dependencies = (
         analysis.split("Dependencies:")[1]
         .split("Action Items:")[0]
         .strip()
      )

   action_items = ""

   if "Action Items:" in analysis:

      action_items = (
         analysis.split("Action Items:")[1]
         .strip()
      )

   return render_template(
      "index.html",
      meeting_notes=meeting_notes,
      analysis=analysis,
      status=status,
      executive_summary=executive_summary,
      risks=risks,
      blockers=blockers,
      dependencies=dependencies,
      action_items = action_items,
      current_year=datetime.now().year
   )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)