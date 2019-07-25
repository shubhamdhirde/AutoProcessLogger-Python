# AutoProcessLogger-Python  
This automation scripts takes snapshot of processes such as its name, PID, memory usage, thread count and number of child processes. scripts executes periodically by the time spacified by the user of script.  
After taking snapshot of processes it creates a log file and sends it to spacifed email address.    
## Important modules used  
1. psutil : iter_process() function is used to take snapshot of process
2. smtplib & email : To send attached log file to user
3. time : time.ctime is used to get currunt time for making log file
4. schedule : To schedule tasks in script    
## Usage  
$Script_name Dir_Name Time(Min) Reciever_Mail_Id    
###### Tip  
Turn on "Less secure apps on" senders gmail account.
