import gradio as gr
import os

from llama_func import *
from utils import *

os.environ['OPENAI_API_KEY'] = ""

def reset_textbox():
    return gr.update(value='')

with gr.Blocks() as llama_difu:
    api_key = gr.Textbox(label="OpenAI API Key", value="", type="password")
    chatContext = gr.State([])

    with gr.Tab("Ask"):
        with gr.Box():
            gr.Markdown("**Select index**")
            with gr.Row():
                with gr.Column(scale=12):
                    index_select = gr.Dropdown(choices=refresh_json_list(plain=True), show_label=False).style(container=False)
                with gr.Column(scale=1):
                    index_refresh_btn = gr.Button("🔄Refresh Index List")
        with gr.Box():
            with gr.Column():
                gr.Markdown("## Ask")
                with gr.Column():
                    with gr.Accordion("Advance", open=False):
                        prompt_tmpl = gr.Textbox(placeholder="Prompt Template", value="Context information is below.\n----------\n{context_str}\n----------\nGiven the above context answer the following question. Answer in bullet points.\n\nQuestion: {query_str}",
                                                 label="prompt_tmpl")
                    query_box = gr.Textbox(lines=3, show_label=False).style(container=False)
                query_btn = gr.Button("🚀", variant="primary")
        with gr.Box():
            gr.Markdown("## Result")
            answer = gr.Markdown("")

    with gr.Tab("Chat"):
        chat_tone = gr.Radio(["Creative", "Balanced", "Percise"], label="Chatbot Tone", type="index", value="Balanced")
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(scale=12):
                chat_input = gr.Textbox(show_label=False, placeholder="Type here...").style(container=False)
            with gr.Column(min_width=50, scale=1):
                chat_submit_btn = gr.Button("🚀", variant="primary")


    with gr.Tab("Construct"):
        with gr.Row():
            with gr.Column():
                upload_file = gr.File()
                with gr.Row():
                    max_input_size = gr.Slider(256, 4096, 4096, step=1, label="Max Input Size", interactive=True, show_label=True)
                    num_outputs = gr.Slider(256, 4096, 512, step=1, label="Num Outputs", interactive=True, show_label=True)
                with gr.Row():
                    max_chunk_overlap = gr.Slider(0, 100, 20, step=1, label="Max Chunk Overlap", interactive=True, show_label=True)
                    chunk_size_limit = gr.Slider(256, 4096, 512, step=1, label="Chunk Size Limit", interactive=True, show_label=True)
                new_index_name = gr.Textbox(placeholder="New Index Name", show_label=False).style(container=False)
                construct_btn = gr.Button("Construct", variant="primary")
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        with gr.Column(scale=7):
                            json_select = gr.Dropdown(choices=refresh_json_list(plain=True), show_label=False, multiselect=False).style(container=False)
                        with gr.Column(scale=1):
                            json_refresh_btn = gr.Button("🔄Refresh Index List")
                    json_confirm_btn = gr.Button("🔎View json")
                    json_display = gr.JSON(label="View index json")

    index_refresh_btn.click(refresh_json_list, None, [index_select])
    query_btn.click(ask_ai, [api_key, index_select, query_box, prompt_tmpl], [answer])
    chat_input.submit(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, chat_tone, chatContext, chatbot], [chatContext, chatbot])
    chat_input.submit(reset_textbox, [], [chat_input])
    chat_submit_btn.click(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, chat_tone, chatContext, chatbot], [chatContext, chatbot])
    chat_submit_btn.click(reset_textbox, [], [chat_input])
    construct_btn.click(construct_index, [api_key, upload_file, new_index_name, max_input_size, num_outputs, max_chunk_overlap], [index_select, json_select])
    json_confirm_btn.click(display_json, [json_select], [json_display])

if __name__ == '__main__':
    llama_difu.queue().launch()
