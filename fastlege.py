#Small script to get an email-alert when a spot opens up at your 'fastlege' providing a free alternative (for myself) to other overpriced services.

import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendMeAnEmailIfSpotOpensUp():

	fromaddr = "INSERT YOUR EMAIL ADDRESS"
	toaddr = "INSERT EMAIL ADDRESS TO SEND TO"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Open spot available"
 
	body = "A Spot just opened up for the doctor you want!"
	msg.attach(MIMEText(body, 'plain'))
 	
	#Settings for GMAIL. Change these settings for other email providers

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "YOUR PASSWORD")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def searchDoctor():

	r = requests.get('https://tjenester.nav.no/minfastlege/innbygger/fastlegesokikkepalogget.do?sok=S%F8k+etter+fastlege&fylke=11&kommune=1102')
	#The url to request changes based on fylke and kommune, the best way to find the right url is to do a google search for e.g 'fastlege Stavanger'

	r.content
	soup = BeautifulSoup(r.content)
	
	desired_doctor = soup.find(text="NAME OF DOCTOR") #Name of the Doctor you wish to set an alert for. Currently needs to be exactly the same as on the website.
	td_tag = desired_doctor.parent.parent
	tags = td_tag.find_all("td")
	name_and_availability = [tags[i] for i in (0, 9)] #Adding name and number of open spots to a new list.
	
	doctors_name = str(name_and_availability[0]) #Converting to String to make facilitate stripping of html tags
	open_spots = str(name_and_availability[1]) #Converting to String to make facilitate stripping of html tags
	
	doctors_name_redacted = re.sub(r'<.*?>', "", doctors_name) #Stripping html tags using regex
	open_spots_redacted = re.sub(r'<.*?>', "", open_spots) #Stripping html tags using regex

	spots_as_int = int(open_spots_redacted)

	print(doctors_name_redacted)

	if spots_as_int > 0:
		sendMeAnEmailIfSpotOpensUp() 
	else: print("No open spots")
	
searchDoctor()

