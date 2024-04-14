import gradio as gr
from llama_index.core.base.llms.types import ChatMessage
from pprint import pprint
from llms import llms_dict

import os
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

with open(os.path.join(current_dir, "README.md"), 'r', encoding='utf-8') as file:
    README_STR = file.read()

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

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            llm_options= gr.Radio(llms_dict.keys(), value="gemini-pro", label="LLM")
            gr.ChatInterface(respond, additional_inputs=[llm_options])
        with gr.Column():
            gr.Markdown(README_STR)
demo.launch()
