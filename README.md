
# HSL API test

This is a simple Python script that takes a number and a list of stop names from the command line,
asks the HSL API for the next five departures from those stops, and outputs a bare-boned
HTML page with the departures organized in a table.

## Setup

Easiest would be with [Pipenv](https://pipenv.pypa.io/en/latest/).
Run `pipenv install` to install the dependencies from the `Pipfile`
and create a virtual environment for running the code.

But right now the only dependency is [requests](https://docs.python-requests.org/en/master/)
so you can just install that any other way and run the code.

Requires Python 3.6 or higher, I think. Only tested on 3.9 right now.

## Example

The file `example.html` in this repo was produced with the command line

```
pipenv run python timetable.py 5 Kalervonkatu Sumatrantie > example.html
```

It prints out the HTML page with the next 5 departures from these two stops combined.
