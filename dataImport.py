import csv
import sqlite3
from django.contrib.auth.hashers import make_password
import traceback


def dataImport(csvpath='datas.csv', dbpath='db.sqlite3'):
    try:
        reader = csv.DictReader(open(csvpath, "r"), delimiter=',', quoting=csv.QUOTE_MINIMAL)
        print('ok')
        conn = sqlite3.connect(dbpath)
        conn.text_factory = str
        c = conn.cursor()
        for row in reader:
            to_db = [row['姓名'], row['Email'], row['电话'], row['单位'], row['科室'],
                     row['职称'], row['职务'], row['工号']]
            password = row['Email']
            password = make_password(password)
            to_db.append("")  # 省份
            to_db.append(password)  # 密码
            to_db.append("")  # is_superuser
            to_db.append("")  # first_name
            to_db.append("")  # last_name
            to_db.append("")  # email
            to_db.append(False)  # is_staff
            to_db.append(True)  # is_active
            to_db.append("")  # date_joined
            try:
                c.execute('INSERT INTO ' + 'web_user' +
                          '''(name,username,phone,unit,office,professional,post,number,province,password,is_superuser,first_name
                          ,last_name,email,is_staff,is_active,date_joined)
                          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);''', to_db)
            except:
                pass
            conn.commit()
    except:
        traceback.print_exc()


if __name__ == '__main__':
    dataImport('datas.csv', 'db.sqlite3')
