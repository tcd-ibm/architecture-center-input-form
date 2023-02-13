# architecture-center-input-form
Input form for Red Hat Architecture Center

run with docker:   
```bash
cd architecture-center-input-form-master
docker build . -t {some_name}
docker run --expose 5297 -p 5297:5297 --expose 4621 -p 4621:4621 --rm -it {some_name}:latest
gunicorn app:app -b 0.0.0.0:5297 -w 8 -k uvicorn.workers.UvicornWorker & yarn dev
```