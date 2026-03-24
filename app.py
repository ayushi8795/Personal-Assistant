from config import personalConfig
from recordDetail import record_user_details_json, record_unknown_question_json, record_user_details, record_Unkonwn_questions
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
       system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
        particularly questions related to {self.name}'s career, background, skills and experience. \
        Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
        You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
        Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
        If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
        If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "
       system_prompt += f"\\n\n## resume Profile:\n{self.resume}\n\n"
       system_prompt += f"please chat with the user, always staying in character as {self.name} and with context to the resume provided."
       return system_prompt
    
    def handle_tool_calls(self,tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)

            # THE BIG IF STATEMENT!!!

            if tool_name == "record_user_details":
                result = record_user_details(**arguments)
            elif tool_name == "record_unknown_question":
                result = record_Unkonwn_questions(**arguments)

            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    

    def chat(self,message,history):
        messages = [{"role": "system", 
                    "content": self.system_prompt()}] + history + [{"role": "user", 
                                    "content": message}]
        tools = [{"type": "function", "function": record_user_details_json},
                 {"type": "function", "function": record_unknown_question_json}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model=personalConfig.openai_model, messages=messages, tools=tools)
            finished_reason = response.choices[0].finish_reason
            print(finished_reason)
            if finished_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_calls(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True

        return response.choices[0].message.content

  


if __name__ == "__main__":
    assistant = personalAssistant()
    gr.ChatInterface(fn=assistant.chat).launch()
    