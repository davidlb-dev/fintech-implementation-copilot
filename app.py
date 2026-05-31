from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
   
   print(request.method)

   meeting_notes = ""
   
   if request.method == "POST":

    meeting_notes = request.form["meeting_notes"]

    print(meeting_notes)

   return render_template(
      "index.html",
      meeting_notes=meeting_notes
   )
   
if __name__ == "__main__":
    app.run(debug=True)