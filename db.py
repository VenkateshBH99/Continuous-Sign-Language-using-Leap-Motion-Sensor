import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

T=[]

class LeapMotionListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

	def on_init(self, controller):
		print("Initialized")

	def on_connect(self, controller):
		print("Motion Sensor Connected")

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print("Motion Sensor Disconnected")

	def on_exit(self, controller):
		print("Exited")

	def on_frame(self, controller):
		global T
		frame = controller.frame()
		# print("Frame ID : "+ str(frame.id))
		# print(str(frame.hands[1]))
		fingers = frame.fingers
		hands = frame.hands
		data=[]
		# print(str(len(frame.fingers)))
		if len(frame.fingers) == 10 or len(frame.hands) >=1:
			counter=5
			finger_feature=[0 for i in range(10)]
			palm_feature=[0 for i in range(2)]
			for finger in fingers:
				if len(frame.fingers)==10:
					if counter>0:
						# print(finger.type,"--"+str(finger.tip_position))
						finger_feature[finger.type]=str(finger.tip_position)
						counter-=1
					else:
						finger_feature[finger.type+5]=str(finger.tip_position)
				elif len(frame.fingers)==5:
					for hand in hands:
						if hand.is_left:
							finger_feature[finger.type]=str(finger.tip_position)
						elif hand.is_right:
							finger_feature[finger.type+5]=str(finger.tip_position)

			for hand in hands:
				if len(frame.hands)==2:
					if hand.is_left:
						palm_feature[0]=str(hand.palm_position)
					elif hand.is_right:
						palm_feature[1]=str(hand.palm_position)
				elif len(frame.hands)==1:
					if hand.is_left:
						palm_feature[0]=str(hand.palm_position)
						palm_feature[1]=str(0)
					elif hand.is_right:
						palm_feature[0]=str(0)
						palm_feature[1]=str(hand.palm_position)
			# print("Finger Features : ",finger_feature)
			# print("Palm Features : ", palm_feature)
			# finger_feature.append(palm_feature)
			for i in palm_feature:
				finger_feature.append(i)
			T.append(finger_feature)

# def process(gesture, arr):
# 	file=open("gesture_1.txt", "w")
# 	for i in range(len(arr)):
# 		file.write()

def main():
	num = input("File number : ")
	listener = LeapMotionListener()
	controller = Leap.Controller()

	controller.add_listener(listener)

	print("Press enter to quit")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

	# if len(T)==90:
	# 	controller.remove_listener(listener)
	# print(T[:90])
	# print(T[0][0])
	
	file=open("Dataset/NO/NO_"+str(num)+".txt", "w")
	# file=open("Test_Dataset/MORNING/MORNING_"+str(num)+".txt", "w")
	for i in range(90):
		file.write(str(T[50+i])+"\n")

if __name__ == '__main__':
	main()