
# HSL API test

This is a simple Python script that takes a number and a list of stop names from the command line,
asks the HSL API for the next five departures from those stops, and outputs a bare-boned
HTML page with the departures organized in a table.

## Install

You need Python 3.6+ with [requests](https://docs.python-requests.org/en/master/).

To run it "properly", use [Pipenv](https://pipenv.pypa.io/en/latest/).
Run `pipenv install` to create a new virtualenv and install the dependencies (just `requests`…)
based on the `Pipfile`.

## Example

The file `example.html` in this repo was produced with the command line

```
pipenv run python timetable.py 5 Kalervonkatu Sumatrantie > example.html
```

It prints out the HTML page with the next 5 departures from these two stops combined.

If you're not using Pipenv, just omit the `pipenv run`, as long as you're in a
Python 3.6+ environment with `requests` installed.
