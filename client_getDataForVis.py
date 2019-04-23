import pymysql
import settingobj
import os

def prepareDataVisOutput():
	setting_obj = settingobj.obj("client.json")
	
	conn = pymysql.connect(
		host = setting_obj.get("ip"), 
		user = setting_obj.get("username"), 
		password = setting_obj.get("password"),
		db = setting_obj.get("db"),
		charset = "utf8mb4",
		cursorclass=pymysql.cursors.DictCursor)

	try:

		with conn.cursor() as c:

			sql = "SELECT DID, CheckedIn, Time, Name FROM Events"
			c.execute(sql)

			result = c.fetchall()

			table = "let data = ["

			for row in result:
				table+="[{},{},'{}','{}'],\n".format(row["Time"], row["DID"], "IN" if row["CheckedIn"]==1 else "OUT", row["Name"])

			table+='''];

let dateOptions = {

"year":"numeric",
"month":"short",
"day":"2-digit",
"weekday":"short",
"hour":"2-digit",
"minute":"2-digit",
"second":"2-digit",
"hour12":false
}'''
	
			
			os.system("mkdir output")
			os.system("mkdir output/assets")

			with open("output/assets/data.js", 'w') as f:
				f.write(table)

			writeOtherFiles()


	except Exception as e:

		print(e)

	finally:
		c.close()



def writeOtherFiles():
	os.system("cp -r datavis/* output")


if __name__ == '__main__':
	prepareDataVisOutput()
