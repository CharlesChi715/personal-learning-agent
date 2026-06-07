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
    score = 0
    rounds = 0
    instr = "Score this greeting out of 10 in terms of cheerfulness and then make it more cheerful(in format: 'Score: X; Improved version: S'):"
    starter = "Greeting in a cheerful tone."
    while score < 9.5 and rounds < 5:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions='' if rounds == 0 else instr,
            input=starter if rounds == 0 else che_sen,
        )
        res = response.output_text.strip()
        che_sen = res.split('Improved version: ')[-1].strip() if 'Improved version: ' in res else res
        score = int(res.split('Score: ')[-1].split(';')[0].strip()) if rounds > 0 else score

        rounds += 1
        print('Score: ' + str(score) + ' | Response in round ' + str(rounds) + ':  ', che_sen)