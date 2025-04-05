# BC2407-Dashboard
<p align="center">
  <a href="https://www.python.org/"><img alt="python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff"/></a>
  <a href="https://www.r-project.org/about.html#:~:text=Introduction%20to%20R,by%20John%20Chambers%20and%20colleagues."><img alt="R" src="https://img.shields.io/badge/R-%23276DC3.svg?logo=r&logoColor=white)"/></a>
  <a href="https://platform.openai.com/"><img alt="gpt" src="https://img.shields.io/badge/ChatGPT-74aa9c?logo=openai&logoColor=white"/></a>
  <a href="https://streamlit.io/"><img alt="streamlit" src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white"/></a>

</p>

## Installation

Open a terminal and run:

```bash
$ git clone https://github.com/Salttyy/BC2407-Dashboard.git
$ pip install -r requirements.txt
$ pip install streamlit
$ cd .\BC2407-Dashboard
$ python -m streamlit run Dashboard.py 
```
Personalize recommendation set up

```bash 
$ mkdir -p .streamlit
$ echo "[general]" > .streamlit/secrets.toml
$ echo "OPENAI_API_KEY = \"your-api-key-here\"" >> .streamlit/secrets.toml
```
