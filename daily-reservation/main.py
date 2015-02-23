#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Author: Lukas Kisza
# Credits: stackoverflow.com, Github
#
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import db
import webapp2
import time
import urllib

testCalendar = 'lcdh8ftqlonl8m0h8u7uiqomjg@group.calendar.google.com'
class UserPrefs(db.Model):
	userid = db.StringProperty()
	email = db.StringProperty()
	name = db.StringProperty()
	calendar = db.StringProperty()
	arival = db.StringProperty()
	departure = db.StringProperty()
	cssURL = db.StringProperty()
	price_per_day = db.StringProperty()
	currency = db.StringProperty()

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		self.response.out.write('<html><head><meta name="description" content="Free daliy resetvation ordering online system based on published google calendar. Setup your daily ordering system in less than 10 minutes!" /><meta name="keywords" content="daily reservation, hotel reservation system, daily reservation system, reservation system, inteligent daily reservation, all day events, google calendar, google daily reservation, google app engine," /> </head><body>');
		if user:
			q = db.GqlQuery("SELECT * FROM UserPrefs WHERE userid = :1", user.user_id())
			userprefs = q.get()
			if userprefs:
				self.response.out.write('Welcome back, %s! (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
				
				self.response.out.write('<script>function deleteCalendar(key){var r=confirm("Delete calendar " + key.id);if (r==true){window.location.assign("./deleteCalendar?key=" + key.id)}}</script>')
				for myCalendar in q.run(limit=50):
					self.response.out.write('<br><br>%s - %s <input type="button" value="Delete" id="%s" onclick="javascript:deleteCalendar(this);">' % (myCalendar.name, myCalendar.calendar, myCalendar.key()))
					calendar_url = '%scalendar?%s|%s|%s|%s|%s|%s|%s' % (self.request.url, myCalendar.key(), myCalendar.calendar, myCalendar.arival, myCalendar.departure, myCalendar.price_per_day, myCalendar.currency, myCalendar.cssURL)
					iframe_html = '<iframe width="630" height="375" frameborder="1" scrolling="no" marginheight="0" marginwidth="0" src="%s"></iframe>' % calendar_url
					iframe_encoded = iframe_html.replace('<','&lt;').replace('>','&gt')
					self.response.out.write(' - (<a href="%s">Link to frame</a>)' % calendar_url)
					self.response.out.write('<br>%s<br>' % iframe_html)
					self.response.out.write('<textarea readonly="readonly" cols="90" rows="5">%s</textarea><br><br><br>' % iframe_encoded)
			else:
				self.response.out.write('Welcome new user, %s! (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
			self.response.out.write("""
				<h2>Add new calendar</h2>
				<form action="./addCalendar" method="post">
				<table>
				<tr><td>Calendar Name</td><td><input type="text" size="40" name="name" placeholder="My booking residence"></td></tr>
				<tr><td>Calendar ID</td><td><input type="text" size="60" name="calendar" placeholder="calendar-ID@group.calendar.google.com"></td></tr>
				<tr><td>Guest have to leave before</td><td><select name="departure"><option>6</option><option>7</option><option>8</option><option>9</option><option selected>10</option><option>11</option><option>12</option><option>13</option><option>14</option><option>15</option><option>16</option></select>(next day hour)</td></tr>
				<tr><td>Acccomodation start</td><td><select name="arival"><option>9</option><option>10</option><option>11</option><option>12</option><option>13</option><option>14</option><option selected>15</option><option>16</option><option>17</option><option>18</option><option>19</option><option>20</option><option>21</option></select>(hour)</td></tr>
				<tr><td>Price pre day</td><td><input type="text" size="5" name="name" placeholder="0 = none"></td></tr>
				<tr><td>Currency</td><td><input type="text" size="5" name="name" value="EUR"></td></tr>
				<tr><td>Design CSS URL</td><td><input type="text" size="40" name="cssURL" placeholder="http://link_to_custom.css leave blank for default"> * If defined, <a href="/default.css">default.css</a> will be replaced</td></tr>
				<tr><td colspan="2"><input type="submit" value="Add"></td></tr>
				</table></form>""")
		else:
			self.response.out.write('<a href="%s">Sign in (register)</a>.' % users.create_login_url('/'));
			self.response.out.write("""
				<h1>Free daliy resetvation ordering system based on published google calendar</h1>
				<p>Integrated with your gmail google calendar. Ideal for all day events such as accomodation or daily renting. Stable, but still beta version of free daily ordering system.</p>
				<h2>Showcase</h2>
				<iframe width="630" height="375" frameborder="1" scrolling="no" marginheight="0" marginwidth="0" src="./calendar?ahNzfmRhaWx5LXJlc2VydmF0aW9uchYLEglVc2VyUHJlZnMYgICAgIDDlQkM|lcdh8ftqlonl8m0h8u7uiqomjg@group.calendar.google.com|15|10|10|EUR|"></iframe>""")
		self.response.out.write("""<h2>How to use it</h2>
			<ol>
			<li>In <a href="https://www.google.com/calendar/render" target="_blank">Google calendar</a> click on "My Calendars" down arow and choose "Create new calendar" </li>
			<li>Name the calendar so you can easily identify it later</li>
			<li>Choose your country and your local time zone</li>
			<li>Set this calendar as public. Ensure to check "Show only free busy status/hide my details!"</li>
			<li>Once you save the calendar, it will appear in the list of your calendars</li>
			<li>Click on donw arow of newly created calendar and choose "Calendar settings"</li>
			<li>Note down your Calendar ID</li>
			<li>Log in to this free Daliy Resetvation Ordering System and add your calendar(s)</li>
			<li>Copy <i>&lt;iframe&gt;</i> to your page and enjoy</li>
			<li>Once someone submit your calendar reservation, you will receive email with summary information and direct confirmation link to your calendar</li>
			</ol>
			<p><img src="./img/publish_public_calendar.jpg"></p>
			<h2>Credits</h2>
			<p>Author: Lukas Kisza (kiszal@gmail.com) - <a href="http://www.lee.sk">LEE.sk</a></p>
			<p>Special thanks to: <a href="http://http://stackoverflow.com/">stackoverflow.com</a> and Google</p>
			<p>Download sources and participate at: <a href="https://github.com/lee-sk/daily-reservation/">https://github.com/lee-sk/daily-reservation</a></p>
			<h2>Bugs and things to do:</h2>
			<ul>
			<li>Add CAPTCHA to avoid SPAM (currently not needed)</li>
			<li>Add languages</li>
			<li>...any other ideas? Do not hesitate to contact me</li>
			</ul>
			<h2>Terms and conditions of usage</h2>
			<p>Service is provided as is without any waranty. Service is for free. We are not collecting any information from submitted forms. App is hosted on free google app engine, so please consider to host it on your own in case you expect more than 10 bookings/day. (free limit is 100 emails/day)</p></body></html>""")

class SaveHandler(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		if user and self.request.get('calendar'):
			entry = UserPrefs(userid=user.user_id(), email=user.email(), calendar=self.request.get('calendar'), cssURL=self.request.get('cssURL'), name=self.request.get('name'), arival=self.request.get('arival'), departure=self.request.get('departure'))
			entry.put()
			time.sleep(1)
		self.redirect('/')

class DeleteHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user and self.request.get('key'):
			q = db.Key(self.request.get('key'))
			if (user.user_id() == db.get(q).userid):
				db.delete(q)
				time.sleep(1)
		self.redirect('/')

class SubmitHandler(webapp2.RequestHandler):
	def post(self):
		try:
			calendar = db.get(db.Key(self.request.get('key')))
			senderName = self.request.get('name').encode("utf-8")
			senderEmail = self.request.get('email').encode("utf-8")
			senderPhone = self.request.get('phone').encode("utf-8")
			senderComment = self.request.get('comment').encode("utf-8")
			dateRange = self.request.get('dateRange')
			dateRangeFormated = '%s.%s.%s %s:00 - %s.%s.%s %s:00' % (dateRange[6:8], dateRange[4:6], dateRange[0:4], calendar.arival, dateRange[23:25], dateRange[21:23], dateRange[17:21], calendar.departure)
			url = 'https://www.google.com/calendar/render?action=TEMPLATE&src=%s&text=%s&dates=%s&details=%s+%s+%s&sf=true&output=xml&add=%s' % (calendar.calendar , urllib.quote_plus(senderName), dateRange, urllib.quote_plus(senderEmail), urllib.quote_plus(senderPhone), urllib.quote_plus(senderComment),urllib.quote_plus(senderEmail))
			email = """New booking request for %s
	Name: %s
	Email: %s
	Phone: %s
	Dates: %s
	Message: %s
	
Reservation confirmation link: %s

This email was automatically generated by Free Daliy Reservation System
Do not reply to this email (nobody will read it). You can mange your published calendars at http://daily-reservation.appspot.com.
Please report any inpropper behaviour to info@lee.sk""" % (calendar.name, senderName, senderEmail, senderPhone, dateRangeFormated, senderComment, url)
			self.response.out.write('Your reservation for %s was submited with folowing details<br>Name: %s<br>Email: %s<br>Phone: %s<br>Dates: %s LOCAL TIME<br>Message: %s' % (calendar.name, senderName, senderEmail, senderPhone, dateRangeFormated, senderComment))
			self.response.out.write("<br><br>Please wait for reservation confirmation email from %s owner" % calendar.name)
			if(int(time.strftime("%Y%m%d")) < int(dateRange[0:8])):
				mail.send_mail(sender='no-reply@daily-reservation.appspotmail.com', to=calendar.email, subject="New booking for %s" % calendar.name, body=email)
		except:
			self.response.out.write('Your reservation was NOT submited correctly<br>Please contact webmaster and try again later')

app = webapp2.WSGIApplication([
	('/', LoginHandler),('/addCalendar', SaveHandler),('/deleteCalendar', DeleteHandler),('/submitOrder', SubmitHandler)
], debug=True)
