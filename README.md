# Live Bus Map for Your Wall

Dublin Bus publishes an API which can be queried to show how long it will be
before the next bus will arrive at a stop. Many of the busier bus stops have
signs that will show you this information while you wait.

My local bus stop doesn't have this info, and I'm pretty lazy¹ in the
mornings. So I built a live map showing buses that were approaching my local
bus stop.

![Photo of picture frame with a light showing the location of a bus, hung on the wall
in a hallway](https://raw.githubusercontent.com/lorcanmcdonald/buses/master/images/FrontDoor.jpg)

This project was inspired by the [People in Space
Indicator](https://projects.raspberrypi.org/en/projects/people-in-space-indicator),
a cute project which lights up an LED for every person currently in space,
right now. However I realised that a Raspberry PI Zero W is small enough to
fit into an [IKEA RIBBA picture
frame](https://www.ikea.com/ie/en/p/ribba-frame-white-00378403/).

I used the [Real-time Passenger Information (RTPI)
API](https://data.gov.ie/dataset/real-time-passenger-information-rtpi-for-dublin-bus-bus-eireann-luas-and-irish-rail)
to retrieve the data

¹ Too lazy to use the
[Dublin Bus App](https://www.dublinbus.ie/Your-Journey1/Mobileapps/) or
[Website](https://www.dublinbus.ie/RTPI/) apparently…
