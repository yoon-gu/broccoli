# Multi-turn Chatbot

## 실행 방법

아래와 같이 명령어를 실행하시면 됩니다.

```bash
$ cd n02_react_agent
$ python main.py
```

## LLM들 로드하는 방법

```python
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
```

## ReAct Agent란?

```
이 밑에 있는 내용은 ChatGPT를 이용한 답변이므로 기능과 관련이 없을 수 있습니다.
```

ReAct Agent LLM은 대화형 언어 모델(Language Model)입니다. 이 모델은 인간과의 상호작용을 통해 다양한 주제에 대해 자연스러운 대화를 진행할 수 있도록 설계되었습니다. 주로 자연어 이해(Natural Language Understanding, NLU)와 자연어 생성(Natural Language Generation, NLG) 기술을 활용하여 사용자의 질문에 답변하거나 정보를 제공하는 데 사용됩니다.

ReAct Agent LLM은 특히 사용자 의도를 파악하고 적절한 반응을 생성하는 데 초점을 맞추고 있어, 사용자와의 상호작용에서 보다 인간적이고 유연한 대화가 가능합니다. 또한, 이 모델은 다양한 분야에서 응용될 수 있으며, 고객 서비스, 교육, 엔터테인먼트 등 여러 분야에서 활용될 수 있는 높은 확장성을 가지고 있습니다.