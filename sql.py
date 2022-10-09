import sqlite3
OLDDB = 'data3.db'
NEWDB = 'data2.db'
outdb = 'datatotal.db'
name2id = {}    # 总数据库中名字到id的映射
name2description = {}
name2file = {}
name2iconfile = {}
name2totaltime = {}
oldid2name = {}
newid2name = {}

oldconn = sqlite3.connect(OLDDB)
oldcursor = oldconn.cursor()
newconn = sqlite3.connect(NEWDB)
newcursor = newconn.cursor()
outconn = sqlite3.connect(outdb)
outcursor = outconn.cursor()
# 处理第一个表
oldcursor.execute('select * from AppModels')
oldconn.commit()
newcursor.execute('select * from AppModels')
newconn.commit()
newdata = newcursor.fetchall()
for i in newdata:
    if i[1] not in name2id.keys():
        name2id[i[1]] = len(name2id) + 1
    newid2name[i[0]] = i[1]

olddata = oldcursor.fetchall()
for i in olddata:
    if i[1] not in name2id.keys():
        name2id[i[1]] = len(name2id) + 1
    oldid2name[i[0]] = i[1]

    name2description[i[1]] = i[2]
    name2file[i[1]] = i[3]
    name2iconfile[i[1]] = i[5]
    if i[1] in name2totaltime.keys():
        name2totaltime[i[1]] += i[6]
    else:
        name2totaltime[i[1]] = i[6]

for i in newdata:
    name2description[i[1]] = i[2]
    name2file[i[1]] = i[3]
    name2iconfile[i[1]] = i[5]
    if i[1] in name2totaltime.keys():
        name2totaltime[i[1]] += i[6]
    else:
        name2totaltime[i[1]] = i[6]

outcursor.execute("""
    create table if not exists AppModels(
        ID INTEGER PRIMARY KEY,
        Name nvarchar NOT NULL,
        Description nvarchar,
        File nvarchar,
        CategoryID INT,
        IconFile nvarchar,
        TotalTime INT
    )
""")
for i in name2id.keys():
    outcursor.execute(f"""insert into AppModels values({name2id[i]} , "{i}" , "{name2description[i]}" , "{name2file[i]}" ,
        0 , "{name2iconfile[i]}" , {name2totaltime[i]})""")
outconn.commit()

# 已完成 AppModels 的整合

outcursor.execute("""
    create table if not exists CategoryModels(
        ID INTEGER PRIMARY KEY,
        Name nvarchar NOT NULL,
        IconFile nvarchar
    )
""")
outconn.commit()

# 已完成 CategoryModels 的添加

outcursor.execute("""
    create table if not exists DailyLogModels(
        ID INTEGER PRIMARY KEY,
        Date datetime NOT NULL,
        Time INT,
        AppModelID INT
    )
""")
dateandnamefortime = {}

def get_daily_data(data,id2name):
    global dateandnamefortime
    for _,date,time,appid in data:
        if appid == 0:  # 早期版本会出现为0的情况
            continue
        if date in dateandnamefortime.keys():
            if id2name[appid] in dateandnamefortime[date].keys():
                dateandnamefortime[date][id2name[appid]] += time # 时间叠加
            else:
                dateandnamefortime[date][id2name[appid]] = time
        else:
            dateandnamefortime[date] = {}
            dateandnamefortime[date][id2name[appid]] = time

def merge_each_data(sheet):
    global dateandnamefortime
    dateandnamefortime = {}
    if sheet == 'DailyLogModels':
        outcursor.execute("""
            create table if not exists DailyLogModels(
                ID INTEGER PRIMARY KEY,
                Date datetime NOT NULL,
                Time INT,
                AppModelID INT
            )
        """)
    else:
        outcursor.execute("""
            create table if not exists HoursLogModels(
                ID INTEGER PRIMARY KEY,
                Datatime datetime NOT NULL,
                Time INT,
                AppModelID INT
            )
        """)
    outconn.commit()
    oldcursor.execute(f'select * from {sheet}')
    oldconn.commit()
    newcursor.execute(f'select * from {sheet}')
    newconn.commit()
    newdata = newcursor.fetchall()
    olddata = oldcursor.fetchall()
    get_daily_data(olddata,oldid2name)
    get_daily_data(newdata,newid2name)

    n = 1
    for date in dateandnamefortime.keys():
        for name in dateandnamefortime[date].keys():
            outcursor.execute(f"""insert into {sheet} values({n},"{date}",{dateandnamefortime[date][name]},
            {name2id[name]})""")
            n += 1
    outconn.commit()

merge_each_data('DailyLogModels')
merge_each_data('HoursLogModels')
