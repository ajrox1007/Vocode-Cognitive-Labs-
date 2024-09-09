from fastapi import FastAPI, Request
import openai

openai.api_key = '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'

app = FastAPI()

def generate_code(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a highly advanced coding assistant that generates high-quality code snippets "
                        "based on detailed user requests. Your goal is to create efficient, modular, well-documented, "
                        "and error-handled code. You should also follow industry best practices for the given "
                        "programming language, including clean code principles, maintainability, and performance optimization. "
                        "If the task is ambiguous, you must make reasonable assumptions."
                    )
                },
                {
                    "role": "user", 
                    "content": (
                        f"Task: {prompt}.\n\n"
                        "Please generate the code to complete the above task. "
                        "Make sure to follow these guidelines:\n"
                        "1. The code should be efficient and optimized for performance.\n"
                        "2. Include modular functions or classes where appropriate.\n"
                        "3. Ensure robust error handling and edge case considerations.\n"
                        "4. Follow best practices for the specific programming language, including proper naming conventions.\n"
                        "5. Provide meaningful comments to explain key sections of the code.\n"
                        "6. If applicable, ensure the code is scalable and easy to maintain."
                    )
                }
            ],
            max_tokens=15000  # Adjust this based on the expected size of the code
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
