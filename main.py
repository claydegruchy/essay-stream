import shutil
from fastapi import UploadFile, File
from fastapi import FastAPI, HTTPException
from uuid import uuid4
from pydantic import BaseModel
from datetime import datetime
from typing import Literal
from models import TTSOptionsPublic
from pathlib import Path


path_base = "server/"

app = FastAPI()


class Job(BaseModel):
    id: str
    timestamp: datetime
    filename: str = None
    status: Literal['awiting_file', 'in_queue',
                    'in_progress', 'complete'] = "awiting_file"
    tts_options: TTSOptionsPublic


queue = []
jobs = {}


@app.post("/upload_file/{job_id}",)
async def upload_file(job_id: str, file: UploadFile):

    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    print("Run: upload_file")
    path = path_base+f"/files/{job_id}/"
    print("creating path", path)
    folder_path = Path(path)
    folder_path.mkdir(parents=True, exist_ok=True)
    filename = path+f"{file.filename}"
    print("Saving the uploaded file", filename)
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    jobs[job_id].filename = filename
    jobs[job_id].status = "in_queue"
    print(jobs[job_id])
    return jobs[job_id]


@app.post("/jobs")
async def submit_job(data: TTSOptionsPublic):

    print("Run: submit_job", data)
    job_id = str(uuid4())
    timestamp = datetime.now()

    # Create the job
    job = Job(id=job_id, timestamp=timestamp, tts_options=data)

    # Store job in jobs dictionary
    jobs[job_id] = job
    queue.append(job_id)

    return job


@app.get("/jobs/next")
def get_next_job():
    print("Run: get_next_job")
    if not queue:
        raise HTTPException(status_code=404, detail="No enqueued jobs")
    return jobs[queue[0]]


@app.post("/jobs/{job_id}/{action}")
def update_job(job_id: str, action: str):
    print("Run: update_job")
    print("job_id", job_id, "action", action)

    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    if action not in {"start", "complete", "fail"}:
        raise HTTPException(status_code=400, detail="Invalid action")

    jobs[job_id]["status"] = "in_progress" if action == "start" else action
    if action in {"complete", "fail"}:
        queue.remove(job_id)
    return jobs[job_id]


@app.get("/jobs")
def list_jobs(status: Literal['in_queue', 'in_progress', 'complete']):
    print("Run: list_jobs")
    print("status", status, )
    return [job for job in jobs.values() if not status or job["status"] == status]
