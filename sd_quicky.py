import gdata
from gdata.calendar import client
from bottle import route, run, debug, template, request, validate, error, response, redirect
import re
from datetime import date, timedelta, datetime
import bitly
import feed.date.rfc3339

BITLY_LOGIN="sdbaltimore"
BITLY_API="R_3677d6826fab742f02f027226dff3d2c"
BITLY=bitly.Api(login=BITLY_LOGIN,apikey=BITLY_API)


def matchOrEmpty(regex,text):
    match=regex.findall(text)
    text=match[0] if match else ''

    #remove any br tags
    text=re.compile("</?\w+\s*/?>").sub("",text)

    return text.strip()


def parseEntry(entry):
    d={}
    d["title"]=entry.title.text
    starttime = entry.when.pop(0).start
    timestamp = feed.date.rfc3339.tf_from_timestamp(starttime)
    d["when"]=datetime.fromtimestamp(timestamp)
    d["where"]=entry.where.pop(0).value
    content=entry.content.text
    if "Link:" in content:
        d["description"]= matchOrEmpty(re.compile("(.*)Link:",re.DOTALL),content)
        #look for a link in the body
        try:
            d["link"]= matchOrEmpty(re.compile("Link:(.*)"),content)

            #try to shorten link, fall back to regular link
            d["short-link"]=d["link"]
            try:
                d["short-link"]=BITLY.shorten(d["link"])
            except:
                pass
        except:
            #if we don't find one, go on
            pass
    else:
        d["description"]=content

    return d

def monday2monday(near):
    #gcal api uses inclusive start date, exclusive end date
    #find the nearest monday => isoweekday 1
    one_day=timedelta(days=1)
    while near.isoweekday() != 1:
        near=near+one_day
    #find the following one
    following_sunday=near+(7*one_day)
    return (near.strftime('%Y-%m-%d'),following_sunday.strftime('%Y-%m-%d'))


@route('/')
def redirect_to_closest_feed():
    closestWeek=monday2monday(date.today())
    redirect('/feed/%s/%s'%(closestWeek))

@route('/feed/:start/:end')
def show_feed(start,end):
    #we got the feed
    calendar_client = gdata.calendar.client.CalendarClient()
    feed_uri="https://www.google.com/calendar/feeds/l4ut8vep3q5ammqv91n205u3lc%40group.calendar.google.com/private-75b3611bd28055ede485cb6afd9380b9/full?orderby=starttime&sortorder=ascending"

    #for time
    query = gdata.calendar.client.CalendarEventQuery()
    query.start_min = start  #start_date "2007-06-26"
    query.start_max = end    #end_date "2007-07-01"

    feed = map(parseEntry,calendar_client.GetCalendarEventFeed(uri=feed_uri,q=query).entry)

    #find out next/prev week start/end
    week_start=datetime.strptime(start, '%Y-%m-%d')
    nextweek=monday2monday(week_start+timedelta(days=7))
    lastweek=monday2monday(week_start-timedelta(days=7))

    return template("feed.tpl",locals())

if __name__ =="__main__":
    debug(True)
    run(reloader=True)

