import os
from llama_index.llms.cohere import Cohere
from llama_index.llms.gemini import Gemini
from llama_index.llms.friendli import Friendli

cohere_apikey = os.environ("COHERE_API_KEY")
llm_cohere_cmd_r_plus = Cohere(api_key=cohere_apikey, model="command-r-plus")
llm_cohere_cmd_r = Cohere(api_key=cohere_apikey, model="command-r")
llm_cohere_cmd = Cohere(api_key=cohere_apikey, model="command")

gemini_apikey = os.environ("GEMINI_API_KEY")
llm_gemini = Gemini(api_key=gemini_apikey)

friendli_apikey = os.environ("FRIENDLI_API_KEY")

llm_friendli = Friendli(friendli_token=friendli_apikey)

llms_dict = {
                "cohere-command-r-plus": llm_cohere_cmd_r_plus,
                "cohere-command-r": llm_cohere_cmd_r,
                "cohere-command": llm_cohere_cmd,
                "gemini-pro": llm_gemini,
                "friendli-gemma-7B-instruct": llm_friendli
            }