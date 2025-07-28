from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

responses = {
    "hello": "Hi there! How can I help you?",
    "how are you": "I’m an AI assistant, I’m always good!",
    "project": "Could you tell me more about your project needs?",
    "thank you": "You’re welcome!"
}

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    msg = request.json['message'].lower()
    reply = responses.get(msg, "Sorry, I don’t understand. Can you rephrase?")
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
