FROM python:3.12

# katalog roboczy w workerze
WORKDIR /app

#aktualizyjemy system w kontenerze | -y potwierdza automatycznie | && od razu wykonuje
RUN apt -y update && apt install -y \
    python3-dev \
    apt-utils \
    build-essential \
&& rm -rf /var/lib/apt/lists/*

#każdy run to osobna warstywa, więc lepiej zrobić to w jednym poleceniu

RUN pip3 install --upgrade setuptools
RUN pip3 install cython

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn -w 3 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT

# docker build -t app-1 .