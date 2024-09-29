import os
from flask import Flask, render_template, url_for, request, redirect, send_from_directory, jsonify, Response
import openai
import base64
from dotenv import load_dotenv
import json
import requests
app = Flask(__name__)
load_dotenv()
# Configure the upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/uploads/')  # Set the upload path to the 'uploads' directory

search_query = ''

# make the http GET request to Rainforest API


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tryon.html")
def tryon():
    return render_template("tryon.html")

@app.route("/upload", methods=["POST"])
def upload():
    global search_query
    print("entered upload")
    if "file" not in request.files:
        print("entered if not")
        return redirect(url_for("home"))

    file = request.files['file']
    search_query = request.form.get("search_query")
    encoded_image = base64.b64encode(file.read()).decode('utf-8') 
    base64_string = f"data:{file.content_type};base64,{encoded_image}"
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the API key directly
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": '''
                    just make search term. nothing else
                '''
            },
            {
                "role": "user",
                "content": [
                    search_query,
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base64_string
                        }
                    }]
            }
        ]
    )
    search_term = completion.choices[0].message.content.strip()

    # Prepare parameters for the Rainforest API request
    params = {
        'api_key': '359CCE8E59FA4CD38A87752395A15F24',
        'amazon_domain': 'amazon.com',
        'type': 'search',
        'search_term': search_term  # Use the generated search term
    }

    # Make the HTTP GET request to Rainforest API
    response = requests.get('https://api.rainforestapi.com/request', params=params)
    print(json.dumps(response.json()))
    return Response(status=204)# for flask not to trigger redirect error
@app.route('/upload/<filename>')
def uploaded_file(filename):
    print("entered uploaded_file")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    print(4)
    app.run(debug=True)
