# Llama_difu —— Llama Do it for You

A Web-UI for [Llama_index](https://github.com/jerryjliu/gpt_index) (gpt_index).
![image](https://user-images.githubusercontent.com/70903329/223749069-4aec7f09-7ff9-4fe5-9958-945cf2f64909.png)

## Feature

- [X] Allow ChatGPT to access your own database
- [x] New Google: like new Bing, but uses Google!
- [X] Simple Query
- [X] Simple Construct index (Only support GPTSimpleVectorIndex now)
- [X] Customize prompt template
- [X] Customize PromptHelper
- [X] .json View
- [x] Chat
- [ ] More files supprot
- [ ] More LLMPredictor
- [ ] More Index methods

## Usage

**Clone this repo**

```bash
git clone https://github.com/MZhao-ouo/Llama_difu.git
cd Llama_difu
```

**Install dependencies**

```bash
pip install requirements.txt
```

**Run**

```bash
python main.py
```

## New Google

Check the "Search Google" checkbox, the chatbot will search the web for you and generate contents based on that. Just like the New Bing, but uses Google! 

It's recommended to use the Balanced or Precise mode when using New Google.

<img width="1129" alt="image" src="https://user-images.githubusercontent.com/51039745/223800748-d48d0c32-844a-4476-b155-702db17d11c9.png">
<img width="615" alt="image" src="https://user-images.githubusercontent.com/51039745/223800850-ce590512-811f-45c5-8e48-ff12cda43b2d.png">

