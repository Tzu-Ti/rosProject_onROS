#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import MySQLdb as mysql
import time, datetime

class Mysql(object):
        def __init__(self):
                self.activity = None

                self.pub_activity = rospy.Publisher("/speech_recognition/activity", String, queue_size=1)
                self.get_data()

        def get_data(self):
                while not rospy.is_shutdown():
			# print("Fetching data...")
                        db = mysql.connect(
                                host = "175.182.105.203",
                                port = 5050,
                                user = "titi",
                                passwd = "titi861203",
                                db = "mydb"
                        )
                        cursor = db.cursor()
                        sql = "SELECT * FROM ros_user_talk ORDER BY time DESC LIMIT 1"
                        try:
                                cursor.execute(sql)
                                results = cursor.fetchone()
                                now_time = datetime.datetime.now()
                                sql_time = results[0]
                                self.activity = results[1]
				# print("SQL time = %s" %sql_time)
                                if self.is_it_now(now_time, sql_time):
                                        print("[mysql] %s" %self.activity)
                                        if self.activity != "False":
						self.send_activity()
                        except:
                                print("Error: unable to fetch data")

                        db.close()
                        time.sleep(4)

        def is_it_now(self, now_time, sql_time):
                now_seconds = time.mktime(now_time.timetuple())
                sql_seconds = time.mktime(sql_time.timetuple())
		delta = now_seconds - sql_seconds
                if delta <= 4:  return True
                else:   return False

        def send_activity(self):
                activity_msg = String()
                activity_msg.data = self.activity
                self.pub_activity.publish(activity_msg)


if __name__ == "__main__":
        rospy.init_node("mysql", anonymous=False)
        mysql = Mysql()
        rospy.spin()
