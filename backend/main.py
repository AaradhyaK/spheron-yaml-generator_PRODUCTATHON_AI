from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.yaml_generator import generate_yaml
from services.validator import validate_yaml
from utils.huggingface import get_nlp_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allow only your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

class UserInput(BaseModel):
    prompt: str

@app.post("/generate_yaml")
async def generate(user_input: UserInput):
    try:
        # Get response from Hugging Face NLP model
        nlp_response = get_nlp_response(user_input.prompt)

        # Generate YAML using the response from the NLP model
        generated_yaml = generate_yaml(nlp_response)

        # Validate the generated YAML
        is_valid, error_message = validate_yaml(generated_yaml)

        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)

        return {"yaml": generated_yaml}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

