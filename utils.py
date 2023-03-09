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
