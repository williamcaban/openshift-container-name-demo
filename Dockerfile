FROM python:3.4
MAINTAINER William Caban

WORKDIR /usr/src/app
ENV APP_CONFIG=/usr/src/app/config.py

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

USER 10001

CMD [ "gunicorn", "wsgi","-b","0.0.0.0:5000" ]

#
# END OF FILE
#