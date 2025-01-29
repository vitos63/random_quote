FROM python:3.12.5
ENV PYTHONUNBUFFERED 1
WORKDIR /random_quote
ADD ./random_quote .
COPY fixtures /app/fixtures
COPY . .
RUN pip install -r requirements.txt
