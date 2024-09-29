import os
from flask import Flask, render_template, url_for, request, redirect, send_from_directory, jsonify, Response
import openai
import base64
from dotenv import load_dotenv
import json
import replicate
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
                    You are a virtual sales assistant for Amazon, helping customers choose clothes based on their photo. When a request is made, return a JSON object with the key 'top' and the summarized search term for Amazon. Return only the JSON object without ```json ```.
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
    # print(completion.choices[0].message.content.strip())
    # search_term = json.loads(completion.choices[0].message.content.strip())["top"]

    # Prepare parameters for the Rainforest API request
    # params = {
    #     'api_key': '359CCE8E59FA4CD38A87752395A15F24',
    #     'amazon_domain': 'amazon.com',
    #     'type': 'search',
    #     'search_term': search_term  # Use the generated search term
    # }

    # response = requests.get('https://api.rainforestapi.com/request', params=params)
    # print(type(response))
    # first_three = response[:3].json()
    # print(jsonify(first_three))
    wear()
    return Response(status=204)# for flask not to trigger redirect error

def wear():
    output = replicate.run(
    "viktorfa/oot_diffusion:9f8fa4956970dde99689af7488157a30aa152e23953526a605df1d77598343d7",
    input={
        "seed": 0,
        "steps": 20,
        "model_image": "https://raw.githubusercontent.com/viktorfa/oot_diffusion/main/oot_diffusion/assets/model_1.png",
        "garment_image": "https://replicate.delivery/pbxt/KTgyzr0WNtcgwN82xEEcc3zoydD8ooXPzMHC18fKZSWu9W5I/blue_jacket.webp",
        "guidance_scale": 2
        }
    )
    print(output)
@app.route('/upload/<filename>')
def uploaded_file(filename):
    print("entered uploaded_file")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    print(4)
    app.run(debug=True)
