import os
import sys
import time
import psutil
import smtplib
import schedule
import urllib.request
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def ProcessLogger(log_dir):
    
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    if not os.path.isdir(log_dir):
        print("Given directive name is not directive")

    listProcess = []

    checkTime = time.ctime()
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict() 
            pinfo = proc.as_dict(attrs= ['pid','name','username'])
            
            vms = round(proc.memory_info().vms / (1014 * 1024),2)  # convert to mb
            pinfo["vms"] = vms
            listProcess.append(pinfo)
        except:
            pass

    # create log file
    separator = "-" * 80
    log_path = os.path.join(log_dir,f"ProLogger {checkTime}.log")
    fp = open(log_path, "w")
    fp.write(separator+"\n")
    fp.write(f"ProLogger: {checkTime} \n")
    fp.write(separator+"\n")
    fp.write("\n")

    # print all process info
    for element in listProcess:
        fp.write(f"{element}\n")
    
    fp.close()
    return log_path

## To check internet connection is there or not
def isConnection():
    try:
        urllib.request.urlopen(url = 'http://216.58.192.142',timeout = 4)
        return True

    except urllib.error.URLError:
        return False

## Send mail 
def SendMail(SEND_TO, subject, body, LOG_PATH):
    
    # checking connection
    connection = isConnection()
    if not connection:
        print("There is no internet connection\n")
        return
    
    GMAIL_USER = "xyz.com" #Sender EmailId here
    GMAIL_PASSWORD = "**********" #Sender password here

    #  Forming MIME mail
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = SEND_TO
    msg['Subject'] = subject
    
    # Body
    # 1. attach text
    msg.attach( MIMEText(body,'plain'))
    # 2 attach document
    with open(LOG_PATH, 'rb') as fp:#file
        attachment = MIMEBase('application','octet-stream')
        attachment.set_payload(fp.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=LOG_PATH)
    msg.attach(attachment)

    # SENDING MAIL via SMPT server
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login( GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER,SEND_TO, msg.as_string())
        server.close()
        print("Mail sent successfully")
    except Exception:
        print(f"Error: Unable to send mail")

# Periodic task
def StartTask():
    log_path = ProcessLogger(sys.argv[1])
    print("Log file created")
    send_to = sys.argv[3]
    subject = "Running Process Log"
    body = f'''
    Hello, {send_to}
        
        Attached document contains Log of running processes.
        This is auto generated mail. Do not reply.
        
        Thanks and Regards,
        Shubham Dhirde
    '''
    # send the mail
    SendMail(send_to,subject,body,log_path)

def main():
    # Filter of help and usage
    if len(sys.argv) < 2:
        print("ProLogger_Error: Invalid Parameter")
        exit()

    #Help
    if sys.argv[1] == '-h' or sys.argv[1] == '-H':
        print("ProLogger_Help: Automation script to take scapshot of running process")
        exit()

    # Usage
    if sys.argv[1] == '-u' or sys.argv[1] == '-U':
        print(f"ProLogger_Usage: {sys.argv[0]} Directory_Name Sender_Mail_ID Time_Interval(min)")
        print("Directory_Name : Directory which may contains duplicate files.")
        print("Time_Interval  : Time interval of script in minutes.")
        print("Sender_Mail_ID : Mail ID of the receiver.")
        exit()
    
    if len(sys.argv) != 4:
        print("ProLogger_Error: Invalid Parameter")
        exit()

    try:
        min = int(sys.argv[2])
        schedule.every(min).minutes.do(StartTask)
        
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as err:
        print(f"err{err}")
        pass

if __name__ == "__main__":
    main()