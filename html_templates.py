from string import Template

HTML_ROW_TEMPLATE = Template("""  <tr>
    <td class='time'>$time</td>
    <td class='route'>$name</td>
    <td class='headsign'>$headsign</td>
    <td class='stop'>$stop</td>
    <td class='note'>$note</td>
  </tr>""")

HTML_HEADER = """<html>
<head>
  <title>Example timetable</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<table>
<th>
<td>Line</td>
<td>Destination</td>
<td>Stop</td>
<td>Notes</td>
</th>
"""


HTML_FOOTER = """
</table>
</body>
</html>
"""