import requests
from pprint import pprint
from string import Template
from sys import argv
from datetime import datetime, timedelta

from html_templates import HTML_HEADER, HTML_FOOTER, HTML_ROW_TEMPLATE
REQUEST_TEMPLATE = Template(open("request_template.txt", "r").read())
URL = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
UTC_OFFSET = timedelta(hours=3)

def get_stop_departures(stopID, N=1):
    "Get the next N departures from given stop as JSON."
    data = REQUEST_TEMPLATE.substitute(ID=stopID, N=N)
    r = requests.post(URL, headers={"Content-Type" : "application/graphql"}, data=data)
    return r.json()

def get_timestamp(departure):
    "Get scheduled/realtime departure datetimes from JSON."
    day_start_unix = departure['serviceDay']
    scheduled_time = departure['scheduledDeparture']
    real_time = departure['realtimeDeparture']
    datetime_scheduled = datetime.utcfromtimestamp(day_start_unix + scheduled_time)
    datetime_realtime = datetime.utcfromtimestamp(day_start_unix + real_time)
    return datetime_scheduled + UTC_OFFSET, datetime_realtime + UTC_OFFSET

def parse_departures(data):
    "Parse response JSON into HTML strings indexed by timestamps."
    departure_list = data["data"]["stops"][0]["stoptimesWithoutPatterns"]
    times_and_html = [parse_html(json) for json in departure_list]
    Departures = [(timestamp, html) for (timestamp, html) in times_and_html]
    return Departures

def parse_html(json):
    "Make HTML string out of departure JSON."
    scheduled, realtime = get_timestamp(json)
    name = json["trip"]["route"]["shortName"]
    headsign = json["headsign"]
    stop = json["stop"]["name"]
    time = scheduled.strftime("%H:%M")
    if abs(scheduled - realtime) > timedelta(minutes=1):
        note = "Estimated: " + realtime.strftime("%H:%M")
    else:
        note = ""
    return scheduled, HTML_ROW_TEMPLATE.substitute(time=time, name=name, stop=stop,
                                                   headsign=headsign, note=note)
    
def main():
    stops = [int(n) for n in argv[1:]]
    print(HTML_HEADER)
    
    Departures = []
    for stop in stops:
        data = get_stop_departures(stop, 5)
        Departures += parse_departures(data)
    for timestamp, html in sorted(Departures):
        print(html)
    print(HTML_FOOTER)

if __name__=="__main__":
    main()