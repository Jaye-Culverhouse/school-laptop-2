import numpy as np
import cv2
from pyzbar.pyzbar import decode as decodeQR

def decode(im) : 
	#QR codes

	codes = decodeQR(im)

	QRs = []

	# Print results
	for code in codes:

		QRs.append(code.data.decode("utf-8"))

	return QRs


def readUntilQRFound():
	cap = cv2.VideoCapture(0)
	cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

	while(True):
		ret, frame = cap.read()

		currentQRs = decode(frame)
				
		cv2.imshow("window",frame)
		cv2.waitKey(1)
		
		if len(currentQRs) > 0:
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	return currentQRs