import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    # get prompt from command line arguments
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()
    
    # create context 
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    # connect to Gemini
    load_dotenv() #get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # check if the API key was found
    if api_key == None:
        raise RuntimeError("API Key not found.")

    client = genai.Client(api_key = api_key)
    prompt = args.user_prompt
    verbose = args.verbose

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0),
        )
    
    # print metadata if requested
    if verbose:
        print(f"User prompt: {prompt}")
        if response.usage_metadata:
            print(
                f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
                )
            print(
                "Response tokens: "
                f"{response.usage_metadata.candidates_token_count}"
                )
        else:
            raise RuntimeError("No response received from API")

    # if there are any function calls in the response
    if type(response.function_calls) == list:
        # print the list of function calls
        for function_call in response.function_calls:
           
            function_call_result = call_function(function_call, verbose)


            # check that response is valid
            if (not isinstance(function_call_result.parts, list) or
                function_call_result.parts == None or 
                function_call_result.parts == [] or 
                function_call_result.parts[0].function_response == None or
                function_call_result.parts[0].function_response.response == None
            ):
                raise Exception("Function call did not return a valid "
                                "response.")
            
            function_results = [function_call_result.parts[0]]
        
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
