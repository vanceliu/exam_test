FROM jerryfage/ubuntu18.04-python3.7:latest

ADD ./flask_exam /usr/src/app/flask_exam/
WORKDIR /usr/src/app/flask_exam/
RUN apt install -y libpython3.7-dev
RUN pip3 install -r requirements.txt 
RUN pip3 install https://projects.unbit.it/downloads/uwsgi-lts.tar.gz
CMD ["uwsgi", "--ini", "uwsgi.ini"]
# CMD ["python3", "/usr/src/app/flask_exam/start.py"]