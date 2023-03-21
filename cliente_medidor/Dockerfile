FROM python:3.10.9-bullseye

WORKDIR /clienteMedidor

COPY . /clienteMedidor

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python","__init__.py"]