import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def generate_content(client, messages, verbose):
    res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )

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
