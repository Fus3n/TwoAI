from twoai import Agent, TWOAI, AgentDetails

# run tests on twoai
import unittest

class TestTwoAI(unittest.TestCase):

    def test_create_agent(self):
        agent = Agent(name="Zerkus", objective="Debate the chicken or the egg with the other AI")
        self.assertEqual(agent['name'], "Zerkus")
        self.assertEqual(agent['objective'], "Debate the chicken or the egg with the other AI")
        self.assertEqual(agent.get('model', None), None)
        self.assertEqual(agent.get('host', None), None)

    def test_twoai(self):
        TEST_MODEL = "qwen2:1.5b" #CHOOSE MODEL
        sys_prompt = """You are {current_name}, you will talk to {other_name}. You will {current_objective}""".strip()
        agent_details: AgentDetails = (
            {
                "name": "Zerkus",
                "objective": "Have a normal converstaion",
            }, 
            {
                "name": "Nina",
                "objective": "Have a normal converstaion",
            }
        )
        twoai = TWOAI(
            model=TEST_MODEL, 
            agent_details=agent_details, 
            system_prompt=sys_prompt,
        )

        # test if generated template is matched or not
        self.assertEqual(twoai.get_updated_template_str(), "You are Zerkus, you will talk to Nina. You will Have a normal converstaion")
        _ = twoai.next_response()
        self.assertEqual(twoai.get_updated_template_str(), "You are Nina, you will talk to Zerkus. You will Have a normal converstaion")