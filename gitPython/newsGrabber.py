# Import libraries
import requests
from bs4 import BeautifulSoup
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# import urllib library
from urllib.request import urlopen
  
# import json
import json
x = datetime.datetime.now()

date_time = x.strftime("%d/%m/%Y")
print("date and time:",date_time)
year = (x.year)
day = (x.day)
month = (x.month)

daily_quote = "https://zenquotes.io/api/today"
daily_image = "https://api.unsplash.com/photos/random/?count=1&client_id=EovFwCmVrYYWtx6Hu7_2rUHk6oH3JW8KtvAJ6fjXPmA"
response_quote = urlopen(daily_quote)
response_img = urlopen(daily_image)
data_json_quote = json.loads(response_quote.read())
data_json_img = json.loads(response_img.read())
print(data_json_img[0]['urls']['regular'])
daily_got_img = data_json_img[0]['urls']['regular']

daily_got_quote = (data_json_quote[0]['q'])

# URL from which pdfs to be downloaded
url = "https://www.pdf247.org/p/the-hindu-epaper.html"

# Requests URL and get response object
response = requests.get(url)

# Parse text obtained
soup = BeautifulSoup(response.text, 'html5lib')

# Find all hyperlinks present on webpage
links = soup.find_all('a')

i = 0
urltodownload = ''
# From all links check for pdf link and
# if present download file
for link in links:
    if ('https://drive.google.com' in link.get('href', [])):
        i += 1
        print("Downloading file: ", i)

        # Get response object for link
        response = requests.get(link.get('href'))
        urltodownload = link.get('href')

        # Write content in pdf file
        pdf = open("The_Hindu_"+str(month)+"_"+str(day)+"_"+str(year)+".pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
        print("File ", i, " downloaded")

print("All PDF files downloaded")
download_date = str(month)+"_"+str(day)+"_"+str(year)
email = 'minnadailynews@outlook.com'
password = 'Jesusislove@6724'
send_to_email = ['binwinviju225096@gmail.com', 'tjminna@gmail.com']
subject = 'Minna Daily News on '+date_time
message = """\
<html>
  <head></head>
  <body>
    <div style="text-align:center; padding:20px; font-family: sans-serif; background-image:linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('{dailygot_img}'); background-repeat: no-repeat; background-attachment: fixed; background-size: cover; color:rgb(255, 255, 255) !important; -webkit-text-fill-color: rgb(255, 255, 255) !important; ">
        <h1>Daily News</h1>
        <div>
            <p>Good Morning<br><br><b>{daily_got_quote}</b><br><br>Please find the daily
            news paper attached to this mail on - {datetime}. <br><br>
            <a href="{urltodownload}">Download Now!</a>
            <br><br><br><br><b>Thanks and Regards</b><br>Minna Daily News
            </p>
        </div>
    </div>
  </body>
</html>
""".format(dailygot_img=daily_got_img, daily_got_quote=daily_got_quote, datetime=date_time, urltodownload=urltodownload)
file_location = '/Users/binwinviju/Desktop/Scripts/NewsPaper/'
files = ["The_Hindu_"+download_date+".pdf"]

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = ", ".join(send_to_email)
msg['Subject'] = subject
erroMsg=[]
isError = 'false'
msgEr = ''
# Setup the attachment
for f in files:
    try:
        filename = os.path.basename(file_location+f)
        print(filename)
        attachment = open(file_location+f, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
    except Exception as ex:
        error = ex
        erroMsg.append(msgEr)
        pass
msgEr = """\
         <div style="text-align:center; padding:20px; min-height:500px; font-family: sans-serif; background-image:linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://cdn.dribbble.com/users/3556928/screenshots/8726854/glitch-trial.gif'); background-repeat: no-repeat; background-attachment: fixed; background-size: 100% 100%; color:rgb(255, 255, 255) !important; -webkit-text-fill-color: rgb(255, 255, 255) !important; ">
       <p>Sorry no link for News Paper found!</p>
        </div>
        """
if isError == 'false':
    message1 = '<br><br><b>Thanks and Regards,</b><br>Minna Daily News'
    print(len(urltodownload))
    if(len(urltodownload) == 0):
        msg.attach(MIMEText(msgEr, 'html'))
    else:
        msg.attach(MIMEText(message, 'html'))



# Attach the attachment to the MIMEMultipart object


server = smtplib.SMTP('smtp.office365.com',587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()  