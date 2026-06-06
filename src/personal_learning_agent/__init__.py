import os
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint as pp

load_dotenv()

def main() -> None:
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    # score = 0
    rounds = 0
    instr = "Make this greeting more cheerful:"
    starter = "Greeting in a cheerful tone."
    # while score < 10 and rounds < 5:
    while rounds < 5:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions='' if rounds == 0 else instr,
            input=starter if rounds == 0 else response.output_text,
        )
        
        rounds += 1
        print('response in round ' + str(rounds) + ':', response.output_text)
    