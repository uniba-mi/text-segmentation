# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

# Install pip requirements
COPY requirements.txt .

RUN python -m pip install -r requirements.txt
RUN python -m nltk.downloader stopwords punkt_tab

WORKDIR /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT bash
