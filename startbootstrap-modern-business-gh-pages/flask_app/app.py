import os
from flask import Flask, render_template, url_for, request, redirect, send_from_directory, jsonify
from together import Together
import base64
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()
# Configure the upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/uploads/')  # Set the upload path to the 'uploads' directory

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tryon.html")
def tryon():
    return render_template("tryon.html")

@app.route("/upload", methods=["POST"])
def upload():
    print("entered upload")
    if "file" not in request.files:
        print("entered if not")
        return redirect(url_for("home"))

    file = request.files['file']
    search_query = request.form.get("search_query")
    encoded_image = base64.b64encode(file.read()).decode('utf-8') 
    
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "user", "content": search_query}],
        stream=True,
    )
    # Process and print the response from LLaMA
    response_content = ""
    for chunk in stream:
        response_content += chunk.choices[0].delta.content or ""
    print(search_query)
    print(encoded_image)
    print(response_content)
    return jsonify({
        "encoded_image": encoded_image,
        "search_query": search_query,
        "redirect_url": url_for('uploaded_file', filename=file.filename)
    })
@app.route('/upload/<filename>')
def uploaded_file(filename):
    print("entered uploaded_file")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    print(4)
    app.run(debug=True)
