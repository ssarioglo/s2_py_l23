FROM python:3.10.9
SHELL ["/bin/bash", "-c"]
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt -y install python3-pip python3-evdev python3-xlib python3-six
RUN pip install --upgrade pip
RUN pip install pynput

RUN useradd -rms /bin/bash runner && chmod 777 /opt /run
WORKDIR /runner
COPY --chown=runner:runner . .

USER runner
CMD ["helicopter_game", "-it", "python3 main.py"]