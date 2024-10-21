FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
#COPY telegram/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV UVICORN_CMD="uvicorn telegram.main:app --host 0.0.0.0 --port 8000"


EXPOSE 8000

CMD ["sh", "-c", "$UVICORN_CMD"]


#docker build -t bot -f telegram/Dockerfile .
#docker run -it --name bot bot