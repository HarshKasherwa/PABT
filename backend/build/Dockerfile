FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt install sysvbanner

WORKDIR /home/pabt

RUN pip install --upgrade pip

COPY ./backend .

RUN pwd

RUN ls -l

RUN pip install -r /home/pabt/build/requirements.txt

RUN chmod +x "/home/pabt/build/entrypoint.sh"

# Set the entrypoint
ENTRYPOINT exec "/home/pabt/build/entrypoint.sh"