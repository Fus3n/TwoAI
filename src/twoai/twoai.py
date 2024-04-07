import ollama
from colorama import Fore, Style
from . import AgentDetails

class TWOAI:
    """
    Class representing an AI that can engage in a conversation with another AI.
    
        ai_details (AIDetails): Details of the AI including name and objective.
        model (str): The model used by the AI.
        system_prompt (str): The prompt for the AI conversation system.
        max_tokens (int): The maximum number of tokens to generate in the AI response.
        num_context (int): The number of previous messages to consider in the AI response.
        extra_stops (list): Additional stop words to include in the AI response.
        exit_word (str): The exit word to use in the AI response. Defaults to "<DONE!>".
        max_exit_words (int): The maximum number of exit words to include in the AI responses for the conversation to conclude. Defaults to 2.
    """
    def __init__(
            self, 
            model: str, 
            agent_details: AgentDetails, 
            system_prompt: str, 
            max_tokens: int=4094, 
            num_context: int=4094, 
            extra_stops: list[str] = [],
            exit_word: str = "<DONE!>",
            temperature: int = 0.7,
            max_exit_words: int = 2
        ) -> None:
        self.agent_details = agent_details
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.num_context = num_context
        self.extra_stops = extra_stops
        self.temperature = temperature

        self.messages = ""
        self.current_agent = agent_details[0]

        self.exit_word = exit_word
        self.exit_word_count = 0
        self.max_exit_words = max_exit_words

    def bot_say(self, msg: str, color: str = Fore.LIGHTGREEN_EX):
        print(color + msg.strip() + Style.RESET_ALL)

    def get_opposite_ai(self) -> AgentDetails:
        if self.current_agent['name'] == self.agent_details[0]['name']:
            return self.agent_details[1]
        return self.agent_details[0]

    def __get_updated_template_str(self):
        result = self.system_prompt.replace("{current_name}", self.current_agent['name'])
        result = result.replace("{current_objective}", self.current_agent['objective'])

        other_ai = self.get_opposite_ai()
        result = result.replace("{other_name}", other_ai["name"])
        result = result.replace("{other_objective}", other_ai["objective"])
        return result

    def next_response(self, show_output: bool = False) -> str:
        if len(self.agent_details) < 2:
            raise Exception("Not enough AI details provided")

        other_ai = self.get_opposite_ai()
        instructions = self.__get_updated_template_str()
        convo = f"""
        {instructions}

        {self.messages}
        """

        current_model = self.model
        if model := self.current_agent.get('model', None):
            current_model = model

        resp = ollama.generate(
            model=current_model, 
            prompt=convo.strip(), 
            stream=False, 
            options={
                "num_predict": self.max_tokens,
                "temperature": self.temperature,
                "num_ctx": self.num_context,
                "stop": [
                    "<|im_start|>",
                    "<|im_end|>",
                    "###",
                    "\r\n",
                   f"{other_ai['name']}: " if self.current_agent['name'] != other_ai['name'] else f"{self.current_agent['name']}: "
                    
                ] + self.extra_stops
            }
        )

        text: str = resp['response']
        if not text.startswith(self.current_agent['name'] + ": "):
            text = self.current_agent['name'] + ": " + text
        self.messages += text + "\n"

        if show_output:
            if self.agent_details.index(self.current_agent) == 0:
                self.bot_say(text)
            else:
                self.bot_say(text, Fore.BLUE)
        
        self.current_agent = self.get_opposite_ai()
        return text

    def start_conversation(self):
        try:
            while True:
                res = self.next_response(show_output=True)
                if self.exit_word in res:
                    self.exit_word_count += 1
                if self.exit_word_count == self.max_exit_words:
                    print(Fore.RED + "The conversation was concluded..." + Style.RESET_ALL)
                    return
        except KeyboardInterrupt:
            print(Fore.RED + "Closing Conversation..." + Style.RESET_ALL)
            return