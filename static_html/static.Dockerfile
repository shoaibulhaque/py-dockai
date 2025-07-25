# declare what image to use
# FROM username/nginx:latest
# FROM image_name:latest

FROM python:3.13.4-slim-bullseye

WORKDIR /app

# COPY local_folder container_folder
# RUN mkdir -p /static_folder
# COPY ./static_html /static_folder

# same destination is /app
# COPY ./static_html /app
COPY ./src .

# RUN echo "hello" > index.html

# docker build -f Dockerfile -t pyapp .
# docker run -it pyapp


# docker build -f username/deploy-ai-app-test:latest
# docker push username/deploy-ai-app-test:latest

# docker build -f username/deploy-ai-app-test:v1
# docker push username/deploy-ai-app-test:v1

# python -m http.server 8000
# docker run -it -p 8080:8000
CMD ["python", "-m", "http.server", "8000"]