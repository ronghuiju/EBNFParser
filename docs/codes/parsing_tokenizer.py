# This file is automatically generated by EBNFParser.
from Ruikowa.ObjectRegex.Tokenizer import unique_literal_cache_pool, regex_matcher, char_matcher, str_matcher, Tokenizer
from Ruikowa.ObjectRegex.Node import AstParser, Ref, SeqParser, LiteralValueParser as L, LiteralNameParser, Undef
namespace = globals()
recur_searcher = set()
token_table = ((unique_literal_cache_pool["MyTokenType"], str_matcher(('abc', '233'))),)

class UNameEnum:
# names

    MyTokenType_abc = unique_literal_cache_pool['abc']
    MyTokenType = unique_literal_cache_pool['MyTokenType']
    parserToTest = unique_literal_cache_pool['parserToTest']
        
cast_map = {}
token_func = lambda _: Tokenizer.from_raw_strings(_, token_table, ({}, {}),cast_map=cast_map)
MyTokenType = LiteralNameParser('MyTokenType')
parserToTest = AstParser([SeqParser([Ref('MyTokenType')], at_least=1,at_most=Undef)],
                         name="parserToTest",
                         to_ignore=({}, {}))
parserToTest.compile(namespace, recur_searcher)