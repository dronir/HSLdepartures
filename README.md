
# HSL API test

This is a simple Python script that takes a list of stop names from the command line,
asks the HSL API for the next five departures from those stops, and outputs a bare-boned
HTML page with the departures organized in a table.

## Example

The file `example.html` in this repo was produced with the command line

```
$ python timetable.py Kalervonkatu Sumatrantie > example.html
```
