import os
import argparse
from time import sleep
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from prompts import system_prompt
from call_function import available_functions, call_function

def generate_content(client, messages, verbose):
    err, res = None, None
    attempts = 5
    for attempt in range(attempts):
        try:
            res = client.models.generate_content(
                model="gemini-2.5-flash",
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

    final_text = None
    func_results = []
    if res.function_calls:
        for func in res.function_calls:
            func_res = call_function(func, verbose)

            if len(func_res.parts) == 0:
                raise Exception("Empty list arr from func response")

            if (
                func_res.parts[0].function_response is None
                or func_res.parts[0].function_response.response is None
            ):
                raise Exception("No function response")

            func_results.append(func_res.parts[0])
            if verbose:
                print(f"-> {func_res.parts[0].function_response.response}")
    else:
        final_text = res.text
    return {
        "candidates": res.candidates,
        "function_results": func_results,
        "final_response": final_text,
    }


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

gemini_client = genai.Client(api_key=api_key)

if api_key is None or len(api_key) == 0:
    raise RuntimeError("Gemini api key wasn't found")

def main():
    try:
        parser = argparse.ArgumentParser(description="Chatbot")
        parser.add_argument("user_prompt", type=str, help="User prompt")
        parser.add_argument(
            "--verbose", action="store_true", help="Enable verbose output"
        )
        args = parser.parse_args()

        if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")

        messages = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
        ]

        final_response = None
        for _ in range(20):
            res = generate_content(gemini_client, messages, args.verbose)
            for c in res["candidates"]:
                messages.append(c.content)
            for fr in res["function_results"]:
                messages.append(types.Content(role="user", parts=[fr]))
            if res["final_response"]:
                final_response = res["final_response"]
            if len(res["function_results"]) == 0:
                break
        if not final_response:
            print("Agent iterations exceeded limit")
            exit(1)
        print("Final Response")
        print(final_response)
    except Exception as err:
        print(err)
        exit(1)


if __name__ == "__main__":
    main()
