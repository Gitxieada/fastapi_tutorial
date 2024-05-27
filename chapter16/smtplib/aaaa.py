# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# 构建邮件头
from email.header import Header


# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '@qq.com'
password = '****'
# 收信方邮箱
to_addr = 'xxxxx@qq.com'
# 发信服务器
smtp_server = 'smtp.qq.com'

html_msg = """
<p>Python 邮件发送HTML格式文件测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
"""


# 创建一个带附件的实例msg
msg = MIMEMultipart()
msg['From'] = Header('张三')  # 发送者
msg['To'] = Header('李四')  # 接收者
subject = 'Python SMTP 邮件测试'
msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
# 邮件正文内容
msg.attach(MIMEText(html_msg, 'html', 'utf-8'))

# 构造附件1，传送当前目录下的 test1.txt 文件
att1 = MIMEText(open('test1.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="test1.txt"'
msg.attach(att1)

# 构造附件2，传送当前目录下的 test2.txt 文件
att2 = MIMEText(open('test2.txt', 'rb').read(), 'base64', 'utf-8')
att2["Content-Type"] = 'application/octet-stream'
att2["Content-Disposition"] = 'attachment; filename="test2.txt"'
msg.attach(att2)
smtpobj = None
try:
    smtpobj = smtplib.SMTP_SSL(smtp_server)
    smtpobj.connect(smtp_server, 465)    # 建立连接--qq邮箱服务和端口号
    smtpobj.login(from_addr, password)   # 登录--发送者账号和口令
    smtpobj.sendmail(from_addr, to_addr, msg.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("无法发送邮件")

# 关闭服务器
smtpobj.quit()
