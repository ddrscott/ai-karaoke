from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from spleeter.separator import Separator
import os
from pydub import AudioSegment

app = FastAPI()

# Ensure output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

@app.post("/mp3/")
async def create_karaoke(file: UploadFile = File(...)):
    try:
        # Determine file extension
        file_extension = file.filename.split(".")[-1]

        # Save the uploaded file
        input_path = os.path.join(output_dir, f"input.{file_extension}")
        with open(input_path, "wb") as audio:
            audio.write(await file.read())

        # Convert to wav if necessary (spleeter works best with wav)
        if file_extension != "wav":
            sound = AudioSegment.from_file(input_path)
            input_path_wav = os.path.join(output_dir, "input.wav")
            sound.export(input_path_wav, format="wav")
            input_path = input_path_wav

        # Use Spleeter to separate vocals and instruments
        separator = Separator('spleeter:2stems')
        separator.separate_to_file(input_path, output_dir)

        # Assuming the output filename follows Spleeter's convention
        output_path = os.path.join(output_dir, "input", "vocals.wav")

        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Error processing the audio file.")

        return FileResponse(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
