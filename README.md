# BRANDit AI Campaign Command Center
## Maldives India Edition

A clean Streamlit prototype created as an additional AI-based submission for the AI Transformation Associate assignment at BRANDit.

## What it demonstrates

- Campaign brief input for Maldives Tourism in the Indian market
- AI-assisted campaign strategy generation
- Social media content planning with reels, hooks and captions
- PR story angle and pitch generation
- Ready-to-attach submission note

The interface has been simplified to focus only on Strategy, Content and PR outputs. It does not show API tokens or model status in the UI.

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Add your Hugging Face token inside `.env` only:

```bash
HUGGINGFACEHUB_API_TOKEN=your_token_here
HF_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
USE_AI=true
```

## Prepared by

Kalpanasingh Chauhan  
+91 8850159663  
chauhankalpana2020@gmail.com
