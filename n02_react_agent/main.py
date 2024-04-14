import functools
import sys
sys.path.append("../")
from io import StringIO
from typing import Any, Dict, List, Optional, Tuple
import os
from llama_index.core.agent import ReActAgent
from llama_index.core.llama_pack.base import BaseLlamaPack
from llama_index.llms.cohere import Cohere
from llama_index.tools.arxiv import ArxivToolSpec
from llama_index.tools.wikipedia import WikipediaToolSpec
from llms import llms_dict

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
with open(os.path.join(current_dir, "README.md"), 'r', encoding='utf-8') as file:
    README_STR = file.read()

SUPPORTED_TOOLS = {
    "arxiv_search_tool": ArxivToolSpec,
    "wikipedia": WikipediaToolSpec,
}


class Capturing(list):
    """To capture the stdout from ReActAgent.chat with verbose=True. Taken from
    https://stackoverflow.com/questions/16571150/\
        how-to-capture-stdout-output-from-a-python-function-call.
    """

    def __enter__(self) -> Any:
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args) -> None:
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


class GradioReActAgentPack(BaseLlamaPack):
    """Gradio chatbot to chat with a ReActAgent pack."""

    def __init__(
        self,
        tools_list: Optional[List[str]] = list(SUPPORTED_TOOLS.keys()),
        **kwargs: Any,
    ) -> None:
        """Init params."""
        try:
            from ansi2html import Ansi2HTMLConverter
        except ImportError:
            raise ImportError("Please install ansi2html via `pip install ansi2html`")

        tools = []
        for t in tools_list:
            try:
                tools.append(SUPPORTED_TOOLS[t]())
            except KeyError:
                raise KeyError(f"Tool {t} is not supported.")
        self.tools = tools

        self.llm = llms_dict["cohere-command-r-plus"]
        self.agent = ReActAgent.from_tools(
            tools=functools.reduce(
                lambda x, y: x.to_tool_list() + y.to_tool_list(), self.tools
            ),
            llm=self.llm,
            verbose=True,
        )

        self.thoughts = ""
        self.conv = Ansi2HTMLConverter()

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {"agent": self.agent, "llm": self.llm, "tools": self.tools}

    def _handle_user_message(self, user_message, history):
        """Handle the user submitted message. Clear message box, and append
        to the history.
        """
        return "", [*history, (user_message, "")]

    def _generate_response(
        self, chat_history: List[Tuple[str, str]]
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """Generate the response from agent, and capture the stdout of the
        ReActAgent's thoughts.
        """
        with Capturing() as output:
            response = self.agent.stream_chat(chat_history[-1][0])
        ansi = "\n========\n".join(output)
        html_output = self.conv.convert(ansi)
        for token in response.response_gen:
            chat_history[-1][1] += token
            yield chat_history, str(html_output)

    def _reset_chat(self) -> Tuple[str, str]:
        """Reset the agent's chat history. And clear all dialogue boxes."""
        # clear agent history
        self.agent.reset()
        return "", "", ""  # clear textboxes


runner = GradioReActAgentPack(run_from_main=True)

import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            chat_window = gr.Chatbot(
                label="Message History",
            )
            message = gr.Textbox(label="Write A Message", scale=4)
            clear = gr.ClearButton()
            with gr.Accordion(label="Agent Thoughts", open=False):
                console = gr.HTML()
        with gr.Column():
            gr.Markdown(README_STR)

    message.submit(
        runner._handle_user_message,
        [message, chat_window],
        [message, chat_window],
        queue=False,
    ).then(
        runner._generate_response,
        chat_window,
        [chat_window, console],
    )
    clear.click(runner._reset_chat, None, [message, chat_window, console])

        
if __name__ == "__main__":
    demo.launch()
