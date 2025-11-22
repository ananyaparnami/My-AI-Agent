from flask import Flask, request, jsonify
from agents import hunter_agent, brainstorm_agent, tutor_agent, router_decision

app = Flask(_name_)
hunter_chat = hunter_agent.start_chat(enable_automatic_function_calling=True)

@app.route('/', methods=['GET'])
def home():
    return "AI Concierge is Running!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    route = router_decision(user_input)
    
    response_text = ""
    if "HUNTER" in route:
        response_text = hunter_chat.send_message(user_input).text
    elif "BRAINSTORM" in route:
        response_text = brainstorm_agent.generate_content(user_input).text
    elif "TUTOR" in route:
        response_text = tutor_agent.generate_content(user_input).text
    
    return jsonify({"response": response_text})

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=8080)