FROM nginx:1.25

RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /usr/share/nginx/html
