from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from openai import OpenAI
from dotenv import load_dotenv
import aiofiles
import os
import base64

load_dotenv()
app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/transcribe/")
async def transcribe_and_generate_audio(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    temp_file_path = f"/tmp/{file.filename}"
    async with aiofiles.open(temp_file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    with open(temp_file_path, "rb") as audio_file:
        client = OpenAI(api_key=OPENAI_API_KEY)
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    os.remove(temp_file_path)  # Cleanup

    user_text = transcription.text

    chat_response = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=[
            {"role": "system", "content": "Please respond casually in English."},
            {"role": "user", "content": user_text}
        ]
    )
    text_response = chat_response.choices[0].message.content
    audio_base64 = chat_response.choices[0].message.audio.data

    audio_bytes = base64.b64decode(audio_base64)
    audio_output_path = f"/tmp/output.wav"
    with open(audio_output_path, "wb") as audio_file:
        audio_file.write(audio_bytes)

    file_path = "/tmp/output.wav"

    # Return the .wav response
    return FileResponse(
        path=file_path,
        media_type="audio/wav",  # Indicates that the file is a WAV audio file
        filename="audio.wav"     # Optional: suggests a filename for the client
    )