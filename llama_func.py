import os
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, download_loader
from llama_index import Document, LLMPredictor, PromptHelper, QuestionAnswerPrompt, JSONReader
from langchain.llms import OpenAIChat, OpenAI
from zipfile import ZipFile
from googlesearch import search as google_search
from baidusearch.baidusearch import search as baidu_search
import traceback
import openai

from utils import *

def save_index(index, index_name, exist_ok=False):
    file_path = f"./index/{index_name}.json"

    if not os.path.exists(file_path) or exist_ok:
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

def construct_index(api_key, file_list, index_name, max_input_size=4096, num_outputs=512, max_chunk_overlap=20, raw=False):
    documents = []
    if not raw:
        txt_set = []
        for file in file_list:
            if os.path.splitext(file.name)[1] == '.pdf':
                CJKPDFReader = download_loader("CJKPDFReader")
                loader = CJKPDFReader()
                documents += loader.load_data(file=file.name)
            elif os.path.splitext(file.name)[1] == '.docx':
                DocxReader = download_loader("DocxReader")
                loader = DocxReader()
                documents += loader.load_data(file=file.name)
            elif os.path.splitext(file.name)[1] == '.epub':
                EpubReader = download_loader("EpubReader")
                loader = EpubReader()
                documents += loader.load_data(file=file.name)
            else:
                with open(file.name, 'r', encoding="utf-8") as f:
                    txt_set.append(f.read())
                documents += [Document(k) for k in txt_set]
    else:
        documents += [Document(k.text.encode("UTF-8", errors="strict").decode()) for k in file_list]

    # Customizing LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=api_key))
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap)

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    if not raw:
        save_index(index, index_name)
        newlist = refresh_json_list(plain=True)
        return newlist, newlist
    else:
        save_index(index, index_name, exist_ok=True)
        return index

def chat_ai(api_key, index_select, question, prompt_tmpl, sim_k, chat_tone ,context, chatbot, search_mode=[], suggested_user_question = ""):
    os.environ["OPENAI_API_KEY"] = api_key
    print(f"Question: {question}")
    if question=="":
        question = suggested_user_question

    if chat_tone == 0:
        temprature = 2
    elif chat_tone == 1:
        temprature = 1
    else:
        temprature = 0.5

    if not search_mode:
        response = ask_ai(api_key, index_select, question, prompt_tmpl, sim_k, temprature, context)
    else:
        print(f"You asked: {question}")
        BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
        loader = BeautifulSoupWebReader()
        chat = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key)
        search_terms = chat.generate([f"Please extract search terms from the user’s question. The search terms is a concise sentence, which will be searched on Google to obtain relevant information to answer the user’s question, too generalized search terms doesn’t help. Please provide no more than two search terms. Please provide the most relevant search terms only, the search terms should directly correspond to the user’s question. Please separate different search items with commas, with no quote marks. The user’s question is: {question}"]).generations[0][0].text.strip()
        search_terms = search_terms.replace('"', '')
        search_terms = search_terms.replace(".", "")
        links = []
        for keywords in search_terms.split(","):
            keywords = keywords.strip()
            for search_engine in search_mode:
                if "Google" in search_engine:
                    print(f"Googling: {keywords}")
                    search_iter = google_search(keywords, num_results=5)
                    links += [next(search_iter) for _ in range(10)]
                if "Baidu" in search_engine:
                    print(f"Baiduing: {keywords}")
                    search_results = baidu_search(keywords, num_results=5)
                    links += [i["url"] for i in search_results if i["url"].startswith("http") and (not "@" in i["url"])]
                if "Manual" in search_engine:
                    print(f"Searching manually: {keywords}")
                    print("Please input links manually. (Enter 'q' to quit.)")
                    while True:
                        link = input("请手动输入一个链接：\n")
                        if link == "q":
                            break
                        else:
                            links.append(link)
        links = list(set(links))
        if len(links) == 0:
            msg = "No links found."
            print(msg)
            chatbot.append((question, msg))
            return context, chatbot, gr.Dropdown.update(choices=[])
        print("Extracting data from links...")
        print('\n'.join(links))
        documents = loader.load_data(urls=links)
        # convert to utf-8 encoding

        index = construct_index(api_key, documents, " ".join(search_terms.split(",")), raw=True)

        print("Generating response...")
        response = ask_ai(api_key, index_select, question, prompt_tmpl, sim_k, temprature, context, raw = index)
    response = response.split("\n")
    suggested_next_turns = []
    for index, line in enumerate(response):
        if "next user turn" in line:
            suggested_next_turns = response[index+1:]
            response = response[:index]
            break
    suggested_next_turns = [i.split()[1] for i in suggested_next_turns]
    response = "\n".join(response)
    response = parse_text(response)
    context.append({"role": "user", "content": question})
    context.append({"role": "assistant", "content": response})
    chatbot.append((question, response))
    os.environ["OPENAI_API_KEY"] = ""
    return context, chatbot, gr.Dropdown.update(choices=suggested_next_turns)



def ask_ai(api_key, index_select, question, prompt_tmpl, sim_k=1, temprature=0, prefix_messages=[], raw = None):
    os.environ["OPENAI_API_KEY"] = api_key
    if raw is not None:
        index = raw
    else:
        index = load_index(index_select)

    prompt = QuestionAnswerPrompt(prompt_tmpl)

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=temprature, model_name="gpt-3.5-turbo", openai_api_key=api_key, prefix_messages=prefix_messages))

    try:
        response = index.query(question, llm_predictor=llm_predictor, similarity_top_k=sim_k, text_qa_template=prompt)
    except:
        traceback.print_exc()
        return ""

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
