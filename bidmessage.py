import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456789', port=3306, db='bid_info')

def savedata(bidcompany ,bidamount ,biddate,purchaser ,purchaseraddr,bidurl ,bidname):
    try:
        if dataexits(bidurl):
            print("message is exits !")
        else :
            cursor = conn.cursor()
            sql = "insert into bid_info.bid_message (bidcompany, bidamount, biddate, purchaser, purchaseraddr, bidurl, bidname) values ('"+ bidcompany + "','"+ bidamount +"','"+ biddate +"','"+ purchaser +"','"+ purchaseraddr +"','"+ bidurl +"','" + bidname + "')"
            cursor.execute(sql)
            conn.commit()
    except Exception:
        print("error sql : \r\n" + sql)

def dataexits(bidurl):
    try:
        cursor = conn.cursor()
        sql = "select count(mid) from bid_info.bid_message where bidurl='"+ bidurl +"'"
        cursor.execute(sql)
        conn.commit()
        values = cursor.fetchone()
        datacount = values[0];
    except Exception:
        print("error sql : \r\n " + sql)

    if datacount >= 1:
        return True
    else :
        return False