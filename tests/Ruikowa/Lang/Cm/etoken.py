
import re
e = re.escape

__regex__ = re.compile("|".join([
	e("/*"),
	e("*/"),
	"//[^\n]*",
	'[a-z]*"[\w|\W]*"',
	e(';'),
	e('`'),
	e(','),
	'0[XxOoBb][\da-fA-F]+',
	'\d+(?:\.\d+|)(?:E\-{0,1}\d+|)',
	'\n',
	'[a-zA-Z_][a-z0-9A-Z_]*',
	e('{'),e('}'),e('('),e(')'),e('['),e(']'),
	e('->'),
	'\/\/|\/|\|\||\||\>\>|\<\<|\>\=|\<\=|\<\-|\>|\<|\=\>|\-\-|\+\+|\*\*|\+|\-|\*|\=\=|\=|\%|\^',
	'\?|\!|\&|\$|\@|\+|\-|\~',
	e(':')	
	]))

def token(input):
	
        return __regex__.findall(input)

