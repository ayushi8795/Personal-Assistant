from config import personalConfig
from recordDetail import record_user_details_json, record_unknown_question_json
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr
import json
import requests

class personalAssistant:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Ayushi Agrawal"
        reader = PdfReader("resume/Ayushi_resume.pdf")
        self.resume = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text

    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, "
        f"particularly questions related to {self.name}'s career, background, skills and experience. "
        f"Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. "
        f"You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. "
        f"Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
        f"If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. "
        f"If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "
        system_prompt += f"\\n\n## resume Profile:\n{self.resume}\n\n"
        system_prompt += f"please chat with the user, always staying in character as {self.name} and with context to the resume provided."
        return system_prompt

    def chat(self,message,history):
        message = [{"role": "system", 
                    "content": self.system_prompt()}] + history + [{"role": "user", 
                                    "content": message}]
        tools = [{"type": "function", "function": record_user_details_json},
                 {"type": "function", "function": record_unknown_question_json}]

        response = self.openai.chat.completions.create(model=personalConfig.openai_model, messages=message, tools=tools)

        return response.choices[0].message.content

  


if __name__ == "__main__":
    assistant = personalAssistant()
    gr.ChatInterface(fn=assistant.chat).launch()
    