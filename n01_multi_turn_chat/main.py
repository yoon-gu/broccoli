import gradio as gr
from llama_index.core.base.llms.types import ChatMessage
from pprint import pprint
from llms import llms_dict

def respond(message, history, llm_name):
    messages = []
    for user_msg, bot_msg in history:
        print(user_msg, bot_msg)
        messages.append(ChatMessage(role="user", content=user_msg))
        messages.append(ChatMessage(role="assistant", content=bot_msg))
    messages.append(ChatMessage(role="user", content=message))
    
    pprint(messages)
    response = llms_dict[llm_name].stream_chat(messages)
    msg = ""
    for token in response:
        msg += token.delta
        yield msg

demo = gr.ChatInterface(respond,
                        additional_inputs=[gr.Radio(llms_dict.keys(), value="gemini-pro", label="LLM")])
demo.launch()
