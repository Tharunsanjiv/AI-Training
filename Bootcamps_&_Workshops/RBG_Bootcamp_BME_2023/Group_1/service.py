from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import shortuuid
import speech_recognition as sr

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def save_file_locally(filename: str, file: UploadFile) -> bool:
    async with aiofiles.open(filename, "wb") as f:
        audio_bytes = await file.read()
        await f.write(audio_bytes)
    return True

@app.post("/service")
async def process(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="File not uploaded.")
    
    extension = file.filename.split(".")[-1]
    filename = f"file_{shortuuid.ShortUUID().random(length=32)}.{extension}"
    
    await save_file_locally(filename=filename, file=file)
    
    # Your audio processing code here (e.g., converting to WAV, speech recognition)
    input_audio_file = filename
    output_wav_file = f"{filename}.wav"
    
    # Add your audio processing logic here
    
    return {"message": "Processing completed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7001)
