FROM python:3.13.4-slim-bullseye

# Create python virtual env
# isolate our python app and installs from system-level python
RUN python -m venv /opt/venv/
ENV PATH=/opt/venv/bin:$PATH

WORKDIR /app

# COPY local_folder/file container_destination
COPY requirements.txt /tmp/requirements.txt
# RUN within container while building
RUN  pip install -r /tmp/requirements.txt

COPY ./src .


CMD ["python", "-m", "http.server", "8000"]