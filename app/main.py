from fastapi import FastAPI, File, UploadFile
# from openai import OpenAI
# import aiofiles
# import os

app = FastAPI()
#client = OpenAI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/transcribe")
# async def transcribe_text(file: UploadFile = File(...)):
    
#     # Save file to temp storage
#     temp_file_path = f"/tmp/{file.filename}"
    
#     async with aiofiles.open(temp_file_path, "wb") as f:
#         content = await file.read()
#         await f.write(content)
    
#     audio_file= open(temp_file_path, "rb")
#     transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

#     # clears temp storage (for input file)
#     os.remove(temp_file_path)
    
#     return {"transcription": transcription}

# @app.post("/translate")
# async def translate_text():
#     pass

# @app.post("/respond")
# async def respond_to_user():
#     pass