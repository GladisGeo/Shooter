import psycopg2 
from config import config
# connection =psycopg2.connect(
#     host="localhost",port="5432", database="shooter",user="postgres", password="CEFgoose@6thAB")
def connect():
    connection = None
    try:
        params = config()
        print("connecting")
        connection = psycopg2.connect(**params)

        crsr = connection.cursor()
        rows=crsr.fetchall()
        for row in rows:
            print("id%s name %s"%(row[0,row[1]]))
        crsr.close()
    except(Exception,psycopg2.DatabaseError)as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("CONNECTION TERMINATED")
if __name__ =="__main__":
    print("GO")
    connect()