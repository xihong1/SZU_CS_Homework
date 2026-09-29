from datetime import datetime,date,time,timedelta

yourBrithday = input("请输入您的生日：")
yourBrithday = datetime.strptime(yourBrithday,"%Y-%m-%d").date()
#计算下一个生日日期
now=date.today()
nextBrithday = date(now.year,yourBrithday.month,yourBrithday.day)
if now>nextBrithday:
    nextBrithday = date(now.year+1,yourBrithday.month,yourBrithday.day)

#计算天数
timeToBrithday = (nextBrithday-now).days
print("距离您的生日还有"+str(timeToBrithday)+"天")
#获取星期几
weekday = nextBrithday.weekday()
weekday_dict = {0:"星期一",1:"星期二",2:"星期三",3:"星期四",4:"星期五",5:"星期六",6:"星期日"}
print("您的生日是是"+weekday_dict[weekday])