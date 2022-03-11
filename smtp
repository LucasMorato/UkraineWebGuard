import smtplib
import email.message


msg = email.message.Message()
msg['Subject'] = 'I found VULNERABILITIES in your site!'
sender = 'your_email@gmail.com'

#Get emails from emails.txt
efile = "emails.txt"
emailFile = open(efile, 'r')
emailsLines = emailFile.readlines()
rez = []
for zx in emailsLines:
    rez.append(zx.replace("\n", ""))

recipients = rez
msg['From'] = sender
msg['To'] = ", ".join(recipients)


password = "your_password"
s = smtplib.SMTP('smtp.gmail.com: 587') # change here if you aren't using gmail
email_content = """
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

</head>

<body>

<p>Hi! Hope all is well out there!</p>

<p>In order to defend your nation, I use a script to find vulnerability in your country's websites.</p>

<p>I am sending you this message to let you know that I have found flaws and vulnerabilities on your site and would like to warn you to protect yourself.</p>

<p>Do not hesitate to contact me if you are interested in knowing what vulnerabilities your site has. <br>
I have a text file called vulns.txt where are all the faults found and I can send it to you at any time for correction, JUST ANSWER ME THIS EMAIL.</p>

<p>I wish God protect you and your nation!<br>
All my support.</p>

</body>
</html>


"""


msg.add_header('Content-Type', 'text/html')

msg.set_payload(email_content)


s.starttls()
s.login(msg['From'], password)
s.sendmail(sender, recipients, msg.as_string())
