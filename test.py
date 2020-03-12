from lark import Lark, Tree
import logging
logging.basicConfig(level=logging.DEBUG)

collision_grammar = '''
    ?start: form

    CONS: "C"
        | "D"

    VAR: "x"
        | "y" 
        | "z"

    ?form: "("form "\land" form")" -> and
      | "("form "\lor" form")" -> or
      | "("form "\implies" form")" -> implies
      | "("form "\iff" form")" ->iff
      | "neg" form -> neg
      |"("CONS"="VAR")" -> eq
      | "("VAR"="VAR")" -> eq
      | "("CONS"="CONS")" -> eq
      | "("VAR"="CONS")" -> eq
      | "P("VAR","VAR")" -> p
      | "Q("VAR")" -> q
      | "\exists" VAR form -> exists
      | "\forall" VAR form -> forall
      | VAR
      | CONS
    
    %ignore " "

'''
p = Lark(collision_grammar, parser='lalr', debug=True)
r = p.parse("""\forall x ( \exists y ( P(x,y) \implies neg Q(x) ) \lor \exists z ( ( (C = z) \land Q(z) ) \land P(x,z) ) ) """)
print(r.pretty())