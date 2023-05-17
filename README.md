# Architecture Center Input Form

Input form for Red Hat Architecture Center: https://www.redhat.com/architect/portfolio/

# Build and run the application with podman:

```bash
cd architecture-center-input-form-master

# Build the back-end and API
export APP_NAME=architecture-center
podman build . -t ${APP_NAME}
podman run --expose 5297 -p 5297:5297 --expose 4621 -p 4621:4621 --rm -it ${APP_NAME}:latest \
gunicorn app:app -b 0.0.0.0:5297 -w 8 -k uvicorn.workers.UvicornWorker

# Run the application with yarn
sudo npm install -g vite
npm i -D @types/node
yarn install
yarn dev
```
