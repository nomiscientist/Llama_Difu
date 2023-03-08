import os
import gradio as gr
from zipfile import ZipFile

def refresh_json_list(plain=False):
    json_list = []
    for root, dirs, files in os.walk("./index"):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                json_list.append(os.path.splitext(file)[0])
    if plain:
        return json_list
    return gr.Dropdown.update(choices=json_list)

def upload_file(file_obj):
    files = []
    with ZipFile(file_obj.name) as zfile:
        for zinfo in zfile.infolist():
            files.append(
                {
                    "name": zinfo.filename,
                }
            )
    return files
