import os
from flask import Flask, render_template, url_for, request, redirect, send_from_directory, jsonify
import openai
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
    base64_string = f"data:{file.content_type};base64,{encoded_image}"
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the API key directly
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": '''
                You are a virtual sales assistant for Amazon where you assist customers in picking out new clothes. The photo is one of your customer. The customer will make a request. Determine an outfit that satisfies the request. Determine if the photo is upper body only. If it is, suggest a single Amazon query to find a {"top":?} that matches the outfit. If it is not, suggest Amazon queries for each of the following to find clothing for the new outfit: {"top":?, "bottom":?}, {"bottom":?}, {"top":}, or {"dress":?}. Select the most appropriate query section. After generating the reply, begin a code block and format the queries and upper_body_only as json. Be sure to include the article of clothing as the key and query as the value for the query section.
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
    # Process and print the response from LLaMA
    print(search_query)
    print(encoded_image)
    print(completion.choices[0].message)
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
