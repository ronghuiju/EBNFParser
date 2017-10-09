#
__VERSION__ = "0.1.1"
__AUTHOR__  = 'thautwarm'
__doc___="""
   what's new in EBNFParser 0.1.2:
	1.
		separate parser with tokenizer.
		You are allowed to whether to define tokenizer automatically in EBNF files.
		You are allowed to define a funtion to be the tokenizer at the first line in a EBNF file
		for instance:
			using {{ lambda string:list(string) }} # or just list

		And you are allowed to write a tokenizer definition in another file, for instance:

		file: ./xxx.eebnf
			using python.token
		file: ./python/token
			lambda x : string(x)
		Take care that you can just write an expression!!!
	2.
		the meta information format has changed from

			"meta":{"rowIdx":<rowIdx>, "count":<count>, "fileName":<fileName>}
		to
			"meta":[<rowIdx>, <count>, <fileName>]

	Enjoy it:)
""" 