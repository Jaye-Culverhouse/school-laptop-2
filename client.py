import client_cv
import settingobj
import pymysql

def main():

	setting_obj = settingobj.obj("client.json")

	while True:
		QRData = client_cv.readUntilQRFound()[0]
		print(QRData)
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

				print(result)

		except:

			pass;

		finally:
			c.close()

			handleDevice(QRData["uid"], result["CheckedIn"])



def handleDevice(uid, checked):
	

if __name__ == '__main__':
	main()