import json
 
class DictionaryReader:
	
	def __init__(self):
		self.file = 'dictEntries.txt'
		self.dictionary = {}
		self.loadDict()
		self.loop = 0
		
	def loadDict(self):
		try:
			with open(self.file, 'r') as f:
				s = f.read()
				self.dictionary = json.loads(s)
		except Exception:
			return

	def whisperCommands(self):
		return self.dictionary["whisper"]
	
	def roles(self):
		return self.dictionary["roles"]

	def admins(self):
		return self.dictionary["authorized"]

	def readEntry(self, entry):
		self.loop = self.loop + 1
		if self.loop > 10:
			print("Loop error")
			return None
		fixed = self.fixEntry(entry)
		print(fixed)
		if fixed in self.dictionary:
			while fixed in self.dictionary:
				fixed = self.dictionary[fixed]
			return fixed
		else:
			print(entry.split('.')[0]+".invalid")
			return self.readEntry(entry.split('.')[0]+".invalid")


			
	def fixEntry(self, entry):
		result = entry.lower()
		#Head
		result = result.replace("helm","head",1)
		#Neck
		result = result.replace("amulet","neck",1)
		result = result.replace("necklace","neck",1)
		#Shoulder
		result = result.replace("shoulders","shoulder",1)
		#Cloak
		result = result.replace("cloak","back",1)
		#Chest
		result = result.replace("robe","chest",1)
		#Wrist
		result = result.replace("wrists","wrist",1)
		result = result.replace("bracer","wrist",1)
		result = result.replace("bracers","wrist",1)
		#Gloves
		result = result.replace("hands","gloves",1)
		#Waist
		result = result.replace("belt","waist",1)
		#Legs
		result = result.replace("leggings","legs",1)
		#Feet
		result = result.replace("boots","feet",1)
		result = result.replace("foot","neck",1)
		#Ring
		result = result.replace("finger","ring",1)
		#Trinket
		#Weapon
		#Off-hand
		
		#Specs
		if "ord" not in result:
			if "discipline" not in result:
				result = result.replace("disc","discipline",1)
		
		result = result.replace("pub.","",1)

		#Aliases
		result = result.replace("weakauras","wa",1)
		if "link" not in result:
			result = result.replace("lexicon","link.lexicon",1)
	
		return result
		
	def commandReader(self, params):
		return self.readEntry('.'.join(params.split(' ')))

	def itemReader(self, params):
		result = self.commandReader(params)
		if 'Invalid' in result:
			itemId = params.split(' ')[1]
			if itemId.isdigit():
				return 'https://wowhead.com/item='+itemId
		return result