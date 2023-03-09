FROM python:3.10

RUN mkdir -p /code
WORKDIR /code
COPY . .
RUN pip install -U pip
RUN pip install -r requirements.txt
CMD [ "python", "main.py", "# LOAD_TEST AAREKUHA" ]
