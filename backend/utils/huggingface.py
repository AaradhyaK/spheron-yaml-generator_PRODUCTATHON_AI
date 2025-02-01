import requests

# HF_API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
# HF_API_TOKEN = "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"

def get_nlp_response(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": prompt}

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        # Return the original prompt from the payload
        return prompt
    else:
        raise Exception(f"Error with Hugging Face API: {response.text}")
