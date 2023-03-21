FROM python:3.10.9-bullseye

WORKDIR /servidor

COPY . /servidor

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8888/tcp
EXPOSE 8080/udp

CMD ["python","__init__.py"]