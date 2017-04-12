from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
import RPi.GPIO as GPIO
import time
import datetime
import signal
import sys

print "Starting buses"

GPIO.setmode(GPIO.BCM)

stops = [ "510", "509", "4518", "1485" ]
pins = [ 5, 6, 13, 19 ]


def signal_handler(signal, frame):
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def get_next_due(stops):
	stop_results = {}
	for stop_id in stops:
		endpoint = "https://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation?stopid=%s&routeid=123&format=json" % stop_id

		session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))

		bus_stop_future = session.get(endpoint, verify=False)
		stop_results[stop_id] = bus_stop_future
		
	stop_data = { stop_id: r.result().json() for stop_id, r in stop_results.items() }

	output = {}

	for stop_id, datum in stop_data.items():
		results = datum["results"]
		results.sort(key=lambda x: x["scheduledarrivaldatetime"])
		for i, r in enumerate(results):
			bus_id = "%s-%s" % (r["route"], i)
			
			due = r["duetime"]
			if bus_id in output:
				output[bus_id].append((due, stop_id))
			else:
				output[bus_id] = [ (due, stop_id) ]



	output = { k: min(times, key = lambda t: t[0]) for k, times in output.items()}

	result = {}

	for _, (due, stop_id) in output.items():
		if due == "Due":
			due = 0
		if stop_id in result and due < result[stop_id]:
			result[stop_id] = due
		elif not stop_id in result:
			result[stop_id] = due

	result = { s: "flashing" if (int(d) < 6 and s == "510")  else "on" for s, d in result.items() }

	default_result = {
		"510": "off",
		"509": "off",
		"4518": "off",
		"1485": "off"
	}
	default_result.update(result)
	return default_result

def rotate(l, n):
    return l[-n:] + l[:-n]

stop_details = {}

for p in range(0, len(pins)):
	GPIO.setup(pins[p], GPIO.OUT)
	stop_details = get_next_due(stops)

last_checked = datetime.datetime.now()
flashing = 1

while True:
	flashing = flashing * -1

	now = datetime.datetime.now()
	if (now - last_checked).total_seconds() > 0.00010:
		stop_details = get_next_due(stops)
		last_checked = now
	for p in range(0, len(pins)):
		stop = stops[p]
	
		detail = stop_details[stop]
		
		value = GPIO.LOW
		if detail == "on":
			value = GPIO.HIGH
		elif detail == "flashing" and flashing > 0:
			value = GPIO.HIGH

		GPIO.output(pins[p], value)
		last_checked = datetime.datetime.now()

	time.sleep(0.065)
