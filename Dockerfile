FROM python:3.8

EXPOSE 3003

WORKDIR /usr/src/app

RUN pip install gTTS
RUN pip install Flask
RUN pip install apscheduler

RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get -y install nodejs

# COPY client ./client
# COPY server ./server
COPY . .

WORKDIR /usr/src/app/client

RUN npm install
RUN npm run build

WORKDIR /usr/src/app

CMD [ "python", "./server/index.py" ]