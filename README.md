[![Build Status](https://travis-ci.org/thautwarm/EBNFParser.svg?branch=master)](https://travis-ci.org/thautwarm/EBNFParser)
[![GPLv3.0 License](https://img.shields.io/badge/license-GPLv3.0-Green.svg)](https://github.com/thautwarm/EBNFParser/blob/master/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/EBNFParser.svg)](https://pypi.python.org/pypi/EBNFParser)


# EBNFParser
Parse Many, Any, Every
---------
[HomePage](https://github.com/thautwarm/EBNFParser)


## Multi-Language-Versions

- [Python Project(Support Python 3.4+)](https://github.com/thautwarm/EBNFParser/tree/master/Python) (v 1.0)
    - [What's new in EBNFParser 1.0](https://github.com/thautwarm/EBNFParser/tree/master/Python/release-note)
    - [Old Version : Misakawa](https://github.com/thautwarm/EBNFParser/tree/master/Misakawa.md)



--------------------

## Install
- Python
    - pip  

    `pip installl -U EBNFParser`
    
    - setup 
    ```shell
    git clone https://github.com/thautwarm/EBNFParser
    cd EBNFParser/Python
    python setup.py install
    ``` 


## An Introduce to EBNFParser

`EBNFParser` seems to be a parser framework for parsing EBNF syntaxes, however, 
the syntax of `EBNF` here is not the same as that standard one.  
The name of current EBNFParser's version  is `Ruikowa`, so you can call this idiom as `Ruikowa` for convenience' sake.

Here is an example for you to get a knowledge of `Ruikowa` for parsing Java `switch` syntax. 

```BNF

Token Token.Java # use the token definition at source file `./Token/Java`.

newline  ::= R'\n' # match by using regular expression

switch   ::= 'switch' '(' expression ')' newline*
             '{'  
                (case | newline  )*
                [default newline*]
             '}' ;

case     ::= 'case' ':' body    ;

default  ::= 'default' ':' body ;

body     ::= block | statement  ;

block    ::= '{' (newline|statement)* '}' ;

...

```

Now I'm going to tell you how to use `EBNFParser` to write a parser for `Lisp` quickly.

- Install
    
    `pip install -U EBNFParser`


- Write a file and name it as `lispGrammar` with following content.

    ```BNF
    Atom    := R'[^\(\)\s\`]+'; # use Regex
    # define a literal parser. `Atom::= R'[^\(\)\s\']+'` is ok, but the ast parsed from the two is a little different with each other.

    Expr  Throw ['\n'] 
        ::= Atom 
            | Quote 
            | C'(' (NEWLINE* Expr* NEWLINE*)* C')' ; 
    # C-prefix announces a character parser.

    Quote ::=  C'`' Expr ;
    NEWLINE := C'\n' ;
    Stmt Throw ['\n'] ::= (NEWLINE* Expr* NEWLINE*)* ;

    ```

- Generate your parser and tokenizer.

    `ruiko ./lispGrammar ./lispParser.py -comment True`

- Test your parser.

    ```shell
    python testLang.py Stmt "(+ 1 2)" -o test
    Stmt[
        Expr[
            "("
            Expr[
                "+"
            ]
            Expr[
                "1"
            ]
            Expr[
                "2"
            ]
            ")"
        ]
    ]
    ```

    Moreover, here is a result in `JSON` format at [test.json](https://github.com/thautwarm/EBNFParser/tree/master/tests/Ruikowa/Lang/Lisp/test.json).


## Usage 

- Command Line Tools
    - `ruiko`.

    ```shell
    ruiko <grammar File> 
            <output Python File(endswith ".py")>
            [-comment <True/False>] # whether any comments in your grammar file.
    ```
    Use command `ruiko` to generate parser and token files, and then you can use `testLang.py` to test your parser.

    ```shell
    python testLang.py <AST Name> "<your codes>"
    ```

- APIs  

    I'll write a documentation for EBNFParser's APIs very sooner.


## Source

- [Source of Ruikowa](https://github.com/thautwarm/EBNFParser/tree/master/Python/Ruikowa)
- [Core : Node.py](https://github.com/thautwarm/EBNFParser/tree/master/Python/Ruikowa/ObjectRegex/Node.py)
- [Bootstrap Compiler](https://github.com/thautwarm/EBNFParser/tree/master/Python/Ruikowa/Bootstrap)

Will support C# and Elixir sooner.


## License  
[GPLv3.0](./LICENSE)

    













