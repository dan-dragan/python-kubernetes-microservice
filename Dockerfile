FROM python:3.9.13
RUN apt-get update -y && apt-get install -y python3-pip

# get curl for healthchecks
RUN apt-get install -y curl

WORKDIR /usr/src/app
COPY requirements.txt ./


# Copy the current directory contents into the container at /app
ADD ./services ./services
ADD ./database ./database
ADD requirements.txt .
ADD pip.conf .
RUN mkdir -p /etc/app/cfg

RUN pip install --no-cache-dir -r requirements.txt


# Define environment variable
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PIP_CONFIG_FILE pip.conf
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
ENV FLASK_APP=services/user.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE $FLASK_RUN_PORT

#CMD ["flask", "run"]
#CMD ["python", "services/user.py"]
CMD ["gunicorn", "-w", "3", "-t", "60", "-b", "0.0.0.0:5000", "services.user:app"]
