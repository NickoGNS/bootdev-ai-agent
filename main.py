import os
import argparse
from time import sleep
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from prompts import system_prompt
from call_function import available_functions

def generate_content(client, messages, verbose):
    err, res = None, None
    attempts = 5
    for attempt in range(attempts):
        try:
            res = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            if res:
                break
        except Exception as e:
            err = e
        if attempt < attempts - 1:
            sleep(3)

    if err:
        raise RuntimeError(f"Something went wrong while requesting Gemini: {err}")

    if not res.usage_metadata:
        raise RuntimeError("Something went wrong while returning Gemini usage metadata")

    if verbose:
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens:", res.usage_metadata.candidates_token_count)

    print("Response:")
    print(res.text)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

gemini_client = genai.Client(api_key=api_key)

if api_key is None or len(api_key) == 0:
    raise RuntimeError("Gemini api key wasn't found")

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(gemini_client, messages, args.verbose)


if __name__ == "__main__":
    main()
