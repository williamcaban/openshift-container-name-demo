FROM python:3

LABEL AUTHOR="William Caban"

ENV APP_VERSION v1 
ENV APP_MESSAGE "Demo Container Default Message"

WORKDIR /usr/src/app
ENV APP_CONFIG=/usr/src/app/config.py

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080

USER 10001

CMD [ "gunicorn", "wsgi","-b","0.0.0.0:8080" ]

#
# END OF FILE
#