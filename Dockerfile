FROM python:3.7
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install gunicorn
ADD requirement.txt .
RUN pip install -r requirement.txt
ADD . .
EXPOSE $PORT
CMD gunicorn -b 0.0.0.0:$PORT app:app