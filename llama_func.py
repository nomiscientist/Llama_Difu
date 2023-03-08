import os
import llama_index
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from llama_index import Document, LLMPredictor, PromptHelper, QuestionAnswerPrompt, JSONReader
from langchain.llms import OpenAIChat
from zipfile import ZipFile

from utils import *

def save_index(index, index_name):
    file_path = f"./index/{index_name}.json"

    if not os.path.exists(file_path):
        index.save_to_disk(file_path)
        print(f'Saved file "{file_path}".')
    else:
        i = 1
        while True:
            new_file_path = f'{os.path.splitext(file_path)[0]}_{i}{os.path.splitext(file_path)[1]}'
            if not os.path.exists(new_file_path):
                index.save_to_disk(new_file_path)
                print(f'Saved file "{new_file_path}".')
                break
            i += 1

def construct_index(api_key, tmp_file, index_name, max_input_size=4096, num_outputs=512, max_chunk_overlap=20):
    # directory_path = f"./data/{directory_name}"
    documents_set = []
    # for root, dirs, files in os.walk(directory_path):
    #     for file in files:
    #         with open(os.path.join(root, file), 'r', encoding="utf-8") as f:
    #             documents_set.append(f.read())
    # documents = [Document(k) for k in documents_set]
    with open(tmp_file.name, 'r', encoding="utf-8") as f:
        documents_set.append(f.read())
    documents = [Document(k) for k in documents_set]

    # Customizing LLM
    llm_predictor = LLMPredictor(llm=OpenAIChat(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=api_key))
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap)

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    save_index(index, index_name)

    newlist = refresh_json_list(plain=True)
    return newlist, newlist

def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    firstline = False
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="{items[-1]}">'
                firstline = True
            else:
                lines[i] = f'</code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("&", "&amp;")
                    line = line.replace("\"", "`\"`")
                    line = line.replace("\'", "`\'`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("#", "&#35;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                lines[i] = "<br>"+line
    text = "".join(lines)
    return text

def chat_ai(api_key, index_select, question, prompt_tmpl, chat_tone ,context, chatbot):
    if chat_tone == 0:
        temprature = 2
    elif chat_tone == 1:
        temprature = 1
    else:
        temprature = 0.5
    response = ask_ai(api_key, index_select, question, prompt_tmpl, context, temprature=temprature)
    response = parse_text(response)
    context.append({"role": "user", "content": question})
    context.append({"role": "assistant", "content": response})
    chatbot.append((question, response))
    return context, chatbot



def ask_ai(api_key, index_select, question, prompt_tmpl, prefix_messages=[], temprature=0):
    os.environ["OPENAI_API_KEY"] = api_key
    index = load_index(index_select)

    prompt = QuestionAnswerPrompt(prompt_tmpl)

    llm_predictor = LLMPredictor(llm=OpenAIChat(temperature=temprature, model_name="gpt-3.5-turbo", openai_api_key=api_key, prefix_messages=prefix_messages))
    try:
        response = index.query(question, llm_predictor=llm_predictor, similarity_top_k=3, text_qa_template=prompt)
    except Exception as e:
        print(e)

    print(f"Response: {response.response}")
    os.environ["OPENAI_API_KEY"] = ""
    return response.response


def load_index(index_name):
    index_path = f"./index/{index_name}.json"
    if not os.path.exists(index_path):
        return None

    index = GPTSimpleVectorIndex.load_from_disk(index_path)
    return index

def display_json(json_select):
    json_path = f"./index/{json_select}.json"
    if not os.path.exists(json_path):
        return None
    documents = JSONReader().load_data(f"./index/{json_select}.json")

    return documents[0]
