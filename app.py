from flask import Flask, request, jsonify
from agents import hunter_agent, brainstorm_agent, tutor_agent, router_decision
import os

app = Flask(__name__)

# Initialize chat session for Hunter agent globally for the web context
hunter_chat = hunter_agent.start_chat(enable_automatic_function_calling=True)

@app.route('/', methods=['GET'])
def home():
    """
    Health check endpoint to verify the service is running.
    """
    return jsonify({
        "status": "active",
        "service": "AI & Data Science Concierge",
        "version": "1.0.0"
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint. Receives user input and routes to agents.
    """
    try:
        data = request.json
        user_input = data.get('message')
        
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Determine routing logic
        route = router_decision(user_input)
        print(f"[System] Web Request Routing to: {route}")
        
        response_text = ""
        
        if "HUNTER" in route:
            response = hunter_chat.send_message(user_input)
            response_text = response.text
        elif "BRAINSTORM" in route:
            response = brainstorm_agent.generate_content(user_input)
            response_text = response.text
        elif "TUTOR" in route:
            response = tutor_agent.generate_content(user_input)
            response_text = response.text
        else:
            # Fallback logic
            response_text = tutor_agent.generate_content(user_input).text
        
        return jsonify({
            "response": response_text,
            "agent_used": route
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))