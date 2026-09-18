from flask import Flask, render_template, request, jsonify
from google import generativeai as genai
import markdown
import re, random
from intent_classifier import classify_intent, get_image_url


API_KEY = "AIzaSyDGuUUKtAgpyMVYAewP6zljfepPvzqU0YA"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

def add_reactions_preserve_formatting(text):
    reaction_emojis = ["😊", "👍", "🎉", "🔥", "😉", "✨", "😎"]
    emoji_text = ""

    for line in text.splitlines():
        if not line.strip():
            emoji_text += "\n"
            continue

        if re.match(r'^[-*\u2022]\s+|^\d+\.', line):
            emoji_text += line + "\n"
            continue

        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', line)
        for s in sentences:
            emoji = random.choice(reaction_emojis)
            emoji_text += s.strip() + " " + emoji + " "
        emoji_text += "\n"
    return emoji_text

def format_response(text):
    with_emojis = add_reactions_preserve_formatting(text)
    return f"<p>{markdown.markdown(with_emojis)}</p>"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    if user_input:
        intent = classify_intent(user_input)
        image_url = get_image_url(intent)
        response = model.generate_content(user_input)
        formatted_response = format_response(response.text)
        return jsonify({"response": formatted_response, "image": image_url})

    return jsonify({"response": "Please enter a message.", "image": None})

if __name__ == "__main__":
    app.run(debug=True)
