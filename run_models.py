from __future__ import annotations

from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Any, Dict, List, Optional, Sequence, Union
import ollama

load_dotenv(override=True)

context_string = """
Return only the code itself organized in a single python function.
"""


def clean_response(response_text: str) -> str:
    return response_text.strip("```").strip("`").lstrip("python\n").strip()


def run_openai(
    prompts: List[str], client: Optional[OpenAI] = None, model="gpt-5.4-mini"
) -> List[str]:
    if not client:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    responses = [
        client.responses.create(
            model=model, input=context_string + "\n" + prompt, store=True
        )
        for prompt in prompts
    ]

    return [clean_response(response.output_text) for response in responses]


def run_ollama(prompts: List[str], model="qwen3.5") -> List[str]:

    responses = [
        ollama.chat(
            model=model,
            messages=[{"role": "user", "content": context_string + "\n" + prompt}],
        )
        for prompt in prompts
    ]

    return [
        clean_response(response["choices"][0]["message"]["content"])
        for response in responses
    ]
