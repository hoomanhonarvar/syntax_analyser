import pandas as pd
import numpy as np
from queue import LifoQueue
class Grammar:
  def __init__(self, productions, terminals, non_terminals,start_variable):
    self.productions = productions
    self.terminals = terminals
    self.non_terminals = non_terminals
    self.first = {}
    self.follow = {}
    self.start_variable=start_variable
    self.sparse_table=pd.DataFrame()

  def calculate_first(self):
    for non_terminal in self.non_terminals:
      self.first[non_terminal] = set()
    updated=True
    while updated:
        updated = False
        for non_terminal, productions in self.productions.items():
            for production in productions:
                # print(production)
                for symbol in production:
                    if symbol in self.non_terminals :
                        if not (self.first[symbol].issubset(self.first[non_terminal])) :
                            self.first[non_terminal] |= self.first[symbol]
                            updated = True
                        if 'ε' not in self.first[symbol]:
                            break
                        else:
                            if "ε" not in self.first[non_terminal]:
                                self.first[non_terminal].add('ε')
                                updated = True
                    else:
                        if symbol not in self.first[non_terminal]:
                            self.first[non_terminal].add(symbol)
                            updated=True
                        break

  def calculate_follow(self):
    for non_terminal in self.non_terminals:
      self.follow[non_terminal] = set()
    self.follow[self.start_variable].add('$')
    updated = True
    while updated:
        updated=False
        for non_terminal, productions in self.productions.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol in self.non_terminals:
                        for j in range(i + 1, len(production)):
                            if production[j] in self.non_terminals :
                                if 'ε' not in self.first[production[j]]:
                                    if not self.first[production[j]].issubset(self.follow[symbol]):
                                        self.follow[symbol] |= self.first[production[j]]
                                        updated = True
                                        break
                                else:
                                    if not (self.first[production[j]] - {'ε'}).issubset(self.follow[symbol]) :
                                        self.follow[symbol] |= self.first[production[j]] - {'ε'}
                                        updated = True

                                    if j == len(production) - 1:
                                        if not self.follow[non_terminal].issubset(self.follow[symbol]):
                                            self.follow[symbol] |= self.follow[non_terminal]
                                            updated = True
                            else:
                                if production[j] not in self.follow[symbol]:
                                    self.follow[symbol].add(production[j])
                                    updated=True
                                    break
                    if i == len(production)-1:
                        if symbol in self.non_terminals:
                            if not self.follow[non_terminal].issubset(self.follow[symbol]):
                                self.follow[symbol] |= self.follow[non_terminal]
                                updated = True

  def print_first(self):
    for non_terminal, first_set in self.first.items():
      print(f"First({non_terminal}) = {', '.join(first_set)}")

  def print_follow(self):
    for non_terminal, follow_set in self.follow.items():
      print(f"Follow({non_terminal}) = {', '.join(follow_set)}")

  def first_product(self,production):
      first=set()
      for symbol in production:
          if symbol in self.non_terminals:
              first|=self.first[symbol]
              if 'ε' not in self.first[symbol]:
                  break
              else:
                  first.add("ε")
          else:
              first.add(symbol)
              break
      return first

  def fill_sparse_table(self):

      temp=self.terminals
      temp.remove("ε")
      temp.add("$")
      self.sparse_table = pd.DataFrame(index=list(self.non_terminals), columns=list(temp))
      self.sparse_table=self.sparse_table.fillna("error")
      for non_terminal, productions in self.productions.items():
          for production in productions:
                tmp =self.first_product(production)
                for a in tmp:
                    if a!="ε":
                        self.sparse_table.at[non_terminal,a]=production

                if production==["ε"]:
                    for j in self.follow[non_terminal]:
                        if  self.sparse_table[j][non_terminal]=="error":
                            self.sparse_table.at[non_terminal,j]=production
      # #panic mode
      # for non_terminal in self.non_terminals:
      #     for follow in self.follow[non_terminal]:
      #         if type(self.sparse_table[follow][non_terminal])!="<class 'list'>":
      #             if self.sparse_table[follow][non_terminal]!="ε":
      #               self.sparse_table.at[non_terminal,follow]="Sync"

