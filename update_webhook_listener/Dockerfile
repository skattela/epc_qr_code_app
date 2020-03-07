FROM alpine:3.7

# install dependencies
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install flask

# update working directories
ADD . /app

CMD chmod +x app/deploy.sh
CMD python app/app.py