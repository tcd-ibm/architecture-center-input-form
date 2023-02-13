# architecture-center-input-form
Input form for Red Hat Architecture Center

`gunicorn app:app -b 0.0.0.0:5297 -w 8 -k uvicorn.workers.UvicornWorker & yarn dev`