FROM python:3.10.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

# COPY wait-for-it.sh /wait-for-it.sh
# RUN chmod +x /wait-for-it.sh
# ENTRYPOINT ["./wait-for-it.sh","db:3306", "--", "echo", "up"]

CMD python manage.py runserver 0.0.0.0:8000