import gdata
from gdata.calendar import client
from bottle import route, run, debug, template, request, validate, error, response, redirect
import re
from datetime import date, timedelta

def matchOrEmpty(regex,text):
    match=regex.findall(text)
    text=match[0] if match else ''

    #remove any br tags
    text=re.compile("</?\w+\s*/?>").sub("",text)

    return text.strip()


def parseEntry(entry):
    d={}

    d["title"]=entry.title.text
    content=entry.content.text
    d["where"]= matchOrEmpty(re.compile("Where:(.*)"),content)
    d["when"]= matchOrEmpty(re.compile("When:(.*)"),content)
    d["description"]= matchOrEmpty(re.compile("Description:(.*)Link:",re.DOTALL),content)
    d["link"]= matchOrEmpty(re.compile("Link:(.*)"),content)

    return d

def monday2monday(near):
		#find the nearest sunday 
		#isoweekday 7 => sunday
		one_day=timedelta(days=1)
		while near.isoweekday() != 1:
			near=near+one_day
		#find the following one
		following_sunday=near+(7*one_day)
		return (near.strftime('%Y-%m-%d'),following_sunday.strftime('%Y-%m-%d'))


@route('/')
def redirect_to_closest_feed():
		closestWeek=monday2monday(date.today())
		print '/feed/%s/%s'%(closestWeek)
		redirect('/feed/%s/%s'%(closestWeek))

@route('/feed/:start/:end')
def show_feed(start,end):
    #we got the feed
    calendar_client = gdata.calendar.client.CalendarClient()
    feed_uri="https://www.google.com/calendar/feeds/l4ut8vep3q5ammqv91n205u3lc%40group.calendar.google.com/private-75b3611bd28055ede485cb6afd9380b9/basic"

    #for time
    query = gdata.calendar.client.CalendarEventQuery()
    query.start_min = start  #start_date "2007-06-26"
    query.start_max = end    #end_date "2007-07-01"

    feed = map(parseEntry,calendar_client.GetCalendarEventFeed(uri=feed_uri,q=query).entry)

    return template("feed.tpl",locals())

if __name__ =="__main__":
    debug(True)
    run(reloader=True)

