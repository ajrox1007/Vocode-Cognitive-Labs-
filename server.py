from fastapi import FastAPI, Request
import openai

openai.api_key = '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'

app = FastAPI()

def generate_code(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that helps with coding."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=8000
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.AuthenticationError:
        print("Authentication Error: Please check your API key.")
        return None
    except openai.error.PermissionError:
        print("Permission Error: You do not have permission to perform this action.")
        return None
    except Exception as e:
        print(f"Error generating code: {e}")
        return None

@app.post("/command")
async def command(request: Request):
    data = await request.json()
    print(f"Received data: {data}")
    prompt = data.get('prompt', '')
    if prompt:
        code = generate_code(prompt)
        if code:
            return {"code": code}
        else:
            return {"error": "Code generation failed"}
    return {"error": "No prompt provided"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
