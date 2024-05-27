# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#构建邮件头
from email.header import Header
# 发信服务器
smtp_server = 'smtp.qq.com'
# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '308711822@qq.com'
password = 'xxxxxxxxxxxxxx'

def send_email(send_to_addr:str,contest_msg:str):
    # 连接发信服务器
    server = smtplib.SMTP_SSL(smtp_server)
    # 建立连接--qq邮箱服务和端口号
    server.connect(smtp_server, 465)
    # 登入邮箱
    server.login(from_addr, password)
    # 配置邮件正文内容

    msg = MIMEMultipart()
    msg['From'] = Header('小钟同学')    # 设置来自于邮件的发送者信息
    msg['To'] = Header('其他人同学')      # 设置来自于邮件的接收人信息
    msg['Subject'] = Header("用户注册通知", 'utf-8')  # 设置邮件主题
    # 邮件正文内容
    msg.attach(MIMEText(contest_msg, 'html', 'utf-8'))

    # 构造附件1，传送文本附件
    file_name = 'test1.txt'
    test_file_att = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
    test_file_att["Content-Type"] = 'application/octet-stream'
    test_file_att["Content-Disposition"] = f'attachment; filename="{file_name}"'
    msg.attach(test_file_att)

    # 构造附件1，传送文本附件
    file_name = 'test2.txt'
    test_file = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
    test_file.add_header('Content-Type','application/octet-stream')
    test_file.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
    msg.attach(test_file)

    # 构造附件2，文件附件
    image_file_name = 'test.jpg'
    image_file = MIMEImage(open(image_file_name, 'rb').read())
    image_file.add_header('Content-Type', 'application/octet-stream')
    image_file.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', image_file_name))
    msg.attach(image_file)

    server.sendmail(from_addr, send_to_addr, msg.as_string())
    # 关闭服务器
    server.quit()


html_msg = """
<p>您好，您申请的XXXX注册成功，请点击下面链接进行确认！</p>
<p><a href="http://www.xxxxxx.com">确认</a></p>
"""
send_email(send_to_addr='3022600790@qq.com', contest_msg=html_msg)

