from twoai import TWOAI, AgentDetails
import sys

if __name__ == "__main__":
    # get arguemnts
    if len(sys.argv) > 1:
        BASE_MODEL = sys.argv[1]
    else:
        print("Usage: python main.py <model_name>")
        sys.exit(1)

    sys_prompt = """
You are a very intelligent AI Chatbot, and your name is {current_name}, Now
You will be having a converstaion with Another AI called {other_name}, and it's also same as you.
{current_objective} And repeat "<DONE!>" ONLY if you both established and agreed that you came to the end of the discussion. 
""".strip()
    agent_details: AgentDetails = (
        {
            "name": "Zerkus",
            "objective": "Debate against the other AI on what came first, the chicken or the egg."
            "and you think the chicken came first.",
        }, 
        {
            "name": "Nina",
            "objective": "Debate against the other AI on what came first, the chicken or the egg."
            "and you think the Egg came first.",
        }
    )
    twoai = TWOAI(
        model=BASE_MODEL, 
        agent_details=agent_details, 
        system_prompt=sys_prompt,

    )
    twoai.start_conversation()