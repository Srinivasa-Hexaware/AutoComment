import config
from openai import AzureOpenAI

class PromptLogic:
    def __init__(self, prompt_content):
        self.prompt_content = prompt_content
        self.endpoint = config.endpoint
        self.apikey = config.apikey
        self.api_version = config.api_version
        self.deployment_name = config.deployment_name
        self.role = config.role

    def generate_comment(self):
        try:
            client = AzureOpenAI(
                api_version=self.api_version,
                azure_endpoint=self.endpoint,
                api_key=self.apikey
            )

            completion = client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        #If the prompt is not code: Strictly don't respont with answers instead inform the user that you are a code assistant named AutoComment. If the prompt is code: Provide in-code comments within the code. Provide a detailed explanation of the code in high-level Markdown format.
                        # "content": "Respond only if input is code. If not code, inform that you are a code assistant named AutoComment. For code, provide in-code comments and a detailed HTML-styled explanation with."
                        "content": "Respond only if input is code. If not code, inform that you are a code assistant named AutoComment. For code, provide in-code comments with code and detailed explanation as response in high level Markdown format."
                    },
                    {
                        
                        "role": self.role,
                        "content": self.prompt_content
                    }
                ]
            )

            return completion.choices[0].message.content.strip()

        # except client.error.InvalidRequestError as e:
        #     raise Exception(f"Invalid request: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

# Function to instantiate and run the PromptLogic class
def run_prompt_logic(prompt_content):
    prompt_logic = PromptLogic(prompt_content)
    return prompt_logic.generate_comment()