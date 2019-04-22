import client_cv
import settingobj
import pymysql

setting_obj = settingobj.obj("client.json")

def main():


	while True:
		QRData = client_cv.readUntilQRFound()[0]
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

		except:

			pass;

		finally:
			c.close()

			handleDevice(QRData["uid"], result["CheckedIn"])



def handleDevice(deviceID, checked):

	if checked == 1: #check out

		studentID = client_cv.readUntilQRFound()[0]["uid"]

		print("Result from student QR: ", studentID)

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
					print("UPDATED")

		except:

			pass; #do some error handling here?

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
				
				if result["Banned"] == 1:
					#banned handling
					print("BANNED")
					pass
				else:
					sql = "UPDATE Device SET CheckedIn=1 WHERE UID=%s"
					c.execute(sql, (deviceID))
					conn.commit()
					print("UPDATED")

		except:

			pass; #do some error handling here?

		finally:
			c.close()

if __name__ == '__main__':
	main()