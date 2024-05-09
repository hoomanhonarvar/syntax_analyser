import sys
import pandas as pd
path=sys.argv[1]
# path="./test.c"

token_txt=open("token.txt","w")
data=[]
main_symbol_table = pd.DataFrame(data, columns=[ 'word', 'name', 'type','line'])
#adding key words to symbol table

Bool={"word":"bool","name":"T_Bool","type":"keyword","line":0}
Int={"word":"int","name":"T_Int","type":"keyword","line":0}
Char={"word":"char","name":"T_Char","type":"keyword","line":0}
false={"word":"false","name":"T_False","type":"keyword","line":0}
true={"word":"true","name":"T_True","type":"keyword","line":0}
If={"word":"if","name":"T_If","type":"keyword","line":0}
Else={"word":"else","name":"T_Else","type":"keyword","line":0}
For={"word":"for","name":"T_For","type":"keyword","line":0}
Break={"word":"break","name":"T_Break","type":"keyword","line":0}
Print={"word":"print","name":"T_Print","type":"keyword","line":0}
Return={"word":"return","name":"T_Return","type":"keyword","line":0}
Continue={"word":"contintue","name":"T_Contintue","type":"keyword","line":0}

main_symbol_table=main_symbol_table._append(Bool,ignore_index=True)
main_symbol_table=main_symbol_table._append(Int,ignore_index=True)
main_symbol_table=main_symbol_table._append(Char,ignore_index=True)
main_symbol_table=main_symbol_table._append(false,ignore_index=True)
main_symbol_table=main_symbol_table._append(true,ignore_index=True)
main_symbol_table=main_symbol_table._append(Break,ignore_index=True)
main_symbol_table=main_symbol_table._append(Else,ignore_index=True)
main_symbol_table=main_symbol_table._append(If,ignore_index=True)
main_symbol_table=main_symbol_table._append(Print,ignore_index=True)
main_symbol_table=main_symbol_table._append(Return,ignore_index=True)
main_symbol_table=main_symbol_table._append(Continue,ignore_index=True)
main_symbol_table=main_symbol_table._append(For,ignore_index=True)
with open(path,'r') as file:

    line =0
    while True:

        buffer=file.readline()
        if not buffer:
            break
        else:
            line+=1
            T_id=""
            state=0
            buffer_index=0
            end=False
            while not end:
                match state:
                    case 0:         #start state


                        #end
                        if buffer_index >= len(buffer) :
                            token_txt.write("end")
                            # print("end")
                            end=True
                            break
                        #ws

                        if ord(buffer[buffer_index])==32 or ord(buffer[buffer_index])==10 or ord(buffer[buffer_index])==9:
                            state=1
                        #id
                        if ((ord(buffer[buffer_index])>=65 and ord(buffer[buffer_index])<=90) or (ord(buffer[buffer_index])>=97 and ord(buffer[buffer_index])<=122) or ord(buffer[buffer_index])==95):
                            state=2

                        #number
                        if ord(buffer[buffer_index])>=49 and ord(buffer[buffer_index])<=57:
                            state = 3
                        #>
                        if ord(buffer[buffer_index])==60:
                            state = 4
                            buffer_index += 1
                        #=
                        if ord(buffer[buffer_index])==61:
                            state = 5
                        #<
                        if ord(buffer[buffer_index])==62:
                            state = 6
                            buffer_index += 1
                        #!
                        if ord(buffer[buffer_index])==33:
                            state = 7
                            buffer_index += 1
                        # +
                        if ord(buffer[buffer_index])==43:
                            state = 8
                            buffer_index += 1
                        # -
                        if ord(buffer[buffer_index])==45:
                            state = 9
                            buffer_index += 1
                        # *
                        if ord(buffer[buffer_index])==42:
                            state = 10
                            buffer_index += 1
                        # /
                        if ord(buffer[buffer_index])==47:
                            state = 11
                            buffer_index += 1
                        # %
                        if ord(buffer[buffer_index])==37:
                            state = 12
                            buffer_index += 1
                        # &
                        if ord(buffer[buffer_index])==38:
                            state = 13
                            buffer_index += 1
                        # |
                        if ord(buffer[buffer_index])==124:
                            state = 14
                            buffer_index += 1
                        # zero
                        if ord(buffer[buffer_index]) ==48:
                            state = 15

                            buffer_index += 1
                        if ord(buffer[buffer_index])==59:
                            state=16
                            buffer_index+=1
                        #string

                        if ord(buffer[buffer_index])==34:
                            T_id+=buffer[buffer_index]
                            state=17
                        #Char
                        if ord(buffer[buffer_index])==39:
                            state=18
                        #(
                        if ord(buffer[buffer_index])==40:
                            state=19
                        #)
                        if ord(buffer[buffer_index])==41:
                            state=20
                        #{
                        if ord(buffer[buffer_index])==123:
                            state=21
                        #}
                        if ord(buffer[buffer_index])==125:
                            state=22
                        #[
                        if ord(buffer[buffer_index])==91:
                            state=23
                        #]
                        # print(ord(buffer[buffer_index]))
                        if ord(buffer[buffer_index])==93:
                            state=24
                        #,
                        if ord(buffer[buffer_index])==44:
                            state=25


                    case 1:         #white space
                        buffer_index+=1
                        if buffer_index == len(buffer):
                            #send token
                            token_txt.write(str(line)+" :T_Whitespace\n")
                            # print(line," :T_Whitespace")
                            break
                        if ord(buffer[buffer_index]) == 32 or ord(buffer[buffer_index]) == 10 or ord(buffer[buffer_index]) == 9:
                            state = 1
                        else:
                            token_txt.write(str(line)+" :T_Whitespace\n")
                            # print(line," :T_Whitespace")
                            state=0


                    case 2:         #letter
                        # print("hello")
                        T_id=T_id+buffer[buffer_index]
                        buffer_index+=1
                        # print(T_id)

                        if ((ord(buffer[buffer_index])>=65 and ord(buffer[buffer_index])<=90) or (ord(buffer[buffer_index])>=97 and ord(buffer[buffer_index])<=122) or ord(buffer[buffer_index])==95)or(ord(buffer[buffer_index])>=49 and ord(buffer[buffer_index])<=57):
                            state=2
                        else:
                            if T_id not in main_symbol_table.loc[:11, "word"].tolist():

                                id = {"word": T_id, "name": "T_Id", "type": "id","line":line}
                                main_symbol_table = main_symbol_table._append(id, ignore_index=True)
                                token_txt.write(str(line)+" :"+str(len(main_symbol_table.index) - 1)+" "+ T_id+"\n")
                                # print(line," :",len(main_symbol_table.index) - 1, T_id)
                            else:
                                for i in main_symbol_table.loc[:11, ["word", "name"]].values.tolist():
                                    if i[0] == T_id:
                                        token_txt.write(str(line)+" :"+str(i[1])+"\n")
                                        # print(line," :",i[1])
                            T_id = ""
                            state=0

                    case 3:         #number
                        buffer_index+=1
                        T_id = T_id + buffer[buffer_index-1 ]
                        if buffer_index==len(buffer):
                            token_txt.write(str(line)+ " :T_Decimal"+str(T_id)+"\n")
                            # print(line, " :T_Decimal",T_id)
                            T_id=""
                        if ord(buffer[buffer_index])>=48 and ord(buffer[buffer_index])<=57:
                            state=3
                        else:
                            if len(T_id)>1:
                                if T_id[0]=="0" and T_id[1]=="x":
                                    token_txt.write(str(line)+" :T_Hexadicimal "+str( T_id)+"\n")
                                    # print(line," :T_Hexadicimal ", T_id)
                                else:
                                    token_txt.write(str(line)+" :T_Decimal"+str(T_id)+"\n")
                                    # print(line," :T_Decimal",T_id)
                            else:
                                token_txt.write(str(line)+" :T_Decimal "+str(T_id)+"\n")

                                # print(line," :T_Decimal ",T_id)
                            T_id = ""
                            state=0


                    case 4:         #>
                        if buffer[buffer_index] == 60:
                            # >=
                            token_txt.write(str(line)+" :T_ROp_GE\n")
                            # print(line," :T_ROp_GE")
                            buffer_index+=1
                        else:
                            if ord(buffer[buffer_index]) == 32 or ord(buffer[buffer_index]) == 10 or ord(
                                    buffer[buffer_index]) == 9:
                                token_txt.write(str(line)+ " :T_ROp_G\n")
                                # print(line, " :T_ROp_G")
                                state = 1
                            else:
                                state=0

                    case 5:         #=
                        buffer_index+=1
                        if ord(buffer[buffer_index])==61:
                            #==
                            token_txt.write(str(line)+" :T_ROp_E\n")
                            # print(line," :T_ROp_E")
                            buffer_index+=1
                        else:
                            token_txt.write(str(line)+" :T_Assign\n")
                            # print(line," :T_Assign")
                        state=0

                    case 6:         #<
                        if buffer[buffer_index] == 62:
                            # <=
                            token_txt.write(str(line)+" :T_ROp_LE\n")
                            # print(line," :T_ROp_LE")
                            buffer_index+=1
                        else:
                            token_txt.write(str(line)+" :T_ROp_L\n")
                            # print(line," :T_ROp_L")
                            state=0
                    case 7:         #!
                        if buffer[buffer_index] == 61:
                            # !=
                            token_txt.write(str(line)+" :T_ROp_NE\n")
                            # print(line," :T_ROp_NE")
                            buffer_index += 1
                        else:
                            token_txt.write(str(line)+" :T_LOp_NOT\n")

                            # print(line," :T_LOp_NOT")
                            state=0
                    case 8:         #+
                            token_txt.write(str(line)+" :T_AOp_PL\n")

                            # print(line," :T_AOp_PL")
                            state=0
                    case 9:         #-
                        if ord(buffer[buffer_index])>=49 and ord(buffer[buffer_index])<=57:
                            T_id+="-"
                            state=3
                        else:
                            token_txt.write(str(line)+" :T_AOp_MN\n")
                            # print(line," :T_AOp_MN")
                            state=0
                    case 10:        #*
                            token_txt.write(str(line)+" :T_AOp_ML\n")
                            # print(line," :T_AOp_ML")
                            state=0

                    case 11:        #/
                        if ord(buffer[buffer_index])==47:
                            token_txt.write(str(line)+" :T_Comment\n")
                            # print(line," :T_Comment")
                            break
                        else:
                            state=0
                            token_txt.write(str(line)+" :T_AOp_DV\n")

                            # print(line," :T_AOp_DV")

                    case 12:        #%
                        token_txt.write(str(line)+" :T_AOp_RM\n")

                        # print(line," :T_AOp_RM")
                        state=0
                    case 13:        #&
                        if ord(buffer[buffer_index])==38 :
                            token_txt.write(str(line)+" :T_LOp_AND\n")

                            # print(line," :T_LOp_AND")
                            buffer_index+=1
                            state=0



                    case 14:        #|
                        if ord(buffer[buffer_index])==124 :
                            token_txt.write(str(line)+" :T_LOp_OR\n")

                            # print(line," :T_LOp_OR")
                            buffer_index+=1
                            state=0
                    case 15:        #zero
                        if ord(buffer[buffer_index])==120 or ord(buffer[buffer_index])==88:
                            T_id+="0x"
                            buffer_index+=1
                        else:
                            if (ord(buffer[buffer_index])>=65 and ord(buffer[buffer_index])<=70)or(ord(buffer[buffer_index])>=97 and ord(buffer[buffer_index])<=102) or(ord(buffer[buffer_index])>=48 and ord(buffer[buffer_index])<=57):
                                T_id+=buffer[buffer_index]
                                buffer_index+=1

                            else:
                                if len(T_id)>=2:
                                    token_txt.write(str(line)+" :T_Hexadecimal "+str(T_id)+"\n")

                                    # print(line," :T_Hexadecimal ",T_id)
                                    T_id=""
                                    state=0
                                else:
                                    T_id=""
                                    buffer_index-=1
                                    state=3

                    case 16:        #;
                        if buffer_index==len(buffer):
                            token_txt.write(str(line)+ " :T_Semicolon\n")
                            # print(line, " :T_Semicolon")
                            break
                        else:
                            token_txt.write(str(line)+ " :T_Semicolon\n")
                            # print(line, " :T_Semicolon")
                            state=0
                        #"
                    case 17:
                        buffer_index+=1
                        if buffer_index==len(buffer):
                            #error
                            state=-1
                            print("double cotation doesn't end")
                        if ord(buffer[buffer_index])!=92:
                            T_id+=buffer[buffer_index]
                        elif ord(buffer[buffer_index+1])==92:
                            T_id+="\\"
                        if ord(buffer[buffer_index])==34  and ord(buffer[buffer_index-1])!=92:
                            token_txt.write(str(line)+ " :T_String  " +str( T_id)+"\n")
                            # print(line, " :T_String  " , T_id)
                            id = {"word": T_id, "name": "T_String", "type": "String","line":line}
                            main_symbol_table = main_symbol_table._append(id, ignore_index=True)
                            state=0
                            buffer_index+=1

                    # char
                    case 18:
                        T_id+=buffer[buffer_index]
                        buffer_index+=1
                        if ord(buffer[buffer_index])!=92:
                            T_id += buffer[buffer_index]
                            buffer_index += 1
                            T_id += buffer[buffer_index]
                            buffer_index += 1
                            token_txt.write(str(line)+" :T_Character: "+str(T_id)+"\n")
                            # print(line," :T_Character: ",T_id)
                            T_id=""
                        else:
                            T_id += buffer[buffer_index]
                            buffer_index += 1
                            T_id += buffer[buffer_index]
                            buffer_index += 1
                            T_id += buffer[buffer_index]
                            buffer_index += 1
                            T_id += buffer[buffer_index]
                            buffer_index += 1
                            token_txt.write(str(line)+ " :T_Character: "+str( T_id)+"\n")
                            # print(line, " :T_Character: ", T_id)
                            T_id = ""
                        state=0
                    #(
                    case 19:
                        token_txt.write(str(line)+ " :T_LP\n")
                        # print(line, " :T_LP")
                        buffer_index += 1
                        state = 0
                    #)
                    case 20:
                        token_txt.write(str(line)+" :T_RP\n")
                        # print(line," :T_RP")
                        buffer_index += 1
                        state = 0
                    #{
                    case 21:
                        token_txt.write(str(line)+" :T_LC\n")
                        # print(line," :T_LC")
                        buffer_index += 1
                        state = 0
                    #}
                    case 22:
                        token_txt.write(str(line)+" :T_RC\n")
                        # print(line," :T_RC")
                        buffer_index += 1
                        state = 0
                    #[
                    case 23:
                        token_txt.write(str(line)+" :T_LB\n")
                        # print(line," :T_LB")
                        buffer_index += 1
                        state = 0
                    #]
                    case 24:
                        token_txt.write(str(line)+" :T_RB\n")
                        # print(line," :T_RB")
                        buffer_index += 1
                        state = 0
                    #,
                    case 25:
                        token_txt.write(str(line)+" :T_Comma\n")
                        # print(line," :T_Comma")
                        buffer_index += 1
                        state = 0

                    #error
                    case _:
                        end=True
                        print("error")

# print(main_symbol_table.to_string())
main_symbol_table.to_csv("main_symbol_table.csv",index=True)
