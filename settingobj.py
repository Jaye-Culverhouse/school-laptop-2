import json

class obj():

	def __init__(self, fn):

		with open(fn, 'r') as f:

			self.settings = json.loads(f.read())


	def get(self, setting):
		return self.settings[setting]