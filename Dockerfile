FROM registry.access.redhat.com/ubi9/ubi:9.1.0-1750

WORKDIR /architecture-center-input-form

COPY . .

ENV PATH /architecture-center-input-form:$PATH
# update 
RUN yum -y update
# get install script and pass it to execute: 
RUN yum install -y python3 python3-pip vim npm sqlite
RUN pip3 install --no-cache-dir -r requirements.txt

RUN npm install -g npm@9.6.2

RUN npm install -global yarn
RUN yarn install

RUN chmod +x start.sh

EXPOSE 5297
EXPOSE 4621

CMD start.sh
# gunicorn app:app -b 0.0.0.0:5297 -w 8 -k uvicorn.workers.UvicornWorker & yarn dev