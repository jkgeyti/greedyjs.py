### Greedy JS construct extracter 
###   Extracts a JS construct from stdin. Useful for extracting json from curl'ed web pages.
###   Will look for a start tag, and greedily print the stream from (and including) that tag,
###   until a "reasonable" end of that JS expression is found, be it the end of a nested object,
###   array, or multiline string.
### Usage: ... | python greedyjs.py "var searchingfor ="

import sys

# holds the output string we're building
output = ""

# get user arguments
starttag = sys.argv[1]
firstvar = False
if (len(sys.argv) > 2):
	firstvar = sys.argv[2].lower() == "true"

# various state variables required by our parser
enabled = False
isvalue = False
expect = None
quote = False
escape = False
plus = False

# loop through stdin input
for l in sys.stdin:
	
	# keep scanning until hitting start search word (starttag)
	if not enabled:
		if starttag in l:
			index = l.index(starttag)
		else:
			index = -1
		if (index >= 0):
			enabled = True
			l = l[index:]
	
	# if start search word found, start greedily parsing JS
	if enabled:
		for c in l:		

			# debugging
			#print expect,quote,escape,plus,c
			if not firstvar or isvalue:
				output += c

			# are we escaping this char / are we in escape mode?
			if escape:
				escape = False
				continue
			# is this an escape char, then enable escape mode?
			elif c == "\\":
				escape = True
				continue
			
			# are we starting/ending a string?
			if c == '"':
				quote = not quote
				continue
			# are we inside a string definition?
			if quote:
				continue

			# are we seing the expected character to end current scope/construct?
			if expect is not None and len(expect) > 0 and c == expect[-1]:
				expect.pop()
				continue
					
			# are we starting a new scope/construct?
			if c == "[":
				if expect is None: expect = []
				expect.append("]")
				continue
			elif c == "{":
				if expect is None: expect = []
				expect.append("}")
				continue
			elif c == "(":
				if expect is None: expect = []
				expect.append(")")	
				continue

			# are we starting a value?
			if (c == "="):
				isvalue = True

			# is it a plus (then we can't end a simple expression, as it may be string concatenation)?
			if c in ["+", "-", "*", "/"]:
				plus = True
			elif plus and c not in [" ", "\r","\n"]:
				plus = False

			# are we at the end of a simple one-line expression?
			if not plus and (c == ";" or c == "\n" and (expect is None or len(expect) == 0)):
				# if only printing value, then remove last char (as it's just a newline/semicolon)
				if firstvar:
					output = output[:-1]
				# dump output and stop
				print output.strip()
				sys.exit(0)