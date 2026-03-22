import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompts
from call_functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api_key is NONE")

client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="NiggaBot")
    parser.add_argument("user_prompt", help="User Prompt", type=str)
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    agent_loop_exceeded = True

    for i in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompts,
                tools=[available_functions]
                )
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("the is no usage metadata, might be a failed api request")

        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_token_count}")
            print(f"Response tokens: {candidates_token_count}")

        function_response = []

        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)

                if len(function_call_result.parts) == 0:
                    raise Exception("function_call_result.parts is empty")

                if function_call_result.parts[0].function_response is None:
                    raise Exception("function_call_result.parts[0].function_response is None")

                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("function_call_result.parts[0].function_response.response is None")

                function_response.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print("Final response:")
            print(response.text)
            agent_loop_exceeded = False
            return

        messages.append(types.Content(role="user", parts=function_response))

    if agent_loop_exceeded:
        print("Agent Loop exceeded the limit with no final result")
        sys.exit(1)


if __name__ == "__main__":
    main()
