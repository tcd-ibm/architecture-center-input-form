FROM registry.redhat.io/ubi9/ubi:9.1.0-1750

WORKDIR /architecture-center-input-form

COPY . .

ENV PATH /architecture-center-input-form:$PATH
# update 
RUN yum -y update
# get install script and pass it to execute: 
RUN yum install -y python3 python3-pip vim npm sqlite
RUN pip3 install --no-cache-dir -r requirements.txt

RUN npm install -global yarn
RUN yarn install

EXPOSE 5297
EXPOSE 4621

CMD ["/bin/bash"]
# gunicorn app:app -b 0.0.0.0:5297 -w 8 -k uvicorn.workers.UvicornWorker & yarn dev