FROM docker.io/python:3.11
LABEL authors="aiquen"

RUN groupadd -g 1000 webgroup
RUN useradd -d /app -m -r -s /bin/nologin -g webgroup -u 1000 webuser

COPY --chown=1000:1000 main.py requirements.txt /app/
USER webuser

RUN pip3 install -r /app/requirements.txt

WORKDIR /app
EXPOSE 8080

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
