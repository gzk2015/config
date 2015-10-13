#!/usr/bin/python
import smtplib
import MySQLdb
import MySQLdb.cursors
import os
from  datetime import date,timedelta
from email.mime.text import MIMEText 

#change dir to script root dir
os.chdir('/root/bin/log_report')

#delete last time report file
os.system('rm -f /root/bin/log_report/report.txt')


date_list=[date.today()-timedelta(days=7),date.today()-timedelta(days=6),date.today()-timedelta(days=5),date.today()-timedelta(days=4),date.today()-timedelta(days=3),date.today()-timedelta(days=2),date.today()-timedelta(days=1)]
report=file('/root/bin/log_report/report.txt','w')
 

def mailto(rec_list,mail_content):

    sender=-.com'
    smtpserver='.com'
    user='guanzhongkai'
    passwd=''
    content = file(mail_content ).read()
    msg=MIMEText(content,'plain')
    msg['From']=sender
    msg['Subject']="PV last week of Mobile-BU"
    msg['To']=",".join(rec_list)
    smtp=smtplib.SMTP()
    smtp.connect('','')
    smtp.starttls()
#    smtp.set_debuglevel(1)
    smtp.login(user,passwd)
    smtp.sendmail(sender,rec_list,msg.as_string())
    smtp.quit()




try:
    conn=MySQLdb.connect(host='10.59.94.80',user='gtuser',passwd='7475sys',db='gtsys',port=3306,charset='utf8',cursorclass=MySQLdb.cursors.DictCursor)
    cur=conn.cursor()


    cmd="select datetime,log_name,sum(pv) as sum  from log_analyze where log_name like %s and datetime=%s group by log_name"


    h1=file('.head1','r').readlines()
    report.writelines(h1)
    for D in date_list:
        cur.execute(cmd,(".access%",D))
	res=cur.fetchall()	
	if res is  ():pass
	else:
	    v1_t=res[1]['sum']
	    v2_t=res[2]['sum']
	    v3_t=res[3]['sum']
	    total=v1_t+v2_t+v3_t
	    data= "%s      %d      %d      %d       %d      %d%%\n"  %(D,v1_t,v2_t,v3_t,total,v3_t*100/total)
	    report.write(data)
	    report.flush()
    
    report.writelines(file('.head2','r').readlines())
    for D in date_list:
	cur.execute(cmd,("m.com.access%",D))
	res1=cur.fetchall()
	data1="%s        %s\n" %(D,res1[0]['sum'])
#	print data1
	report.write(data1)
    
    report.writelines(file('.head3','r').readlines())
    for D in date_list:
	cur.execute(cmd,("jiong%",D))
	res2=cur.fetchall()
	if res2 is ():pass
	else:
	    data2="%s        %s\n" %(D,res2[0]['sum'])
	    report.write(data2)
    
    
    report.writelines(file('.head4','r').readlines())
    for D in date_list:
	cur.execute("select datetime,log_name,sum(pv) as sum  from log_analyze where datetime =%s and (log_name like %s or log_name like %s)   group by log_name",(D,'api.m.17173.com%','mobile.app%'))
	res3=cur.fetchall()
	
	data3="%s        %s\n" %(D,res3[0]['sum']+res3[1]['sum'])
	report.write(data3)
  
    cur.close()
    conn.close()

except MySQLdb.Error,e:
    print "mysql error %d:%s" %(e.args[0],e.args[1])

report.close()



if os.path.exists('report.txt'):

    mailto(['',''],'report.txt')

