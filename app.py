from config import personalConfig
from openai import OpenAI
from pydf import Pdf

import gradio as gr
import json
import requests

class personalAssistant:
    pass

if __name__ == "__main__":
    assistant = personalAssistant()
    gr.ChatInterface(fn=assistant, inputs="text", outputs="text").launch()
    