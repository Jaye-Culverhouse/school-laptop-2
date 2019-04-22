import json

class obj():

	def __init__(self, fn):

		with open(fn) as f:

			self.settings = json.load(f)


	def get(self, setting):
		return self.settings[setting]