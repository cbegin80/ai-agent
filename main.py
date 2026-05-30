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

    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0),
            )
        
        if response.candidates is not None:
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)
        
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
                messages.append(types.Content(role="user", parts=function_results))
                # print(f"Messages: {messages}")                                                      # TRACE

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                
                if i == 19:
                    print("ERROR: The model could not reach an answer after 20 iterations.")
                    exit(1)
        else:
            print(response.text)
            break
        


if __name__ == "__main__":
    main()
