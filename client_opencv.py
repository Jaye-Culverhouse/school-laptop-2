import numpy as np
import cv2
from pyzbar.pyzbar import decode as decodeQR
import json

def decode(im) : 
	#QR codes

	codes = decodeQR(im)

	QRs = []

	# Decode response and resolve json
	for code in codes:

		QRs.append(json.loads(code.data.decode("utf-8")))

	return QRs


def readUntilQRFound(text=""):
	cap = cv2.VideoCapture(0)
	cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

	while(True):
		ret, frame = cap.read()

		currentQRs = decode(frame)
		
		cv2.putText(frame, text, (50,100), cv2. FONT_HERSHEY_PLAIN, 1, (255,0,0))

		cv2.imshow("window",frame)
		cv2.waitKey(1)
		
		if len(currentQRs) > 0:
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	return currentQRs

shouldBreak = False

def breakLoop(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		global shouldBreak
		shouldBreak = True

def showScreenWithText(text):
	cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
	frame = np.zeros((1080,1920,3), np.uint8)

	for t,i in zip(text, range(len(text))):

		textsize = cv2.getTextSize(t, cv2.FONT_HERSHEY_PLAIN, 5, 2)[0]
		textX = (frame.shape[1] - textsize[0]) // 2
		
		cv2.putText(frame, t, (textX,100+100*(i+1)), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255))

	cv2.setMouseCallback("window", breakLoop)
	global shouldBreak
	shouldBreak = False

	while True:

		if shouldBreak:
			break;

		cv2.imshow("window",frame)
		cv2.waitKey(1)

	# When everything done, release the capture
	cv2.destroyAllWindows()