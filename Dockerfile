FROM nginx:1.25

WORKDIR /usr/share/nginx/html

COPY index.html .
COPY cspm/ cspm/
