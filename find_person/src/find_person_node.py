#!/usr/bin/python
import rospy
from std_msgs.msg import Int32, Bool

class Find_person(object):
	def __init__(self):
		# Publishers
		self.pub_camera = rospy.Publisher("~exe_camera", Bool, queue_size=1)
	
		# Subscribers
		self.sub_exe_find = rospy.Subscriber("~exe_find", Bool, self.start, queue_size=1)
	
	def start(self, exe_msg):
		exe_msg = exe_msg
		print("[find_person_node]", exe_msg)
		print("[find_person_node] Start find person!!")
		if exe_msg:
			self.send_exe_camera()

	def send_exe_camera(self):
		exe_msg = Bool()
		exe_msg.data = True
		self.pub_camera.publish(exe_msg)

if __name__ == "__main__":
	rospy.init_node("find_person", anonymous=False)
	find_person = Find_person()
	rospy.spin()
