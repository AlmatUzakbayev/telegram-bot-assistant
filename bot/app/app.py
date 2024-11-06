from fastapi import FastAPI
from bot.chatgenerator import ask, voice_ask, image_ask
from bot.app.data import UserInput, UserVoiceInput, UserImageInput

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/chat/ask")
async def ask_endpoint(request: UserInput):
    bot_response = ask(request.user_input)
    return {"bot_response": bot_response}

@app.post("/chat/voice")
async def voice_endpoint(request: UserVoiceInput):
    bot_response = voice_ask(request.file_path)
    return {"bot_response": bot_response}

@app.post("/chat/image")
async def image_endpoint(request: UserImageInput):
    bot_response = image_ask(request.image_input)
    return {"bot_response": bot_response}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
