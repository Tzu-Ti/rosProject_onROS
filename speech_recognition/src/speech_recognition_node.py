#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, String, Bool

class Speech_recognition(object):
	def __init__(self):
		self.num_activity = None

		# Publishers
		self.pub_control = rospy.Publisher("~control_cmd", Int32, queue_size=1)
		self.pub_exe_find = rospy.Publisher("~exe_find", Bool, queue_size=1)
		
		# Subscribers
		self.sub_activity = rospy.Subscriber("/speech_recognition/activity", String, self.speech_control, queue_size=1)

	##### After receive the data from mysql #####
	def speech_control(self, activity_msg):
		activity_msg = activity_msg
		activity = activity_msg.data
		print("[Speech_recognition] %s" %activity)
		num_activity = self.explain_cmd(activity)
		# print(num_activity)
		if num_activity == 100:
			self.execute_find_mode()
		else:
			self.send_control(num_activity)

	##### Convert the data from mysql to digital data #####
	def explain_cmd(self, activity):
		if activity == "turn around":
			return 0
		elif activity == "go ahead":
			return 1
		elif activity == "go back":
			return -1
		elif activity == "find person":
			return 100
	
	##### Send the digital data to control_car_node #####
	def send_control(self, cmd):
		control_msg = Int32()
		control_msg.data = cmd
		self.pub_control.publish(control_msg)

	def execute_find_mode(self):
		exe_msg = Bool()
		exe_msg.data = True
		self.pub_exe_find.publish(exe_msg)

if __name__ == "__main__":
	rospy.init_node("speech_recognition", anonymous=False)
	speech_recognition = Speech_recognition()
	rospy.spin() 
