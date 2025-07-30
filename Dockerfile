# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

# Install pip requirements
COPY requirements.txt .

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install numpy==1.26.4 spacy
RUN python -m pip install -r requirements.txt
RUN python -m nltk.downloader stopwords punkt_tab
RUN apt-get -qq update
RUN apt-get -qq -y install curl

WORKDIR /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT bash
