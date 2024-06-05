import pandas as pd
import numpy as np
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
                                    if self.first[production[j]] not in self.follow[symbol]:
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
      for non_terminal, productions in self.productions.items():
          for production in productions:
                for a in self.first_product(production):
                    if a!="ε":
                        self.sparse_table.at[non_terminal,a]=production
                if production==["ε"]:
                    for j in self.follow[non_terminal]:
                        self.sparse_table.at[non_terminal,j]=production
      #panic mode
      for non_terminal in self.non_terminals:
          for follow in self.follow[non_terminal]:
              if pd.isna(self.sparse_table[follow][non_terminal]):
                  self.sparse_table.at[non_terminal,follow]="Sync"

grammar = Grammar({
    "E": [["T", "E'"]],
    "E'": [["+","T","E'"], ["ε"]],
    "T": [["F","T'"]],
    "T'": [["*","F","T'"], ["ε"]],
    "F":[["(","E",")"],["id"]],


},{"id","+","*","(",")","ε"},{"E","E'","T","T'","F"},"E")
grammar.calculate_first()
grammar.print_first()

grammar.calculate_follow()
grammar.print_follow()

grammar.fill_sparse_table()
print(grammar.sparse_table)

















