<h1>Our Calendar</h1>

%for i,evt in enumerate(feed):

{{evt.title.text}}

When: {{re.compile("When:(.*)").findall(evt.content.text) }}
Where: {{re.compile("Where:(.*)").findall(evt.content.text) }}
More Info: http://bit.ly/jehJWW

In this salon, well discuss one of the most sticky issues our industry faces: delivering the design solutions we think are appropriate to clients and managers who disagree, dont want to invest the appripriate level of resources, or simply dont understand the difference between good enough design and great design.
