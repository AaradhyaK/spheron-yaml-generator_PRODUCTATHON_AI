# Spheron YAML Generator

This project provides a web-based tool to generate and validate YAML configurations for Spheron's Infrastructure Composition Language (ICL) from natural language inputs.

## Features
- Interactive UI for entering prompts
- NLP-based YAML generation
- Validation of generated YAML configurations
- Supports defining service, port, CPU, memory, and replica count

## Installation and Setup

### Frontend Setup
The frontend runs on localhost using Live Server.
1. Open the frontend folder.
2. Use a Live Server extension (such as the one in VS Code) to serve the files.

### Backend Setup
1. *Uncomment Hugging Face API Credentials:*
   - Navigate to backend/utils/huggingface.py.
   - Uncomment the token and URL for the Hugging Face API.

2. *Create a Virtual Environment:*
   - *Windows:*
     sh
     python -m venv venv
     
   - *Linux/macOS:*
     sh
     python3 -m venv venv
     

3. *Activate the Virtual Environment:*
   - *Windows:*
     sh
     venv\Scripts\activate
     
   - *Linux/macOS:*
     sh
     source venv/bin/activate
     

4. *Install Dependencies:*
   sh
   pip install -r requirements.txt
   

5. *Run the Backend:*
   sh
   uvicorn main:app --reload
   

## Usage
1. Start both the frontend (via Live Server) and the backend (via uvicorn).
2. Enter a natural language prompt describing the desired configuration.
3. The system will generate a YAML configuration specifying:
   - Service
   - Port
   - CPU allocation
   - Memory allocation
   - Number of replicas

## Repository
[GitHub Repository](https://github.com/AaradhyaK/spheron-yaml-generator_PRODUCTATHON_AI.git)
