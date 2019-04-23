import client_opencv
import settingobj
import pymysql
import time
import sys

setting_obj = settingobj.obj("client.json")

def main():


	while True:
		client_opencv.showScreenWithText(["Welcome.","Please follow the onscreen","instructions to check out a laptop", "Press on the screen to advance"]) # show a welcome screen
		
		try:

			QRData = client_opencv.readUntilQRFound(text="Please present device ID")[0]
		
		except:
		
			client_opencv.showScreenWithText(["This QR code doesn't seem to be setup", "Please tell someone"]) # show a welcome screen	
			continue

		print(QRData)
		
		if QRData["uid"] == "SPECIAL":

			if (QRData["type"] == "MANAGE") & (QRData["auth"] == setting_obj.get("mangement_password")):

				handleManagement()

			elif (QRData["type"] == "RESET") & (QRData["auth"] == 41326244631921666612):
				setting_obj.set("mangement_password", "PASSWORD123")
				print("reset management password")

			elif (QRData["type"] == "EXIT") & (QRData["auth"] == setting_obj.get("mangement_password")):
				sys.exit()

		else:
			print("QR from Device QR: ",QRData)
			conn = pymysql.connect(
				host = setting_obj.get("ip"), 
				user = setting_obj.get("username"), 
				password = setting_obj.get("password"),
				db = setting_obj.get("db"),
				charset = "utf8mb4",
				cursorclass=pymysql.cursors.DictCursor)

			try:

				with conn.cursor() as c:

					sql = "SELECT CheckedIn FROM Device WHERE uid=%s"
					c.execute(sql, (QRData["uid"]))

					result = c.fetchone()

					print("Result from checked query: ",result)

			except Exception as e:

				client_opencv.showScreenWithText(["Something went wrong, please press the screen and take a photo of the next page to show someone"]) # show a welcome screen
				client_opencv.showScreenWithText([e])
			finally:
				c.close()

				handleDevice(QRData["uid"], result["CheckedIn"])



def handleDevice(deviceID, checked):

	try:

		studentID = client_opencv.readUntilQRFound(text="Please present student ID")[0]["uid"]
	
	except:
		client_opencv.showScreenWithText(["This QR code doesn't seem to be setup", "Please tell someone"]) # show a welcome screen	
		return 0

	eventType = -1

	print("Result from student QR: ", studentID)

	if checked == 1: #check out

		conn = pymysql.connect(
			host = setting_obj.get("ip"), 
			user = setting_obj.get("username"), 
			password = setting_obj.get("password"),
			db = setting_obj.get("db"),
			charset = "utf8mb4",
			cursorclass=pymysql.cursors.DictCursor)

		try:

			with conn.cursor() as c:

				sql = "SELECT Banned FROM Students WHERE uid=%s"
				c.execute(sql, (studentID))

				result = c.fetchone()

				print("Result from student query: ",result)
				
				if result["Banned"] == 1:
					#banned handling
					print("BANNED")
					pass
				else:
					sql = "UPDATE Device SET CheckedIn=0 WHERE UID=%s"
					c.execute(sql, (deviceID))
					conn.commit()
					print("CHECKED OUT")
					eventType = 0

		except:

			client_opencv.showScreenWithText(["Something went wrong, please press the screen and take a photo of the next page to show someone"]) # show a welcome screen
			client_opencv.showScreenWithText([e])

		finally:
			c.close()

	else: #check in

		conn = pymysql.connect(
			host = setting_obj.get("ip"), 
			user = setting_obj.get("username"), 
			password = setting_obj.get("password"),
			db = setting_obj.get("db"),
			charset = "utf8mb4",
			cursorclass=pymysql.cursors.DictCursor)

		try:

			with conn.cursor() as c:
				
				sql = "UPDATE Device SET CheckedIn=1 WHERE UID=%s"
				c.execute(sql, (deviceID))
				conn.commit()
				print("CHECKED IN")
				eventType = 1

		except:

				client_opencv.showScreenWithText(["Something went wrong, please press the screen and take a photo of the next page to show someone"]) # show a welcome screen
				client_opencv.showScreenWithText([e])

		finally:
			c.close()

	if eventType != -1: # ONLY DO THIS IF AN EVENT *ACTUALLY* HAPPENED

		conn = pymysql.connect(
			host = setting_obj.get("ip"), 
			user = setting_obj.get("username"), 
			password = setting_obj.get("password"),
			db = setting_obj.get("db"),
			charset = "utf8mb4",
			cursorclass=pymysql.cursors.DictCursor)

		try:

			with conn.cursor() as c:
				
				sql = "SELECT Name FROM Students WHERE uid=%s"
				c.execute(sql, (studentID))

				SName = c.fetchone()["Name"]

				sql = "INSERT INTO Events (UID, DID, CheckedIn, Time, Name) VALUES (%s, %s, %s, %s, %s)"
				c.execute(sql, (deviceID, studentID, eventType, int(time.time()), SName))
				conn.commit()
				print("INSERTED EVENT")
				if eventType == 0:
					client_opencv.showScreenWithText(["You've successfuly checked out the device"]) # show a welcome screen
				else:
					client_opencv.showScreenWithText(["You've successfuly checked in the device"]) # show a welcome screen

		except Exception as e:

				client_opencv.showScreenWithText(["Something went wrong, please press the screen and take a photo of the next page to show someone"]) # show a welcome screen
				client_opencv.showScreenWithText([e])

		finally:
			c.close()

def handleManagement():

	print("management area accessed")

if __name__ == '__main__':
	main()