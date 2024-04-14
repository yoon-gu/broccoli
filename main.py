import gradio as gr
from n01_multi_turn_chat.main import demo as demo01
from n02_react_agent.main import demo as demo02
demo03 = gr.load("akazakov/rag-gradio-sample-project", src="spaces")

demo = gr.TabbedInterface([demo01, demo02, demo03], ["01. 멀티턴 챗봇 with 멀티 LLM", "02. ReAct", "03. RAG"])

if __name__ == "__main__":
    demo.launch()