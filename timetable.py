import requests
import logging
from pprint import pformat
from string import Template
from sys import argv
from datetime import datetime, timedelta
from itertools import islice

from html_templates import HTML_HEADER, HTML_FOOTER, HTML_ROW_TEMPLATE
REQUEST_TEMPLATE = Template(open("request_template.txt", "r").read())
URL = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
UTC_OFFSET = timedelta(hours=3)

logging.basicConfig(level=logging.WARN)

def get_stop_departures(name, N=1):
    """HTTP request for the next N departures from given stop.
    """
    query = REQUEST_TEMPLATE.substitute(ID=name, N=N)
    logging.debug(f"Making GraphQL query:\n{query}")
    r = requests.post(URL, headers={"Content-Type" : "application/graphql"}, data=query)
    return r.json()


def parse_departures(data):
    """Parse response JSON into (timestamp, HTML string) pairs.
    """
    departure_list = data["data"]["stops"][0]["stoptimesWithoutPatterns"]
    return [parse_html(json) for json in departure_list]


def parse_html(json):
    """Make HTML string out of departure JSON.
    """
    scheduled, realtime = get_timestamp(json)
    name = json["trip"]["route"]["shortName"]
    headsign = json["headsign"]
    stop = json["stop"]["name"]
    time = scheduled.strftime("%H:%M")
    # Add note if the bus is more than a minute late
    if abs(scheduled - realtime) > timedelta(minutes=1):
        note = "Estimated: {}".format(realtime.strftime("%H:%M"))
    else:
        note = ""
    return scheduled, HTML_ROW_TEMPLATE.substitute(time=time, name=name, stop=stop,
                                                   headsign=headsign, note=note)


def get_timestamp(departure):
    """Get scheduled/realtime departure datetimes from JSON.
    """
    day_start_unix = departure['serviceDay']
    scheduled_time = departure['scheduledDeparture']
    real_time = departure['realtimeDeparture']
    datetime_scheduled = datetime.utcfromtimestamp(day_start_unix + scheduled_time)
    datetime_realtime = datetime.utcfromtimestamp(day_start_unix + real_time)
    return datetime_scheduled + UTC_OFFSET, datetime_realtime + UTC_OFFSET


def main():
    N = int(argv[1])
    stops = argv[2:]
    print(HTML_HEADER)
    
    Departures = []
    for stop_name in stops:
        raw_data = get_stop_departures(stop_name, N)
        logging.debug(f"Received response:\n{pformat(raw_data)}")
        Departures += parse_departures(raw_data)
    
    for timestamp, html in islice(sorted(Departures), N):
        print(html)

    print(HTML_FOOTER)

if __name__=="__main__":
    main()