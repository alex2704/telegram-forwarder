FROM python:3.8.5

EXPOSE 80
RUN mkdir -p opt/tgforwarder
WORKDIR /opt/tgforwarder

COPY . /opt/tgforwarder
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]