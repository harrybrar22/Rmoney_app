FROM python:3.8.5
COPY . /code
WORKDIR /code
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt 
