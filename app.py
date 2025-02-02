import os
from flask import Flask, request, render_template
from analyzer import analyze_resume

app = Flask(__name__)

UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_resume():
    if request.method == "POST":
        if "resume" not in request.files:
            return "No file uploaded", 400

        file = request.files["resume"]
        if file.filename == "":
            return "No file selected", 400

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        resume_data = analyze_resume(file_path)

        return render_template("result.html", resume_data=resume_data)

    return render_template("index.html")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

