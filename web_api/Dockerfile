FROM orderinds/ubuntu-python3.7:latest
MAINTAINER westwind3122@hotmail.com # 維護者

# COPY flask_exam /usr/src/app/flask_exam/
ADD ./flask_exam /usr/src/app/flask_exam/
WORKDIR /usr/src/app/flask_exam/
RUN pip3 install -r requirements.txt 
RUN pip3 install https://projects.unbit.it/downloads/uwsgi-lts.tar.gz
CMD ["uwsgi", "--ini", "uwsgi.ini"]
# CMD ["python3", "/usr/src/app/flask_exam/start.py"]