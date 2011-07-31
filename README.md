#StartUp Digest Quicky

Format events for startup digest from a google calendar feed

use:

`$ pip install -r requirements.txt`

to resolve requirements

##TODO
 * add check for multiday events
 * add functionality to 'approve' event, which updates it with result as description and moves it to production cal
 

##TODONE:
 * ~~Bug: SDq crashes when trying to bit.ly a bit.ly, which will hereafter be reffered to as the 'Xibit Bug'~~
 * ~~can only assign one value to 'link', need room for multiple links to display~~
 * ~~get dotcloud deployment working~~
 * ~~change when format to to weekday month day from time to time (Tue Jul 5 from 6pm to 8pm)~~
 * ~~change rendering of apostrophes from &#39; to '~~
 * ~~banished regexes~~ 
 * ~~fixed descrition bug~~
 * ~~shorten links with bit.ly~~
 * ~~order events by date~~
 * ~~handle missing link~~
 * ~~flip by week through listings~~
