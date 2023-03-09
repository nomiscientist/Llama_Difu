import gradio as gr
import os

from llama_func import *
from utils import *
from presets import *

os.environ['OPENAI_API_KEY'] = ""

with gr.Blocks() as llama_difu:
    api_key = gr.Textbox(label="OpenAI API Key", value="", type="password")
    chat_context = gr.State([])
    new_google_chat_context = gr.State([])

    with gr.Tab("Ask"):
        with gr.Box():
            gr.Markdown("**Select index**")
            with gr.Row():
                with gr.Column(scale=12):
                    index_select = gr.Dropdown(choices=refresh_json_list(plain=True), show_label=False).style(container=False)
                with gr.Column(min_width=50, scale=1):
                    index_refresh_btn = gr.Button("🔄")
        with gr.Box():
            with gr.Column():
                gr.Markdown("## Ask")
                with gr.Column():
                    with gr.Accordion("Prompt Template", open=False):
                        sim_k = gr.Slider(1, 10, 1, step=1, label="Similarity", interactive=True, show_label=True)
                        tmpl_select = gr.Radio(prompt_tmpl_list, value="Default", label="pre-prompt-template", interactive=True)
                        prompt_tmpl = gr.Textbox(value=prompt_tmpl_dict["Default"], show_label=False)
                    query_box = gr.Textbox(lines=3, show_label=False).style(container=False)
                query_btn = gr.Button("🚀", variant="primary")
        with gr.Box():
            gr.Markdown("## Result")
            answer = gr.Markdown("")


    with gr.Tab("New Google"):
        with gr.Row():
            chat_tone = gr.Radio(["Creative", "Balanced", "Precise"], label="Chatbot Tone", type="index", value="Balanced")
            search_options_checkbox = gr.CheckboxGroup(label="Search Options", choices=["🔍 Search Google", "🔍 Search Baidu", "🔍 Manual Search"])
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(min_width=50, scale=1):
                chat_empty_btn = gr.Button("🧹", variant="secondary")
            with gr.Column(scale=12):
                chat_input = gr.Textbox(show_label=False, placeholder="Type here...").style(container=False)
            with gr.Column(min_width=50, scale=1):
                chat_submit_btn = gr.Button("🚀", variant="primary")
        suggested_user_turns = gr.Dropdown(choices=[], label="Suggested User Turns")


    with gr.Tab("Construct"):
        with gr.Row():
            with gr.Column():
                upload_file = gr.Files()
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
                        with gr.Column(min_width=50, scale=1):
                            json_refresh_btn = gr.Button("🔄")
                        with gr.Column(scale=7):
                            json_select = gr.Dropdown(choices=refresh_json_list(plain=True), show_label=False, multiselect=False).style(container=False)
                        with gr.Column(min_width=50, scale=1):
                            json_confirm_btn = gr.Button("🔎")
                    json_display = gr.JSON(label="View index json")

    index_refresh_btn.click(refresh_json_list, None, [index_select])
    query_btn.click(ask_ai, [api_key, index_select, query_box, prompt_tmpl, sim_k], [answer])
    tmpl_select.change(change_prompt_tmpl, [tmpl_select], [prompt_tmpl])

    chat_input.submit(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, chat_tone, chat_context, chatbot, search_options_checkbox, suggested_user_turns], [chat_context, chatbot, suggested_user_turns])
    chat_input.submit(reset_textbox, [], [chat_input])
    chat_submit_btn.click(chat_ai, [api_key, index_select, chat_input, prompt_tmpl, chat_tone, chat_context, chatbot, search_options_checkbox, suggested_user_turns], [chat_context, chatbot, suggested_user_turns])
    chat_submit_btn.click(reset_textbox, [], [chat_input])
    chat_empty_btn.click(lambda: ([], []), None, [chat_context, chatbot])

    construct_btn.click(construct_index, [api_key, upload_file, new_index_name, max_input_size, num_outputs, max_chunk_overlap], [index_select, json_select])
    json_confirm_btn.click(display_json, [json_select], [json_display])
    json_refresh_btn.click(refresh_json_list, None, [json_select])


if __name__ == '__main__':
    llama_difu.queue().launch()
