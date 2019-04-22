import client_cv

def main():
	while True:
		QRData = client_cv.readUntilQRFound()[0]
		print(QRData)

		



if __name__ == '__main__':
	main()