grammar = Grammar({
    # "Program": [["FunctionDeclarations", "Declarations","Statements"]],
    "Program": [["FunctionDeclarations"]],
    "FunctionDeclarations": [["FunctionDeclaration","FunctionDeclarations"], ["ε"]],
    "FunctionDeclaration": [["Type","T_Id","T_LP","ParameterList","T_RP","Block"]],
    "ParameterList": [["Parameter", "ParameterListPrime"], ["ε"]],
    "ParameterListPrime": [["T_Comma", "Parameter","ParameterListPrime"], ["ε"]],
    "Parameter": [["Type", "T_Id","ArraySpecifier"]],
    "Declarations": [["Declaration","T_Semicolon", "Declarations"], ["ε"]],
    "Declaration": [["Type", "T_Id","ArraySpecifier","AssignmentPrime"]],
    "AssignmentPrime": [["ArraySpecifier","T_Assign","Expression"],["ε"]],
    "Type": [["T_Int"], ["T_Bool"],["T_Char"]],
    "ArraySpecifier": [["T_LB", "Num","T_RB","ArraySpecifier"], ["ε"]],
    "Num":[["T_Decimal"],["T_Hexadecimal"],["ε"]],
    "Statements": [["Statement", "Statements"], ["ε"]],
    "Statement": [["Declaration","T_Semicolon"],["T_Id","StatementPrime","T_Semicolon"],["Assignment", "T_Semicolon"], ["PrintStatement","T_Semicolon"],["Loop"],["IfStatement"],["Block"],["T_Continue","T_Semicolon"],["T_Break","T_Semicolon"],["T_Return","Expression","T_Semicolon"]],
    "StatementPrime":[["FunctionCallPrime"],["AssignmentPrime"]],
    "Assignment": [["T_Id","ArraySpecifier", "T_Assign","Expression"]],
    "PrintStatement": [["T_Print", "T_LP","FormattingString","T_RP"]],
    "FormattingString": [["T_String", "ExpressionsList"]],
    "ExpressionList": [["T_Comma", "Expression"]],
    "ExpressionsList":[["ExpressionList","ExpressionsList"],["ε"]],
    "Assignment_Declaration":[["Assignment"],["Declaration"]],
    "Loop": [["T_For", "T_LP","Assignment_Declaration","T_Semicolon","Expression","T_Semicolon","Assignment","T_RP","Statement"]],
    "IfStatement": [["T_If", "T_LP","Expression","T_RP","Statement","ElsePart"]],
    "ElsePart": [["T_Else", "Statement"], ["ε"]],
    "Block": [["T_LC", "Statements","T_RC"]],
    # "Condition": [["Expression","Condition_tmp"]],
    # "Condition_tmp":[["RO_Expression"],["ConditionPrime"]],
    # "RO_Expression":[["T_ROp","Expression"]],
    # "ConditionPrime": [["T_LOp", "Expression","ConditionPrime"], ["ε"]],
    "Expression": [["Term", "ExpressionPrime"]],
    "ExpressionPrime": [["T_AOp_PL", "Term","ExpressionPrime"],["T_AOp_MN", "Term","ExpressionPrime"], ["ε"]],
    "Term": [["Factor", "TermPrime"]],
    "TermPrime": [["Operation", "Factor","TermPrime"], ["ε"]],
    "Operation":[["Aop"],["T_LOp"],["T_ROp"]],
    "Aop":[["T_AOp_DV"],["T_AOp_ML"],["T_AOp_RM"]],
    "T_LOp":[["T_LOp_AND"],["T_LOp_OR"],["T_LOp_NOT"]],
    "T_ROp": [["T_ROp_NE"], ["T_ROp_E"], ["T_ROp_L"], ["T_ROp_G"], ["T_ROp_LE"], ["T_ROp_GE"]],
    "Factor": [["T_Id","FunctionCallPrime"], ["T_Decimal"], ["T_Hexadecimal"], ["T_Character"], ["T_String"], ["T_True"], ["T_False"], ["T_LOp_NOT","Factor"], ["T_LP","Expression","T_RP"]],
    "FunctionCallPrime":[[ "T_LP","ArgumentList","T_RP"], ["ε"]],
    "FunctionCall": [["T_Id", "T_LP","ArgumentList","T_RP"], ["ε"]],
    "ArgumentList": [["Expression", "ArgumentListPrime"], ["ε"]],
    "ArgumentListPrime": [["T_Comma", "Expression","ArgumentListPrime"], ["ε"]],

},{"T_Id","T_Decimal","T_Hexadecimal","T_Character","T_String","ε",
   "T_ROp_NE","T_ROp_E","T_LOp_AND","T_LOp_OR","T_LOp_NOT","T_Assign",
   "T_LP","T_RP","T_LB","T_RB","T_LC","T_RC","T_Semicolon","T_Comma","T_Bool",
   "T_Break","T_Char","T_Continue","T_Else","T_False","T_For","T_If","T_Int",
   "T_Print","T_Return","T_True","T_AOp_PL","T_AOp_MN","T_AOp_ML","T_AOp_DV",
   "T_AOp_RM","T_ROp_L","T_ROp_G","T_ROp_LE","T_ROp_GE","$"}
    ,{"Program","FunctionDeclarations","FunctionDeclaration","Statement","StatementPrime",
      "ParameterList","ParameterListPrime","Parameter","Declarations","Declaration",
      "AssignmentPrime","Type","ArraySpecifier","Num","Statements","Assignment","ExpressionsList",
      "PrintStatement","FormattingString","ExpressionList","Loop","IfStatement",
      "ElsePart","Block","Condition","RO_Expression","T_ROp","ConditionPrime",
      "T_LOp","Expression","Term","TermPrime","Aop","Factor",
      "FunctionCall","ArgumentList","ArgumentListPrime","Condition_tmp","FunctionCallPrime","Assignment_Declaration","Operation"
      ,"ExpressionPrime"}
    ,"Program")
