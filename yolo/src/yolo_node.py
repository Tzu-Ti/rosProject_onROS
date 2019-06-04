#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, Bool

import cv2
import picamera
import numpy as np
import time
import socket

class Yolo(object):
	def __init__(self):
		##### Socket #####
		### GPU computer ###
		self.HOST = "192.168.0.177"
		self.PORT = 8080
		### ROS ###
		self.ip = "192.168.0.145"
		self.port = 5050

		# Subscribers
		self.sub_camera = rospy.Subscriber("~exe_camera", Bool, self.camera, queue_size=1)

	##### Receive results from GPU computer #####
	def receive(self):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((self.ip, self.port))
		server.listen(1)
		client, addr = server.accept()
		print("Connected by", addr)
		objCounts = client.recv(1024)
		print("[receive] %s" %objCounts)
		server.close()

	##### take a picture and send to GPU computer #####
	def camera(self, exe_msg):
		exe_msg = exe_msg
		with picamera.PiCamera() as camera:
			camera.resolution = (640, 480)
			camera.framerate = 24
			time.sleep(1)

			### Connect to GPU computer ###
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.HOST, self.PORT))
				
			### Take a picture ###
			image = np.empty((480 * 640 *3,), dtype=np.uint8)
			camera.capture(image, format='bgr')
			image = image.reshape((480, 640, 3))
			cv2.imwrite("test.jpg", image)

			### Send to GPU computer ###
			imgFile = open("test.jpg")
			while True:
				imgData = imgFile.readline(1024)
				if not imgData:
					break
				s.send(imgData)
			imgFile.close()
			print("transit end")

			s.close()
       
			self.receive()

if __name__ == "__main__":
	rospy.init_node("yolo", anonymous=False)
	yolo = Yolo()
	rospy.spin()
