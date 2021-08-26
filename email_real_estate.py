import smtplib, ssl
import sys
from craiglist_scrapper import data
import smtplib
import getpass

to_adress = sys.argv[2]
from_address = sys.argv[1]
daily = True if sys.argv[3] == 'daily' else False
password = sys.argv[4]

html = f"""\
        <html>
          <head>These are the properties found:</head>
            <body>
                {data(daily)}
            </body>
        </html>
        """
if __name__ == '__main__':
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_address, password)
    server.sendmail(from_address, to_address, html)
    server.quit()
