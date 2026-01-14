import httpx

# URL of the local Ollama API
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
# Default LLM model to use
MODEL_NAME = "phi3:mini"


# Send a prompt to the Ollama LLM API and return the generated response
async def generate_response(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    # Use an async HTTP client to call the Ollama API
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        # Raise an exception if the API call fails
        response.raise_for_status()
        data = response.json()

    # Return only the model's text output
    return data["response"]
