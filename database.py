import sqlite3
conn=sqlite3.connect('Login_data.db')
cursor=conn.cursor()

cmd1="""CREATE TABLE IF NOT EXISTS USERS(username varchar(50) not null,
                                        email_id varchar(50) PRIMARY KEY,
                                        password varchar(50) not null)"""

cursor.execute(cmd1)

cmd2="""INSERT INTO USERS(username,email_id,password)values('tester','tester@gmail.com','test')"""

cursor.execute(cmd2)
conn.commit()

ans=cursor.execute("select * from USERS" ).fetchall()
for i in ans :
    print(i)