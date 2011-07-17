<!DOCTYPE HTML>
<html>
<head>
<title>Startup Digest Formatter</title>
  <style>
    textarea{
    width:90%;
		height:600px;
    overflow-x:auto;
    padding:10px;
    border:1px solid black;
    }
  </style>
</head>
<body>
  <h1>Calendar</h1>
<p><a href="../{{lastweek[0]}}/{{lastweek[1]}}">Last Week</a> | <a href="../{{nextweek[0]}}/{{nextweek[1]}}">Next Week</a></p>
<textarea>
%for evt in feed:
{{evt["title"]}}

When: {{evt["when"]}}
Where: {{evt["where"]}}
%if evt.has_key("short-link"):
%for link in evt["short-link"]:
More Info: {{link}}
%end
%end

{{evt["description"]}}

--

%end

</textarea>


  <div class="footer">
  <h3>SD Calendar Formatter</h3>
  </div>
</body>
</html>
