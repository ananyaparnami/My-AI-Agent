from agents import hunter_agent, brainstorm_agent, tutor_agent, router_decision

def run_chat():
    print("--- 🤖 AI Student Concierge Started ---")
    print("Ask me to find hackathons, give ideas, or plan studies. (Type 'exit' to stop)")
    
    hunter_chat = hunter_agent.start_chat(enable_automatic_function_calling=True)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit": break

        route = router_decision(user_input)
        print(f"(Routing to: {route})...")

        if "HUNTER" in route:
            print(hunter_chat.send_message(user_input).text)
        elif "BRAINSTORM" in route:
            print(brainstorm_agent.generate_content(user_input).text)
        elif "TUTOR" in route:
            print(tutor_agent.generate_content(user_input).text)
        else:
            print("I didn't understand that.")

if __name__ == "__main__":
    run_chat()
