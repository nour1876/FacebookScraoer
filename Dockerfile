# Use the official Python base image
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev && apt-get install -y python3-dev && apt-get install -y build-essential && apt-get install -y postgresql-client && apt-get install -y postgresql-contrib && apt-get -y install uvicorn
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "facebookScraper:app", "--host", "0.0.0.0", "--port", "8000"]