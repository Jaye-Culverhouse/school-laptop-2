import numpy as np
import cv2
from pyzbar.pyzbar import decode as decodeQR
import libs.QR

def decode(im) : 
	#QR codes

	codes = decodeQR(im)

	QRs = []

	# Print results
	for code in codes:
		QRs.append(libs.QR.QR(code.data.decode("utf-8"), code.polygon))

	return QRs


def readUntilQRFound():
	cap = cv2.VideoCapture(0)
	cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

	while(True):
		ret, frame = cap.read()

		currentQRs = decode(frame)
		
		for qr in currentQRs:
			cv2.putText(frame, qr.data, (qr.points[3].x,qr.points[3].y-10), cv2. FONT_HERSHEY_PLAIN, 1, (255,0,0))
			for point in qr.points:
				cv2.circle(frame, (point.x,point.y), 5, (255,0,0))
		
		cv2.imshow("window",frame)
		cv2.waitKey(1)
		
		if len(currentQRs) > 0:
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	return currentQRs