from twoai import TWOAI, AgentDetails

if __name__ == "__main__":
    BASE_MODEL = "openhermes"
    sys_prompt = """
You are an AI Chatbot, you are an LLM, and your name is {current_name}, Now
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