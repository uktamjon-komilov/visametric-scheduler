FROM python:3.9.6-alpine3.14

WORKDIR /home/user/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade setuptools pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /home/user/web/entrypoint.sh
RUN chmod +x /home/user/web/entrypoint.sh

RUN apk add chromium
RUN apk add chromium-chromedriver

COPY . .

ENTRYPOINT ["/home/user/web/entrypoint.sh"]