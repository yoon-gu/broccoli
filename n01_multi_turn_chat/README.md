# Multi-turn Chatbot

## 실행 방법

아래와 같이 명령어를 실행하시면 됩니다.

```bash
$ cd n01_multi_turn_chat
$ python main.py
```

## LLM들 로드하는 방법

```python
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
```

## 기타 내용

```
이 밑에 있는 내용은 ChatGPT를 이용한 답변이므로 기능과 관련이 없을 수 있습니다.
```

멀티턴 챗봇을 LlamaIndex LLM class를 사용하여 테스트하는 다양한 예제를 설명하겠습니다. 이 예제들은 챗봇의 다양한 능력을 테스트하고, 다양한 상황에서의 대응 방식을 이해하는 데 도움이 됩니다.

### 예제 1: 사용자 질문에 대한 연속적 대답 테스트

**목적**: 챗봇이 이전 대화 내용을 기억하고 이를 바탕으로 일관된 대답을 할 수 있는지 확인합니다.

**과정**:
1. 사용자가 "오늘 날씨는 어때?"라고 물어봅니다.
2. 챗봇이 해당 지역의 날씨 정보를 제공합니다.
3. 사용자가 "그럼 내일은?"이라고 물어보면 챗봇은 내일의 날씨 정보를 연속적으로 제공해야 합니다.

**예상 결과**:
챗봇은 이전의 대화 내용, 즉 오늘의 날씨에 대한 질문을 기억하고, 내일의 날씨 정보를 제공할 수 있어야 합니다.
