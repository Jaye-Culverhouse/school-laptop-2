import json

class obj():

	def __init__(self, fn):
		self.fn = fn

		with open(fn) as f:
			self.settings = json.load(f)

	def get(self, setting):
		return self.settings[setting]

	def set(self, setting, newval):
		self.settings[setting] = newval
		self.save()

	def save(self):
		with open(self.fn, 'w') as f:
			json.dump(self.settings,f)