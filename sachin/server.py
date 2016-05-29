#Server Connection to MySQL:

import MySQLdb
conn = MySQLdb.connect(user="sac0",passwd="sac0",db="wpcentaur",unix_socket="/opt/lampp/var/mysql/mysql.sock")
x = conn.cursor()
'''

"""
number_of_rows = x.execute("""
            INSERT INTO speedo (id,speed)
            VALUES
                (%s,%s)

        """,(myid,speed))
'''
speed = int(1001)
myid = int(121)
number_of_rows = x.execute("""
   UPDATE speedo
   SET speed=%s
   WHERE id=%s
""", (speed,myid))
conn.commit()
conn.close()