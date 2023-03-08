# Llama_difu —— Llama Do it for You

A Web-UI for [Llama_index](https://github.com/jerryjliu/gpt_index) (gpt_index).
![image](https://user-images.githubusercontent.com/70903329/223749069-4aec7f09-7ff9-4fe5-9958-945cf2f64909.png)

## Feature

- [X] Allow ChatGPT to access your own database
- [X] Simple Query
- [X] Simple Construct index (Only support GPTSimpleVectorIndex now)
- [X] Customize prompt template
- [X] Customize PromptHelper
- [X] .json View
- [ ] Chat
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

**Caution**
The OpenAI API Key at the top of the webpage is currently not working. Please fill it in `main.py`.
![image](https://user-images.githubusercontent.com/70903329/223749763-d67a3265-41db-442f-a68d-8ce95ebf9d1c.png)
