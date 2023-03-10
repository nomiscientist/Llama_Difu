# Llama_difu —— Llama Do it for You

[![LICENSE](https://img.shields.io/github/license/MZhao-ouo/Llama_difu)](https://github.com/MZhao-ouo/Llama_difu/blob/main/LICENSE)
[![Web-UI](https://img.shields.io/badge/WebUI-Gradio-fb7d1a?style=flat)](https://gradio.app/)
[![base](https://img.shields.io/badge/Base-Llama_index-cdc4d6?style=flat&logo=github)](https://github.com/jerryjliu/gpt_index)

---

A Web-UI for [Llama_index](https://github.com/jerryjliu/gpt_index) (gpt_index). Allow ChatGPT to access your own content, even databases!

## Feature

- [X] Allow ChatGPT to access your own database
- [X] New Google: like new Bing, but uses Google!
- [X] Simple Query
- [X] Simple Construct index (Only support GPTSimpleVectorIndex now)
  - [X] support .txt, .pdf, .docx, .epub
- [X] Customize prompt template
- [X] Customize PromptHelper
- [X] .json View
- [X] Chat
- [X] Multi-files support
- [ ] More LLMPredictor
- [ ] More Index methods

## Screenshot

**Ask Mode**
![image](https://user-images.githubusercontent.com/70903329/224219711-b2ff45d7-7584-479b-9ddf-0e44a42a93b1.png)

**New Google**

Check the "Search Google" checkbox, the chatbot will search the web for you and generate contents based on that. Just like the New Bing, but uses Google!

It's recommended to use the Balanced or Precise mode when using New Google.

![image](https://user-images.githubusercontent.com/70903329/224219722-92f0d8b9-3100-4009-95b9-5d406d3d951f.png)

**Construct your own index**
![image](https://user-images.githubusercontent.com/70903329/224219727-725d865d-a3fb-40a9-ba6f-8bc2e3448d15.png)

## Usage

**Clone this repo**

```bash
git clone https://github.com/MZhao-ouo/Llama_difu.git
cd Llama_difu
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Run**

```bash
python main.py
```