grammar.calculate_first()
grammar.print_first()

grammar.calculate_follow()
grammar.print_follow()
# pd.set_option('display.max_columns', None)
grammar.fill_sparse_table()
print(grammar.sparse_table)
f=open("token.txt","r")
stack=LifoQueue()
stack.put("$")
stack.put(grammar.start_variable)
panic_mode=False
count =0
for token in f:
    count+=1
    if count%465==0:
        print("hello")
    var =stack.get()
    stack.put(var)
    if token=="end":
        tmp="$"
    else:
        tmp = token.split(":")[1][:-1]
    if tmp!="T_Whitespace" and tmp!="T_Comment":
        if len(tmp.split(" "))>1:
            if tmp.split(" ")[0]=="T_String":
                tmp="T_String"
            elif tmp.split(" ")[0]=="T_Decimal":
                tmp="T_Decimal"
            elif tmp.split(" ")[0]=="T_Hexadecimal":
                tmp="T_Hexadecimal"
            elif tmp.split(" ")[0]=="T_Character":
                tmp="T_Character"
            else:
               tmp="T_Id"

        print(tmp, "   :", stack.queue)

        while var not in grammar.terminals:
            if var=="ε":
                stack.get()
            else:
                if grammar.sparse_table[tmp][var] =="Sync":
                    print("error    i just see sync")
                    stack.get()
                elif grammar.sparse_table[tmp][var] =="error":
                    panic_mode=True


                else:
                    stack.get()
                    for production in reversed(grammar.sparse_table[tmp][var]):
                        stack.put(production)
            var = stack.get()
            stack.put(var)
        # print(grammar.sparse_table[token.split(":")[1][:-1]][var])

        if var in grammar.terminals:
            if tmp!=var:
                print("error")
            else:
                stack.get()
print("done")















