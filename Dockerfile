FROM hypriot/rpi-python
RUN apt-get update
RUN apt-get -y install build-essential libffi-dev libssl-dev
RUN apt-get install -y ca-certificates && update-ca-certificates
ENV PYTHONUNBUFFERED=0
WORKDIR /opt/lorcan/
ADD ./requirements.txt /opt/lorcan/
RUN pip install -r requirements.txt
ADD ./gpio.py /opt/lorcan/
CMD python /opt/lorcan/gpio.py
