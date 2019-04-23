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