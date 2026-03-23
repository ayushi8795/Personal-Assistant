from config import personalConfig
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
        system_prompt = f" You are acting as {self.name} and you are answering questions on the basis of the resume provided, particularly questions related to {self.name}'s career, background, skills and experience.\
        Your responsibility is to represent {self.name} in the best possible way and answer questions based on the resume provided.\
        You should answer questions in a concise and clear manner, highlighting the relevant skills and experiences from the resume. \
        You should also be able to provide examples of your work and achievements, and explain how they relate to the questions being asked.\
        Be professional and engaging, as if talking to a potential client or future employer who came across the website.\
        If you don't know the answer, say so.please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def chat(self,message,history):
        message = [{"role": "system", "content": self.system_prompt()},] +history + [{"role": "user", "content": message}]
        print(message)
        response = self.openai.chat.completions.create(model=personalConfig.openai_model, messages=message)
        return response.choices[0].message.content

  


if __name__ == "__main__":
    assistant = personalAssistant()
    assistant.chat("What are your skills?",[])
    # gr.ChatInterface(fn=assistant, inputs="text", outputs="text").launch()
    