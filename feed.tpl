<!DOCTYPE HTML>
<html>
<head>
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

<textarea>
%for evt in feed:
{{evt["title"]}}

When: {{evt["when"]}}
Where: {{evt["where"]}}
More Info: {{evt["link"]}}

{{evt["description"]}}


%end

</textarea>


  <div class="footer">
  <h3>SD Calendar Formatter</h3>
  </div>
</body>
</html>
