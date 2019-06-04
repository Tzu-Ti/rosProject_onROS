#!/usr/bin/python
import rospy
from std_msgs.msg import Int32
from duckietown_msgs.msg import Twist2DStamped
from sensor_msgs.msg import Joy

import time

class Control_car(object):
	def __init__(self):
		self.joy = None
		
		# Setup parameter
		self.v_gain = 0.41
		self.omega_gain = 8.3
		
		# Subscribers
		self.sub_joy = rospy.Subscriber("joy", Joy, self.cbJoy, queue_size=1)
		self.sub_speech = rospy.Subscriber("~control_cmd", Int32, self.move, queue_size=1)
		#self.sub_find = rospy.Subscriber(

		# Pubishers
		self.pub_car_cmd = rospy.Publisher("~car_cmd", Twist2DStamped, queue_size=1)

	##### Joy Control #####
	def cbJoy(self, joy_msg):
		self.joy = joy_msg
		joy_v = self.joy.axes[1] * self.v_gain
		joy_omega = self.joy.axes[3] * self.omega_gain
		self.send_car_msg(joy_v, joy_omega)

	##### Speech Control #####
	def move(self, control_msg):
		control_msg = control_msg
		num_activity = control_msg.data
		print("[control_car] %d" %num_activity)
		if num_activity != 0:
			print("execute go_direction!")
			self.go_direction(num_activity, 0)
		else:
			self.go_direction(0, 8.5)


	def go_direction(self, direction, turn):
		start_time = time.time()
		end_time = time.time()
		while (end_time - start_time) <= 2:
			self.send_car_msg(2 * direction, turn)
			end_time = time.time()
	
	##### Send car_msg #####
	def send_car_msg(self, v, omega):
		car_cmd_msg = Twist2DStamped()
		car_cmd_msg.v = v
		car_cmd_msg.omega = omega
		self.pub_car_cmd.publish(car_cmd_msg)
	
		

if __name__ == "__main__":
	rospy.init_node("control_car", anonymous=False)
	control_car = Control_car()
	rospy.spin()
