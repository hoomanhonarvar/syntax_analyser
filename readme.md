# Syntax Analyser

* compiler project part_2 
* implementing syntax analyser for PL language

## Description

In this part of the project, we want to design and implement a syntax analyzer for the PⅬ language.
The parser receives a sequence of tokens extracted by the lexical parser from a file containing a program in the PⅬ language.
If the program has no syntax errors, it prints the syntax tree in the output, otherwise it reports program errors.
The simplest way to implement a parser is to use a predictive parser.
If the input encounters an error, the compiler must use error recovery methods

## Getting Started

### Dependencies

* reading a lexeme analyser in https://github.com/hoomanhonarvar/lexeme_analyser


### Executing program

* run lexeme analyser 
  
```
python lexeme.py file.pl
```
* new output should be smt like token_list.txt and dataFrame of main_symbol_table

* now run 
```
python syntax_analyser.py tokne_list.txt main_symbol_table.pkl
```



## Authors

Hooman honarvar 

student number :993613063
