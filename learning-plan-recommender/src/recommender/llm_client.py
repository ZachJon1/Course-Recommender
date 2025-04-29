import json
import openai

class LLMClient:
    def __init__(self, host, port, api_key):
        self.client = openai.Client(base_url=f"http://{host}:{port}/v1", api_key=api_key)
        self.model_name = self.client.models.list().data[0].id

    def query_llm(self, message, history_json="[]"):
        history = json.loads(history_json) if history_json else []
        messages = history + [{"role": "user", "content": message}]
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.6,
            top_p=0.95,
        )
        
        return {
            "content": response.choices[0].message.content,
            "role": "assistant"
        }