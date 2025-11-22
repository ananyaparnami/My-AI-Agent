from agents import hunter_agent, brainstorm_agent, tutor_agent, router_decision
import sys

def run_chat():
    print("--- AI & Data Science Concierge System Initialized ---")
    print("I can assist you with finding hackathons, brainstorming project ideas, or creating study plans.")
    print("(Type 'exit' to terminate the session)\n")
    
    # Initialize chat session for the Hunter agent to enable function calling history
    hunter_chat = hunter_agent.start_chat(enable_automatic_function_calling=True)

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                print("System: Session terminated. Good luck!")
                break

            # Determine the appropriate agent via the Router
            route = router_decision(user_input)
            print(f"[System] Routing request to: {route} Agent...")

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
                # Fallback response
                response_text = "I could not determine the specific intent, but here is some general advice: " + \
                                tutor_agent.generate_content(user_input).text

            print(f"\nConcierge: {response_text}\n")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_chat()
