from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from spleeter.separator import Separator
import os
import subprocess
from textwrap import dedent
import logging

app = FastAPI()

@app.get("/")
async def read_root():
    return FileResponse('public/index.html', media_type="text/html")

@app.post("/mp3/")
async def create_karaoke(file: UploadFile = File(...)):
    try:
        # Create a temporary directory to store the output files
        output_dir = os.path.join(os.getcwd(), "output")

        os.makedirs(output_dir, exist_ok=True)

        _, base_name, ext = split_path(file.filename)

        src_path = os.path.join(output_dir, file.filename)

        # write the file to disk
        with open(src_path, "wb") as f:
            f.write(await file.read())

        # Use Spleeter to separate vocals and instruments
        separator = Separator('spleeter:2stems')
        separator.separate_to_file(src_path, output_dir)
        # wait for things to finish
        separator.join()

        # Assuming the output filename follows Spleeter's convention
        vocal_path = os.path.join(output_dir, base_name, "vocals.wav")
        accompaniment_path = os.path.join(output_dir, base_name, "accompaniment.wav")

        if not os.path.exists(vocal_path) or not os.path.exists(accompaniment_path):
            raise HTTPException(status_code=500, detail="Error processing the audio file.")


        mp3_path = os.path.join(output_dir, base_name + "-karaoke.mp3")
        merge = dedent(f"""ffmpeg -y -i '{vocal_path}'
           -i '{accompaniment_path}'
           -filter_complex '[0:a]aformat=channel_layouts=mono,pan=stereo|c0=c0[left]; [1:a]aformat=channel_layouts=mono,pan=stereo|c1=c0[right]; [left][right]amix=inputs=2:duration=first:dropout_transition=3[a]'
           -map '[a]'
           -ac 2  '{mp3_path}'
        """).replace('\n', ' ')

        # use ffmpeg to convert the accompaniment to mp3# Execute the command
        with subprocess.Popen(merge, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
            # Iterate over the output lines
            for line in process.stdout:
                print(line, end='')
        return FileResponse(path=mp3_path, filename=base_name + ".mp3", media_type="audio/mpeg")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))

def split_path(path):
    base_dir, filename = os.path.split(path)
    base_name, ext = os.path.splitext(filename)
    return base_dir, base_name, ext
