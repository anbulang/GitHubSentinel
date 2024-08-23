# src/llm.py

import os
import openai
import socket
import socks


class LLM:
    def __init__(self, api_key=None):
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
        socket.socket = socks.socksocket
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def generate_daily_report(self, markdown_content):
        prompt = f"Please summarize the following project updates into a formal daily report:\n\n{markdown_content}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
