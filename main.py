import gradio as gr
from n01_multi_turn_chat.main import demo as demo01
demo02 = gr.load("akazakov/rag-gradio-sample-project", src="spaces")

demo = gr.TabbedInterface([demo01, demo02], ["01. 멀티턴 챗봇 with 멀티 LLM", "02. RAG"])

if __name__ == "__main__":
    demo.launch()