FROM python:3.10.9
SHELL ["/bin/bash", "-c"]
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN apt update && apt -qy install libjpeg0dev libxslt-dev
RUN useradd -rms /bin/bash runner && chmod 777 /opt /run
WORKDIR /runner
COPY --chown=runner:runner . .

USER runner
CMD ["gunicorn", "-b", "0.0.0.0:8081", "soaqaz.wsgi.application"]