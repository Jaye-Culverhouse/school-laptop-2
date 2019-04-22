import client_cv
import settingobj


def main():

	setting_obj = settingobj.obj("client.json")

	while True:
		QRData = client_cv.readUntilQRFound()[0]
		





if __name__ == '__main__':
	main()