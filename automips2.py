from r import *
# region NOT-CODE
# TODO # ▶ bubble_sort_byte_array £address £length ~ £address £length ⮤ lambda x:[x.replace('byte',t) for t in ['word','byte','half']]
# TODO Δ ⟵ Add line of code to data segment if label not there already: Can only allocate number of bytes
# TODO Δ ƒ.Hello 25*4 ⟵ evaluates the expression as an integer and stores the max seen amount without causing conflicts using .space
# TODO Δ .word ƒ.Hello 3,4,1,4,2 ⟵ If first character is '.' Will cause conflict errors if multiple exist
# TODO: ⮤ at beginning of any line means to 'exec' the pycode while parsing: useful for creating lambdas that are the same across multiple functions
# TODO: ⍿ for ┷ for inlining methods (replaces jr 'method' with it's body copypasted without jumps. This can even be done on recursive methods:  the number of ┷ symbols determines the depth that we do it to: giving it a head-start on anything recursive..). When inlining, WHICH IS PERHAPS BETTER DONE AS A MACRO, you could search and replace the registers inside it to get rid of the swap step usually called before and after 'jr funtction. The macros accept parameters for EVERY register used, except constants, beause then we can assign them to $t0 or $t2 or etc that the function calling it doesn't use.
# swap_right $a3 $a2 $a1
# jal swap_byte_array
# swap_left $a3 $a2 $a1
# Can be replaced with some macro that looks like 'jal_with_swap swap_byte_array $a3 $a2 $a1'  ⟵ SHould be optional: might want to fine-tune things ⟵ This would make inlining much more possible
#

# Why McDonnell might like it: Consistency of formatting, code obfuscation to protect my work, code reusability, higher level explanation for easy debugging, the debugger‚
# At lest should be fine with: Using it for non-hw helper methods
#
#
# PSEUDO MIPS: A higher level than assembly but still lets you code in assembly for fine-tuning etc. Not so high-level that it makes nitpicky things difficult.
# Language must be able to separate things into chunks in lists from indents, function declarations, etc. THen after that it processes them.
# Should keep a .bank of function objects to determine if there are duplicates etc and the number of arguments they have (perhaps a dict?)
# ⓦ 'blt £A 0' or 'beqz £F' or 'some macro that works the same way: accepts a goto LABEL at the end' ⟵ Must have knowledge of what function it's in during translation to name the labels properly!
# ⓦ while (r)repeat (f)for (u)until (i)if () ⟵ Perhaps some (like (f) or (r)) should be in pseudo-pseudo_mips via nested recursion?
# ⓘ blt £A 0 or beqz etc ⟵ Must have knowledge of what function it's in during translation to name the labels properly!
# Label examples: if.if2.if4.goto0  or f.if3
# Most of pseudo_mips is literally written in mips, except for function calls and equations etc, which must be manually called with some unicode symbol, perhaps ⓟ for pseudo.
# ⓟswap x y ⟵ is an example of pseudo_mips ⓟ
# ⓟ is used for lines of code only - not inside statements. Since
# Little trick I discovered: " ⓦ j " is an infinite loop
# ⛤ All functions have: a body, a name, a list of input variables, a list of output variables (can be empty)

"""
SYNTAX DOCUMENTATION:

• There are acronyms such as te, pe, etc... that are defined with .eqv statements in the beginning of the code. Their meanings can be found there. te, for example, is 'times equals', analagous to '*=', which decreases reduncancy. (A*=B is preferable to A=A*B because in the second one, A has to be written twice; which is redundant, thus making it more confusing)
• Pseudo-mips doesn't use keywords. Instead, it uses key Unicode characters. Here they are:
    ▶   ⟵ Function declaration
    ▷   ⟵ TODO: Manual mips function: Yet to be implemented; lets you code the ENTIRE function in mips; bypassing everythig except tomato seed covers. No luxuries such as £. Compiler will still recognize the function name though; that's the important part.
    £   ⟵ £ is analagous to $ (a different kind of currency): upon compilation each one is assigned a register. £Hello, for example, might be replaced with $s4 during compilation.
    ∘   ⟵ Symbol used to call functions that are declared in pseudo-mips. Examples: '∘ f £x' ⟺ 'f(x);'   AND     '∘ £y = f £x' ⟺ 'y=f(x);'. Symbol was chosen because it is associated with functional composition; aka 'f ∘ g' etc.
    =   ⟵ Currently it's only context is with '∘' . Examples: '∘ f £x' ⟺ 'f(x);'
    ⮐  ⟵ Return symbol. Has three different contexts: '⮐ £a £b' , '⮐ £a', and '⮐'. The first two DON'T exit the function; ONLY the last one does. The first two merely specify the outputs of the function (so a function with '⮐ £a ¶ ⮐ £b' will (assuming there's no other code) return £b but not £a; MEANWHILE... a function with '⮐ £a ¶ ⮐ ¶ ⮐ £b' will (definately, for sure) return £ but not £a)
    ⓘ  ⟵ If branch. Example: 'if(a==b)' ⟺ 'ⓘ beq £a £b'
    ⓞ  ⟵ TODO: Not yet implemented: Allows for 'or' on ⓘ, ⓦ, and ⓕ loops. Example: 'ⓘ bgt £i 10 ⓞ ble £i 0 ⓞ bnez £debug'
    ⓑ  ⟵ TODO: Not yet implemented: break out of loops
    ⓔ  ⟵ Else
    ⓦ  ⟵ While
    ⓕ  ⟵ For
    ⓧ  ⟵ End (uses matlab-like syntax for flow control)
    §   ⟵ Safety: Let's say somebody made a macro or fucntion, lets call it function 'f', that changes a temp variable you want saved. According to register conventions, the function acall
    ƒ   ⟵ Refers to the function name of the function currently being defined
    ⇥   ⟵ Add an indent to the mips output (all lines after it carry that indent as well)
    ⇤   ⟵ Subtract an indent from the mips output (all lines after it carry that indent as well)
    ~   ⟵ Used after a function definition to specify which registers you DON'T want to be saved to the stack
    #   ⟵ Used to denote comments in pseudo-mips as well.
    ¶   ⟵ Is similar to '\ n', except that it doesn't get turned into a new line until a bit of preprocessing (which is why '∘ £quotient = [div £numerator £denominator ¶ mflo ◊]' works)
    ⮤   ⟵ Runs python code (Or: yet to be implemented: evaluates python code as string). Has two different contexts: If placed after a function definition, you give it a python function to
    ⮦⮥ ⟵ TODO: Python regions: Yet to be implemented! Runs before any other preprocessing step at all (no exceptions). Top one can use a lambda; bottom one can store the result as a variable in python or run code on it or something. Perhaps somehow making macros in pseudomips?
    Δ   ⟵ Adds a line of code to the data section
    ◊   ⟵ Temporary variable used in brackets []
    [   ⟵ Only used with ◊
    ]   ⟵ Only used with ◊
    Ƭ   ⟵ Really only a special character in the preprocessing stage; but you could screw with the compiler by using this. £Ƭ0, £Ƭ1 etc are used as temp variable names for [ ◊ ] expressions
    ℳ  ⟵ Still dangerous: not finished yet! Works on some methods, but breaks others. Turns functions into macros when the function name starts with this character. '▶ ℳfibbonacci' creates a function called 'fibbonacci' but also creates an inner macro that can be used to assign all used registers, allowing for hyper-efficient inlining.

• Often functions are even easier to make than macros

"""

# Function call
#       out0,out1,out2=f(A,B,C):# Matlab-like syntax: out0=f(A,B,C) is perfectly valid, too: this is expanded via pseudo-pseudo mips to take care of the difference between registers ad labels
#       swap A $s0, swap B,$s1 swap C,$s2 ⟵ (NOT NESSECARILY $s0 $s1 $s2, correct registers should be stored in python function definiton!)
#                                               (ALSO NOTE: swaps are generalized to BOTH labels AND registers!)
#       jal f
#       ⓟout0=$hi#⟵ The output addresses are stored in python's function definition!
#       ⓟout1=$lo#⟵ The output addresses are stored in python's function definition!
#       ⓟout2=label_f.out3#⟵ The output addresses are stored in python's function definition!
#       swap A $s0, swap B,$s1 swap C,$s2
# DOWN THE ROAD:
# ⓟ((f) ∘ (x) (y))⟵ regular function call
# ⓟ(*(f) ∘ (x) (y))⟵ function call where all temps inside of it, which are usually NOT preserved, ARE preserved
# ⓟ((f) ∘ (x) *(y))⟵ also a function call but the *y means "don't preserve y"
# ⓟ((f) ∘ ((x)+(y)) *(y))⟵ also a function call but the *y means "don't preserve y"
#       ⓘf
#       ⓔlse
#       ⓧend
#       ⓦhile
#       ⓕfor ffor
#       ƒ(unction name)

# swap $a1 $a0 $a3 $a1  ⟵ PROBLEM: THIS IS WRONG AND CAUSES ERRORS FORCING YOU TO USE § FOR SAFETY
# jal read_word_array
# swap $a1 $a0 $a3 $a1
# "ΓΔΘΛΞΠΣϒΦΨΩ αβγδϵζηθικλμνξπρστυϒϕχψω"
# LANGUAGE RESTRICTION: Cannot call f(A,A) can only call f(A,B)

# Using more than 18 variables in a method will break the compiler cause then there aren't any registers left (unless I say its ok to use the $a registers etc
# Ordering of the methods doesn't matter, at all
# Comments are only guarenteed to do their job properly if they start at the BEGINNING of a line, with ONE EXCEPTION:
# That one exception is register pushing/popping. If you put a comment that says '#$t0 $t1 ' it will save those registers unless explicitly disabled with the ~ operator at the function definition. This is was a glitch, but not it's a feature - it can be useful if you have macros that might modify some variables that you want saved (for example, my macros use $t0 a lot, but if I want my function to both use that macro but preserve $t0's value, just include $t0 in a comment somewhere in the function)
# To mitigiate this effecy you can use ⮤ # to run it as a python comment instead
# White-space via spaces or tabs don't matter at all, it is only at the end of that white-space that we consider it to be the beginning of a line
# Right now it will compile, even if you ask a method to return values (when it doesn't return anything). It will simply grab whatever's in the return register.
# The unicode keyword-characters can cause problems if they're in string literals or comments (unless that comment starts at the beginning of a line)
# Often spces are really important when giving commands with keywords. ⓘ5==6 would fail whereas ⓘ 5 == 6 would not
# Currently doesn't support using parenthesis for functions. '∘ f ( x )' wont compile but '∘ f x' will
# Some special Keyword-Characters: ▷ ▶ £ ∘ ⮐ ⓘ ⓔ ⓦ ⓕ ⓧ § ⇥ ⇤ ~ = # ¶ ⮤ Δ [ ◊ ]
# Using random hashes for the if-else branches etc is good (instead of numbering them) because if you want to rename them, it's trivial: just use a search and replace throughout the mips code
# ⓕ uses ⓦ in it's implementation, which uses ⓘ in it's definition, which uses ⓘ ⓔ in its definition. The assembly output for those increases in readability from right to left ⓕ, ⓦ, ⓘ, ⓘ ⓔ
# 'zmain' is used in place of 'main' because J. Wong seems to be using a method by that name during grading, and said we'd get 0's if we had a method called 'main'. ALSO, because methods are sorted alphabetically, zmain places the main method near the bottom (if you don't have other z-flavored methods)
# make a function called 'zmain' to get all the macros in default_macros
# ~ can be used to create side effects like multiple  outputs or mainly just for optimization
# ¶:     # ⓕ li £length 0 ; bnez £char ; increment_register £length ¶ ∘ zmain4     ⟵ this is legal syntax!!
# $a0 $v0 § print_int_register £c   ⟵ Forces the compiler to preserve $a0 and $v0 while running that line
# ∘ f £a £b £c ⟵ Good      ∘ f £a £a £b ⟵ bad: contains duplicates in variable arguments: this will break the swapping routine used to call functions
# Anything written before the first function definition can be raw code that gets run (in mips) before any of the functions are defined (Example uses: .eqv)
# In debug mode, each time you enter or exit a funciton, it will record all registers and tell you which function it's entering/exiting; and print out all (but only) the registers which have changed since the last debug call. Very useful for diagnosis of problems.
# TODO: Fix simul search/replace. Using names £l and £length in the same function can cause problems: When search/replacing for £l, £legnth 's l character might be replaced first, resulting in weirdness. Moral: Use completely unique variable names!
# Obfuscation: Destroys all comments. Renames all nameable entities (including labels (function names and data names), macro arguments) to randomly hashed homographic gibberish that looks identical and would require an absurd amount of search/replaces to decipler even a few of them. Shuffles the registers so that arguments might accept a temp, and return the stack pointer (whereas they previously returned $v0). Randomly shuffles the order of the definition of functions. [Treats the code like a deck of cards; ignoring macros, cuts the code into several pieces and uses tons of jump statements to glue it all back together again. It does this several times in a row.]
# Bracketing is a thing you can do now! Use the [◊] characters. You must always specify an output using ◊ or else you'll get a syntax error (courtesy of me protectin' you)
# Bracketing on returns for functions (in one line) makes it really easy to make things more efficient later on if you need to inline that function (which currently can't be done manually) or even more calculate things it does manually; since it can just be copypasta'd and variables renamed. Expressions are useful!
# The debugger is also really useful for profiling the code and figureing out which functions are hogging all the clock cycles. In 20 minutes I was able to bring my program from over 5600 instructions to 1900.
# This language is a HUGE improvement over working with bare mips: you can start out inefficient, but then use the debugger to profile it and make optimizations as needed incrementally, AFTER it does what you need it to!
# Just a bit of optimization; now ⮐ [li ◊ 25] is equally efficient as li $v0 25
# endregion
# region UserInput+﹢
from rp import r
hilo_mode=False
every_line_should_have_a_comment=False
flow_control_hash_length=3
super_safety=False  # Enables creating tons and tons of swappers
obfuscate=False
# region  Only applicable if obfuscate:
obfuscate_with_spaces=False
obfuscate_unindent=True
obfuscate_random_indent_max=3
obfuscate_decoy_label_proportion=.5
# endregion
strip_comments=True or obfuscate and True
function_ordering_method=obfuscate and shuffled or identity  # identity, sorted, shuffled, etc ⟶ You can alphabetize the methods or leave the original order they were written in
show_source_code=False
indent='\t'
post_gist=True and not obfuscate
gist_url_shorten=True# Doesn't matter if not post_gist
mips_debugger_mode=False
show_end_function_call=False# Whether to have '#(End Function Call)' at the end of every '#Function Call: write_word_array($a2, $a3, $a0)' etc
show_bracketed_expression_end=True# Analagous to show_end_function_call except its for bracketed expressions
#region  How simply should control flow be implemented?
optimize_while_loops=True# Primes: 6522 ops vs 6543: Truly tiny gains.
shorten_for_loops=True
if_as_if_else=False
allow_silent_pushpop=True
#region Run the code in python:
isolation_test=False
run_code=False
max_steps=20000
marsjar='/Users/Ryan/Desktop/CSE220/220Mars_Fall17.jar'
asmdir='/Users/Ryan/Desktop/CSE220/'
asmfile='MetamipsOutput.asm'
#endregion
try_to_optimize_return_brackets=True# Will replace ⮐ [li ◊ 358]  with  li $v0 358
main_name="zmain"  # Name of main method. ORIGINALLY called 'zmain'
def obfuscate_hash(func_name=""):
    return "L"+func_name
    # return shuffled(shuffled("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm")[:20]+"ryan")
    # return shuffled("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm")[0]+''.join(shuffled(random_namespace_hash(20)+"ryan"))#They all appear to be random, but EVERY single label generated has the letters 'r','y','a' and 'n' scattered in them somewhere. This would be so easy to overlook if plaigarizing
    import HomographGenerator
    # return func_name+"BOOB"
    # return HomographGenerator.random_name_homograph("OOOOOOOOOOOOOO")
    # return func_name
    # Method 1:
    # return ''.join(shuffled(["_."] * 100 + ["_"] * 100))
    # Method 3:
    #     return ''.join('_'*randint(1000,2000))
    # Method 2:
    #     import HomographGenerator
    #     return HomographGenerator.random_name_homograph('OOOoooohhhTrumpIsKinky')
    # Method 5: Rick Roll
    return HomographGenerator.random_name_homograph("oooooohhhhh.") + random_element(['NeverGonnaGiveYouUp','NeverGonnaLetYouDown','NeverGonnaRunAroundAndDesertYou','NeverGonnaMakeYouCry','NeverGonnaTellALieAndHurtYou','NeverGonnaSayGoodbye'])
# endregion
#endregion
# Processdatagram Questions: Very very cryptic output
examples=\
''''''
# Changed:Replace1st (should be fixed 100% now)
code=0*examples+\
"""
▶ clear_board £board £num_rows £num_cols
    lbei £end £num_rows 1
    te £end £num_cols
    pe £end £board
    lz $0 #Can never be too safe
    ⓕ move £i £board ; blt £i £end ; pei £i 2
        sh $0 (£i)
    ⓧ

▶ merge_left_to_right £r £l
    #Macros read(out,array,index) and write(in,array,index)
    ⓕ l1 £i ; blt £i £l ; inc £i
        addi £j £i -1
        read £a £r £j
        read £b £r £i
        ⓘ beq £a £b
            ⓘ bne £a -1
                add £a £a £b # a*=2 AKA a=2*b AKA a+=a etc
                write £a £r £j
                li £a -1
                write £a £r £i
            ⓧ
        ⓧ
    ⓧ

▶ merge_row £A £w £h £r £d
    # A ≣ Array     = board address
    # h ≣ height    = number of rows
    # w ≣ width     = number of columns
    # r ≣ row       = the row # to merge
    # d ≣ direction = 0 for ⟶≣left-to-right, 1 for ⟵≣right-to-left
    # if ( d = 1 ≣ ⟵ )
    ⓘ beq £d 1
        # X = A+2((r+1)w-1)
        ⇥
            addi £X £r 1 # X = r + 1
            te   £X £w   # X *= w
            dec  £X      # X -= 1
            pe   £X £X   # X += X ≣ X *= 2
            pe   £X £A   # X += A
        ⇤
        li £Δ -2 # Δ = -2
    ⓔ
        # assert d = 0 ≣ ⟶
        ⓘ bnez £d
            ⮐ [li ◊ -1]
            ⮐
        ⓧ
        # X = A+2rw
        ⇥
            mul £X £r £w # X = rw
            pe  £X £X    # X += X ≣ x *= 2
            pe  £X £A    # X += A
        ⇤
        li £Δ 2 # Δ = 2
    ⓧ
    merge read_half write_half £X £w £Δ £a £b £i £j


▶ check_state £A £h £w
    # First scan for -1 or 2048, then scan for duplicates.
    # for( i=A ; i<A+2*h*w ; i+=2 )
    ⓕ move £i £A ; blt £i [add ◊ £A [mul2 ◊ [mul ◊ £h £w]]] ; pei £i 2
        lh £x (£i) # x = *i
        ⓘ beq £x -1
            # If any cell contains -1, return 0 because the game can still go on
            ⮐ [li ◊ 0]
            ⮐
        ⓧ
        ⓘ bge £x 2048
            # If any square contains value ≥ 2048, return 1 because the user won
            ⮐ [li ◊ 1]
            ⮐
        ⓧ
    ⓧ



    lz £i         # i=0
    addi £Δ £w -1  # Δ=w-1
    mul £z £h £w   # z=h*w
    l1 £c          # c=1
    # Python Code for the below section: https://goo.gl/PC6b6Z
    # while True:
    ⓦ j
        lh £a ([add ◊ £A [mul2 ◊ £i]]) # a=l[i]
        pe £i £w   # i+=w
        # if i<z:
        ⓘ blt £i £z
            lh £b ([add ◊ £A [mul2 ◊ £i]]) # b=l[i]
            ⓘ beq £a £b
                pstrl "FOUND a="
                pint £a
                pstrl ", b="
                pint £b
                pstrl ", i="
                pint £i
                pl
                li $v0 0 #Game can continue because there are duplicates
                ⮐
            ⓧ
        ⓧ
        me £i £Δ #i-=Δ
        ⓘ bge £i £z
            li $v0 -1 # There are no duplicates. You lose!
            ⮐
        ⓧ
        ⓘ bne £c £w
            inc £c
            lh £b ([add ◊ £A [mul2 ◊ £i]]) # b=l[i]
            ⓘ beq £a £b
                pstrl "FOUND a="
                pint £a
                pstrl ", b="
                pint £b
                pstrl ", i="
                pint £i
                pl
                li $v0 0 #Game can continue because there are duplicates
                ⮐
            ⓧ
        ⓔ
            l1 £c
        ⓧ
    ⓧ

▶ user_move £A £h £w £d
    # assert d in 'LRUD'
    ⓘ bne £d 'L'
        ⓘ bne £d 'R'
            ⓘ bne £d 'U'
                ⓘ bne £d 'D'
                    j ƒ.fail
                ⓧ
            ⓧ
        ⓧ
    ⓧ
    beq £d 'R' ƒ.horz
    ⓘ beq £d 'L'
        ƒ.horz:
        #Next sw line: MIGHT need to switch this OR might even need to swap the shift's direction
        sw [seq ◊ £d 'L'] 4($sp)
        ⓕ lz £i ; blt £i £h ; inc £i
            sw £i ($sp)
            #
            jal shift_row
            beq $v0 -1 ƒ.fail
            jal merge_row
            beq $v0 -1 ƒ.fail
            jal shift_row
            beq $v0 -1 ƒ.fail
        ⓧ
        jal check_state
        move $v1 $v0
        li $v0 0
        ⮐
    ⓧ

    beq £d 'U' ƒ.vert
    ⓘ beq £d 'D'
        ƒ.vert:
        #Next sw line: MIGHT need to switch this OR might even need to swap the shift's direction
        sw [seq ◊ £d 'U'] 4($sp)
        ⓕ lz £i ; blt £i £w ; inc £i
            sw £i ($sp)
            #
            ⮤ ##Needs £A £h £w £d §
            jal shift_col
            beq $v0 -1 ƒ.fail
            jal merge_col
            beq $v0 -1 ƒ.fail
            jal shift_col
            beq $v0 -1 ƒ.fail
        ⓧ
        jal check_state
        move $v1 $v0
        li $v0 0
        ⮐
    ⓧ

    j ƒ.pass
    ƒ.fail:
    ⮐ [li ◊ -1] [li ◊ -1]
    ⮐


# .macro merge %Read %Write %v0 %X %l %Δ %a %b %i %j
# 	# Δ is element size for read and write in bytes. s == 2*num_col or s == 2
# 	# X is address of row/col
# 	# l is length of  row/col in elements
# 	# a,b,i,j are temporary variables
# 	# read, write are macros in the form read(value,array,index,element_size) and write(value,array,index,element_size,temp) write/read halfwords
# def shift_left_to_right(X):
#     l=len(X)
#     c=0
#     for i in range(l):
#         x=X[i]
#         if x!=-1:
#             X[c]=x
#             c+=1
#     x=-1
#     while c<len(X):
#         X[c]=x
#         c+=1
#     print(X)
▶ ℳshift £X £l
    lz £c
    ⓕ lz £i ; blt £i £l ; inc £i
        %read £x £X £i £Δ #x=X[i]
        ⓘ bne £x -1
            %write £x £X £c £Δ £temp #X[c]=x
            inc £c
        ⓧ
        ln1 £x
    ⓧ
    ⓦ blt £c £l
        %write £x £X £c £Δ £temp #X[c]=x
        inc £c
    ⓧ



"""
code='''
.text
.macro abbc %a %b %c
j ybezfrxlazaunuubqms
nbgygnrxayevcnvsscn:
j mssrhuunjxfwwyiinan
ypyyuyahrdkbapwnpqg:
%a %b %b %c
j ixyhbvrxxppsanuascw
ybezfrxlazaunuubqms:
j ypyyuyahrdkbapwnpqg
ixyhbvrxxppsanuascw:
j nbgygnrxayevcnvsscn
mssrhuunjxfwwyiinan:
.end_macro
.macro pe %a %b
j ojydwesrnendtvafwsl
rdevsynprewupainoua:
abbc add %a %b
j nroaocrtzmtykhuxkah
ojydwesrnendtvafwsl:
j fdinykxatrnzrdicytn
nroaocrtzmtykhuxkah:
j rtrvxdseyvcyfsaypny
fdinykxatrnzrdicytn:
j rdevsynprewupainoua
rtrvxdseyvcyfsaypny:
.end_macro
.macro pei %a %b
j ddvyrzartyunevvsrua
ygvsjriwvrfpnkdanto:
abbc addi %a %b
j njfbyrfsynjwybaywqc
utnwyqjjkwadbvrrgvi:
j gjenplysnbncpxdreaa
ddvyrzartyunevvsrua:
j utnwyqjjkwadbvrrgvi
gjenplysnbncpxdreaa:
j ygvsjriwvrfpnkdanto
njfbyrfsynjwybaywqc:
.end_macro
.macro inc %a
j mtkdtfoiorzahynnyan
qtvlwytyvblrenljawy:
j tnkrunvadtyqrkgqqbw
agrdmcxgvpmhmydccyn:
pei %a 1
j wmypfndrnalrwigpbio
mtkdtfoiorzahynnyan:
j agrdmcxgvpmhmydccyn
wmypfndrnalrwigpbio:
j qtvlwytyvblrenljawy
tnkrunvadtyqrkgqqbw:
.end_macro
.macro me %a %b
j yainwuvkfgdtubybcro
ttrrlflgnamivkpnbyv:
j rybadulmhpkrcnqkvjy
hyoalrknzigxqlpjsui:
abbc sub %a %b
j qctzalgihykkbavnycr
yainwuvkfgdtubybcro:
j hyoalrknzigxqlpjsui
qctzalgihykkbavnycr:
j ttrrlflgnamivkpnbyv
rybadulmhpkrcnqkvjy:
.end_macro
.macro mei %a %b
j dxnbwcrsxamynyhmria
qaynflnnaqliryonzxq:
addi %a %a -%b
j pynhraiuaqkinggfyla
dxnbwcrsxamynyhmria:
j qjxknruaryqkuzhnwja
pynhraiuaqkinggfyla:
j kxqiafanadnyygzrbxa
qjxknruaryqkuzhnwja:
j qaynflnnaqliryonzxq
kxqiafanadnyygzrbxa:
.end_macro
.macro dec %a
j ernmevybwplrnrkafea
jlrnyxfmxayqlhtnvma:
mei %a 1
j arrptgknginoszfhwyx
tmopqyjvyrbrgnraabc:
j zyxikzglunyjrzaxvrh
ernmevybwplrnrkafea:
j tmopqyjvyrbrgnraabc
zyxikzglunyjrzaxvrh:
j jlrnyxfmxayqlhtnvma
arrptgknginoszfhwyx:
.end_macro
.macro te %a %b
j mlpfbrybnrfangglhyg
teoemvrjycfgpnvuauj:
j nwcrgtwkqapdmykagur
atnppvjhksrjplacury:
abbc mul %a %b
j cnwqnhcgbcryzcovail
mlpfbrybnrfangglhyg:
j atnppvjhksrjplacury
cnwqnhcgbcryzcovail:
j teoemvrjycfgpnvuauj
nwcrgtwkqapdmykagur:
.end_macro
.macro lbei %a %b
j aklmkzyalntzcnyrikn
fnaysyrjrmaljjmcazy:
j dqxcryrnxdnraemreyf
aacsheqvjvrxncdyxlb:
abbc sll %a %b
j ntqwlcbaxplxdymlxra
aklmkzyalntzcnyrikn:
j aacsheqvjvrxncdyxlb
ntqwlcbaxplxdymlxra:
j fnaysyrjrmaljjmcazy
dqxcryrnxdnraemreyf:
.end_macro
.macro ae %a %b
j ygaryizooylcovkntsn
ljebrzgyrsjcyurnayn:
j uvarlnmcgpxfcbqiybp
xcknqybmrervabahknr:
abbc and %a %b
j akbfswanrnliyfblqhu
ygaryizooylcovkntsn:
j xcknqybmrervabahknr
akbfswanrnliyfblqhu:
j ljebrzgyrsjcyurnayn
uvarlnmcgpxfcbqiybp:
.end_macro
.macro mul2 %a %b
j rlufwmydibyzmnabqnb
nnkyysnqbzccrgnphap:
j cebltpktayntrnybsoz
nwprlglmxnraysvildn:
add %a %b %b
j ksualhbcnyudoryinlk
rlufwmydibyzmnabqnb:
j nwprlglmxnraysvildn
ksualhbcnyudoryinlk:
j nnkyysnqbzccrgnphap
cebltpktayntrnybsoz:
.end_macro
.macro lz %x
j nkjrbwaopduzytvaoxr
nqlidwoaljafgbryodj:
li %x 0
j xgirqnrlouaydljajni
xxdpwicnbyyiarwaxis:
j ieoreheraskohhyzjyn
nkjrbwaopduzytvaoxr:
j xxdpwicnbyyiarwaxis
ieoreheraskohhyzjyn:
j nqlidwoaljafgbryodj
xgirqnrlouaydljajni:
.end_macro
.macro l1 %x
j zkardrnxybznzrypldh
bfjpyubtapoinlfxrct:
li %x 1
j enqyxgrzrdykpanimnt
rayqoncaroznkmeyaha:
j kqryqairppdgrqbxksn
zkardrnxybznzrypldh:
j rayqoncaroznkmeyaha
kqryqairppdgrqbxksn:
j bfjpyubtapoinlfxrct
enqyxgrzrdykpanimnt:
.end_macro
.macro ln1 %x
j ayozofqrwrkzmnekcvf
rodiwyqvarneivdevcy:
j wpneymjkjrocwalnxar
rqznukrdaubtylhncoi:
li %x -1
j pxgnrrtmcevgvjlkayu
ayozofqrwrkzmnekcvf:
j rqznukrdaubtylhncoi
pxgnrrtmcevgvjlkayu:
j rodiwyqvarneivdevcy
wpneymjkjrocwalnxar:
.end_macro
.macro stack_op %f %reg %num
j ndgyninaxrfrykagumg
rnytfhsiluasyrllyte:
%f %reg %num($sp)
j wytjrrhotbznapnvlex
ndgyninaxrfrykagumg:
j mrymmggxaytirnriaka
wytjrrhotbznapnvlex:
j gcufaaytygriewayknv
mrymmggxaytirnriaka:
j rnytfhsiluasyrllyte
gcufaaytygriewayknv:
.end_macro
.macro stack %f

j vtcbbabyrrjlnmykbjm
vtcbbabyrrjlnmykbjm:
.end_macro
.macro stack %f %0
j denmygfrnaypabrakjy
atdvdmahdopandrqyts:
⇥
eyiyrsegluwazznphfk:
⇤
nzsyddqaoqgyrfngyfu:
stack %f
j rsychtubnxinwbkwass
ngavkizcytbuvbvyslr:
j eyiyrsegluwazznphfk
aalraxszdbnkgymimbd:
rsychtubnxinwbkwass:
⇥
stack_op %f %0 0
j uhnrgnnbcasamyfqyyt
iwypzjybauenrnttztk:
⇤
j ngavkizcytbuvbvyslr
⇤
uhnrgnnbcasamyfqyyt:
⇥
⇤
najuyrydcbprcdnhsfy:
j yyljrselnulvwrlaoet
j rfyeytawyvruyafpnah
denmygfrnaypabrakjy:
j iwypzjybauenrnttztk
rtjmlttnuiylaxvmrlp:
rfyeytawyvruyafpnah:
j atdvdmahdopandrqyts
yyljrselnulvwrlaoet:
.end_macro
.macro stack %f %0 %4
j soknyhrhtypdrpkaool
ryxpndlqdibehkrfhna:
⇥
j myaniqmxejnhdlzmrhd
surelzlqjymeefanxjx:
j yizkyglanrawauqgwlb
⇥
myaniqmxejnhdlzmrhd:
j nheynarjammfekyibun
rrlcqmtjnuyuztnaafd:
j grohcfalanbkqbyvplc
yizkyglanrawauqgwlb:
j qqnrbhfamibofneaypa
soknyhrhtypdrpkaool:
j surelzlqjymeefanxjx
qqnrbhfamibofneaypa:
⇤
⇤
jarlparkwxenluzpyqv:
⇤
aopmhbtpgfvlybnrxir:
⇥
j rrlcqmtjnuyuztnaafd
⇤
grohcfalanbkqbyvplc:
isrsnwihempxarrtyaa:
stack %f %0
xtebaohwryknaufrngy:
stack_op %f %4 4
j ryxpndlqdibehkrfhna
nheynarjammfekyibun:
.end_macro
.macro stack %f %0 %4 %8
j yrlhnwzhiayadcaujjh
iycdpbufaatdrjkqekn:
⇥
stack %f %0 %4
ojenzzrhemadlrxwuyi:
coyqvxnymyjokamhrig:
j pnsagvllorysivcilmw
rsbaeaaykytidxykszn:
⇤
msvitanbgvytnwyrrzh:
j imnyrxxainyhffrfise
pnsagvllorysivcilmw:
j odhyknanrxmbqgdwygb
jqyyfurzlnvjafdxrac:
j rsbaeaaykytidxykszn
odhyknanrxmbqgdwygb:
stack_op %f %8 8
j fnkfxpsqparyrweknfy
yrlhnwzhiayadcaujjh:
j jqyyfurzlnvjafdxrac
⇤
fnkfxpsqparyrweknfy:
⇤
⇥
j ljabzyonorvpygxicku
⇤
⇥
imnyrxxainyhffrfise:
ykotdbriebpuncqiawy:
j iycdpbufaatdrjkqekn
ljabzyonorvpygxicku:
.end_macro
.macro stack %f %0 %4 %8 %12
j hykorbacenvrbffsycx
xyorxjiwnuaqhxxamot:
⇥
yycvizanacfsrxorutz:
⇤
⇤
j xxjmrwnluuxpcbrwuay
iyjmawvyunyiekoynra:
j vtlusaheihyyencuxrf
xxjmrwnluuxpcbrwuay:
stack_op %f %12 12
tywnwtqjyyyrkiagaiu:
j paytnfrrtnesyltyrnr
⇤
rsdrayrjbxhnaydglgf:
qgeworbeanaryaohhla:
bncbwygcjiyamrgners:
stack %f %0 %4 %8
⇤
j yycvizanacfsrxorutz
vtlusaheihyyencuxrf:
j rsdrayrjbxhnaydglgf
j odvnnnwjlrhnoyxpaga
hykorbacenvrbffsycx:
xlzkznhrvygtrabicda:
⇥
j iyjmawvyunyiekoynra
odvnnnwjlrhnoyxpaga:
j xyorxjiwnuaqhxxamot
paytnfrrtnesyltyrnr:
.end_macro
.macro stack %f %0 %4 %8 %12 %16
j hdzdityavsijmqgrcny
rfdgxwdjialuygknrlc:
⇥
stack_op %f %16 16
dxrrxnaiyfboyadtsls:
⇤
kmtfeunyrqyeuoaxnqx:
j wybqaqhfjtrznynzlsa
⇤
⇥
azltciplvdaeepuynir:
hgkaryvdgnmzapvsino:
⇤
⇤
j dusrananfudkabfjyyg
wybqaqhfjtrznynzlsa:
j rgbmrctiyagxnxouvgd
dusrananfudkabfjyyg:
j hryriavkwikyngltysf
yymmedmjpnmzljhruqa:
j hgkaryvdgnmzapvsino
hryriavkwikyngltysf:
j jvtnypkzaxuuhrgunnf
hdzdityavsijmqgrcny:
j yymmedmjpnmzljhruqa
jvtnypkzaxuuhrgunnf:
lcqfyarjgxnykvsfisa:
⇥
stack %f %0 %4 %8 %12
j rfdgxwdjialuygknrlc
rgbmrctiyagxnxouvgd:
.end_macro
.macro stack %f %0 %4 %8 %12 %16 %20
j ywwjgapuerdnmryupmd
cusavyluzrtganpbeoj:
stack_op %f %20 20
yamgvsngnhryzrqlubo:
j daxreyndybwlhjvflca
⇤
ylnrktkhavcvyorwwam:
j acvmvrphndxkevysman
daxreyndybwlhjvflca:
⇥
j bnxnwbrsqacngrerhxy
⇤
⇤
j yakrysyepsdtnnehfhm
mancgnuociyovsrbfyb:
j ylnrktkhavcvyorwwam
yakrysyepsdtnnehfhm:
⇥
tmayrwaiaenwkhumnma:
acvmvrphndxkevysman:
stack %f %0 %4 %8 %12 %16
mwhararbzniwyihaysn:
nxlrknymukxnklvatdg:
j lirsynnbyaurimyjlvx
ywwjgapuerdnmryupmd:
⇥
⇤
j mancgnuociyovsrbfyb
lirsynnbyaurimyjlvx:
j cusavyluzrtganpbeoj
bnxnwbrsqacngrerhxy:
.end_macro
.macro stack %f %0 %4 %8 %12 %16 %20 %24
⇥
j nyonksiitjdiacxhker
kyagrcnaypltruatoyj:
⇥
stack_op %f %24 24
⇤
⇥
j agtcwwundfnabrayrbu
qygledaiygtsryqnnfx:
ibnyqtyagwpsgzynqkr:
j ereocoaucctbantrgyv
nyonksiitjdiacxhker:
j mdmadbjanyucphqybrb
ereocoaucctbantrgyv:
⇤
⇤
yhljnanwzrckzyzsrxn:
etpmjozyonrroahufbm:
trcndhgtzafbryxcfdr:
stack %f %0 %4 %8 %12 %16 %20
j novnqazzgbnftoyriyu
zpnehxnkktrchmpyakp:
⇤
j qygledaiygtsryqnnfx
⇥
novnqazzgbnftoyriyu:
j xjyxjbmtsgianrayzdr
mdmadbjanyucphqybrb:
j zpnehxnkktrchmpyakp
xjyxjbmtsgianrayzdr:
j kyagrcnaypltruatoyj
agtcwwundfnabrayrbu:
.end_macro
.macro stack %f %0 %4 %8 %12 %16 %20 %24 %28
⇤
j sclkbebjoazyrhplfnj
wrrzyuwjunxxnaxjtyy:
⇤
⇥
j snfwbforltysqivcoca
⇤
nuecizcrqjaznnwyayi:
j dgcbaartxbvnmfpykva
sclkbebjoazyrhplfnj:
j wywsxbqmqrnvazygxzp
dgcbaartxbvnmfpykva:
⇥
⇥
nfkvwbyekyercppdaap:
nruynatwhslnroukaca:
stack %f %0 %4 %8 %12 %16 %20 %24
stack_op %f %28 28
j rezoujnavziykeutwlu
⇥
amdpoityrgkrtpejnzy:
⇤
rhuwaqouycyxanvgcfl:
shehngcxyiuoragndfw:
j nuecizcrqjaznnwyayi
rezoujnavziykeutwlu:
j azbsytfnpzzrozccaaa
wywsxbqmqrnvazygxzp:
j amdpoityrgkrtpejnzy
azbsytfnpzzrozccaaa:
j wrrzyuwjunxxnaxjtyy
snfwbforltysqivcoca:
.end_macro
.macro stack %f %0 %4 %8 %12 %16 %20 %24 %28 %32
j arudqdiqxnpboiacbny
ryjdwwosnjaxrcyxeys:
⇥
stack_op %f %32 32
eakourhayqnzruejkik:
⇤
bncyqxaqzyjvtxrfajg:
j yqrmbiwpcgtnptnaupg
arjknnlpegtarxtyfmq:
⇤
yolnthhyjgulmrnwawr:
j jarknuznsyygvmoxnyn
yqrmbiwpcgtnptnaupg:
znsaekjyparislbxqty:
j azndqhkzvqkjarsytiw
jarknuznsyygvmoxnyn:
⇤
stack %f %0 %4 %8 %12 %16 %20 %24 %28
⇥
j ssacgtrcwynguwmvxkg
arudqdiqxnpboiacbny:
j alrrayoccorqkkhrhqn
⇥
ssacgtrcwynguwmvxkg:
⇤
⇥
j buynnygamuhescdxrvh
alrrayoccorqkkhrhqn:
j yolnthhyjgulmrnwawr
buynnygamuhescdxrvh:
j ryjdwwosnjaxrcyxeys
azndqhkzvqkjarsytiw:
.end_macro
.macro push  %0 %4 %8 %12 %16 %20 %24 %28 %32 %36
j ieonyqltfmrpapiwytm
nwnvrwqqstnlcyhlqae:
mei $sp 40
j lrpmpaonqyvacxpxind
ieonyqltfmrpapiwytm:
j xmqysrlnbkryaqapxdj
⇤
lrpmpaonqyvacxpxind:
⇥
stack sw %0 %4 %8 %12 %16 %20 %24 %28 %32 %36
drankeipvzefbnjiccy:
⇤
j saqnnylhruonueadnmz
overhmrkepnyapusqmg:
⇤
j arcyzntitwuhndglzai
saqnnylhruonueadnmz:
⇥
j mpsznhrplwyqgmkahiv
arcyzntitwuhndglzai:
okntfaaiujvxlymoryu:
aarkyvenkwpsbilertg:
j knhtrfrpphyoyanmeyj
carynonealmqlcknboy:
⇤
xmqysrlnbkryaqapxdj:
j overhmrkepnyapusqmg
knhtrfrpphyoyanmeyj:
j nwnvrwqqstnlcyhlqae
mpsznhrplwyqgmkahiv:
.end_macro
.macro pop   %0 %4 %8 %12 %16 %20 %24 %28 %32 %36
j iojjnpmaxunnebdcrys
wzyrgvypfzabfajnybh:
j bhwmnkrwmojcrnljyaw
azeasyonawrqjuiroml:
⇥
⇤
⇥
rqpkhbpycvfvndidmxa:
naboipatrxpqziziygm:
j sxgyucfrznleyrinata
cqyrgsjpvpafjnwsarv:
j rqpkhbpycvfvndidmxa
sxgyucfrznleyrinata:
dycrsyafdnhicadnycj:
⇥
j ijdawxzysnzznurrxld
iojjnpmaxunnebdcrys:
⇥
j ullasyweyzhrjlpnnok
⇤
ijdawxzysnzznurrxld:
⇤
stack lw %0 %4 %8 %12 %16 %20 %24 %28 %32 %36
j lyasxvuodrjxwzvnydn
ullasyweyzhrjlpnnok:
j cqyrgsjpvpafjnwsarv
lyasxvuodrjxwzvnydn:
pei $sp 40
⇤
ihkivwanrysklrnunoy:
j wzyrgvypfzabfajnybh
bhwmnkrwmojcrnljyaw:
.end_macro
.macro push  %0 %4 %8 %12 %16 %20 %24 %28 %32
j hhgqsanflrzqbetcgyk
utdnrsanrcynljxtykd:
⇤
nlmydeljjlrfmtnkadn:
j uraocnnbwofultvnyya
j bsnsluafmpiryfngudv
atadtnpyvvzhtwewrry:
⇥
j nlmydeljjlrfmtnkadn
bsnsluafmpiryfngudv:
⇥
enhxzgohxgzrqyahgxk:
j rsqnzcbynkjrayyelqr
syrltqdwnfapanycfho:
uraocnnbwofultvnyya:
⇤
mei $sp 36
zlaqnznkwrpxgzryyae:
injnnbbwlmayruslagp:
stack sw %0 %4 %8 %12 %16 %20 %24 %28 %32
⇤
j enhxzgohxgzrqyahgxk
⇤
j cmcfglnqbztyhmrjpay
hhgqsanflrzqbetcgyk:
j atadtnpyvvzhtwewrry
⇥
cmcfglnqbztyhmrjpay:
naqykdaprrnhjrgqkyx:
j utdnrsanrcynljxtykd
rsqnzcbynkjrayyelqr:
.end_macro
.macro pop   %0 %4 %8 %12 %16 %20 %24 %28 %32
j rbysjvnpfvbeamthyhh
dqwmpsrzeyyanlbklao:
⇥
⇤
drwozagalscnaajshyi:
yyqlqkanrudmifaaivf:
⇥
pei $sp 36
j dndwuwcpryjrlxkrfsa
rbysjvnpfvbeamthyhh:
j nryactgrnbdwnmodkcc
dndwuwcpryjrlxkrfsa:
j jpyqpyznfxiryajrata
⇤
nqscpauseuycuruskrs:
slvgyenrenabaispvje:
engvyryeanlttlphnqh:
stack lw %0 %4 %8 %12 %16 %20 %24 %28 %32
j yyqlqkanrudmifaaivf
ldnskshsfzrkmaywqoo:
j nqscpauseuycuruskrs
j rkdyzanbqihclfqnrrc
⇥
btyirlanrnkgcovdrts:
nryactgrnbdwnmodkcc:
j ldnskshsfzrkmaywqoo
rkdyzanbqihclfqnrrc:
⇤
⇤
j dqwmpsrzeyyanlbklao
jpyqpyznfxiryajrata:
.end_macro
.macro push  %0 %4 %8 %12 %16 %20 %24 %28
j ubeojgablosnyysrnyr
nbvizfqazztrnaawwry:
⇤
qyflrnjagwhylfiypov:
j ayhinlzowljyxmracld
axrynanrmwoasecfply:
⇥
⇤
stack sw %0 %4 %8 %12 %16 %20 %24 %28
j bnylyhamlprtygoclre
ayhinlzowljyxmracld:
⇤
aqtnshrvypnnrwrswyb:
j ifdyrrpvtsyasmopknh
⇤
npjaeybrmrisyjthrif:
rjqrabiechmnyehnovu:
j qyflrnjagwhylfiypov
ifdyrrpvtsyasmopknh:
j whmbxtyrjaoqjtnilyw
ubeojgablosnyysrnyr:
j npjaeybrmrisyjthrif
whmbxtyrjaoqjtnilyw:
mei $sp 32
⇥
xrpygwhsnvyhakwbnvt:
onejyvfvgrfejyralyf:
j axrynanrmwoasecfply
j nbvizfqazztrnaawwry
bnylyhamlprtygoclre:
.end_macro
.macro pop   %0 %4 %8 %12 %16 %20 %24 %28
⇥
j vnlqvaqmvgnrkqxckjy
mvplmnhruypbyrlnjua:
stack lw %0 %4 %8 %12 %16 %20 %24 %28
nlorbgquzyncnklacay:
wazdrirbvkiucyzvvan:
⇥
fninqnzpnarsoqjyywn:
j irckeuyryeaanddenkm
⇤
zyfryaniieocacldrsl:
j knwajyuirgrqvarzuhx
irckeuyryeaanddenkm:
⇤
pei $sp 32
⇥
btepibyyrnngjlpaglo:
j nncaizmtrywfhuflcur
vnlqvaqmvgnrkqxckjy:
j srjhxfmckaynpmfumus
nncaizmtrywfhuflcur:
j ubuzzyraqxicatxqkbn
j qngwyvjyxelarayqkkw
srjhxfmckaynpmfumus:
j zyfryaniieocacldrsl
qngwyvjyxelarayqkkw:
⇤
knwajyuirgrqvarzuhx:
⇤
j mvplmnhruypbyrlnjua
ubuzzyraqxicatxqkbn:
.end_macro
.macro push  %0 %4 %8 %12 %16 %20 %24
j gzyvyidrxssjrsqanex
nksndjmqrfnaacvyqug:
⇥
⇤
umyhvkxjnccrhwaudkl:
j yrprjatkqsnxeofpnrh
jrtzyjqhyagfypvfnwi:
j xvbayrzaouuwcpncgkb
⇤
yrprjatkqsnxeofpnrh:
j rnynvfehcmwwawazznn
rtcytaanznqmycpyhbu:
rcuohepagfwkdyqbniu:
anbrqspdsftohaxgfby:
⇤
⇥
j vqwycrjzjlflnazjazr
gzyvyidrxssjrsqanex:
j jrtzyjqhyagfypvfnwi
vqwycrjzjlflnazjazr:
mei $sp 28
pgcslwnraxrndyitplj:
⇤
bgimrfnoebisabhmydx:
⇥
stack sw %0 %4 %8 %12 %16 %20 %24
j umyhvkxjnccrhwaudkl
xvbayrzaouuwcpncgkb:
j anbrqspdsftohaxgfby
j nksndjmqrfnaacvyqug
rnynvfehcmwwawazznn:
.end_macro
.macro pop   %0 %4 %8 %12 %16 %20 %24
j nkrankvbraushjyfshn
trxakncghjktyrqyydc:
⇤
⇥
j xapmlarygixaimawnaz
mrgfuwaycwtzwdywnlb:
j iyhwvayrqnpncgxyrtc
⇥
⇤
xapmlarygixaimawnaz:
akrfhjakyvwnydanrxa:
⇥
ypakqrowacwdranzcyr:
j oipzysidgxnfauprevj
iyhwvayrqnpncgxyrtc:
j snrykpajqwyjvryinjb
zyirxavvnkeawyswzaz:
j mrgfuwaycwtzwdywnlb
xarnaigpnyqplfllvtu:
snrykpajqwyjvryinjb:
stack lw %0 %4 %8 %12 %16 %20 %24
unzpydaviqukflelzrs:
pei $sp 28
j hygyxmmaqlpynbtednr
nkrankvbraushjyfshn:
j zyirxavvnkeawyswzaz
⇤
hygyxmmaqlpynbtednr:
⇤
j trxakncghjktyrqyydc
oipzysidgxnfauprevj:
.end_macro
.macro push  %0 %4 %8 %12 %16 %20
j cnyguomxdrotaazkiyi
gryhfbbairnocktycpz:
mei $sp 24
j grpbykyznqmxadkyrrm
⇥
arkybxpnabvrytvswln:
qxepscaubengwnczkyr:
j atjcrgdzssnadjnytsj
grpbykyznqmxadkyrrm:
stack sw %0 %4 %8 %12 %16 %20
j tyjaxqrynangdoxriny
⇤
atjcrgdzssnadjnytsj:
j ykajnppaedgruyprphg
yqcbtdaruvbrntaaaki:
⇤
⇤
⇤
tyjaxqrynangdoxriny:
⇥
j payhnlgbwilxrxzndix
ykajnppaedgruyprphg:
j hfnyhyrcekmraldvidg
cnyguomxdrotaazkiyi:
j arkybxpnabvrytvswln
hfnyhyrcekmraldvidg:
⇥
aonlgrevyhifgyzjiuu:
iarelxtpkajynaarqzr:
⇥
j gryhfbbairnocktycpz
payhnlgbwilxrxzndix:
.end_macro
.macro pop   %0 %4 %8 %12 %16 %20
j qpraxroovnknqgijymx
xvrtuenlfzmdyunovra:
stack lw %0 %4 %8 %12 %16 %20
⇥
snrrcoqgnmtgzachkfy:
⇤
j frejvestrnsiyanxpgs
qpraxroovnknqgijymx:
j jwuiqrcnewhanvqwysz
frejvestrnsiyanxpgs:
pei $sp 24
j unaqdentykkqlmjcrew
wonacacrnvzliotvdvy:
kbpfrknnkycthieaoln:
j wornnyhdoxceuaruqek
lzcbanshruhttneoyoj:
⇤
unaqdentykkqlmjcrew:
j ioyjnrgjrezzakpkygh
tkmrhhalsrwanuayitz:
jwuiqrcnewhanvqwysz:
⇤
⇥
j wonacacrnvzliotvdvy
ioyjnrgjrezzakpkygh:
⇥
⇤
j mwlncamanysyuaqxorq
wornnyhdoxceuaruqek:
j xvrtuenlfzmdyunovra
mwlncamanysyuaqxorq:
.end_macro
.macro push  %0 %4 %8 %12 %16
j wrlzarluhneajtdtlyn
coaynkfhrsoiykpffdm:
j lwnyajurmktbuzuyung
azirijnuniyoazkkoyc:
j rethympxvzqxkmsxnak
ragkvktkhvgvnvwywvg:
j rdemrjkhnjhlsuoavyp
rethympxvzqxkmsxnak:
mei $sp 20
rmanffhituqtirzhssy:
⇤
rcuvjhmyeucazygcnvb:
j nrknfyjtbtezqbfixas
wrlzarluhneajtdtlyn:
j ragkvktkhvgvnvwywvg
nrknfyjtbtezqbfixas:
⇤
⇥
⇤
vagosscnwykatuqjrpu:
stack sw %0 %4 %8 %12 %16
⇥
j pdrvnusnyaxvkirmvao
rdemrjkhnjhlsuoavyp:
fynuureqavpwlixyuae:
j azirijnuniyoazkkoyc
pdrvnusnyaxvkirmvao:
⇤
j coaynkfhrsoiykpffdm
lwnyajurmktbuzuyung:
.end_macro
.macro pop   %0 %4 %8 %12 %16
j qfrcxnvrnyawykslqjr
ioqdsrapyjcrqbnrdja:
⇥
⇥
⇤
nzaixywlrrthyrbgccj:
pei $sp 20
j ncnfphaemnqfwjbrcye
nsopzqgtxxymatdrayp:
j poghydcnluereldaowc
yijgnhjlaoprrafssrd:
j qycfarhjvxaguojbeun
ukiziyrncsfzeaxwyfa:
j yijgnhjlaoprrafssrd
qycfarhjvxaguojbeun:
⇤
j aurdggnvxyoxhnipvnb
qfrcxnvrnyawykslqjr:
⇤
j ukiziyrncsfzeaxwyfa
aurdggnvxyoxhnipvnb:
⇤
j nsopzqgtxxymatdrayp
iwyjnplrxszieyagnmu:
poghydcnluereldaowc:
stack lw %0 %4 %8 %12 %16
hppbbcflkynuyeravnx:
skyhqmnmarmpjvnohzn:
j ioqdsrapyjcrqbnrdja
ncnfphaemnqfwjbrcye:
.end_macro
.macro push  %0 %4 %8 %12
j fuwoytrnmdarnivsmvh
nhnyyspzrwzaswkftkt:
j anjyvprqebzkpyargjd
⇤
armncapibrrbyhnpkye:
nwohtgpuhaqfrfnykrl:
j qvranzoaqgibfnzysqs
yajsuynxltntkasgorz:
j tiulnrovshwmnooaoey
qvranzoaqgibfnzysqs:
uipwaanvziurrytrvno:
⇥
mei $sp 16
⇤
omyralzgkqrjgflnlkk:
j udyukafytnnhanbqhlr
tiulnrovshwmnooaoey:
j armncapibrrbyhnpkye
gonyxauvruuqtbnqkro:
⇥
udyukafytnnhanbqhlr:
j xwuuyrxgutjqanbniya
fuwoytrnmdarnivsmvh:
j yajsuynxltntkasgorz
⇤
xwuuyrxgutjqanbniya:
stack sw %0 %4 %8 %12
⇤
j nhnyyspzrwzaswkftkt
anjyvprqebzkpyargjd:
.end_macro
.macro pop   %0 %4 %8 %12
j iawooaptmyxolrlndlp
tmxzrtkcawynymlhqxa:
pei $sp 16
j gynlnoxalgrrqevlqch
lfctyaqnmnjzaqayeyr:
j rbdqbyzxrgpbrnamlpy
gynlnoxalgrrqevlqch:
ionmyhlcdrmascbwnqn:
⇥
qxoarkefdgkkjrllynb:
⇤
⇤
j funsrekyygjkxrvdbab
ctnlbragmgawyadjuuw:
stack lw %0 %4 %8 %12
⇥
j gvrnahqiprtwemimeyl
iawooaptmyxolrlndlp:
j lfctyaqnmnjzaqayeyr
gvrnahqiprtwemimeyl:
⇥
⇤
ynnrwefyynhybbzaflk:
j ylewunrlmjmqhvpdhga
zaewakhyuvgicjnqjfr:
rbdqbyzxrgpbrnamlpy:
j ctnlbragmgawyadjuuw
ylewunrlmjmqhvpdhga:
⇤
j tmxzrtkcawynymlhqxa
funsrekyygjkxrvdbab:
.end_macro
.macro push  %0 %4 %8
j pbxirmnacnzuaqrjbcy
apynrcvabauwxjeijgc:
⇥
bmwausvyzbrllinizjx:
arhumyntyurpapxqjdp:
⇥
⇤
mei $sp 12
j rcnyggaisqtrzzjxaby
ybbttzvurczanczcyps:
j vzjcfrygjakdyrdlfdn
bladbpyaagcqnrnmwiy:
rcnyggaisqtrzzjxaby:
kolyevohxkrsccanrhx:
⇤
stack sw %0 %4 %8
j ncyyucxrxbnnmaukpto
nagbfbbpmgzpkkwrvyd:
rljhnyznaqdcdliihcl:
⇤
j nyrlwmazyidtastcfsq
pbxirmnacnzuaqrjbcy:
j ybbttzvurczanczcyps
⇥
nyrlwmazyidtastcfsq:
⇥
j arhumyntyurpapxqjdp
⇤
vzjcfrygjakdyrdlfdn:
j nagbfbbpmgzpkkwrvyd
j apynrcvabauwxjeijgc
ncyyucxrxbnnmaukpto:
.end_macro
.macro pop   %0 %4 %8
j acfemowbrxwfyjfddyn
ijairkguthcfyzxfknf:
⇥
j drnyaabepwkpzurnird
igkfcanwyrbkrzqawjn:
pei $sp 12
⇤
⇥
j bmwahonjyvrxsqgvrus
acfemowbrxwfyjfddyn:
ijunwloltdrnammfaky:
j uykakkeahllwznreyvh
bmwahonjyvrxsqgvrus:
⇤
hmdklayssnchrzprxcw:
wpvabtncpdgvmsnlyrd:
j luggtsgznrisswyslal
drnyaabepwkpzurnird:
stack lw %0 %4 %8
lsznqzatpdzrenfdaky:
j igkfcanwyrbkrzqawjn
⇤
uzaiqahrktsyqpntzvk:
j ranqemlbveiynxjiuju
uykakkeahllwznreyvh:
j uzaiqahrktsyqpntzvk
⇤
ranqemlbveiynxjiuju:
j ijairkguthcfyzxfknf
luggtsgznrisswyslal:
.end_macro
.macro push  %0 %4
⇤
j pmnzrxjvjuwkadoyzco
ctxrrldnyfzvpatowlx:
⇤
wljmfvpryyaiaofhinl:
j nrxrwyepmauymyqppvr
oxwepkdzqarynddqnvb:
uutjrxrxayynlyatqqe:
j vzqaclnvndzmcrjywev
nrxrwyepmauymyqppvr:
mei $sp 8
⇤
⇥
xeavyjaqorzudgvrlwn:
apuwrjlidivyfjkmgpn:
j txrxyjfaetjpgyvqjqn
pmnzrxjvjuwkadoyzco:
j mlkarsqrvihnzxauuyu
⇥
txrxyjfaetjpgyvqjqn:
stack sw %0 %4
⇥
j lfgwdzxrnkhpnlhbtya
⇤
vzqaclnvndzmcrjywev:
j amrgytjjxbltnxohubz
mlkarsqrvihnzxauuyu:
j oxwepkdzqarynddqnvb
amrgytjjxbltnxohubz:
j ctxrrldnyfzvpatowlx
lfgwdzxrnkhpnlhbtya:
.end_macro
.macro pop   %0 %4
j nayuuqruukppncptiaj
uodqizhofyrdsxansdd:
⇤
⇤
j cxiydvryrkyyukwnfao
nluubjwerdaybdntgwv:
j wnkuaibnvpcoryydtzy
nayuuqruukppncptiaj:
j sbfeajrldotfnynmxna
wnkuaibnvpcoryydtzy:
qnhyfpaswlipharyxyv:
⇥
pei $sp 8
j gihnqrgsnirwyghasea
vgukirwmajbngqbyrup:
⇤
pyarcavqnoydfnrmnji:
zhvcnbzlaypoicwrfzm:
j nnvrxrqrnysaqryonvd
cxiydvryrkyyukwnfao:
⇤
⇥
j vgukirwmajbngqbyrup
ephywrlianblacyyzan:
nnvrxrqrnysaqryonvd:
stack lw %0 %4
j nluubjwerdaybdntgwv
sbfeajrldotfnynmxna:
⇥
j uodqizhofyrdsxansdd
gihnqrgsnirwyghasea:
.end_macro
.macro push  %0
j rrnmaymzhkoqriqntpk
cdtfyrmhnfamywhaqqy:
mei $sp 4
⇤
amnlomqyeljjrmkvqmz:
jlnukyjyauwrhghnjci:
j kkiunkryooenbptepqa
rmepkaalnynperjkrhr:
j uagsqgmrnveylkkesho
kkiunkryooenbptepqa:
j rxdtkqycdqnsewabgsm
rrnmaymzhkoqriqntpk:
j rmepkaalnynperjkrhr
rxdtkqycdqnsewabgsm:
stack sw %0
⇥
j naqyrveabptqyhyrlho
runzikcyaypqguommta:
⇤
ihafyqunryqtysfpnab:
j qjfcvxyixwrahrdbnzq
uagsqgmrnveylkkesho:
⇤
⇥
⇤
j runzikcyaypqguommta
chorbnarlwsuzlwpyrk:
qjfcvxyixwrahrdbnzq:
j cdtfyrmhnfamywhaqqy
naqyrveabptqyhyrlho:
.end_macro
.macro pop   %0
j fmzcmqsgbztannhxyrz
yunnymhmzcihmarluep:
⇥
j xuodcahpaxywnhqhnmr
wnntoacxyqogbbmrryb:
j ityswracecxxhnujote
xuodcahpaxywnhqhnmr:
stack lw %0
j hrageynwwuhsyqlhffj
ityswracecxxhnujote:
j cazjuatcfsyawnqtrrd
hrageynwwuhsyqlhffj:
⇥
⇤
enkfxoybsyangyrrtfn:
⇤
pei $sp 4
⇥
j hfikpuryonaaiaelynr
nfayburaosntcjrjpal:
cazjuatcfsyawnqtrrd:
⇥
pnknifoioywazyrikoq:
⇤
gyphwaqcmgsrsxcivnn:
j zvahnbvyreimgancras
fmzcmqsgbztannhxyrz:
j wnntoacxyqogbbmrryb
zvahnbvyreimgancras:
⇤
j yunnymhmzcihmarluep
hfikpuryonaaiaelynr:
.end_macro
.macro push

j wfqmnsyzjrprpsxdanb
wfqmnsyzjrprpsxdanb:
.end_macro
.macro pop

j kantnlactaoyogumrmy
kantnlactaoyogumrmy:
.end_macro
j functions.end #Prevent from running all the functions even if they're not called by anything
.macro validate_dimensions %num_rows %num_cols %v0 %return
j bsjtqvwlaykapnrvnce
asrqeynzjlgaewnuqdd:
⇤
euaayferbpybdnsvhqj:
yytpiudmksaaylbrrna:
fwssnqlbweyyedvurad:
j hocaohbhngvzypuoyry
bsjtqvwlaykapnrvnce:
j tavzyerbfmnvgrrxriz
hocaohbhngvzypuoyry:
⇤
rfgkckcnfuuzyrejwja:
nbfsoyrirxxiiazrazy:
⇤
⇤
awnwxdydnrruscpuepa:
otalrabmgnbxhlyscnq:
j qddrchqytnemkgxzkam
nyriqrfyorsbjlcmkta:
⇥
bge %num_rows 2 pass
⇤
ayqanhrfpssbszjwdpe:
⇤
⇤
rrpbcapintjeyesblhh:
⇤
qajryvrvnztkkwjmaac:
cwjxtykzaxsvslnqrzg:
zwegfsjyrykdnrcannc:
⇤
j wngbyijbrjatodsjoer
sgwpqmxrrvanvlziziy:
j pnhxcyoraayrkahbmwb
qnmacqoayxtrqngeteh:
wngbyijbrjatodsjoer:
bge %num_cols 2 pass
⇤
piyzrvohublqnartqyy:
j yycabtrnegkrlsemkgu
yvpgrnvpjfdzanlgyce:
j sgwpqmxrrvanvlziziy
⇥
⇤
yycabtrnegkrlsemkgu:
⇥
⇤
⇤
j mgcnyrrhtheoeqbhaky
rzefrsvuneqnbarniyc:
⇥
bwsmykzhnblayyonlrh:
⇥
j nyriqrfyorsbjlcmkta
⇥
nboppsasyprdydgrqyi:
mgcnyrrhtheoeqbhaky:
li %v0 -1
j aynupreayeejcnhptcr
⇥
eyabcmhnrcthfvgkcfy:
nyrauohslpljpwxiwro:
⇥
⇤
gayrjiruamfeunscymx:
⇤
⇤
vhbwnceepsyxmjarmxr:
⇥
nplxzywbqyfnqukrcca:
j rzefrsvuneqnbarniyc
⇥
⇤
⇤
aynupreayeejcnhptcr:
⇥
⇤
⇤
j  %return
⇥
⇤
j rvtfahfgqxelawrnylu
tkjmrbmnkhhuvqoxrya:
⇥
⇤
naijnvhpwkzreoirbwy:
fbypjorqnbaxyawpvsr:
j vhbwnceepsyxmjarmxr
rvtfahfgqxelawrnylu:
j tebsyaghjhaizmnrvne
⇤
slefonoxyrsaclvrtrd:
j uaarnawitydseqeunnm
tebsyaghjhaizmnrvne:
⇥
⇤
izaylneoprkycgtertp:
⇥
pass:
j pkaxoweyrxjynpbfzfe
⇤
pnhxcyoraayrkahbmwb:
xntubioozeapryurabk:
qynamosprgzwlnrawxi:
cybaeiwnrikoysbmqxs:
j mysudzyrcycrtawmngr
⇥
⇤
pkaxoweyrxjynpbfzfe:
⇥
dhciqajewzthnqyrrhb:
j tyyfyarvpsmzzrnguhu
vvszptonkjzdyrexapl:
uaarnawitydseqeunnm:
j yvpgrnvpjfdzanlgyce
tyyfyarvpsmzzrnguhu:
⇤
riecvasczynomfchlrf:
⇤
⇤
⇥
j gbndrwxrrntiyggaaqb
ibzyswzuacvcndiutrt:
mysudzyrcycrtawmngr:
⇥
⇤
⇤
j tkjmrbmnkhhuvqoxrya
gbndrwxrrntiyggaaqb:
⇥
⇥
paddyrsxlnfohkynaus:
⇤
⇥
⇥
li %v0 0
yanglulwqkqrafjovup:
j sgatrwzhontquvyxaro
tavzyerbfmnvgrrxriz:
j slefonoxyrsaclvrtrd
sgatrwzhontquvyxaro:
⇤
yxiyguoxabujgryavrn:
palyrdudkwnlkdokiwd:
⇤
⇤
⇥
acrxxcydeafinyxbivz:
⇤
vxpnolvrciqnqyaasoh:
j asrqeynzjlgaewnuqdd
qddrchqytnemkgxzkam:
.end_macro
.macro get_end %end %board %num_rows %num_cols
j ycdkqwnqivdoagrkxaj
qblvsczjluuxcryanzn:
⇤
j rrnybshzgrxgnfsuaru
rgcaaoamzhvyizknjcz:
j motezmrmrnandeykcju
⇤
rrnybshzgrxgnfsuaru:
⇤
⇤
ktjzngqqypabikarwvt:
j aaooyuivcblknunmarx
harnbwyfaazrhgubzdp:
j weitueccviwrlnbkayc
aaooyuivcblknunmarx:
sll %end %num_rows 1
j sbtntyawapuxeqdzrjr
⇥
weitueccviwrlnbkayc:
j rgcaaoamzhvyizknjcz
sbtntyawapuxeqdzrjr:
j mkyynspalgvjfrtbztc
ycdkqwnqivdoagrkxaj:
j harnbwyfaazrhgubzdp
mkyynspalgvjfrtbztc:
te  %end %num_cols
⇥
j czruylreraqbdvmbnyu
⇤
⇥
motezmrmrnandeykcju:
jlfqnnbbtlrskxtayuk:
j zpnwjxdbydrcjafhvnt
⇤
czruylreraqbdvmbnyu:
⇥
pe  %end %board
⇥
xggnyahcsegrraqyxql:
oabeoxskrwynomzbisy:
j frjzatbweyngrirachu
hfjxnoaxdukthgyrmte:
zpnwjxdbydrcjafhvnt:
buddjcrqlclazynzmav:
j qblvsczjluuxcryanzn
frjzatbweyngrirachu:
.end_macro
clear_board:
.macro clear_board.macro %v0 %board %num_rows %num_cols %end %i %n1
j blmsxjkyyrlaireanqb
bplkhyuwnpuryaymjtk:
⇥
j saiaybaryjilyfnfkjd
⇤
nyrwpatiaentvhyhhxk:
runruziyaerwykhndjp:
nhpvhryuaofyipnyrnm:
ayshbnrkrlosgbpcmyh:
⇤
j panltaczoeaqbyjmnmr
⇥
zrpnkkhqutlnbeaycqr:
zngwoncraxqyawoatjv:
j gnvndiuplloyrfqygax
bszcywaawaiypkgihrn:
panltaczoeaqbyjmnmr:
⇤
xaanjnfujgabchyryfv:
onydwhrwmpvagstutyb:
ln1 %n1
ljsnqkkwyruhbfapvny:
yjykkytrwaiiairnppt:
⇥
⇤
j yoqnzuglitednabnrvr
fxnqezvkwfaoaslyfrh:
j mssrlaiggnbfwytwtmn
yoqnzuglitednabnrvr:
⇥
jmtyoartgqdfdrnrron:
gxnxrnaqgbspyayyyha:
egtfymairaacwnrqtsy:
j nhnyejrafbvsbnancvz
areptaarnbnwnyxfbbk:
j pazztvnuurzyqnogubp
⇥
nhnyejrafbvsbnancvz:
move %i %board
bge  %i %end return
⇤
⇥
yntxubalmraztqtinsi:
rnwxrjyjejqvzmmkrta:
sjdatfxnrwyarotlzvh:
rcnarwyaellopfyxdvb:
ilhanddvhowyzjfrnxa:
⇤
j awocayreocdtaqnsokg
⇤
⇥
csxjaxmgqrrlnccgynj:
wrpawovdwmdeynilqkz:
j ryerultrufalnbvaxmd
awocayreocdtaqnsokg:
⇥
hunficbywpvwrzvarih:
uhoafzeynraarrqpgcb:
⇥
⇤
loop:
jdprrjuanokayqhlbnh:
⇥
⇥
⇤
⇥
⇥
iqotiucrplbyrjaunzr:
⇤
⇤
⇤
⇥
jnixyronkavyebskhaz:
⇤
knctyngfrbargozazxi:
⇤
xxyrbvgrkucuxvyvjan:
cedcyrxaqbrovrncmyg:
⇤
lymmjbrfsjaknqneizy:
⇤
⇤
⇤
⇥
⇥
j znlpaowzryennhghylu
bbyvajffabcptrkarun:
j mejugnorygnauruqcaa
⇥
⇤
⇤
⇤
⇥
⇥
znlpaowzryennhghylu:
sh  %n1 (%i)
⇥
⇤
fspjcrpvnnynqmogaxr:
⇥
⇥
yjewratnsksvnfqfzjy:
ystungojaanohbleylr:
pei %i  2
⇤
j kngcrvafesrashvdury
nlaxwiofppgrtcykaaj:
j usowerfxshebrnytyar
kngcrvafesrashvdury:
⇥
⇤
j pvfeagsjanrokhenjyc
gnvndiuplloyrfqygax:
⇤
⇤
j csxjaxmgqrrlnccgynj
letypzzwaqwndxaytcr:
pvfeagsjanrokhenjyc:
⇤
rhywrxbjcnoawfzorxu:
bfgajxnrgapkegjjpqy:
dkudrpyancdarjnyupc:
⇥
⇥
ansifywresgclrqwboy:
j jjnoqzpdznrpvxyuaay
yqrvadrgdagtzznyzss:
j fxnqezvkwfaoaslyfrh
⇥
⇥
jjnoqzpdznrpvxyuaay:
yomcxnpbrhlyaxarpau:
⇥
blt %i  %end loop
⇤
⇤
⇤
kdqxnraipaoxylfbjxu:
giajdalawjkrcrqnsyz:
jqafbtyzmernxibkayn:
⇤
⇤
⇥
⇤
⇥
syyzbzppxnarjjkkkvu:
⇤
myuwaqmkrjgtywyymfn:
iffzartbrnhtittirya:
⇥
⇤
⇤
⇤
⇤
⇤
zecdtugadrvqdstyqnw:
zepsplknhyradeziqwq:
⇤
⇥
oytivrlwlstaglydbno:
⇤
wrtnoaykwjyoswmrdqa:
srarxbkbpydharjnlog:
⇤
⇤
gzhamyzrknymjgsanmg:
⇤
j xckpnvbmkuqlhgayrao
pvnnleylowaixnfryxh:
j yqrvadrgdagtzznyzss
xckpnvbmkuqlhgayrao:
return:
⇥
⇤
efsrdaqexhrzcwisyln:
eoclozaynewsctezvrx:
⇤
⇥
⇤
nxibsrfuzeygjnapqrx:
⇥
uclmhnajxhpwlarvyya:
hiamymyzancboyrnlya:
j wprqhlrzlbvbaqiyvjn
⇤
⇤
ryerultrufalnbvaxmd:
⇥
⇥
⇤
j btxadcfzerhnytyxagy
lrdrgznzukkaxhchiyg:
⇤
wprqhlrzlbvbaqiyvjn:
rwnhydqbqlyfvtaghar:
⇥
j rfgnpwwyqtxsrkyrzaf
usowerfxshebrnytyar:
j areptaarnbnwnyxfbbk
⇤
rfgnpwwyqtxsrkyrzaf:
⇤
nsbtylvvamsxhmnrosk:
j nfabyaylwngxfvxxrlv
⇤
⇥
btxadcfzerhnytyxagy:
⇤
raqpayynushvfnsygyd:
oycktrioxptzrylaann:
⇥
j aynuhhyqleiorbrpbcy
tfahzsthrqyzbmraipn:
⇤
bletaukvrumxwkknysh:
nfabyaylwngxfvxxrlv:
⇤
⇤
⇤
⇤
pxyehrtmdxnhnyaliju:
⇥
j ymyajmvbuzstrngotar
ryxqkqrmaypnhjbbsru:
⇤
plroquibbnyahpjwqmr:
⇤
saiaybaryjilyfnfkjd:
⇥
⇤
⇤
⇤
⇤
wcngrbydacaqlalkhin:
habugvmrahyttzbyncx:
jhblcjfknhkajfrdpyq:
msauyqruuunigoccfqg:
⇤
⇤
wyragjdvnspocpppgfw:
j vmasaxxbtqbrzwfayhn
djayirvpwkrnxhnyzjw:
ptlunbrpyjqzawyhunq:
j bbyvajffabcptrkarun
apjnqdnysrdxrljxxjc:
vmasaxxbtqbrzwfayhn:
⇥
⇥
⇤
ycsnawokjeoyracznyy:
⇤
⇤
j zblyrhncyuaatqquspn
micannrcyzccbjpciqh:
j pvnnleylowaixnfryxh
zblyrhncyuaatqquspn:
⇥
⇤
j rlroyxbjxndvuhafrpy
pazztvnuurzyqnogubp:
⇤
j micannrcyzccbjpciqh
rlroyxbjxndvuhafrpy:
⇤
⇥
⇤
⇥
ouokcrndywbrtpajcmx:
wbenymwtrfbjnksagiu:
ynbyrgzyfkmzricahls:
nqkssezwdbyladfzyhr:
⇤
nyifqrivfaocuorvnsf:
⇤
⇤
⇥
kqgwarvzqkyenbdnais:
⇤
oczyeydasnjahwyjrlg:
karznaglpiypdbizutf:
j qaevdrdivulvyusnppl
⇤
aynuhhyqleiorbrpbcy:
nqzvrsffnkxdzyazral:
⇤
⇤
rofryscdrowxxzgoahn:
j ptlunbrpyjqzawyhunq
⇤
⇥
qaevdrdivulvyusnppl:
validate_dimensions %num_rows %num_cols %v0 return
⇤
nqrrozadtqfuhueonfy:
barfjwrdezgnofufywy:
nmrdcmruuwaymlqvmdt:
⇤
⇥
⇥
utlrybnrjfaxlylnayd:
⇤
⇤
⇤
⇤
get_end %end %board %num_rows %num_cols
⇥
jcyiibnpytbuerxpams:
unyngdoxwoaprzvagay:
⇥
⇤
snreyraeznsjaccwfkr:
⇥
anqyaefcjbcrxlnpusd:
lbtenpkperxaqfbujuy:
ahxkfrbsynauqckynyr:
j cpxhykqfacdtnemrjcl
blmsxjkyyrlaireanqb:
j nlaxwiofppgrtcykaaj
cpxhykqfacdtnemrjcl:
⇤
⇥
⇤
⇥
⇤
urndvrikvbylcofavyk:
⇤
⇤
xjawyovrbnrdyabbzps:
⇤
wniaptyznihfborajwg:
urpyrglbqhnhwtagzlp:
j xaanjnfujgabchyryfv
mrcjyanvndleyljntri:
⇤
⇤
ckaruqhxhpinnynbnjv:
⇥
mejugnorygnauruqcaa:
jvsiamjyrjhrcdznjxj:
⇤
⇥
mwypbdasinkrrbixzhj:
⇥
xbypwrtqnbdzvpnanzk:
j nyrmvzzcwynerqmuazp
mssrlaiggnbfwytwtmn:
⇥
⇤
⇥
j zngwoncraxqyawoatjv
nyrmvzzcwynerqmuazp:
⇥
j bplkhyuwnpuryaymjtk
ymyajmvbuzstrngotar:
.end_macro
clear_board.macro $v0 $a0 $a1 $a2 $t0 $t1 $t2
jr $ra
.macro get_cell %cell %board %row %col %num_cols
j yivamfqvntfprugnsar
jlezpezkdnygnfrqnba:
⇤
j rtwydalytnukemkyunr
kryturdaqbyncfxfcki:
⇥
j hamyytlejgtfrpzbnyr
rtwydalytnukemkyunr:
⇤
fbgnenygdwjxtpdramn:
sll %cell %num_cols 1
te  %cell %row
uqedsnocdkyicraudyz:
htfnwdxgachraqyxskk:
⇤
j jkrxywnzqztnrhdzalb
ugamlxrokhyqdbawvnn:
rnxzxiylxexvavyzsvy:
j ayknzjbvbvbyremltvc
jkrxywnzqztnrhdzalb:
j hrdobbbstrnnayzvdxa
⇥
igpntvnpyanhtjevhzr:
j ugamlxrokhyqdbawvnn
hrdobbbstrnnayzvdxa:
pe  %cell %col
pe  %cell %col
nukklrisyywqagvgorg:
⇤
⇤
⇤
whcarjnnuzloogycucu:
j wyaoesfjvynxglnnrhb
vqepybnkxwrqhyziazr:
⇥
j afnibarhwnyhpkrnbsu
hamyytlejgtfrpzbnyr:
j igpntvnpyanhtjevhzr
afnibarhwnyhpkrnbsu:
j rugryeyaqoqtbhknnej
⇥
yivamfqvntfprugnsar:
j jryzzvginmpgoahrjly
rugryeyaqoqtbhknnej:
⇥
⇤
⇥
⇤
j gkunottulttdglayork
enugxgqhfaytbbtgrik:
gkuyywhrzamrioyhnfp:
mwkpauhunwnyzkardea:
⇤
⇥
⇥
wyaoesfjvynxglnnrhb:
khsamgbsnioyryatskw:
pe  %cell %board
j jdbqqgurukvggwnaywy
⇥
ayknzjbvbvbyremltvc:
iyngkqxadrrjwyqpwqx:
j homltsalwxqrkfseyny
aaslcdqrianowntypuc:
jdbqqgurukvggwnaywy:
alwddynxrskvcayvqnl:
⇤
⇤
⇥
iwqdyfvgaqiamrmnrnl:
⇤
ybtyyjnmvgvadyfrlyy:
⇤
j yyyuzikaqgavbitnpdr
homltsalwxqrkfseyny:
j vqepybnkxwrqhyziazr
⇤
⇥
yyyuzikaqgavbitnpdr:
⇤
⇤
⇤
⇤
gfrvnbycwexjlkawgff:
⇥
j zjsrlcqrnyzdqeauyaw
jryzzvginmpgoahrjly:
j kryturdaqbyncfxfcki
zjsrlcqrnyzdqeauyaw:
j cvyrilnnaitakcvfvjf
uzznrkpsnlyynvqxpna:
vswmrbwnjhtzycbbixa:
⇤
gkunottulttdglayork:
ylusdaxdnrtlryguanu:
maebikidynaqueqrkvh:
⇤
j jlezpezkdnygnfrqnba
cvyrilnnaitakcvfvjf:
.end_macro
.macro validate_cell %cell %end %v0 %return
j qoaihblerybyuhobdnk
khayubaukjrocxnmelg:
⇥
⇤
⇥
j nkioisqawbgbzrzyiah
j lybmyqzianrqzsvfoli
uacnfqzyburenmrvqma:
j yafgnkqlqpryxovrckx
lybmyqzianrqzsvfoli:
⇥
nrataglwkyryxsmqrkm:
⇤
⇥
cvkyamntyengneywrfr:
xsfzwnftriyhlldafsn:
⇤
⇤
j nrydemsamoznhaknaeb
nkioisqawbgbzrzyiah:
j sjayaripnsnfgqobysv
yafgnkqlqpryxovrckx:
yiyceamcnqlnrqnyndz:
⇤
fbhewykrytctrswadan:
⇥
j zusrvayywybckinaiin
sjayaripnsnfgqobysv:
⇤
j xrdgnzwbpufqzkvreay
qoaihblerybyuhobdnk:
j iuynlqrraenpruafwfr
xrdgnzwbpufqzkvreay:
⇥
⇤
⇥
⇥
j jdvaqtyywrwqcwngqwl
zusrvayywybckinaiin:
⇤
j xsfzwnftriyhlldafsn
⇤
⇤
jdvaqtyywrwqcwngqwl:
j yizoyshwfohpcrnhjya
iuynlqrraenpruafwfr:
j nofhynhhllnoahnrpaz
lrbgdajynpdgxthaqyo:
⇤
yizoyshwfohpcrnhjya:
⇤
li %v0 0
tlaubwnamsrqddtyrze:
ywarergphnqkjruzxga:
omniwryafaktueqdrgf:
⇤
ablrcpjbyprbdaeydsn:
j gykvakfnhtmxsgyrfaz
gqiuzyvnzfaegkorean:
j zenacizqpiyzirofhrt
ngmaplflervkbctagly:
j gqiuzyvnzfaegkorean
zenacizqpiyzirofhrt:
⇥
j uacnfqzyburenmrvqma
gykvakfnhtmxsgyrfaz:
rsfsjzunafzjyphwlhi:
⇤
j ltnyfjaqwuthyfjqsrr
⇤
⇤
nrydemsamoznhaknaeb:
⇥
otlcakeernjaavyseji:
blt %cell %end pass
⇤
⇤
⇥
xzqqargaefjgryvkonf:
arcsbaytrfrunahygwh:
jaxtznbrjghotyhyyrj:
li %v0 -1
vfmnzarujcpgrosrlya:
j  %return
⇥
pass:
j nqnrlvlplhtitguarhy
inhxrzpaoewmaigyfno:
ycxyjbburylkurnappr:
nofhynhhllnoahnrpaz:
j ngmaplflervkbctagly
⇥
nqnrlvlplhtitguarhy:
⇤
xarunpqpsvtpyttghxd:
dyqjqogjnfknyxaarac:
⇤
sjmrnahaybyqiiatqkr:
j khayubaukjrocxnmelg
ltnyfjaqwuthyfjqsrr:
.end_macro
.macro validate_row_col %row %col %num_rows %num_cols %v0 %return
j nmdesveriqnpnygtpda
ietrycmnvwtrtjtyawc:
⇤
j dixqzhsbwyjkdgnrxat
eeqygedfafrufarxnfa:
j uymimsgvraworfnhgaf
tthctgcjnymatkhmrdz:
dixqzhsbwyjkdgnrxat:
ylfeyqxzotrfjefoanf:
iivffnnpxabniyfugro:
⇥
⇤
⇤
aducypsshnrtyatnqsp:
⇤
⇤
lebrnzokadauunqrrya:
⇤
⇥
⇤
⇤
⇤
abzuycrabnyqmzzsrsm:
aaxuvynsgjnbaxychlr:
⇥
⇤
qotarwnnjzrgreayhpj:
vifnuxrgecnymlcwlat:
⇥
fail:
⇤
⇥
⇤
nrfypygymurcjzbhsha:
li %v0 -1
⇥
zrrcgejadgameeynrdw:
azhslryhcqrgtjosdnm:
yhdfniwowysvddararu:
⇤
⇥
qukifybyrczqcnmiayq:
⇤
⇥
aphragayibfpvylacnd:
j  %return
pass:
j hfpwtahrwintuaaiytm
mryelyaszbmurnuekgf:
⇤
j mragalcvvynbbmrxqcy
hfpwtahrwintuaaiytm:
j vyfdausxzyhdzqvxnrz
knwaatxqgiwafpysriz:
⇤
j yqrfotnfjahdyyvxktk
vyfdausxzyhdzqvxnrz:
⇤
rxxaanrpcapcplukywr:
⇥
⇥
li %v0 0
j ujtmwnprjwoyaoxrufn
⇥
⇤
⇥
⇤
yyrcolsaergdwnagcjx:
⇥
j iaeuowdpyhordayalnp
fbognxrbnwbwyaurgnr:
⇤
yanjwxvmborybrkfhra:
⇥
⇤
⇤
cnblkytatacrrpxqcfu:
j gybwzjcacepsekernuo
⇤
snfxrdhpaoebobfmzoy:
iaeuowdpyhordayalnp:
wypwtjerxqonlaseyel:
⇤
⇥
⇥
⇤
jyaqntqhghnzurcpnht:
j kzjylwlzornrgddxbma
yqrfotnfjahdyyvxktk:
j gskpqaxdrfnywhuogdf
⇤
kzjylwlzornrgddxbma:
⇤
⇥
xhignoadlycryquiulk:
⇤
bjthjtxfnzrynfzaqct:
ylylyarinzdejaubcbg:
ymbybejcgzatrbdnyoj:
szimuvihkxnysrwjlad:
alamwmoxhsryfthnfqe:
⇤
yqasrwfshzqpdinpxiu:
eyjozrqhmiatrndsqwn:
⇤
lziynevhwxfvravnxav:
noavrjtvsrqrxjsreyr:
⇤
⇤
nxrqyewamdxnjkxuzhv:
bkojunmgknmygrdltay:
ayedarduaaxvrrlnfbu:
⇤
⇥
gxlblaabwyxsxnfzrct:
⇥
⇤
xpxhedrnuzlcynlacer:
j ranuzwrlryypfwalajx
cagxwqnpkskqryogiaq:
adbpvrmyggqgvqfnqya:
j pyirzdeevntdeewyayn
uymimsgvraworfnhgaf:
j zgrzzmtyzndacybuxak
pyirzdeevntdeewyayn:
⇤
qyopwotrnyiwdgjvtar:
xconjavurvroymtoyxo:
atsxgznrlkvnayelccz:
⇤
j cnblkytatacrrpxqcfu
ranuzwrlryypfwalajx:
eknxksamrecmrqoyjko:
⇥
⇤
⇤
⇤
⇤
arxomytrnoydmmxcumb:
⇤
j akrvraeirlmyanlrtso
dnxaqmxymxruhocbkax:
kcckymykyrfnaarxnrh:
⇥
⇤
⇥
⇥
⇥
yyrayhoyxfspncazvpd:
⇥
zscvqytyrrmhwnnlqga:
j wpnomrknapzrwyoccba
⇤
nstagukiyvmetelankr:
neryugizyoargfaqoym:
j fqkeaorgowtesycwtnx
mragalcvvynbbmrxqcy:
j kurfsnawaynprocayxu
fqkeaorgowtesycwtnx:
⇥
⇥
uncrvnhpfrzhuradqgy:
akrvraeirlmyanlrtso:
⇥
xngexhaygrrypczafaz:
bltz %row           fail
yffgdtirzaouuwkansh:
j ydiolaeyhuncbrloibz
j qqnicvnuuramjuqyaer
uaaztlzqnulvrezsywa:
⇤
⇥
j adbpvrmyggqgvqfnqya
qqnicvnuuramjuqyaer:
⇤
rzdphpnndypuowaotww:
⇥
⇥
ychlqqwgazxhnrzpuhs:
⇤
⇥
⇤
wpnomrknapzrwyoccba:
⇤
ntydlryamzrkwodjjct:
czmsqvryanmngzjvudu:
bpuizoyfdgeunnxbbra:
⇤
j eyjozrqhmiatrndsqwn
ydiolaeyhuncbrloibz:
⇤
⇤
⇤
eifanytfxqczyqnvrjr:
⇤
⇥
bltz %col           fail
byvprxheadxroxumbnt:
⇤
veyhlnorwpymxfviazs:
noebvbxamiyavarkfah:
⇤
⇥
⇤
qnoqabxyuoqvdrokhgy:
⇤
⇤
⇤
⇥
⇤
hjtakmbaknnpzifytra:
aznjjvroktdcjyyabbo:
⇥
rkoupemnuafyfxgijwa:
phyluheshnbsviappra:
⇤
⇥
ywandbdterqboalapri:
j rjkcevfboqcfijyhvna
rrykqzjnnamyjdsyeti:
⇤
j eeqygedfafrufarxnfa
pbklrygnfhlldrsavxs:
rjkcevfboqcfijyhvna:
⇥
⇥
j cybwnjerabsrekoqmdn
gskpqaxdrfnywhuogdf:
j rrykqzjnnamyjdsyeti
cybwnjerabsrekoqmdn:
⇥
bge  %row %num_rows fail
j engaunnlbnapuforyzw
nmdesveriqnpnygtpda:
j knwaatxqgiwafpysriz
engaunnlbnapuforyzw:
⇤
⇥
osruarowxlnbrtxlwdy:
⇥
⇥
⇤
j ydnoprekdhmwcbtadcw
zgrzzmtyzndacybuxak:
j mryelyaszbmurnuekgf
ydnoprekdhmwcbtadcw:
⇥
⇥
⇤
⇤
⇥
j aoysrisaojnhiumjxsi
⇥
jqugyyaxfrfarjnuczf:
gybwzjcacepsekernuo:
jyxngakaointvmeoikr:
j yyrayhoyxfspncazvpd
⇤
aoysrisaojnhiumjxsi:
j yxnxbuhnrydygknaxtu
msnwneyiofwhjazrfms:
kurfsnawaynprocayxu:
⇥
⇥
j uaaztlzqnulvrezsywa
yyurifauntgwmrwnmsb:
⇤
yxnxbuhnrydygknaxtu:
⇤
blt  %col %num_cols pass
⇥
⇤
⇥
⇤
⇥
⇤
audfnynzxmydveyzyrl:
j ietrycmnvwtrtjtyawc
ujtmwnprjwoyaoxrufn:
.end_macro
.macro lz_iff_power_of_two %out %x
j vyaarnogfropqfeibce
sndbrdwgsuyzxzntxna:
⇤
fbplbbjarosrlyrnjae:
⇤
vrzoajnfznynafwaojb:
j ghrrohaoundozgyyukj
teidoapiunaryfdafom:
⇤
j pbpnczwaechjuymqerz
ghrrohaoundozgyyukj:
addi %out %x -1
rrnzifqfpajygmuvuyf:
j ceqijcnrytwakunrycz
vyaarnogfropqfeibce:
j dlfuyjvytfmwnaufryf
ceqijcnrytwakunrycz:
ae   %out %x
j jblnbrbzdwrraqlaugy
dlfuyjvytfmwnaufryf:
j teidoapiunaryfdafom
⇤
jblnbrbzdwrraqlaugy:
j szsyapqlrfnrywchaot
nhjvtjyanipqrajripy:
pbpnczwaechjuymqerz:
j sndbrdwgsuyzxzntxna
szsyapqlrfnrywchaot:
.end_macro
.macro validate_value %value %v0 %return
j onziryiqxqacaunsyrz
xvfwoynawdrfanyadbp:
⇥
⇤
⇥
j nherguqelgernkbwayr
srigangwygnidjhaxas:
⇥
⇥
qnyicyraeqvqftyfuby:
⇤
galqvxeqanlnrgrbywx:
⇥
fail:
rdeptszjmyxhahyetqn:
zhzrnciyxaiquyerqfi:
⇥
sxnnmrcvfsatkrcafym:
⇤
j adrwnqnwosrafqlnyze
xqzngruayuxypyjsjwn:
j mbhruhnbwfahrwysnav
adrwnqnwosrafqlnyze:
⇤
⇥
⇥
⇤
⇤
yhjargoqqvaerzuaneb:
⇤
⇥
⇤
⇤
⇤
nalrhwjtmbsavhkbybn:
⇤
⇥
anltjuxzrbvksieyeqo:
⇥
⇥
j rybfarzltrdahsjmnay
⇤
dnrarthwabiyxdcadid:
j kulxyalgntorwnfluui
rybfarzltrdahsjmnay:
⇤
⇤
⇥
⇤
cudmxgzruannomyvqlo:
sqnxzyrammrrlfjoykn:
li %v0 -1
lysnshrrakinyasitin:
sznbnfxjangjeiwjyar:
⇤
uxatrgauypneuywgyng:
⇥
izgernocnvyvahnrzur:
j gsergrfgaqwdcndsykr
wwmnrhtpwbgrgateiyf:
aozbjnrsfirbcjwbyjv:
⇤
j dnrarthwabiyxdcadid
gsergrfgaqwdcndsykr:
j  %return
alrofednnuayockooyx:
⇥
⇤
auytujgnrymbxgbgntj:
⇤
pass.a:
⇤
blt %value 2 fail
⇥
⇤
⇥
⇥
j arrnfaxljazapycknle
onziryiqxqacaunsyrz:
j gsazmnrahrrudalaasy
arrnfaxljazapycknle:
⇤
⇤
⇥
⇥
syyjjurnorsaynnapcf:
⇤
j mnrwuvtxaksdufnfpty
⇤
uthwanasbyvxjpnorys:
j xqzngruayuxypyjsjwn
mnrwuvtxaksdufnfpty:
⇤
hdayqukxoanxrmyigfm:
rbzzpnytkrcolxayyyx:
pphyxpfbxyvlnralupn:
nceawlgerhneodlyrnd:
⇥
⇥
⇤
⇤
⇤
⇤
pass.b:
⇥
⇥
⇥
⇤
⇥
onrxnsuwqatabrmivqy:
⇤
j fwfwxunyrwbcbryvant
j wgpayfxxlwpzsrnegni
tpyrykskmlwuhajnsib:
roankuumzctytorfray:
j yirksvxfzunxzamycji
wgpayfxxlwpzsrnegni:
yzybikuqsvwxnwremza:
⇤
xbykagghrwawnjzmjym:
nherguqelgernkbwayr:
gcdxjirbadyrfblranx:
⇤
⇤
⇥
j zeamfllcxgrunwwyvrf
⇥
⇤
nnbanrwwypdoylmhnrh:
kbdrynacolqsomcujnt:
⇤
⇤
⇤
⇤
⇤
⇥
⇤
fwfwxunyrwbcbryvant:
prwascvbsrjslyfqrqn:
srcqxsaaojdfwpueynx:
ahngxdvrjcmvltyhzny:
uddffphnyrjosyintga:
li %v0 0
⇤
⇤
⇤
pawrrswinctylrqciie:
ntcmndmnzfyutoraiaa:
⇥
j aleumwavnltidrmotay
⇤
aoyylsinmyzprwtcjbx:
⇥
j rqjjynovawjorvdidje
⇥
rarcqeylgdntpshpjqq:
beyadsvipnxgtjqndra:
⇥
j joyanqzkecagnkvfrcs
⇥
rqjjynovawjorvdidje:
⇤
qhibtrajakqpybrnckm:
⇤
j rpacnpnuruyavydpgdt
mbhruhnbwfahrwysnav:
⇤
j rarcqeylgdntpshpjqq
rpacnpnuruyavydpgdt:
⇤
⇤
ywaytfnhzdpcplsmrzv:
hmoqwrbcjynchhoveaa:
j rnjhmmlpatywznkkjci
⇥
joyanqzkecagnkvfrcs:
j urdynkftohvaarkgruw
rnjhmmlpatywznkkjci:
⇤
zeamfllcxgrunwwyvrf:
⇤
compnrjcjzmmpcyctaf:
⇤
⇥
⇤
⇥
tcmsuwrtrnpurgghayt:
unessjrrsfahzzraaey:
urnhajuhcyerkmlbxwn:
zsorexvywerlrnarflc:
xaruvpmhxnbkyxaygwp:
⇤
ajyhbrnkobyomskhkbu:
⇤
enkanywarnyfiyhtryu:
dcrraxnopjkzonlywha:
ynpdrsankpbxatauqmv:
⇥
j anpipbyvqrlunfswfrg
urdynkftohvaarkgruw:
j blnyairdlriodkrznjq
anpipbyvqrlunfswfrg:
⇤
gkcywmvfprvigannzwa:
⇥
nndyalkfrkzgpaeizrv:
uuamdjhweoshyyrener:
jyyezhxhaertstmnqyo:
uwbfbrwubwzyfngrbav:
⇤
⇤
ovhnxuaxxyojcnknerh:
⇤
⇤
pahxrtnxyltorghunnt:
⇥
npzjnrazhnxyppsuvnp:
j obtkwbjudpynxyekarl
blnyairdlriodkrznjq:
mgnjzqsramrkjyxcwsg:
j wwmnrhtpwbgrgateiyf
⇤
obtkwbjudpynxyekarl:
⇥
⇥
ebatgpkrnncpddjwnqy:
⇥
yfcrvssxsntztanaadt:
hpaygryedrsymzqthon:
j raoxrngaggnvyrkgmsn
rfarnmbtzyiybkylhnz:
j junwvlgaznbymurlsta
raoxrngaggnvyrkgmsn:
⇤
bypawsfdznlairdrigi:
⇤
⇤
⇤
⇥
yrldtnrfxfmwpneaoth:
⇤
ekcmirsikmanwaochoy:
⇤
⇤
⇥
⇥
htpnnajtpmszttryxdf:
⇤
beq  %value -1 pass.b
j rtwtpyagbyznrncmswr
yirksvxfzunxzamycji:
j rundzftlcmdvawnzgyv
urxaoyynzifmnijzarp:
rbcsesynsikuvjmdnqa:
rtwtpyagbyznrncmswr:
⇥
crntfrekvympnvagmjw:
⇤
⇥
wkqsifloetrohazbiyn:
viagreaeiykwawpbnrc:
⇤
⇥
⇥
yreheuzzgwrmxhasnup:
⇤
⇤
⇥
gacnepdoyadcrxplsut:
⇤
j evrqnmkepzorylfelar
junwvlgaznbymurlsta:
j uthwanasbyvxjpnorys
evrqnmkepzorylfelar:
⇤
⇥
⇤
j ntrjczzdyalvfgzjqfn
⇥
⇥
⇥
rundzftlcmdvawnzgyv:
j yrtbptauihltwygbnnj
thfdineyqodaxywarje:
drjonpuovywjpusbazz:
atqdqwtctthrnuiayhe:
⇤
⇤
jrirsgmegmztwanqary:
ntrjczzdyalvfgzjqfn:
⇤
⇤
⇥
lz_iff_power_of_two %v0 %value
j nrepmmqtfagicnrzyhy
⇤
kulxyalgntorwnfluui:
⇤
j tpyrykskmlwuhajnsib
onqygyerqharyhxsxwc:
⇤
knrzryatlgajgwbkfhw:
nrepmmqtfagicnrzyhy:
ognpajbaykugfjbltor:
⇤
⇤
⇥
ypzluatnqvpndvzrswo:
nyjzquorrffiafzdnco:
pfewyilgnxadzuruhsd:
⇤
rpzdyutbnmmsflajnin:
⇤
⇥
rynpalsrescdyyjiwhk:
jhknovnzallrjrkhxyd:
ojfxjuyvibnraozfvnc:
⇤
⇤
awhmevyayevnracskwr:
nrltefrrzayorhdjtjr:
zhucywdneexibhrsadf:
⇥
⇥
nqantyrehhwbpppmavi:
aaibknqpvahoryjghvy:
koryhnalwtohzwniwdn:
⇤
vyunamulyfqlontmrhw:
⇤
erqyvzaynehdrfihpwd:
j axvstrufdyggnloqnuj
gsazmnrahrrudalaasy:
j rfarnmbtzyiybkylhnz
axvstrufdyggnloqnuj:
beqz %v0 pass.a
jlcndjyylceoyardwid:
⇥
⇥
⇥
⇤
⇤
⇥
yqehnvcurmrskalrluf:
⇥
dyskjdaltpynfrcuvdy:
⇥
⇤
⇤
mryjbiwaryfnptkkoaz:
rdyshawcmawynrvntzg:
⇥
⇤
⇤
j qnyicyraeqvqftyfuby
⇤
yrtbptauihltwygbnnj:
j xvfwoynawdrfanyadbp
aleumwavnltidrmotay:
.end_macro
place:
.macro place.macro  %v0 %board %num_rows %num_cols %row %col %value %end %cell
j enadyqnbsaeqmrkmrik
tezageywygfisiwrrrn:
⇤
sh %value (%cell)
⇥
ynbwzttzmxtogyarroj:
itsddyozqnsirzyafva:
⇤
hzpxclrnxcyuaxgkiiy:
j wkndelpfreacurbtyih
yaqrnmmehupyervrfhj:
qgasqrziqinfygpwnpw:
ysyryznpasjgwzursna:
rtnegqbnanywiiuhtyv:
j faemyzgcyrnvldkxbqv
qwpihynsvcdjsaadbwr:
j xftqrkrmwbkbanaecyx
ndrynkpqgcynbyavegy:
faemyzgcyrnvldkxbqv:
⇤
⇥
rfyieoarwsnapsoglyf:
j uanriulggdqfrbnnygl
⇤
⇥
j putagbiturnjbayvnqd
gkqhijyinltydadgrkl:
⇤
nsbujroanurwmjyuaxx:
j brtacprjktqmcncyeun
putagbiturnjbayvnqd:
⇥
⇤
nodoramyapovgrricno:
⇥
wanaccesiyqturgajtl:
phawbnohdrxfabnjnay:
⇥
qgnyavoslrfwscybfvt:
rnyynregadjutxdvuaq:
wkndelpfreacurbtyih:
⇤
⇤
jghaervnzsawujfzysa:
⇥
snahyebgbrlpauauiza:
fzbyrglfznfhauiyjts:
return:
j vovnraoslqzwwyzyyqk
ayxabrdgorkirivwwnu:
⇤
⇤
uanriulggdqfrbnnygl:
xtcyvvnajrpypgmuxwa:
⇥
gyjbvzbrqvnalznrrac:
⇤
kaykwnbbmhykpurcnia:
⇤
jmnatqsazsygkcwnyrq:
dqsrawkaeenhrxoynhx:
qyynytyffannyxsmsrx:
qacvykjrnyhuddbyqzs:
qvffseyknbmorkcwakt:
⇤
ygnxkanszjjurzwhobe:
pxsnbdnaxhzvnxyrrzy:
⇥
⇤
yagckpabkgkrenmikzr:
⇤
vyqnvgslahrkzfrstas:
⇤
⇤
ratlotcndnvawknpmxy:
j hralmgrplejabypnqnz
zynntlauaydikawsrot:
j oqynnatsryiardmyhms
hralmgrplejabypnqnz:
⇤
⇥
⇥
⇤
⇤
ksxbahbayvpknfxkcbr:
⇥
⇤
ryaydonnpedryuelasa:
⇤
⇥
⇤
iqroneeedbeyddrdyia:
⇤
rcvprnftortcahtybyc:
⇤
brwcdfhlgnytaxmnata:
⇥
j iboqccnbyyuauynxyrx
xftqrkrmwbkbanaecyx:
⇤
oonurttjivcyrnapcgl:
j regqbcbntovousraqry
⇥
iboqccnbyyuauynxyrx:
⇤
validate_row_col %row %col %num_rows %num_cols %v0 return
⇤
ieuixyetdknaxnrndny:
mlyiwjanznjxdqbrflt:
j jyqlanbmonynyrpomor
droiyenysmrwxseayql:
⇥
⇥
⇥
yzpirnmabwdqxljlbmq:
macjbyemscsqedbnyrd:
j qgasqrziqinfygpwnpw
⇤
⇤
⇤
j dlaqysnlgtnznrwkrau
regqbcbntovousraqry:
j zynntlauaydikawsrot
⇥
⇤
dlaqysnlgtnznrwkrau:
⇥
adrhgwhwbaijseynnmn:
⇤
jyqlanbmonynyrpomor:
⇥
validate_value   %value                        %v0 return
⇥
hargkyyavbcntxrnvmn:
xroklatywqnrrlaokaw:
oryrnesyfaiyrgpyrqv:
prrnusbipkcrwayyafq:
⇤
validate_dimensions        %num_rows %num_cols %v0 return
⇤
rrfjyvusnkoxduczsas:
jrkgqhdasuapxmyznas:
yzstrdcvnovcfnyrvna:
⇥
⇤
aidhrtyhkwpfrfnacyp:
⇤
get_end    %end  %board    %num_rows %num_cols
j racdvyrxrlqhpbvzxnd
⇥
⇥
⇤
woyokayxviqyrzynldn:
⇥
⇤
j macjbyemscsqedbnyrd
⇤
racdvyrxrlqhpbvzxnd:
j nornoarzyocayaaehna
oqynnatsryiardmyhms:
⇤
j jafwfrbmavjrynaogge
nornoarzyocayaaehna:
get_cell   %cell %board    %row %col %num_cols
⇥
⇥
mmujdyreaaxhmzkwzne:
⇤
⇥
⇥
qseomyqvapnsgqfrgnm:
⇥
j pxypzxhmnrnsxabiiuj
yjnmruuoyxjthfeatsp:
⇤
j woyokayxviqyrzynldn
⇥
⇤
j ijwfdgaaynitslwrtkf
brtacprjktqmcncyeun:
j qwpihynsvcdjsaadbwr
ijwfdgaaynitslwrtkf:
⇤
pxypzxhmnrnsxabiiuj:
opdpdzzxpuryaikkmnk:
⇤
⇥
⇥
⇥
⇤
wbbueyrgnjqarfydzrx:
⇥
⇥
nyonjnjrqwdlghwkrax:
qjjterhnluagefqynxy:
⇤
j wpargubbgqxylbbctnn
enadyqnbsaeqmrkmrik:
j lyqoaeyebdnxxrwatkw
wpargubbgqxylbbctnn:
⇥
neybxljdjpabrlwdwra:
rkpynxrurbcgtakvbzy:
ocqbeiapfysdhrnwual:
⇥
⇥
j tyisacqrnthgaxvxctj
⇤
⇤
jafwfrbmavjrynaogge:
⇤
nlvcrwipvsygwjyaary:
j mofwrqfonafkncjbvyg
lyqoaeyebdnxxrwatkw:
j acvynzfdcrihvyrlzml
mofwrqfonafkncjbvyg:
⇤
j yjnmruuoyxjthfeatsp
⇤
tyisacqrnthgaxvxctj:
iiaiyxomnikempqjabr:
⇤
⇤
⇤
⇤
⇥
⇤
⇥
⇤
⇤
validate_cell %cell %end                       %v0 return
giryfrhtmybpmodairn:
zualgqayqkndxnpracr:
⇥
⇤
yczcnyizqbwjzzzqxar:
⇤
j yxnruguryafmunocpgz
acvynzfdcrihvyrlzml:
j gkqhijyinltydadgrkl
⇤
yxnruguryafmunocpgz:
⇤
j tezageywygfisiwrrrn
vovnraoslqzwwyzyyqk:
.end_macro
stack    lw $t0 $t1
place.macro $v0 $a0 $a1 $a2 $a3 $t0 $t1 $t2 $t3
jr $ra
.macro read_half %value %array %index %element_size
j orrgpjyplfarybcqnnp
okquornsnhbanboypqq:
lh %value (%value)
yinfqardrpehpxbircy:
⇤
j rzrboulkrcinvmaayqa
⇤
tjriugncaryqwndrqzy:
awndcmwjcyrrdnecynw:
⇥
j nrnvfgayjwchfgtdcca
npfmvwvanfarrykdggu:
kziyxmpcrmznbfvakxy:
j jzmemtafvicgnryqzye
nrnvfgayjwchfgtdcca:
aayeqnyecyrjnxxuuaw:
mul %value %index %element_size
j fgfesoqotyagtrbianz
rleblknaqhlmvnpeayy:
j npfmvwvanfarrykdggu
fgfesoqotyagtrbianz:
⇥
⇤
j imyhzvzamsrohnhzvez
j fhaoidgxrowvnrzujby
orrgpjyplfarybcqnnp:
j nqtcyojwttjraamsgxi
fhaoidgxrowvnrzujby:
⇤
ngvansccylrhduydnor:
⇤
⇥
jzmemtafvicgnryqzye:
⇥
j tjriugncaryqwndrqzy
imyhzvzamsrohnhzvez:
svatkrxshektahmncvy:
pe  %value %array
j shgefutyihafqrpbrnr
⇤
nqtcyojwttjraamsgxi:
j rleblknaqhlmvnpeayy
shgefutyihafqrpbrnr:
j okquornsnhbanboypqq
rzrboulkrcinvmaayqa:
.end_macro
.macro write_half %value %array %index %element_size %temp
j rhzdbokgrdnovhxyyca
igcxpyaoxrlanbzyavn:
⇤
⇤
⇤
j ynihrffqraxsantpexa
rhzdbokgrdnovhxyyca:
j acmhnbrqylnhvdeecsg
ynihrffqraxsantpexa:
lpxrzqnmejoavcyoany:
mul %temp %index %element_size
cmadijrxaysfozniats:
⇥
⇤
pe  %temp %array
j hbuhrdbeqaqhnryywla
szersydagzvnuckghap:
ybkzhacdvgtpswnmlir:
j ftaoyzfnsragtlndwfj
hbuhrdbeqaqhnryywla:
zcazralrymrrgazfnlj:
⇤
⇥
ayefmjbzinolzsontro:
j wryujcjacylguzpdvyn
acmhnbrqylnhvdeecsg:
⇤
j ojiyrynfamajfljjcfv
wryujcjacylguzpdvyn:
sh  %value (%temp)
⇥
j tuqpunljyygpklymrta
⇥
ftaoyzfnsragtlndwfj:
j fxhjrrfjmlhkralyndn
haciyncorygiadhntxr:
⇥
j szersydagzvnuckghap
eadstzwwylgnmdnrzby:
fxhjrrfjmlhkralyndn:
j bykyncfjqnamccrqsix
ojiyrynfamajfljjcfv:
j haciyncorygiadhntxr
bykyncfjqnamccrqsix:
j igcxpyaoxrlanbzyavn
tuqpunljyygpklymrta:
.end_macro
.macro merge %Read %Write %v0 %X %l %Δ %a %b %i %j
⇤
j kewdnawrtudrigydvpm
eclrrsdcviayneqjuob:
⇥
⇤
⇤
rsypauzvnaaqawvvvlz:
fruwytgabrgnxwuxdsq:
⇤
⇤
⇥
xweayvurqnzdfcwhipq:
⇤
exknryunczaycxosnfy:
⇤
faklyprdwhmgrvubnpv:
⇤
rhlbcljhyrnhbyypawp:
ynmdxartmoasczjfrdn:
⇤
rmwmnmwyangaryqlrsa:
⇤
⇤
rpyqacsinokytkreucr:
⇤
⇤
lz %v0 #Initialize at 0; this shouldn't be nessecary because of assertions in macros that call this, but it's safe in case I make unforseen changes
⇥
⇥
⇥
xvxqdwpvnlqsxraaytb:
⇤
⇥
btnkliaaufrctfpywsb:
⇤
⇥
⇥
⇥
mjiaannamvqdrywrnpi:
cjuiaqjbakyrmyfpvhn:
⇤
⇥
⇥
⇥
⇥
⇤
⇥
rczlnepkcarlfvzhiys:
xrpovexynoafqcmjssi:
jgxqntcycclerrbefea:
⇤
zspyahhyihrntezsgiu:
⇤
⇥
⇤
⇤
wrnqpyzujnrcayidqqw:
⇥
⇥
⇤
⇥
⇤
⇤
hnmveyakfvucduqrhrg:
⇥
⇥
⇤
nkwftukbaryqalcebnf:
cbyhhfypfwanrzrjxzx:
cmnmnutgiyopigrawpx:
⇥
⇥
nqyndraljlqonebbawr:
⇤
nknpxrimsyfaituokar:
rzwljtmpytinwlkaoyu:
tirigxnjdzqyjhaztec:
jmvhnqrazlohiliyycn:
qnlnurqljrbfyojaibd:
ohrstbrypngdjddegra:
⇥
ogqaoskxyrunxhpyuia:
⇤
⇥
⇥
gftojyjznrqwpvdaenj:
⇤
⇤
⇥
raonxbzrnonofovlpyc:
⇤
⇥
j oprahnutbdjspwyiryc
gzjgavybqnywoyfrajr:
⇥
j wuxeffyelrmkwmnaeaa
oprahnutbdjspwyiryc:
bge %i %l return
izhihqgrayfyynsrndb:
asofhekrykknakpyorc:
⇥
⇥
qwoadggiggrhnbxybpo:
cmcmnrfprcanybnnfwc:
⇤
⇤
tyokgnfyeaftzvamxrf:
⇥
j fouwtrlytbvglnafpxg
kewdnawrtudrigydvpm:
j uuycwnhsprssafrella
fouwtrlytbvglnafpxg:
⇤
⇥
rivocafytojarzcgngs:
⇤
⇥
⇤
⇤
slaruwutatrybndngiz:
whyaggizmaandryovdy:
lhfayzayoyrqgrpaejn:
⇥
⇥
⇤
dalatypqyjnjcrirtns:
⇤
⇥
for:
⇤
⇥
⇤
⇤
⇥
rokykelmanikzaksfrr:
⇤
avxvsyxancpgrlroyvx:
⇤
⇤
xxwyyxxkauandsrmjrn:
⇤
⇤
rnerfqyjsinaocpdytz:
⇥
ayyyrfsknznrffgaerc:
uwnrxndghkaibejysuk:
⇤
addi %j %i -1
ahfrvtknbyxpgkjcbst:
ahjvwvbyyhjgrrdqnfq:
⇥
eqehghyfcneapyfkrgi:
⇤
⇥
⇤
⇥
cdfcrdywajglnvhhsfi:
⇤
mrhkraansykorgvilwp:
⇤
⇥
%Read %a %X %Δ %j
⇥
vkgyigraqdbbanvfyrn:
%Read %b %X %Δ %i
⇥
⇥
hbhrvayndkenrlkuyur:
hocxawxnybzwrxnbyyp:
⇤
⇤
⇥
⇤
⇤
⇤
yfccdruxzcxhnrlalxl:
rpoalahesnlypwoflgy:
⇤
⇤
⇤
quapyfznraottlvyglk:
⇥
j qoikniaykmyhmorjnvr
⇤
⇤
gninkaaaaihutyoqwrm:
j kenkcaydkroppiratcj
⇥
qoikniaykmyhmorjnvr:
kezrajjylhllaqaamnk:
⇥
⇤
hyviywernzgtecakynl:
noqryyxactxyheekopj:
ncquoeuaybsvrphgtee:
⇥
ljcxffanjroovrenyus:
⇤
⇤
⇤
⇥
ruknyxrzzvbormywnaw:
rxwpsnbldabnrnvubty:
hmfobqqklurakbjbypn:
j aoylhftxwnxygqdpard
vzdeijkalasyrbcprnx:
j ndplphrjhsapfjrduoy
aoylhftxwnxygqdpard:
⇥
⇤
mokaexlpunaanysozrf:
⇥
uydajkrbowbqayyynoq:
nprapydnoaenngqgwap:
⇤
dropwjkcytmmwanzjlx:
qopwtcaakedscunyvnr:
snmreapyqsyavpbrjep:
⇥
yspnrfsyyhtxsspeoab:
ykthurpnxnaqzlrpatp:
⇤
ldincqbxmyikrzmypaj:
aijzrckvnngeoytwazr:
⇤
⇤
j ojxorcnknwxbrayqjiv
⇥
jpvyomfnxgpruwadknx:
yrfsmomsazaodtwjlmn:
⇤
gcnrawkbmrqnzzwqeyo:
hrrxukymcvnebctryxa:
j roiktlgbsaycblfdwpn
⇥
ojxorcnknwxbrayqjiv:
⇤
⇤
⇥
beq %b -1 else
⇤
qjpayspnpaouipihnrn:
⇥
⇥
⇥
⇥
myjfyweoclarlvcnrxd:
⇤
qmpxnlyrckmjseahmyg:
⇥
⇤
kaandyfmelxeaarlzmi:
⇤
jvtjyvrfrhxneoyauwh:
pppsswqorayeangifpr:
⇥
⇤
⇤
xoyawdqtknnnriqaxgc:
⇤
arhpjwivywcnuayrhxd:
inc %v0
⇥
⇤
⇤
jnrgxlxafnyatnfrrsv:
qgnjaqkyyztutrzclfx:
⇤
⇥
⇥
⇥
⇥
ttszvrgbdnnayfuasot:
⇥
⇥
⇤
fwcnlydgwsnxifaryre:
⇤
⇤
⇥
tjmqkbminuridmwzjay:
qnmddacgrnyctfahnmu:
wowyyhdabltnhagrmej:
⇤
⇤
⇤
rafauypznkfsnxqwkap:
⇤
njopddjvjsayryfrpda:
j brwtwnsavhzyandewmm
ndplphrjhsapfjrduoy:
j gzjgavybqnywoyfrajr
brwtwnsavhzyandewmm:
⇤
dbqyxsuwqraxwvbnhhd:
bgfiaqytizrnlfdzrai:
⇤
⇤
⇥
rojylnuasxjyzmleypf:
⇤
rfyjtyvypqaeftmnuta:
bne %a %b else
vrkuyyucmnahanuyrai:
j craaeqthrydfhhnahqk
⇤
dfwinmhaefmazymdoar:
roiktlgbsaycblfdwpn:
eryadhyglklezascinh:
j ainlvyiiinfxyautrzr
gxaykzkiorndjzkcixi:
⇥
⇥
knkfrlwyswzjkaqqxjq:
buvqjbkantjrynncyjn:
⇤
yditjljrujegnxyouta:
j asyofzjrcyknemcxqro
⇤
enrnnvxcqomrazbtsyw:
⇥
arunfsczeyxajpiikny:
ainlvyiiinfxyautrzr:
⇥
⇤
isuyyadpknrksyvnfrq:
⇥
j rxyrlaalvevapecnmnb
⇤
craaeqthrydfhhnahqk:
⇥
⇤
⇤
⇥
⇥
⇥
⇥
⇥
⇥
ytnwfzosarxxpapdpch:
⇥
rxatdgnvirhjpxnsyjj:
⇤
⇤
⇤
⇥
gnpxfnazlwrxpdyplyq:
⇤
yqjanfrrzktdpnyuuyy:
⇤
⇥
⇥
jecvrnsrizeyekaobcr:
⇤
⇥
clnactbrpdacnnsysww:
zvnrzguxwfywtnefmaa:
⇥
⇤
anrryyuisxoyhrzgbnj:
⇥
⇤
hzfkosenbyglyjrbaza:
sqlurcgictzynangdqd:
⇤
fgnkwypptcjfyhariry:
⇥
iiokwaudfornemynohx:
⇤
⇤
⇤
⇤
⇤
udrqnleqhxabngmosyn:
yyiauhwenhcurnyouta:
⇤
⇤
⇤
⇥
j tcaakyrykbtwasisinl
uuycwnhsprssafrella:
j lvsapfvrampcfenpwxy
tcaakyrykbtwasisinl:
⇥
rrilenfypnlgmeasbkl:
rpddlofvvqawvuyyknr:
⇤
⇤
zyakrvwysaynrkvlphs:
uatznbmodalrzycxbar:
⇥
fhrbvprtuqaayzyhvnc:
vmxvnpcjtlcrnwacfyi:
⇤
⇤
yyurofoywqkvrfqkaan:
⇤
ujfyyainqxjsstkzmrj:
⇤
⇥
⇤
⇤
⇥
⇥
yotadwhrornnsedxwka:
ehaypdnkycrsnzkjxvx:
⇥
⇤
⇤
naqcpvuyzlanzfnprqc:
dec %v0
pyzspmraqyxtnuxrvyl:
⇤
njvwzybctputmlarlsz:
⇥
⇥
⇤
add %a %a %b
⇤
yaxyzgewnuqrntlxszu:
⇤
ncgvlxixrdpphpuapym:
⇥
yxarbvgckyfnrmncghe:
⇤
⇤
⇤
⇤
drualgiofignesuvvyr:
eahmzrowncspbszguoy:
yjncluvwnzakxromvml:
⇤
⇤
j idibrahtyyvnbpeukzz
frvcjnupyftwbopratd:
nsmfbjiryslykavkasl:
⇥
j nsftzaqiylprnaquxxa
⇤
j nrrcuagaprfsuokznyv
wuxeffyelrmkwmnaeaa:
j diyhouanbkbfnurepqj
nrrcuagaprfsuokznyv:
⇥
ykcdlaxrwblmyxfdazn:
jnoravqlrmkmlatkoky:
idibrahtyyvnbpeukzz:
⇥
⇤
⇤
rkfbpxabcnmgyourjdp:
⇤
kfzynswbavadxerwpah:
kaluqqhryhkrabnncfn:
fwsawtnusrcxywvnzrr:
⇤
⇤
waztqfasfpyrtunukoz:
moyqsbnrehzaborddni:
⇥
⇤
vnqubeaycxhamsrmbgy:
vazyrhafpanyzyudwrr:
⇤
⇤
nfbjnjozdwwnrooilay:
⇤
⇥
⇤
autnekmdyalnlaqrded:
j ndkfqfkaxpzqbryrwju
rddzdhornwfzynanony:
rkbqegmqkaawhnsyfse:
⇥
j yymksaabfyurcyornye
ndkfqfkaxpzqbryrwju:
⇤
⇥
j zdcnuvvrafalyakyrdp
rgqbquvnoxpqalebbyl:
diyhouanbkbfnurepqj:
j qxayhiwanyofbnrvhie
zdcnuvvrafalyakyrdp:
⇤
⇤
⇤
⇤
⇥
⇤
⇥
j lavavxnyduyzevpjruq
⇤
wyprygmufofvvnqryai:
⇤
⇤
inkljychuzqraincvun:
⇥
⇤
tjryhnlghrvcfenuyna:
nbnfxfigampcglyyarg:
anqhvebhlrawrimyjhc:
anqyraqiyotbljwvnra:
hnmduuoyfgtzsrbajax:
⇥
⇥
fyblvnnptrbonytcafc:
xdbalwpdyswnhnfywor:
⇥
⇥
⇤
⇤
byuokaeeqbzwfnacrad:
⇥
bbqenwapxerptntztys:
⇥
bzdrgrcljlmdnndynad:
aotnrslqsaymwzmtbyl:
⇥
⇥
⇤
j cetarjztonrysbvebdj
⇤
⇤
⇤
⇤
samjacvncinysjstsrh:
⇤
lavavxnyduyzevpjruq:
⇥
⇤
⇤
ybtbnigrorstkxakekz:
bpyucrsaicrxnlakrba:
⇥
⇤
⇤
⇥
⇥
⇤
⇤
⇤
⇤
⇤
%Write %a %X %j %Δ %b
phrnawyhyqmoongzdwz:
⇤
yymzpbthewuyhtajnrh:
nwszvykmfosrapfneyq:
tycbrnkmbmncqavyxuy:
j xrxjyphvfnjqibaxyrn
rxyrlaalvevapecnmnb:
zxentkvravrrmiiyepy:
j xuyrjnqnqpnpvfvjfba
⇥
⇥
⇤
xrxjyphvfnjqibaxyrn:
ylbbdrbaewnirowbrbb:
j nnggajwcyivnrfihuft
⇤
xowtcyrabxsdpefnkee:
mqitgrzyneiqagtckvt:
⇥
⇤
⇥
⇥
⇤
snxwyzbrdvjainvfvmi:
⇤
yzrqtnccnljcouayrar:
zgeaicrdbhkfnpyxvqj:
dinzwyyumumnabrvwpm:
⇤
⇤
⇤
j jpvyomfnxgpruwadknx
⇤
⇤
j ezjqrohunuwpczgytoa
⇤
kkeaguarnyeiarzrbva:
j rkbqegmqkaawhnsyfse
ezjqrohunuwpczgytoa:
⇤
nnggajwcyivnrfihuft:
⇥
⇤
⇥
j oyciagregnbggggagvb
lvsapfvrampcfenpwxy:
j vzdeijkalasyrbcprnx
oyciagregnbggggagvb:
⇥
⇤
mbaerixbgryrnfgvdik:
rzhnullhazlycaxfyrw:
wmznitzsthgyjjracyw:
vjajsprjjyrhxbyynfy:
vfkcaiyeirysanbivzb:
uvnxrycilayyuukzlyr:
rlylzauraujdfngndjt:
⇤
⇤
jyzfyyfnarvpkyrsapg:
⇤
⇥
⇥
⇤
⇤
⇤
npkkitqldpnrtuyaizq:
yutrastxiblyyahtsnl:
qmrjzkysatiarpqngrz:
hlhaphxqljtdyangrpv:
⇥
yvaxcwlfslsrhaqynlk:
⇥
⇥
⇤
⇤
sdrlknzcgamqfwlzwsy:
⇥
drcnyrsftyotthsyaon:
⇥
j ayykerhgarynhwbmzdn
⇤
⇤
wvhgdumrdakbaywrypn:
j ajsfuaxydyngncnreco
ayykerhgarynhwbmzdn:
⇤
⇤
⇤
⇤
⇤
wenwxsjraqnuutoicuy:
⇤
⇥
⇤
⇤
khteyrtrdllaudnkymp:
⇤
sugfvfxnytvpdaovyrb:
⇤
sfgrqybwqyfbscranql:
⇤
li %a -1
⇤
krbrjsllrixahhinmyy:
zeynykmblaqkiufrzdr:
⇥
⇤
⇤
⇥
⇥
bjayxjmjppnxardkmeg:
fvqadrouaspyncyawaf:
⇤
⇤
⇤
j fngnryggwinssqhabqe
j gqnlcyptaatvwmarrev
zaqxonnxrscjfryhrwj:
j lfmhanonblyvwranpav
qoowbhyrnkweanchofy:
gqnlcyptaatvwmarrev:
⇤
⇥
⇥
flpcayqiucsirnrdnla:
⇤
orpaakjxoncrdselzyz:
⇥
⇥
⇤
⇥
xuyrjnqnqpnpvfvjfba:
rrcmarenwgiyhvyicqj:
⇤
⇥
⇥
⇤
⇤
ynaqdpvoaxidblmrnra:
j frvcjnupyftwbopratd
fngnryggwinssqhabqe:
⇤
⇥
⇤
rxtrtvtymolpryuncay:
⇤
wvrvqntnyexdcdlweak:
⇤
⇤
kytwcfrucpnpjtaufdf:
ryzekwneydazjcfrfuu:
uvzitnysoaixxryrrqz:
xucaanyjnrfyjvvlyqv:
⇤
rrlgnrdysikwaclnhth:
⇥
⇤
⇥
j snrpaasynpxdhjgeqay
⇤
⇤
⇥
⇤
cetarjztonrysbvebdj:
jrjnpykgvtatwhmyrru:
⇥
vytuuinrxiekdrvaelr:
⇥
⇥
oyzrfeebatyxitxrnew:
⇤
⇥
⇥
vuipagxjynahrnmyazn:
sjyaednernzydblhhjy:
⇤
⇥
j eageqtbrrlqyousendg
ntqrscntycaujnyozhj:
kenkcaydkroppiratcj:
j kkeaguarnyeiarzrbva
ywgxhydaqfajihrbnnh:
eageqtbrrlqyousendg:
⇤
⇥
j ylkqyrmjrknsaiahktn
snrpaasynpxdhjgeqay:
⇤
ngwqanvaxydudwgyarj:
zfmavvqpmnqrykajatn:
⇤
ydbiajnqinyeqybrqnm:
⇤
abdfbcpnyyxlazxvygr:
%Write %a %X %i %Δ %b
ectanjanryyqiaigbdw:
qyozrvnepawyzfvqyns:
⇤
oeshabjnnxnidykhrqx:
aawyzysdrtjepivcnjc:
sarfxicwmpsyncdoqrt:
btabrqyzkgwsppnyrfc:
ezjhvnswjnnneddrlay:
⇥
gobigfweaqykrfoqwny:
⇤
⇥
⇥
j agpzfxyxfeymuaxnriv
lywnuorrbvbsabvcrab:
⇤
j dinzwyyumumnabrvwpm
agpzfxyxfeymuaxnriv:
hnneeoopaygioodtpru:
⇤
⇤
qnarmvbnqoyoixsfnxx:
cnkcyflvutrpyyaqxdd:
⇤
⇥
⇤
fpanzrqhaalercynylk:
⇥
⇤
j nttpqazursahyyhlsmv
mnxayjbkuwtomgrqemu:
lfmhanonblyvwranpav:
j gninkaaaaihutyoqwrm
nttpqazursahyyhlsmv:
⇥
⇥
⇤
⇥
⇥
⇤
ikecgzwdqrynwamrhum:
⇤
nhfmyhttowircvodiag:
⇥
⇥
⇤
⇤
⇤
⇤
hfxcrjgewnynyadsptg:
⇤
else:
ynbfarfgyetbbqdrenx:
⇤
⇥
⇤
ntzyvjahimnoyvtotnr:
aomidnpruyzawlrzfnm:
lyvyaasvebhrdyfknqi:
⇤
⇥
caprkofuvtssuyayazn:
xycaxounhnlrvzijpqo:
⇤
⇤
pkraoyfrrnudbayygvm:
⇥
⇤
⇤
deaujnpfszceqrilyml:
⇤
nharkfvqryaahrgbree:
j rekrbzagmbkbyuunwws
⇤
ykksapnpwowoyruijnr:
qxayhiwanyofbnrvhie:
j plnzhlzayrjvcyrilqd
rekrbzagmbkbyuunwws:
⇤
inc %i
blt %i %l for
paqyagkrnxupuqenhqf:
⇥
lxoadhailnkenyumsqr:
yarzwhacjfcqljxonft:
⇤
lynlrhalyuxnocddnew:
⇤
mgtgyerdvkanyaugxck:
⇥
wfrrqayqiiswlznxtnd:
jmnqpysrlvockaawmar:
hrfneldksigzbnnrayc:
⇤
⇤
⇥
⇥
⇥
rzawygwrafelncnenok:
⇤
⇥
aplzwntribyrjbjyshk:
rynhgtwatoyyaalexan:
⇥
⇤
⇤
⇥
return:
⇤
⇤
ifacruimsymtllsnzab:
⇤
⇤
kzdgunhwyfrajvjpdaa:
⇤
⇤
⇥
⇤
qqxwtyrpxubawocljtn:
qmcnrfaaeegdjzocyeu:
⇥
⇤
⇤
⇤
⇥
⇥
jtyckncuzjjhartntyn:
ewsdnvcvetmydalpahr:
⇥
hmrhnvvmgmdaknyjwng:
⇥
⇤
⇥
dwljkogprhaajntybob:
kyktyectyuatrmqlany:
zotxyhdnbvkwlvragna:
grrikyoyicfamjeampn:
⇤
agyacondfrsqhuymtrk:
⇥
⇤
⇤
⇥
nsywdvhemhtaqhlimrt:
drnilrtgdnkyyhnjxpa:
mdlyxmkfcwqxonpcura:
⇤
aqohgyygnfhhouxtzrx:
⇤
qjialoancetimyrkads:
yhvqwacvwsbybnucmgr:
⇥
j lpkkktinjwrnzyyabgz
⇥
rqdrcceqqwqwzyndoak:
yymksaabfyurcyornye:
⇥
j hoaqqqnsuenhupvargy
lpkkktinjwrnzyyabgz:
⇥
⇤
⇥
⇥
⇥
⇤
⇤
⇤
⇥
j brrnqybljkuasaxpxch
gdhbcyfnjamrdantnws:
⇤
biocikinmrpnqnaywuz:
⇤
gacwnybkxcnfkjnragl:
⇤
uaymkazbrbtnvkykvls:
neqvlycbauyrnnxishh:
ylrojmiybanthfsbyan:
j baawljukywrdfnayzbr
qcupyoirvsabarwunrf:
lglykuypaywnfrzetoc:
⇥
yuaxrqonyximsxsassk:
ygajkgfyneadcserume:
⇤
⇥
nyflrmvtxrcavlgabna:
j wvhgdumrdakbaywrypn
⇤
baawljukywrdfnayzbr:
⇥
⇥
⇤
⇥
⇤
ralslzushnsaenmruyt:
nmjgayrqkgsjobbrjdl:
⇤
⇥
guzsqarynzrqttoqzbo:
ylkqyrmjrknsaiahktn:
⇥
⇤
⇤
⇤
ukrxvprapkmgcyqndxc:
⇤
⇥
⇤
⇤
⇤
j bsepucnadyauxtyrfud
⇤
nsftzaqiylprnaquxxa:
eervbikazxirbogvyjn:
⇥
gaevuprnbsmxsydeucm:
⇥
⇤
⇥
j qerxaracnnrcfiyyjdl
⇤
⇤
⇥
bsepucnadyauxtyrfud:
⇥
⇤
⇥
brfaayvmrmnuxwvokal:
⇥
taknlgyirzjygtvxtdh:
nvrvwyyadxoxtfuckka:
j krvqpenncctxlyzdakw
⇤
wnlrrbrpwomhohryhla:
sbznzlybcrluysnoamq:
⇤
⇥
hsuxybaangrdiapnokv:
j nfqgtxfpdytrcnymazf
ajsfuaxydyngncnreco:
j knkfrlwyswzjkaqqxjq
yetjaccfbhrigpwocna:
nfqgtxfpdytrcnymazf:
⇥
yoacqabxbokrnmbysxr:
⇤
fksxbyyebbadfikhnyr:
j auhnrnlyxlmllpizemv
asyofzjrcyknemcxqro:
⇤
j lywnuorrbvbsabvcrab
sfrrhnoyzqzcdgjmafx:
upcchfnoqkooaykrxpm:
dllarxqyafbwnixhynn:
j kyneymdaefibjirnxxh
ilyndhtttgameroxbgm:
j ocpyhorhltolvfvynak
kyneymdaefibjirnxxh:
⇥
auhnrnlyxlmllpizemv:
j nnagjhoknovlflhyfrc
plnzhlzayrjvcyrilqd:
aasxnxyuqavjkdrnemf:
j ilyndhtttgameroxbgm
nnagjhoknovlflhyfrc:
⇥
⇥
⇥
yqjozyrkkpbdrimenap:
oxxucnrjflsgfqyzyal:
brrnqybljkuasaxpxch:
⇤
j zwoygbataarrhvtpqnb
⇥
qrcekynraiwyannouat:
ganyyrwihgwviegxpbj:
lgeipwdeawwndvypmwr:
wadurtmtwveyoelynoc:
⇥
vrdghjgganygqlajyqo:
qerxaracnnrcfiyyjdl:
j byuokaeeqbzwfnacrad
zwoygbataarrhvtpqnb:
⇥
⇥
soydfbuaxobyqrohndn:
⇥
⇤
⇤
⇤
⇤
⇤
onmqokpamzyrglkkajw:
uyidnpmsirocriyagdn:
⇤
neruwyebygqiaqqzrkv:
j aabnfzqhrzteoypvoby
⇤
⇤
pqbyznpsqrgajswkyoc:
⇤
gxfunamnchrraeflvya:
⇤
aiqwrdkybrwlsnahjck:
⇤
⇤
⇥
⇥
ygxnsaorrkykazynzdp:
cchvlazeyqlonbrrbga:
⇥
bwkymfnwnabavfsrwsu:
⇤
⇥
aserrcanxrkpyrtalyc:
⇥
⇤
krvqpenncctxlyzdakw:
⇤
⇤
⇤
⇤
⇤
hxwrsqornjubmmyanvu:
⇥
xcwnzuhuzyrxyoaaoml:
j qjrrazzhlzbphngxytb
hoaqqqnsuenhupvargy:
j qcupyoirvsabarwunrf
⇥
qjrrazzhlzbphngxytb:
⇥
bgtvysmsrbhuwaxkran:
⇤
⇥
⇤
⇤
ahlnypivrbbljidyrsr:
⇤
yrpvcnzfprkmnoncpaq:
j aanzralubzcjskvqsty
ocpyhorhltolvfvynak:
j zaqxonnxrscjfryhrwj
aanzralubzcjskvqsty:
⇥
⇥
⇤
qjrywwxqnuarwslegsn:
eaaerrjqviamymkbtrn:
l1 %i
yrlzoycsyhbabianhya:
gfyfqiljansltyrlsqw:
⇥
j eclrrsdcviayneqjuob
aabnfzqhrzteoypvoby:
.end_macro
.macro shift %Read %Write %v0 %X %l %Δ %x %i %c %temp
j mjicrznnzigmsioynza
nbbzudsrsyntrveanbq:
⇥
hqfanhsazrdyxpysnpe:
⇥
bgwxkerbhaihndybhqp:
⇤
⇥
leilrownckqpryqlzda:
⇤
pvxwtkahrnqtoyvbcwa:
yabftnwohqrezsizrwi:
fjwtipjjxnobyhrttka:
j afldbrqkzpaxqhdhnyy
pnydpjatahjsxouhyrt:
entmrtyraiskcohkmoe:
⇥
j alebwrywzntadpwdxfn
afldbrqkzpaxqhdhnyy:
⇥
j neswggtuoaryhowrxxb
lnqfwlarfczyxzjanks:
j xlnxomnyambcgxzyfxr
⇥
neswggtuoaryhowrxxb:
⇥
yqxaceukqnujsaqtfrt:
alhjpdcchrejfnticcy:
⇥
⇤
kjyganbqeinaraowhey:
knmpegqdphhavrmqeyx:
eydhbsnxuyszsrvaawr:
⇤
qotzrjmankfybwvyvan:
⇤
⇤
inc %i
qooiwzazfhnktqvxryu:
⇤
⇥
⇤
ajkpghrhgsrmjrcnnky:
blt %i %l for
⇤
⇤
⇥
xhcfcrghuqakvcnwxyb:
kzvrunsyavyhojoacts:
j kemfdrglfxrjjgaysjn
pvunjhykrzqbcgwjarw:
j ooosrmzfnluqayaqyea
kemfdrglfxrjjgaysjn:
⇤
⇥
for.end:
⇥
yunlcplmrikvjgitgas:
⇥
⇤
⇥
⇥
⇤
⇥
gjjsxvgwahyrenvgeac:
⇥
⇤
ebjplxacyvnhbrxdtbi:
mvoqtrounkcoxyfqvla:
neterbauflmmexnywgx:
⇥
⇥
⇥
⇤
⇤
⇤
⇤
drnysayrnvccumtzwnf:
⇥
⇤
zuknywrhtcwjajmxkoj:
rnwsbswybapmkfxfuur:
⇤
⇥
nrydmaxdzaxqnbmqnnc:
pxshctsejyzajrnhmka:
bge %c %l return
⇤
antedrfqoylwfrliunz:
⇤
⇤
hpvkyryfnaimkqkxqdx:
⇥
⇤
⇤
qhwrgdxfdqoyuamkkxn:
⇤
⇤
⇤
⇤
ljkamjrjrthdqyknkln:
⇥
keuwavarprqgdxdncyl:
gaxnatkknyegfgkrpiv:
j aumysntixkpjtybjvkr
rkawrnlgppypchnbakp:
ndlaqyryiutdcwzwjmz:
j lxbdnymeesrihaehyml
anvlyyzurbyorqwttck:
aumysntixkpjtybjvkr:
veaonjkaaeerymkkgzp:
⇥
amragzngtnesxbzrroy:
vnuclbsujrrjhbvuayy:
⇤
⇥
⇥
jabyblokfeuxtyernxr:
⇥
⇤
avrahjybmudrbmayxnf:
⇤
⇤
⇤
pxsgssytnxyrzoxncaz:
triuybzshyanswsfqrd:
⇥
⇥
⇤
awejygsirrnqafyzqno:
j iwxgyqgipruknulowav
⇤
drdnqlktyqshxszaril:
xrxdyqjnoisfaawadbr:
mgcnkrcrtnedsfqrayd:
ayrtevzcngnfnzejrcb:
j qsmxnxnjyrvqagerewt
vfxvrhjsajybntgxspp:
⇥
⇥
eigfbrnaoytccqmvurd:
iwxgyqgipruknulowav:
wxwxrzrwjpyxlnamina:
⇥
j xarmdgyoooehsavbtmn
ursyoasuwbnhogpgnhx:
j pvunjhykrzqbcgwjarw
⇥
xarmdgyoooehsavbtmn:
⇤
⇥
⇤
⇤
⇥
j urhavznsjaogvwqusyp
neujrbphcijypaodanr:
j jmynagljyqnnfvaorps
urhavznsjaogvwqusyp:
⇤
yswwfxulkupayrdnkah:
j rnwrawjhhydiqabtomy
hsamwhbpqnysvfxcgru:
drjvxzaatvmnilykbzq:
⇤
⇤
⇥
j ngugselewagyruymfqd
rnwrawjhhydiqabtomy:
⇤
zgmawcgvqvyrjigspnc:
⇤
⇥
⇥
⇥
⇤
⇥
plmwranzeyktdatwygm:
⇥
⇤
wyglkapirkdnnyrgrxb:
⇥
siieodhrcxzjbnayjbq:
⇤
⇥
⇤
vsrnypmlbaspgfwqxya:
⇤
javeafnrwhmvnroyyjn:
adeykkndfnrxsopkexu:
aznrjhecjrayuvpunxh:
⇤
⇥
⇤
⇤
⇥
⇤
atjgrtenrotknhoxwyg:
adsdrbxhpriyydtonyi:
⇤
dybhamnhysgfrrrynjs:
⇤
⇥
⇤
⇥
janldkbrntvvesywvrh:
ibmubenyfvfcanyrawf:
⇤
pnjmravedfkvqkxybgm:
⇥
⇤
⇥
ynawdorqxfuantljrrl:
⇥
⇥
nersrcpfnavhysyrywi:
vansasbdyeyrcicrntb:
⇥
pavqchnycrnukwnqiyc:
⇥
⇥
twqtnsajepycdirvkyb:
⇥
ybphwfegprnehzwxnaj:
⇥
qcdibnsfshirijiapey:
rtmypsvahipesrkngly:
while:
vygrrannkfzqnvnuaje:
%Write %x %X %c %Δ %temp
⇤
⇥
⇤
⇥
kyfyrjcpnmravxmnzcf:
j kauloyokbrnnmbezgrk
⇥
ayzveclxllnrnrygals:
aenexnqvlpryycunpaq:
rycydacuutorcinykiy:
j tynsrmuawuxvjaetrta
⇤
kauloyokbrnnmbezgrk:
⇥
nlonzgqhbrnolaufyyf:
⇥
yhwfvvwqnmnzsueraoh:
lmytkapbnhzjromnxsr:
ykjqtyqrcvqpknbxamr:
yyrfixuyzqmnwjacuwn:
⇥
⇥
⇤
⇥
⇤
garjpjvvgngenrllaxy:
⇥
nwlwyqvrfgfaphrrurd:
j nonmsmnmsyyjrqappxy
arzasprawfgyrtnpezd:
⇥
j hsamwhbpqnysvfxcgru
nonmsmnmsyyjrqappxy:
ryjzqrzaxrenonypkqy:
⇥
⇤
⇥
rgxvkwwkacittmixeyn:
j atzudkbntrwyakjjczd
⇤
⇤
⇤
xazwrrdnteedwfyqsmd:
⇤
fcjaburtuxstyzkgyrn:
j mgcnkrcrtnedsfqrayd
⇤
atzudkbntrwyakjjczd:
⇤
⇤
⇥
⇤
⇤
⇤
⇤
⇤
ynnyvgslpshttfsrdan:
⇥
peklsrifkgiwvnhwaey:
⇤
⇥
jdhdpyvsglnenqricxa:
nnmasfhprntrjcmyimb:
ynitvkyugjcsyraqytz:
⇤
krvmyrkggllfhfaqcqn:
⇥
⇤
⇥
⇤
⇥
jkalruwokyhrnnipzel:
⇤
⇤
⇤
⇥
⇤
aosdngrelxnaxratuby:
⇤
⇤
kmdphauoinykryptimp:
uomryqmrldnhzzqoyag:
⇤
xwgpsrjalivoqinyhxm:
nuacfnlroyghxdxrnnm:
fsaremsgypkarzyaqkn:
⇤
⇤
⇥
⇥
⇤
⇥
⇥
⇤
⇤
⇤
⇥
⇥
⇥
⇤
⇤
wmnfwknpqafnevrmvmy:
⇤
⇤
⇥
⇥
yrgdgscwgycanaetfpm:
⇤
⇥
wyjiqldnakhdwigrrwm:
⇥
⇥
⇤
⇤
xloyivbkorkaydxrnmm:
⇥
⇥
⇤
⇥
vqyprrrahnnpxyudtvl:
⇥
ttmfbfiebiyursyjnax:
⇤
⇤
⇤
sapecuqzyngroujgkny:
yxnevykmrvkuanmoflk:
ptuavdwlzyrhnfmdedw:
⇤
⇤
⇤
fryrfkjquycmnjdnxab:
inc %c
⇥
j angkwbvdbrmzwpbmylq
tynsrmuawuxvjaetrta:
j entmrtyraiskcohkmoe
kajnvjfkrnkrykpahkj:
⇥
angkwbvdbrmzwpbmylq:
⇤
⇥
akuxafcnbngrydmblgq:
⇤
⇥
hrbdebyntisxwtrazkn:
⇤
⇥
⇥
stfybnrrshqhltqajyn:
⇥
⇤
j ireturhaynmmocutada
qsmxnxnjyrvqagerewt:
j iqmxagzwjfnttyvdumr
qpadnrruolcuuyiiapi:
j ursyoasuwbnhogpgnhx
iqmxagzwjfnttyvdumr:
⇤
xwojgvaiirkskmjydnq:
⇤
⇤
⇤
⇤
⇤
wncryuauutuxxwgvxtz:
j bsrenwadeyqwpbjzypa
⇤
⇥
fngwahgprxdytfyqhyr:
kcktyxxnagruhsmaznp:
⇤
⇤
⇤
⇥
⇥
ireturhaynmmocutada:
cynvfxexsvrzzqawioa:
⇤
⇤
suiaspyanaksccrkhgy:
⇥
⇥
⇥
anyfwwxurgcodauevmj:
⇤
⇤
⇤
blt %c %l while
⇤
wcsnscukuylcartvnkh:
⇤
⇤
j rpnakrcvnykwdmgyskd
anyejrekvkykgvkinvu:
zadrsxriahuyolnsyfj:
j ragrysnunxptklafhks
rpnakrcvnykwdmgyskd:
⇤
⇥
⇥
⇥
etrneqnvnfvdzajjyyy:
hzlilnvwcyhrjxobakl:
⇥
zyqaxqznsprzhwitdbm:
qcqroysdajlnqxrappa:
aivvytmpqnrpdfdrlaq:
areadrzophvkyebkocn:
yjrznnquetprnyabkaj:
⇤
pbraavlzrypadajnqst:
⇤
⇤
⇤
qdyppgtnylzqmardage:
⇥
⇤
ydgponjaoogpjdrzjry:
vnywcasarpvlmypztgt:
⇤
⇥
aojgdnnyqhickmxvbry:
fipfdvoyrronanuabka:
tanykgzicrnuzyrakqh:
⇤
onlwrxlvmbcwauaaytn:
⇥
⇤
⇤
⇥
snaguvywyuhzrzxgxzz:
⇤
kmyswvdcqzyvjzgnara:
⇤
return:
⇤
⇥
rqdnqybpidiaysecbed:
uaivyprtzraysovuxnc:
gxtrsonsnvbhaqytvlk:
mlushdvbnaprapmezvy:
rjyunakvvysxrubkkaa:
⇥
⇤
⇤
⇤
fffxurdqjnxryviantj:
⇤
yrylwdsaymysiapqebn:
⇤
⇤
j earayvnlfsuftwlydiw
ngugselewagyruymfqd:
⇥
⇤
⇤
naxwpctaginqufryrgf:
⇤
rlvwvgdkdjkyveatrmn:
⇥
⇤
⇤
j napsxydkroyukdqjwgx
earayvnlfsuftwlydiw:
⇤
⇥
⇥
bgonsxyeparnoraofgc:
⇥
⇥
⇥
yeladteqynfrdorzydj:
yrfdpjiitnalovxgbse:
j yjosqtkhgrynxdapikc
ntubyaqykddfdrseuua:
j agnlhyddjyrkravgeaz
⇥
yaqzhlphwwrzymnatwx:
j nyyfrsnnrlredfravto
⇤
ajczbnsysuyskrlpozs:
⇥
agnlhyddjyrkravgeaz:
rnrvaqmynhazsnxoudi:
fnaqmkyrxqfnkpyujtr:
⇥
⇤
⇤
tlujvrnipuwcvhyansr:
j hntlllcaprywqyzsbgl
⇤
ooosrmzfnluqayaqyea:
j lnqfwlarfczyxzjanks
hntlllcaprywqyzsbgl:
⇥
ldnvlarkayvangvgdiq:
⇤
⇤
⇤
⇤
rlaxmuzqyriljyvnraz:
⇤
⇥
⇥
⇤
uanrkatjymipmocyppu:
pigsraqjfxpblanyykw:
⇥
⇥
⇤
⇤
⇥
⇤
⇤
iyxymqytgynakxwryzj:
⇤
nrlxnybphklwerelnag:
sanbubxnmhrelihyfwh:
dlgyhmrbsjpervrnbay:
nggboyrvkdaptiqqtay:
⇤
aytqshdnrkzjhhcaesj:
zokfbarfcwpcyagnfen:
nagpydbkrxsbqqbeear:
wbjeizbjbihodyraxcn:
⇥
⇤
⇥
⇥
ngamybujnolrdhebkgh:
⇥
⇤
lz %c
⇤
⇥
⇤
⇤
⇥
⇥
opkwmexpyonrakrtylv:
⇥
⇥
sioeayevittdvgnrujw:
⇥
⇤
⇤
mdahlapsfdnryjysnnb:
⇤
⇤
idrfiyrexscbnvnajgz:
⇥
⇥
⇥
⇥
⇥
⇥
⇤
⇤
⇤
maahoeuvpromnyyhnuw:
nczyaqrboveaggtbhvs:
⇤
j yychyrcojpskalnqtny
qzxynrsyfnhahwyilbn:
j neujrbphcijypaodanr
yychyrcojpskalnqtny:
⇥
⇤
runibbuiguizqvazyya:
⇤
⇤
⇤
⇤
⇥
⇤
⇥
rrdkmvhswnjoyadntnm:
j ndkaucdamayjrxacumv
seajrrikmecyenndiex:
⇤
j ndlaqyryiutdcwzwjmz
⇥
ndkaucdamayjrxacumv:
⇤
⇥
⇥
fnsjcykktgbwharaktw:
jiyfyhoqyckixrjrnap:
pvrmoygrncdkdatnpzn:
⇥
dbrbyaxjdconfeoykao:
rbloizhltdcrydubapn:
j hanvaarcqvfwksfoypi
akwoymbinrqtnrdyodo:
tnrydiryadsldcbffpb:
jpgcoryhwnwojnweacb:
⇥
⇤
⇤
j mlmorlcqtnjannriyls
aippnbsgtaecjvrgydy:
⇥
⇤
ancvovrnywdzfkshngm:
kfwxarrxdvmcnmuvgyh:
mgwnadvrztdmekyprad:
⇥
yilptyrkhhawettrlnn:
⇤
⇥
goglnwjkqfvkbyravya:
⇥
rlknvlelpsryznatryx:
knraliyibaybosdtsre:
⇥
uxnldfmnyafrznurbwe:
⇤
hanvaarcqvfwksfoypi:
⇤
⇥
⇤
byohqramgmygbdnndhq:
tgifanjpariyemovpyv:
lz $v0
zanqnolnryljcfjnbnw:
⇥
⇤
⇥
⇤
⇤
⇤
⇤
⇤
⇤
rhcsqpnipryfibwwagm:
rpaqyglwjjajgglcenp:
⇤
ynlnmdykaogfwarmypy:
yhxjsirdtsuysafnsuc:
⇥
yjgayravgnolptapmju:
dmdgherabyggumnihlz:
nwayctnxxolpkmlrynl:
⇥
⇤
⇤
⇥
kxytaxranntvaengvgy:
⇤
gniyuyyrapclnrccydl:
⇤
⇥
ndwdjrnjmaayeyzyksp:
⇥
⇤
⇥
⇥
fawpznxakkdeckyrxjp:
⇥
⇤
⇥
yibunuwkptapatrghbr:
⇥
⇤
⇤
rpgcqvwrcyntaodzfjq:
⇥
⇥
⇤
⇥
⇤
⇤
⇥
⇤
⇤
oxalxqjznwtrintlwyp:
⇤
⇥
⇤
⇥
untlaarrxlypyadlqpm:
⇤
yadmrtnnmazxkbcnjpr:
⇥
⇥
nhrunlhljfkczoyasle:
zqanzhnadvrikmhkyad:
efyrbwdspkggfgikaln:
ctyfruzqwayuovnohtj:
⇤
yifdrrmpnkfvxybnvam:
vqpcaqikeqguhrypkcn:
mnolglliqgysrlyaliy:
hrhyeqjkjhnfhmhnyha:
⇤
yzgaupngeilxsrzmyru:
⇤
wknksflnyrnttzraeur:
⇤
lz %i
azqwnwekuomuerwdbyy:
anuttiijfzyfcmabrfr:
⇤
⇤
⇤
lnxryfslpmxabjfuzmp:
aowasqrkuzfwmjxnyfv:
zbctrreonaveyxnrbrq:
⇤
⇤
⇥
⇤
⇤
⇤
asmnbzroqjopwqiychg:
j rsatljzgqpnkeurytut
⇤
⇤
mlmorlcqtnjannriyls:
⇤
⇥
⇤
faujmyfctvnkarnnovu:
zafyjywxnrjgbvdnhat:
yacochwtribaunsulgb:
⇤
j iasnqysqhrqbqanvrjt
quauhyecrwunrkpmftf:
j seajrrikmecyenndiex
iasnqysqhrqbqanvrjt:
⇤
gnbqyhuxzryanvnkvmf:
pzlzsqccuynolaaymrl:
⇤
⇤
⇤
⇤
iawfutcaycecrxynarj:
mzjykaniklorsmgegvn:
⇤
wjsnwcurqcxiayrqpyv:
lznvyriinziwaectqay:
⇥
⇥
⇤
⇥
⇤
⇤
⇥
equapnocycraqkzkvjq:
tgcsraenqyuvzuynsfl:
⇤
j aytqshdnrkzjhhcaesj
j fhskpspyhnriasknaes
⇥
alebwrywzntadpwdxfn:
⇥
⇤
rduxajnibqvoirrmyiq:
⇥
⇤
j yzcsipriytujhrgagni
⇤
⇤
fhskpspyhnriasknaes:
⇤
⇤
nzpaeyqongvbvxrbawh:
adreroyijpafdlojncv:
⇤
⇥
⇤
⇥
ynpxaowdnrpqbpjnana:
⇤
glhdajnlrdqnykxhkql:
⇤
⇥
⇤
mmydngcrtagxunrjddi:
⇤
⇥
⇤
⇥
⇤
bibqlprukrkonyruuaf:
kdhduaruqynanycsags:
rsatljzgqpnkeurytut:
wyvrprymbkiadxatbna:
⇤
kyapsnoylepvrprqesi:
zbnygynyasxqiaaemrg:
⇤
kgjcawlazonryiadrmq:
⇥
⇥
⇤
anxkfnnwmnrpxeroyrn:
ofkroyzfstsdtantotr:
⇥
⇤
wmuxaytqsrrzndjqqzp:
lzmlanaybfrscutwoel:
⇥
j nslknyripizcoalmafo
⇤
ragrysnunxptklafhks:
j qzxynrsyfnhahwyilbn
⇤
nslknyripizcoalmafo:
⇥
⇤
⇥
⇤
anfrexsbtigelactrly:
⇥
rmvrknpoyatnyvfznho:
⇤
vrnehjaxjtnphroqywq:
⇥
⇥
zpitxnbmcfatiunyrcj:
⇥
feoiprnxbwyobaxjwkk:
jaalvnrwgzyxwdifiya:
⇤
⇤
⇤
⇤
tjdhhajcgaommnylwdr:
⇥
j elayasrehnopqfdyijb
vitxxntenmeluryriap:
xmxbyfrlelnraqazrsy:
⇤
ibriaknpdsnkfjarpym:
nxmkryiydvueiabhbka:
⇥
j qasinabfnvaxmyrqhaz
⇥
elayasrehnopqfdyijb:
⇤
⇥
⇥
autbzktxhrymoywcson:
⇥
⇤
esndyeajnbepexpjrfz:
⇤
bge %i %l for.end
⇥
kfaabhxyyirbsgsnqxo:
⇥
⇤
⇥
⇤
⇥
noaynfytcapgyjrparf:
fsmvhhnjrhxlrdyzana:
⇤
⇥
⇥
⇤
⇤
fanezfrufxrxamypnac:
⇤
ycybgidjaldnrwvaswo:
⇤
bjorkllzymwvfayganr:
pwnjlyntoxaknzunrth:
sjnahnyrihzwbtyrakj:
⇤
⇤
⇤
⇤
⇥
xorjbbtmnicycbrxand:
⇥
rwrxmhgkadxhbnxyqry:
vyfyyaqcvngrqiakeps:
⇥
⇥
ifznadmuqazrbrysygm:
⇥
bnddehxrgycborasmyy:
⇥
⇥
⇥
⇤
lyhdfpyuhlfjwgarnqa:
yyabargkkfghjnfbenf:
j zyrrygghvzbtaenwaac
⇥
hngvmnpmzsqabsmjyrv:
⇥
⇤
nnafrqlgrgxumgkmwyj:
⇥
⇤
yunqycoihgmcnedreak:
⇤
⇥
⇥
⇥
⇥
⇤
dvanaexlcbnyyyojrgz:
khmawmnbxcpjghrtzyq:
aqbwbnraqfitsotnydt:
⇤
⇤
ayisrlhlminpikcmixq:
⇤
⇤
dxlrznubfwauwdxwpyn:
⇤
⇥
⇥
⇥
vgzlkynoapzrmbisojn:
vwlrnyjoapiuxwqugri:
yflynnphtdqejemaljr:
⇥
⇥
yqaqjjraadchrwnywtf:
mbnaaybizjuimbarvjw:
rakljnlcyharfzfxyyg:
olahffajyniupxhargy:
⇤
yacrvtjjxekusbnczay:
j mvfifnqpwaoyjasvrrn
⇤
⇤
⇤
⇥
⇥
snrclpynralykxneara:
zyrrygghvzbtaenwaac:
⇤
⇥
syltlajfxznrzjetaxn:
rnwebhjefwryzhpijaz:
⇥
ncaywaarhlhaoeyuvru:
⇤
yjxneyoxhmayrgppjra:
ranfmtyurqqyjxgehmq:
⇤
⇤
⇤
⇤
⇤
htngryykvknkafnamrx:
jriapytqszdhjrypnru:
⇥
hizqkariquoxbrgdyhn:
⇤
⇤
⇥
⇤
⇤
⇤
argrunyzumilzroojlp:
⇥
⇤
⇤
⇤
⇤
⇤
zhqdnrykwaigiwnxvty:
gbbfwggomfsyannrsrs:
⇥
oizkzshvaybrjnwrhjq:
⇤
nntroyrbaufippbpqhr:
⇥
⇤
⇤
vaeyyczknmrnmjfnsgq:
lrhvkcyadcdccsuwsan:
yyxkeriuivggazmedmn:
dpnqrnfdityyxyctavf:
for:
rraymjplvhcbiwyenfd:
qrnsgayegcyuvsxvmyc:
⇥
⇥
⇤
⇤
tnyymrcgmfahenadoju:
⇥
⇥
⇤
hunyjarenrkpsirwylk:
⇤
⇤
⇤
⇤
miyamdvtfpnownhvrna:
bprmfmyxtnrhtyntbba:
nctawjybmdrltkytnaz:
⇤
nbyxeivdmljnugomraj:
eaofyxmyvhvmadrvqnz:
j rynlcubsasdzgfhnurp
⇤
⇤
⇤
nyyfrsnnrlredfravto:
j gejyyhplozfzrpffgna
zyronqmtgzpkswofkap:
nryhvssjzaxxmaamdnk:
⇥
⇤
frljnapyfevtfbvzazl:
⇤
ipikdcyamcenarxargn:
⇤
debxadunydxkrydafqj:
j xazwrrdnteedwfyqsmd
gejyyhplozfzrpffgna:
⇤
yskmgraazyirbanraom:
eyzejlrunvyvasnsqnh:
j ctllraynjafyrypgqkt
cyamrxrksklhcogonhy:
⇥
⇤
⇥
⇥
rynlcubsasdzgfhnurp:
⇤
⇤
j anumjkunajiqwyrtajh
xpryakikqnrjryganwp:
j qpadnrruolcuuyiiapi
anumjkunajiqwyrtajh:
%Read %x %X %i %Δ
⇤
⇤
jorhuzaxsiyranddgrs:
eyehlardtebfueenaay:
⇤
fpzjupyaniaddzroynw:
npaylraxpqftyucrryg:
wwxbkyjrtwsyarntsdk:
⇥
beq %x -1 else
⇥
ybaklsrimzqrjycirmn:
⇥
⇥
⇤
xnltysrvrlaqdtmeyco:
penynhayawudmslxtwr:
⇥
nnyzdemawixrbzgoycr:
dhntmknoyrxgnovaamn:
⇤
⇥
injyvakjryqnhrjghqz:
⇤
⇤
nryhavruwhawiqxbswy:
tsarafznwofwyctdgyn:
tmmvrazwaytuzywzykn:
⇤
nnxardeycgxqzlrwmtl:
mrlbxyxlfawynjchgar:
yargarbgbnxclolxpzq:
⇤
⇥
nrvyinybxasfanjyywi:
⇤
beq %i %c else.0
akwpykpzupnhpknrqzc:
⇥
zdjaopvznddrtpyrlyy:
xzonyomkrqrrzewhaep:
⇥
⇤
xdiogrdntnautvhdbyi:
⇤
agnjqbrrvjrnzcyzews:
⇤
⇤
⇤
mwsrbnqucymuanktkta:
lgglynhrayepvpxkaeq:
⇥
mhuqrriawzyqkzavlng:
⇤
nciywsnrruygiaknanb:
⇥
⇥
⇥
kvamzcnrlakryxfcmkt:
j onzjybbzdqubjvgrgam
qasinabfnvaxmyrqhaz:
⇥
⇤
j debxadunydxkrydafqj
⇤
onzjybbzdqubjvgrgam:
⇤
⇤
⇤
⇥
⇤
⇤
⇥
⇥
⇤
⇥
nshktpldtitrrmhaojy:
⇤
%Write %x %X %c %Δ %temp
⇤
⇥
⇤
⇤
mhnernfabyxcprfjkmz:
⇥
osvapqydlwfjlzrcnyq:
bvxiatooyjcirnruynu:
⇤
wnakmwmrerjddyeuhur:
⇥
⇤
yikcvlvelmfhyvnatrg:
zeipsfnyhezagztsrrz:
⇥
daobjqrqyxwcmyaznsc:
nqkadbnxywkzlrafezd:
uanbmamymmvmxqvbrqi:
ayccairnvzdaeqpkkys:
⇤
⇤
zeyoynoixahratmnqrr:
⇥
⇤
⇤
⇤
⇤
chqxjosserwkmnrayyd:
⇤
fwfjemdaccigyrynojs:
cyqqntcekqqvytifare:
⇤
inc %v0
tdukqmhrotswbnyifay:
jlolytjotraepnzzjpr:
⇤
⇥
⇤
⇤
⇤
j xhjxtrzgdwmnythvuna
⇤
⇤
⇥
⇥
hcyrnyxfelqtbftaqnb:
⇥
afzkpvysoyrvaeknjxk:
⇥
⇥
khgtdzaaaigznqrrmsy:
movnexvpvawywcytwsr:
qatozencwbyyrlxashv:
⇤
⇥
⇥
⇥
⇥
⇤
mvfifnqpwaoyjasvrrn:
⇥
tbgpnayporrywndcrad:
⇥
pqyytwiswaovgnjlicr:
⇤
⇥
rxtxazyuekaywzyvlnb:
eadamkngsrpytpgyrlk:
brguzrdxryfyhauvnow:
⇤
⇥
rawycaxarzjcpczzknw:
j tnylxhxlqkhhagmrrwo
nbbeshilriwyakgrcvr:
lxbdnymeesrihaehyml:
⇤
⇤
⇤
j ayzveclxllnrnrygals
⇤
tnylxhxlqkhhagmrrwo:
⇥
⇤
ayxqahgbfbnpdxfrxrw:
otjyudnafhijyrnliaq:
toxdkgukdyvnifzvrna:
nbarnxkaszyxusyvouq:
⇤
⇥
⇤
⇤
⇥
j tnrydiryadsldcbffpb
⇤
fnrsdxbookaopynofiq:
ktksyrhnwgmjtdeazek:
⇤
⇥
⇤
⇤
⇥
rvulrsiukbwuuaybfln:
hbsakoulrkxgrqynfan:
bowvyaccybqraynxlym:
⇤
⇥
⇤
⇤
⇤
⇤
lghvylmagerkvzcnrxn:
j rgjikennsriqiyareay
⇥
nhzatrmxxyvpzldhokj:
⇤
yzcsipriytujhrgagni:
iynriyabegidkraxmqt:
⇤
j arzasprawfgyrtnpezd
⇥
⇥
rgjikennsriqiyareay:
⇥
⇥
⇤
vyrnibhqtvdexpddray:
xhjxtrzgdwmnythvuna:
⇤
j jiypbxyhqxcdrsawenz
asizdgxyspjaoldjrng:
j acaygwkfnionwyyqrbt
jiypbxyhqxcdrsawenz:
⇤
⇤
dfybrnsaiumyrboghaq:
⇥
else.0:
lnxpyavxrlhpuqmhmre:
lbvdjthlvvdayrnjurm:
⇥
⇤
⇤
kbdrnnyffxofnaprrtn:
nvaryaxfczgreebwhxa:
ymakaioaanfjyxnrtrd:
pknwubrtfaodxmypmfd:
⇥
afyrrysnapxgdfphrvs:
mrovyzewjrgaanyiyau:
riasuypenbicoxkffzj:
j hnepjvayxefrtstzrya
mjicrznnzigmsioynza:
j xpryakikqnrjryganwp
hnepjvayxefrtstzrya:
⇤
⇥
⇤
rhylnacgijvzyyxcyia:
gguxnyypcrqpmqrlaeg:
⇤
⇥
⇤
qnykqjkacdlusrjsjdx:
brelwnwfevoswtyrusa:
⇤
⇤
⇤
trtsanmqxzxgaazymrl:
rxsqqounnzxiyremafj:
⇥
mrbnnvobjiaxtyweslr:
⇤
⇤
⇥
⇤
⇥
⇥
⇤
kirqqomtrratnzpygxh:
⇤
rdruskakzzyjzwvnijs:
⇥
j azehytjkqnnrlolaaop
nzygvaoimmcryvfqipu:
⇥
napsxydkroyukdqjwgx:
⇥
j ibriaknpdsnkfjarpym
pcrndsbcsmaspgqtyrn:
azehytjkqnnrlolaaop:
⇥
⇥
⇤
⇥
⇤
⇤
⇤
pyrdaogonrabrpxycmd:
j qksauyttarnxnibrkay
jmynagljyqnnfvaorps:
j quauhyecrwunrkpmftf
⇤
qksauyttarnxnibrkay:
vsbleybpnrsgdaygbfh:
⇥
⇤
⇤
arhbyfvmnjcbyhdevui:
⇤
nohojraxbrvmljlyhwp:
⇥
⇤
⇤
kfkyafauwvurgwvhndg:
⇥
rxhnvqgeewwvamgoeyp:
⇤
cgprcyanuccufnyayly:
⇤
⇤
uvrnjbmufciwyaqwzxw:
ehgvwwaryzhzdndgfpn:
iunhoqqmrpyvznrmadk:
j rtaqnzdaimbudxybivv
zswrnruoxfkuxacyrmg:
⇥
⇤
gagozxjetyirrrfvnin:
xyaqirvrjqbcyixznnz:
⇤
⇤
⇥
⇥
⇤
⇥
j yhcwpgytroneggdadtw
acaygwkfnionwyyqrbt:
j ijziryjqxmbakkgaanw
⇥
⇤
⇤
zxvzwhanknbujhrygev:
yhcwpgytroneggdadtw:
⇥
⇤
⇤
tyrriantyijmyoepmua:
⇤
j aqbwbnraqfitsotnydt
j eloteavsryjpcoyntfq
ijziryjqxmbakkgaanw:
j anyejrekvkykgvkinvu
eloteavsryjpcoyntfq:
⇤
rtaqnzdaimbudxybivv:
⇤
⇤
⇤
⇤
⇤
xybajdvyvynyrkjcucu:
⇤
⇤
⇥
⇤
⇤
nscvaqrbpzcbsydjcmn:
⇤
pzlcnjqguyyrbarooiv:
guyvagdnpjdzanzwrjp:
⇤
⇤
nwlnfqyrlseajzmboip:
qnhajjguqryjuoaprcq:
fdgpniyclyzzfnrhatx:
ahsbytarvnpdenzfndg:
⇥
daykkxravnykmtrsuhx:
⇤
jgkgryfpaiqyzowlrnc:
⇤
⇥
⇤
inc %c
aejyirrcgqlsexaygnd:
⇤
oxwwooviorrawayiznq:
⇤
⇥
rbkegbazldiyngcjbtq:
yyvgaanluahbinmqdyr:
⇤
⇥
wfvyomihgvaropdankm:
xrygzhvskaofvgklnak:
⇥
⇥
j apwvxehhnffmyrlxxsy
bsrenwadeyqwpbjzypa:
j yaqzhlphwwrzymnatwx
apwvxehhnffmyrlxxsy:
qwbnddzyliaibnsurse:
j mhyuclemtasuaapnvrc
kyvzradrnmoelavnjwg:
xlnxomnyambcgxzyfxr:
⇤
j asizdgxyspjaoldjrng
mhyuclemtasuaapnvrc:
⇤
⇤
else:
⇤
zrydlvgeqoaaopnfrzt:
⇥
taankgnyihcgrycaqhw:
xrfgcekayxzxnfhynrt:
ayyssauabbxvrlnrurt:
⇤
⇥
⇤
nakmygtrlqxmpflrwlq:
qemxyinnrfkgmsnyiua:
wgryrrnxmpixarmfnpa:
⇥
bndvdymwsmranjgmewt:
⇤
⇤
⇤
fdrtjszoyltcapyinfd:
enargrhrghyqoyddkjq:
mjsrmhddzigyafbvans:
⇥
msrxqidpsjcvyyhskna:
⇥
rxgnoicreyiqfczalpc:
⇤
⇥
⇥
nigjrlbarcmxbtzrydi:
zelxsntkarkqynpjwoa:
⇤
⇤
⇤
⇤
⇤
⇤
⇤
ttkarkgnuceoyibrgal:
⇥
⇤
yrlaqocgijymnanrmpy:
ln1 %x
ypznekniytyrmbwuaso:
uttokcprggxzhzyulna:
⇥
⇥
wfcnnybworvijhrrazr:
⇤
⇤
nbcwaojrqfmhyjnwxnl:
j ubfhqqokrsxhyaqehyn
⇥
⇤
⇤
ubpnfyuyaaigjycpoor:
uearuydglvkabsnnzyu:
⇤
wognmgaspqslratosry:
sjnivhjwaztsrdyqxkr:
srurtzxedtyjangszbv:
uzcuyotinarvidarcjt:
yaqhndxiiyoagprdxdm:
⇥
fvfyyeiulajtcmqndrw:
⇥
duinqywcxzaklafrhkj:
nvsoyqgadorqrmqtjuc:
njmogyairenckrjntrr:
⇤
hnkaauoiryewyllynej:
⇤
eibqwrxoalbrvnpynic:
mnnurnnbnvkacnfmyyu:
⇥
⇤
⇤
⇥
ulxrkzogvndnhqryuaf:
⇥
pklslyrbfqzeyxawyna:
ljumtyrnstpuqtncafq:
⇤
larnsyihqgsmuptyogn:
cacmcagvrtddpqnylja:
albunlfyhrbntrydcny:
aggrbsbjdwrbrhblynw:
⇤
⇤
vrhmhaymrbrnozqnbal:
⇤
⇥
j zswrnruoxfkuxacyrmg
eydlwrrykraxnsjnjxk:
⇥
ubfhqqokrsxhyaqehyn:
⇥
⇤
onayxjzxuprinyvewok:
⇤
⇤
⇥
⇥
arnncnmkrxofpplangy:
srvridnolxcmonayaug:
⇥
⇥
j hqfanhsazrdyxpysnpe
lhrqokmtryuvanebzah:
⇤
ytvtnpchyqrnjayhwcp:
⇥
rnwbwssoycigyaqpvir:
⇥
⇤
nqnafaacsfddixyrhhu:
iinyvotnardoiynrsxe:
⇥
ctllraynjafyrypgqkt:
vfbmwbylpyllbagnrsy:
j mnnurnnbnvkacnfmyyu
⇤
j nbbzudsrsyntrveanbq
yjosqtkhgrynxdapikc:
.end_macro
.macro validate_row_xor_col %row_xor_col %num_rows_xor_cols %v0 %return
j wwjeryqmncafnlrhvjy
krhcnsunpaxxrykkndq:
⇥
btluzprbnnhyrarrnta:
j mafqefrrbnoyscksapl
⇤
⇤
⇤
myyrgohpknazprbpavn:
⇤
j kwxarnkgbwtehmqoyvt
vnvfancgbryyylcsaew:
j bacsvlsruagnachrary
kwxarnkgbwtehmqoyvt:
⇥
⇤
⇤
⇤
bekqnyvaspxrxcuibrp:
alyigfaaenpvrjiouin:
j ypcfezwndyftrnadflp
esgypeknvrtmyalmrap:
j rtqbpyefkirnvgaoihm
tgrdnxamarpkraynjwe:
mafqefrrbnoyscksapl:
j yyloqtpsnzdazlghrne
rtqbpyefkirnvgaoihm:
⇥
⇤
sackbvxklnmreecqeyj:
⇤
dgafkwyfkdqnyorivsn:
wrabimdbkdnmxsjlaqy:
ajhlwonwnpryyrndave:
⇤
bge %row_xor_col %num_rows_xor_cols fail
⇤
⇥
⇥
⇥
afdagytfhabhnxmpoar:
⇥
⇤
⇤
⇥
⇤
arnauaolpqumiynxtkk:
bge %row_xor_col 0 pass
⇤
⇥
pvouriobzcacyaqktwn:
⇤
⇤
⇥
gannuotkhajyrtqehet:
fail:
haouzmpdnmvvxgryylr:
⇥
⇤
⇤
⇤
mydoybjcvspqlunrbaj:
j sxmvmyrnppneexelika
⇤
yhryaaebsjcekotnyly:
⇤
ayxksayuinrpjkvfhvl:
j amngxkqhlhhjbrngynr
⇥
sxmvmyrnppneexelika:
⇥
fnutbjayqpkqgargwee:
⇤
j lgyvocabpwxwntnbrft
wwjeryqmncafnlrhvjy:
j xhgrechxynhenrqarbz
lgyvocabpwxwntnbrft:
⇥
xmrmkanrepisgyckirg:
li %v0 -1
avpmqrityglmknslqia:
j oaaimyrgberlynzkvez
hwsarexyvowjppnemnw:
j pmunvfyqhrgarzrpsrb
hexyzxzrzeabeqgnrrw:
j vnvfancgbryyylcsaew
pmunvfyqhrgarzrpsrb:
⇥
⇤
ypcfezwndyftrnadflp:
j bjzuarbbykklncuzfgy
⇤
oaaimyrgberlynzkvez:
ydhrnuxirkgatfsyufx:
jrevrhnvwpymrwweafg:
ooaotvasyqytnnmxrqg:
syaerpjrloroonnaylv:
ubihgamrpnzfsuwtrfy:
⇥
⇥
j %return
pass:
hyytnihauwirunvywpm:
atfozmrnfcdbzcfyati:
⇤
j yinzvswsueklqyaktrp
⇥
⇥
⇥
yjnmwaammjqolnpyiwr:
j bekqnyvaspxrxcuibrp
⇤
⇥
⇤
⇥
nyjicdxlacdmrffjalb:
yinzvswsueklqyaktrp:
⇤
li %v0 0
⇥
⇥
⇤
wlhxrxcyrwsepiaorny:
houtniavdcqddgurwxy:
eqafsksvhdmpaxykrvn:
wmakdkzrpvnppayannw:
lfejayrfsxcnckyeqtn:
⇥
zjanlrsuhoygtewidua:
⇤
j vsjapmrvsnyhjxirpoc
j hcnjheryksvffahruay
yyloqtpsnzdazlghrne:
j yhryaaebsjcekotnyly
zlrxondxyaqpzyaczjh:
galrgynuyhoxorvvmon:
hcnjheryksvffahruay:
⇤
⇥
⇥
⇤
⇥
⇤
ydkgtrgjzumudbaanfa:
vlifmdrjaslhnyywntb:
⇤
bjzuarbbykklncuzfgy:
⇤
rrfyphjkntgaeuwndaa:
j xhrfnkbuufadnroybsl
xhgrechxynhenrqarbz:
j hexyzxzrzeabeqgnrrw
xhrfnkbuufadnroybsl:
⇤
⇤
j esgypeknvrtmyalmrap
⇤
j zayayxrkhsnmiueyjsj
amngxkqhlhhjbrngynr:
j yjnmwaammjqolnpyiwr
⇤
fcaxaypmmtgnrknjpnw:
rqakiymywvnizojxamb:
zayayxrkhsnmiueyjsj:
j hvoqhkysentaauormae
xbyymniqkaothdzlryx:
bacsvlsruagnachrary:
wtynwrswvyadjoyyljr:
⇤
j cwabcwnerlymwwxbbkt
hvoqhkysentaauormae:
⇥
⇤
j myyrgohpknazprbpavn
hnwrpjriihylgaqyhix:
cwabcwnerlymwwxbbkt:
j krhcnsunpaxxrykkndq
vsjapmrvsnyhjxirpoc:
.end_macro
.macro validate_direction %direction %v0 %return
j puytanvaotmrlhomikq
ydqstcfynqrasxwlstr:
⇤
nnlwfkkkarzyonfkpoh:
j ffnyfxwkdnafmrrqrlk
zftyvapynjnbremtfay:
j rtdanzvziqccyojpjry
aertpiykgwnrrenqlpy:
xnyqjspavofoymcrhvl:
ffnyfxwkdnafmrrqrlk:
li %v0 -1
yykdddrzhabnnrphpaj:
⇤
mfbdkyxpnvdvkxmhyar:
nkyszrwstsynwhhwrab:
⇤
layrfasgyawncgavnns:
oduafoatnnrqnywwdaq:
j gabynwbipnotrcoyfqk
rtdanzvziqccyojpjry:
mxdhrgydznpjlpwynac:
⇤
j oeynzfurtflggtyaeej
xbaiwlatyejrgsrknbu:
⇥
gabynwbipnotrcoyfqk:
⇤
⇤
pamlyuicmyavtbenrim:
j wrqnwyhvvqvaalnsrar
avbghnvhuwdpkzyqryd:
⇥
j kaprdqnyfackfibjaxi
wrqnwyhvvqvaalnsrar:
⇤
⇥
j %return
j hclywkdgdyyithamrmn
⇤
yvveynrtxvbnpmhsank:
j avbghnvhuwdpkzyqryd
hclywkdgdyyithamrmn:
⇥
⇥
⇥
alnwieyggrhcdfqbbfl:
j exsutnansrhwmarglyu
etyaepnbqatwmhrtnda:
⇥
vgjyyhukredgnniprqa:
j yvveynrtxvbnpmhsank
exsutnansrhwmarglyu:
⇥
⇤
pass:
j whydoayhfwborsojneu
⇥
⇥
⇤
oeynzfurtflggtyaeej:
⇤
j irafqgrelnayynyeyvz
ayzriibhxhmszkxnrnq:
⇥
pisunaajpyiuatbrmxa:
⇤
whydoayhfwborsojneu:
j vvqymcantrwpwphmauo
puytanvaotmrlhomikq:
j tnmjgetryafuaznoqee
⇤
vvqymcantrwpwphmauo:
li %v0 0
caxynakvlpbwxrraujt:
svmnamkryvdjgetguix:
ylfkoesznxryervvqoa:
zodaqgtrfnfxpsrycmd:
j nkbadufaarivmcuhaay
irafqgrelnayynyeyvz:
rlhayvrqkuoxnvqrjdz:
⇤
j nbnorhyuuajiysyneea
⇥
kaprdqnyfackfibjaxi:
⇤
⇥
j zftyvapynjnbremtfay
nbnorhyuuajiysyneea:
⇤
bleu %direction 1 pass
⇤
⇤
j unawsxnvuranrwytfyc
tnmjgetryafuaznoqee:
j vgjyyhukredgnniprqa
unawsxnvuranrwytfyc:
⇤
⇤
⇥
j ydqstcfynqrasxwlstr
nkbadufaarivmcuhaay:
.end_macro
merge_row:
.macro merge_row.macro %merge %Read %Write %v0 %A %h %w %r %d %X %Δ %a %b %i %j
j syennfrajqxayoepvtv
nyeaqaxonxpeumjrnkn:
⇥
⇥
⇤
⇤
⇥
yryaazbpauapnpvuvdr:
⇤
⇤
⇤
j ergqlrydyhuaafmtrsn
hcfvyrnyvndnxxnyapw:
⇥
⇤
⇤
⇤
⇤
⇤
evnhnuhzlueaaiqygrb:
zrlaqwfyjryicykhuen:
⇥
⇥
j jteivcraaqqauwnypsc
⇥
ergqlrydyhuaafmtrsn:
⇥
aqzahdmyjvynsrillye:
jhcrrqavydnknrsqtqj:
⇥
ronjxkxseyncxkrljka:
nftclaeuzmoyhbgrnqr:
⇤
⇥
⇤
⇤
⇥
⇥
⇤
nrwyewlbnaaryimjksa:
nibvavnttaypuuhodqr:
rnuyraoyjzrarnggkav:
rpndilejkaxckiyhhaa:
lykbnopiarydtxijmfj:
⇥
nyvnirrtmaosyrfpicl:
gjaiwjrijjjmyrxbfmn:
⇥
hajwnyimknxyrnojrna:
⇤
⇤
⇥
zonflmurchcyaqhvrge:
⇤
⇤
atypryhrlvwioonwrjm:
frvnqrwmvxxzyavxpra:
rdpxcovrtaynbnctayl:
cbqjgcdnuyaeafriiyz:
⇥
⇤
yauawrmpwnvrsywdqzf:
vhndjaeradhiuehnxoy:
⇤
ynrcebyrqnlahlcawny:
⇤
⇤
rjajaghynbdqywsxmcx:
⇥
⇤
ynjtrjgtuahsaaovsyu:
⇤
twlrsekigygucaxadmn:
⇥
⇤
j ocpuablrqnzujsaxvty
ydbmkayqqysblnrkfrr:
⇥
bsvwfdyaponobrksyyz:
⇥
pucwkwkyedrdanyseho:
⇥
eqehyvoacfsnsryboqq:
nrfiuyegnkjfttzatrb:
⇥
j suranneymnugvaorxfy
ocpuablrqnzujsaxvty:
⇥
⇤
⇥
⇤
⇥
ygexahvrzjoogknxrwm:
⇤
uweyrwvpgnjfeocboxa:
dkmnnhkajofmnafyryn:
knfycvpjanrganqephq:
⇤
⇤
hrjwguqysnrjebazali:
⇥
j xofnyrgdgppfasfhmpw
⇤
⇥
axnsffrpkpjyjensndn:
j ynrcaftpjuvljcrrvkv
⇥
⇥
xofnyrgdgppfasfhmpw:
⇥
⇤
⇥
ayxxsnwrbcgqyahnjcn:
⇤
nmseycgytmansdjrbfn:
⇤
pe  %X %X
⇤
⇤
pe  %X %A
⇥
rbrnzjgasiytynkpbxe:
itvlaxbocyehrzcrrnn:
aciprhjymhaekcyhpnn:
j nfxvsajadoyxwihmnrj
j vainxkcyyxidzlrqomh
ynhwuynrsnyzatzkixb:
j radntrxdalisgryrztu
vainxkcyyxidzlrqomh:
⇤
fryrivkpanccrrncyny:
j jruvykzabvonplgltyu
isbjycovpigynrdkxja:
ynrcaftpjuvljcrrvkv:
⇤
iaronbynwczubartlmb:
⇥
⇥
⇤
j cdfdpfrbalywgnpxxpm
jruvykzabvonplgltyu:
rnktxynrgvcafgljnbr:
⇤
⇤
⇤
⇤
⇤
⇤
rrguylpdnponhqanirt:
nagyncrkeajrarepwbv:
⇥
j bahnfqxyrdybbrbvkin
cdfdpfrbalywgnpxxpm:
⇥
⇤
waknunohawzywayyrqt:
j aonviualrrzxygaonjv
hgdiyfvuqynvvniraor:
bahnfqxyrdybbrbvkin:
⇤
⇤
⇤
⇥
⇤
wxfapknmfbsrbyarkac:
⇤
j strqjgngvagtgyvtnzh
dxuylxwalclnrydhtkk:
j gjnicvbjacsfcsgydry
strqjgngvagtgyvtnzh:
⇥
⇥
xovywqngronstrmoavx:
⇤
⇤
bwqxtidtkurmayehhnr:
vpqxdyegamzdwnnfaar:
j epzytvltvdryvmadman
⇥
⇤
⇥
⇤
bvlgronolywktxlaipc:
tcncyyurmvbaimlvlcq:
⇥
⇤
⇤
nfxvsajadoyxwihmnrj:
⇤
⇤
uyqakrpvrrnneyamasw:
⇥
⇥
⇤
⇤
⇤
mncraoqpeayvnbvftre:
⇤
li %Δ 2
⇥
⇥
⇤
⇤
⇥
⇤
⇤
⇥
⇤
⇤
coerluybneypnazaxxa:
⇤
wskkzvsjcayfsranrvx:
dlbabpnkzasyrjqyzgl:
trkvvqkgvparnsakgyj:
⇤
ixbbiigfripynkdzaym:
⇥
jdachiavlkhngbyyarj:
j dmqijnxnvdwrjraymfr
hnnniiyfkeydjlcyrea:
j axnsffrpkpjyjensndn
⇤
dmqijnxnvdwrjraymfr:
⇥
ilrnardncnnszyyglct:
⇥
⇥
⇥
rzstnfnrynyrhaqerva:
nlrsxiyzncdtfyavdhr:
ocdsadjybravnpdgrhx:
fernriphvkizkchiaqy:
cykhkeavunrtfsxmbrn:
apooratgvqbbeknnxpy:
⇥
pjylynxnmbtxwyrlpah:
j fhrabayvsyfjznfrztx
wljcaulrvysbcynsnwv:
⇤
tpiepmrganvanizylub:
j yaeaxrasprorhfrynos
kprjdrycayxmxinmgdi:
⇥
suranneymnugvaorxfy:
j rhaqkuyfumknhhrfqeg
⇤
⇥
⇤
nywvzfkgmihrangigjf:
⇤
yaeaxrasprorhfrynos:
rzdtpityxougaflonav:
ztbosqzyekawnhrtaiq:
j bbvfpyraqvnlnmsfbaj
⇥
erufliaernkpmfcynkw:
j hnnniiyfkeydjlcyrea
⇤
bbvfpyraqvnlnmsfbaj:
⇥
⇤
⇤
⇥
⇥
⇥
gxrnsarymoagpvurbqe:
j hcfvyrnyvndnxxnyapw
⇥
fhrabayvsyfjznfrztx:
xksihrnrhamtyqzmvns:
shmgypivarbbwiuignt:
rpbgikgjnabyqapzrfa:
⇤
⇥
⇤
yyyqexfohtansfdmarb:
⇥
⇤
⇤
⇥
taqolwefvrdmwyynfqr:
⇤
⇥
⇥
⇥
jrmmmoknsyvjnwhkdan:
⇤
j npgyzdillmrlylxozan
yaijmnfpjpcjngararp:
warybwosxnjrfedtgyg:
⇤
dirrxyhxypqzyenzarr:
ydojnmqaadufmyyzkri:
aaumsfvrnrujpzaslyn:
⇥
socyermasnxdbxbnhzf:
⇤
⇥
⇤
nmrncagycaifelsedrh:
gaeylrcyiyiwuelnczh:
jteivcraaqqauwnypsc:
⇤
⇤
⇤
⇥
⇤
⇤
⇤
⇥
⇤
j rdjrbwpuianyerndogq
gjnicvbjacsfcsgydry:
⇤
j lpdyayyztkcundszsrm
rdjrbwpuianyerndogq:
⇥
⇤
⇥
⇤
ainycyznzzmprveeczp:
⇤
zotbrnrtwddvyiacpsg:
j bwqxtidtkurmayehhnr
⇤
fffhycpoaxvnuxrywcy:
colwunjlyaarrxlsnbg:
⇥
qadxgpkzqlurfuynyol:
⇤
⇤
⇤
⇤
npgyzdillmrlylxozan:
if.end:
heyzavcqrmnaycsofqo:
rdnyuabbaoahfancqcd:
⇤
txyrozurimnxujarapg:
⇤
⇥
adyaicnikhyamaurfjh:
nnsrtxuetjaynrpzgea:
rlbyrpegnxkgxvaynpg:
⇥
efcchukefqfklharyng:
sozwuzjogbmprqfvayn:
⇥
⇥
⇤
ornpouyrbmqaldmojak:
⇤
cayelnilykvndrnhgza:
mgcqddmrngaqptyarrj:
tyiadowwrnyxdyrdjvo:
⇥
⇤
⇤
⇤
⇤
ywantwaiborhnahniux:
⇤
⇤
xclmauonxqtkepggrry:
⇤
⇤
⇤
⇤
⇥
zowkyfohrownqoazcgy:
⇥
⇥
⇤
⇤
ypalyvhcufhdarhyznj:
⇤
iyrznideyerjamnsodz:
⇥
mgkkenbhrwhiyhgeant:
⇥
jpvvkrptuynyagnvmjn:
%merge %Read %Write %v0 %X %w %Δ %a %b %i %j
j jaburbwqsiynnupyfuk
znajayiwrqnrenjmhji:
⇥
j erufliaernkpmfcynkw
⇤
⇥
jaburbwqsiynnupyfuk:
⇥
⇤
epnbyqhyansqpjmwmrb:
⇤
⇤
⇤
⇤
⇤
⇥
nrngfodxcbymbljnyya:
⇥
⇥
j bemannbfurfvjiyvsnc
⇥
ruynzoammxihyrnqovn:
j nqzasarfzwiujsyzlfg
⇥
epsxysnvfcxdraabdxb:
bemannbfurfvjiyvsnc:
⇤
⇤
⇤
zsraxeoncjgysoswiye:
pulyxktndpanlrdnesb:
⇤
⇥
punyrycralrowbhsiqx:
⇥
⇤
⇥
eefraruyyoodnyjansu:
⇤
⇥
rootyjakwvsaycnvoln:
⇤
⇥
zspnymtrpfagrcvounf:
⇤
⇤
oaanqmrwopjytpnrvpr:
jvkagynudrwwvvarboy:
⇤
⇥
rpymdwnsxbbpqbrnraw:
⇤
⇤
⇥
⇥
⇤
kjnmyszmravjyoqyord:
⇥
⇥
sanazywomldbnlnrumw:
⇤
⇤
ueaeguwmbnrxvurmapy:
⇤
⇤
return:
⇤
ixiyeynbixlroryvabe:
⇥
⇤
⇤
ajsufnryzbnnjlcmbje:
jfogyjzlrlgualnhyqb:
tsrfrrqdrvazybnaott:
aynrqacknpdxhsjjwyx:
⇥
⇤
⇥
⇤
⇤
mcasagfspfbqryendvk:
accnyqgzrzycdseyrvy:
⇤
vyghyptssnrzyeavzjf:
⇤
⇤
⇥
lelnaraynwpfaptbnvh:
⇥
sntlgareyajuqifoilb:
⇤
⇥
⇥
vxmrunaxkbnywjongua:
j dhyaqqlgehwecpaxndr
rrfadjedmkynvdicodv:
strnuyfmvqnlnzaknvr:
j clzjyenoovsrqvwcnae
dhyaqqlgehwecpaxndr:
j lsrtpnamwwbdxxqcpyv
ormfawjqnypowxjvzox:
⇤
pxamercsyvnrnaosapr:
orvvvkwnadaagsbnyzi:
⇤
j rvaicnhnlytwyxxvucp
boccirnaaznhyrdfezr:
daunrehjohtrheyawds:
yqtrvcafwgywwbxnoto:
j znajayiwrqnrenjmhji
rvaicnhnlytwyxxvucp:
⇤
lbzmvtmapnryjascxun:
⇥
fksnqageyyroabbyibv:
nqrwwsvomgumyanexvi:
ueorkrgttgynybgjzia:
oudzlyeqarjxyuzdanr:
⇥
⇤
⇥
⇥
⇤
⇥
⇤
⇥
fcrvnahgakvhguhhcyb:
⇤
validate_direction      %d %v0 return
vawlyzyxknjuunryzhs:
arnlodzegpbxynfqrzg:
⇥
⇤
dlhamypudrmpmnlsgib:
⇥
qprbpfwnyenoxnayobi:
⇥
ryydoxjcyswqbainsio:
⇤
pjxwlbfvytqfngbnakr:
xtnerayylrahwxamnoc:
⇤
⇥
jxyxkavffovqrnryatn:
nayyizzhjcbriknueyn:
⇤
lsafrlygvmvtvpdnnbk:
⇤
mhruglyroakxnsaessr:
j rorqgnygwzqolngmeam
radntrxdalisgryrztu:
eepksygsebiaignhhrz:
j depccakngrrfzwpqyud
rorqgnygwzqolngmeam:
⇤
insyleltyuvjdafyrsm:
matbnhulzjarylvrufy:
⇤
⇤
nxokptqzpeysrhlayrk:
⇤
sakytqztrvjupadnegd:
ygaidxdcfiwnrnpqgkz:
⇤
⇤
⇤
validate_dimensions  %h %w %v0 return
ngcukbtnhyzwprsnaxe:
vxabpkfmybjackynmur:
tfavinrrcfryfmkjljr:
⇤
⇤
iurmehnywylnwadqjst:
⇤
feiyxrgyjndyreqaxyg:
⇥
j nnbkyhagywanvrodysu
syennfrajqxayoepvtv:
j awxrdtarxggyyjwnlrm
nnbkyhagywanvrodysu:
⇤
⇤
⇥
⇤
⇤
validate_row_xor_col %r %h %v0 return
⇥
⇤
rsenacxzrtgxwyahate:
tprinnrrwyatjsnvvaw:
⇤
nxprqwadkgzruhstncy:
⇤
⇤
⇤
⇤
⇤
⇥
⇥
ehyvkfryodqtvaktmnd:
⇥
⇥
pqnrkbpvgymuqbanril:
⇤
⇤
ibeounwayvakvpyrtrl:
⇥
pmptopyxuhtdfnrvtaw:
anbfqxzabjdhrnsrcjy:
⇤
⇤
raatngyeapntnzcncxn:
⇤
⇥
kkgylcvzanyrmsivhhk:
⇥
⇤
⇤
⇥
⇥
hkntpidorivbnkuycaf:
oukkgakrtxnlbgvmciy:
⇤
⇤
⇥
j nvuoytndlhrtuqxmasj
awxrdtarxggyyjwnlrm:
j ynhwuynrsnyzatzkixb
nvuoytndlhrtuqxmasj:
⇥
ozjaqtcoknzmyqrcfwh:
⇤
noyglrliimaeauvutss:
⇥
⇥
djoiyvlnzjxlragiuti:
j hnrxingagxsbaihpdvy
iluxatvqyxgjngnyrey:
⇥
⇤
j gvaynlzrahrcswcwntw
⇥
⇥
⇥
hnrxingagxsbaihpdvy:
⇥
nawfateyryykfmjkzsx:
bne %d 1 else
nqgryocqapmkrvrrjny:
ghcahnemrcrcuylrgoj:
⇥
dxtnymfkjrbdrntmasp:
j fnrtyraysdpryqtfntv
depccakngrrfzwpqyud:
j iruaipealwunaccbvyx
fnrtyraysdpryqtfntv:
⇥
aydyajqnssktozcbryb:
⇤
j kqewpgynerqvgmozfva
cfrgapndinhavherqjy:
zoeiyqxkarnydlqsthe:
⇤
⇤
⇥
⇤
⇥
⇤
epzytvltvdryvmadman:
xrnpfooyzgtjrtipcaa:
rbnaureaunivyvyjxyf:
⇤
⇤
⇥
jnmrrekuqrpprbjafry:
tadkyxruutlrnzruynd:
⇤
j lbzmvtmapnryjascxun
zhyzqynwryclmyioarn:
⇤
⇤
⇤
qfhilraypuxjnagausj:
hwenrgpnqhidwbgtyay:
⇥
⇤
qnzayitglbrkjfoutvq:
⇤
j pdohylrrncabkydqmyx
cryzndmaflvsnljxexc:
j aqsavngewundtqhnbry
pdohylrrncabkydqmyx:
⇤
fvsripsfrabantqiypp:
⇤
nnwbysrlpahuyzxpany:
kqewpgynerqvgmozfva:
⇤
rorrjyayyvmkcbfonxn:
rtiiagbyewqjqfnoruu:
⇤
⇤
⇤
⇤
⇥
⇤
⇤
zzrypwnanmygdjroxsa:
kyfraksrvhintaqrsyx:
brbqolnyonnqaatwxra:
⇥
brflaoeayimggrsmzwn:
tcmuorbmhnmiaajrtzy:
⇥
⇤
⇥
⇤
⇤
lnlxgtxgizrqvaybiqn:
nyvkfrhnavrdzryoqan:
⇥
⇥
⇤
⇤
hkhzuazzngnvrobrpyr:
⇥
⇥
⇤
⇤
yulpnnourbrkwxtracn:
⇥
zakmsnrpsymlhsnador:
⇤
⇥
vtesajgompgykqnsyir:
segexcsjafrnyvbbzcq:
⇤
zazmnsayjskcnmrqdgk:
⇤
⇤
⇥
⇥
mul %X %r %w
acrnkfcsukdyorhsubc:
⇥
⇥
tjxnekrcrybbmakoref:
⇥
⇤
⇤
meyzycrmgaohhfnatpg:
⇤
⇤
ytrzcqsskbyvnrlaamo:
rmjmeganrafnrtzyzxx:
aarmdrgnfpbkgnxtgny:
⇥
rqaravkacpnjyelksho:
exaipicwkyvfnnberyq:
⇤
⇤
pe  %X %w
byqjapnxfttpfarmnbr:
sktwylnkycaphtkrgzz:
⇤
⇥
qnpqrltloctyawxoxnp:
liamujgzdrynlaqybzm:
alonarryukblgyoxbyw:
nazlarpmyrmbypukazd:
xrwxtfuzisqniajevyu:
yxqrgejcoarsmnqrrii:
dculaytnszrazknveye:
swuanhpqoyzevoejcra:
roxqagsngnwzdfmnyox:
weyguwocrauoqkxcynv:
uynrakzlpuhukmnotno:
⇥
nkdcrddujfamaicayxa:
yrpflnahiwprgoofohd:
⇥
⇥
⇤
⇤
⇤
⇤
nsxrnzdgkvrfgagbyhs:
⇥
⇤
⇤
⇥
xnnuhpbruaynyjlfbdd:
⇤
⇥
⇤
fxoyncndhfxzrareacr:
arvbcjyalfvgparawne:
⇥
⇥
qsdsarynnuouarncxpc:
j ywwpcsenvrakgqrhlij
aqsavngewundtqhnbry:
j jdcnrrrxavnttmywwet
⇥
⇤
ywwpcsenvrakgqrhlij:
oofjyqlapffhnwrgbwc:
⇤
⇤
⇥
⇤
rnovghmcrsrtlmapyqi:
j bavcnmtynzcrkaytkry
⇥
iurzsnaaywglrntcuyv:
⇥
clzjyenoovsrqvwcnae:
jwqyanlhrvbcsezqfxv:
j dxuylxwalclnrydhtkk
bavcnmtynzcrkaytkry:
⇥
nntarztdpmupavnxyup:
qrlonkyaongvrcwjxgr:
tybaroftlkfynrjhjda:
⇤
⇤
⇤
znvtligolrvaageylir:
⇤
⇥
⇤
ikdrrynjahsuadwrjgc:
⇤
⇤
hqfndynwfpnramtprir:
dec %X
tfnrpuvhaobugdthyyx:
⇥
⇥
⇤
⇤
trynsphnrlqjijaadsc:
⇥
⇤
⇥
⇥
afwjywaynzenudrkbvp:
j hhiifdfngryvapuqlny
amgscmnygwyvgfrrsba:
⇤
jdcnrrrxavnttmywwet:
⇤
j ruynzoammxihyrnqovn
hhiifdfngryvapuqlny:
⇤
jlynaaurctytcbqfmvo:
⇤
⇤
pe  %X %X
⇤
⇥
djviynhrprmygaianaa:
⇥
qpqwyonrtlxagqchgoj:
zbmoaynrftbabpbqpar:
⇥
⇤
dhibonjmruqhawjleyc:
pe  %X %A
lsaatpdiankrnxycrlc:
yklxpiadtcowrrgonde:
jrrrnycvceaanvcjmbq:
⇥
plqqjsapjtysnroaxre:
⇥
bggnmpyatutrrlpbdev:
⇤
⇥
nkplzkwiyamcngvlrnp:
⇤
⇤
⇥
⇤
⇤
⇤
lvsynprkudrrfnaybaw:
fadjattbmacyuwdnwyr:
⇤
ppylyvrpdbatnhvnenu:
⇥
mjkxbwbtytdnpygarhc:
ranrnnoyixykedjawtx:
giafnwmkdyaourjjyad:
fwpoicsrpyynfakwltx:
nnnjarynnurjqdsjlzf:
udoqglrcyfnwrmibtla:
hxyvgnnxsjajltzzwrc:
⇥
⇤
⇥
⇥
yhynozuaaqrbciayoxu:
⇥
⇤
⇤
li %Δ -2
qnyumecvrisaeaixtvh:
yrsbclklcngapwjeyjg:
qyrvkvxnmbrayeggxlt:
⇤
⇤
snujcaiekzqgbjdyxdr:
sfyoylykzjnjaaqrgpy:
xoufmanbnrlahzwgbjy:
⇥
najrlbhthbwnlyjryuf:
⇥
hliyakfklnynrvkfpmz:
vegyjyvkcntfxrrmalu:
⇤
⇤
hyyejaswzwqemacaner:
vijukuyrzwvhpcnalfg:
⇥
⇤
auamaarifpytnuxuwej:
⇥
dyonavdufntgtacqrnl:
⇥
⇥
onanyunaowragvfhfdp:
⇤
⇤
aghryzjiysyhnswfnwd:
lqxulnufyaoybadrrmu:
⇥
⇥
⇤
swnylyrmaudxqqkxgcy:
⇤
⇥
j nyutyntebdirazynavy
srajowwnnyfkaztxlnp:
j fwvymyhbjrauaqwnztv
ptbjwmrxoqvlfynrafn:
xamoarhyzrltyxymnad:
j mnualogoadkllryynlm
fwvymyhbjrauaqwnztv:
⇤
gvaynlzrahrcswcwntw:
⇤
arbotohzyhdqypxajno:
⇥
j tpiepmrganvanizylub
⇤
⇥
hajxxbyygsslnrzrnsb:
nyutyntebdirazynavy:
auycrfywyxbazkjmmdn:
kfhkwbnojaagebfryih:
⇥
⇥
j qufnfecwpzqapyrsyhs
rghtyhrynjumapnedky:
⇥
kayhnmnrenojyvaoprg:
tnrdyuzwamfnkljrlac:
j yqtrvcafwgywwbxnoto
⇥
⇤
⇥
qnfuenkgervomwydtoa:
qufnfecwpzqapyrsyhs:
⇤
pferhazwkenpyqibulj:
owzyfbdmcxbnxrilona:
aknncrdswzrhnnryapa:
⇥
⇥
⇥
j wueedpbyhyxspnirald
mnualogoadkllryynlm:
⇤
j cryzndmaflvsnljxexc
wueedpbyhyxspnirald:
⇤
⇥
⇤
rdyscznfbwsdoyfgcaa:
axqlhkaoajrcvndpkyn:
⇥
xnzxyazginmrfclisrh:
⇤
j nluojgkzyrddunvacrg
iruaipealwunaccbvyx:
tncnxtyuvvdysxarfan:
j strnuyfmvqnlnzaknvr
nluojgkzyrddunvacrg:
⇤
⇤
cssryjaudnyazmmohbl:
⇤
j lqpqylgroilawdanyne
aonviualrrzxygaonjv:
⇤
⇥
⇥
eafacijcyxnktxcurhn:
j ydbmkayqqysblnrkfrr
⇤
⇥
zgnylnbhjbajrlxkruf:
⇥
⇥
fruywuxeynfmyisbxva:
lqpqylgroilawdanyne:
sxlqrankumdryqlegcl:
byapgaudhncuzrchjnj:
zsynpsswqvaxlfwoonr:
⇥
⇥
⇥
⇤
⇥
⇥
⇥
⇤
⇤
⇤
⇤
⇤
⇤
⇤
⇥
⇤
⇤
cinrmyrqqqmuypfgabv:
⇤
rytdzjtnvatlpqdbrjl:
⇤
⇤
⇥
⇤
xyrrenvoplluvxyaryh:
papmzhvtjrqksdplynr:
⇥
⇤
j if.end
⇤
nlfducpsayydjrcolft:
⇤
cxhamuvsvzyxznpyrts:
else:
j nymigybuvmaehirzeok
⇤
rhaqkuyfumknhhrfqeg:
j iluxatvqyxgjngnyrey
⇤
⇥
⇤
⇤
nymigybuvmaehirzeok:
⇤
⇥
⇤
rkawbjyhybuhzxtknbl:
⇤
⇥
⇥
⇤
⇤
⇥
abkngsyukxhwiryyxtv:
⇤
⇥
nanbashlcrkajeyzfuc:
⇥
⇤
⇥
ddyoboaoqxjunvrrlvx:
sxvnpldhpnbdunyryas:
⇤
anjauiraywzkiobbuur:
⇥
lyrncnujhmaihyrpzyn:
⇤
j ufyortrxdjanvukursv
hvndnapktunjbwdjyrl:
qbaverudyatkwerolnf:
⇤
⇤
nqzasarfzwiujsyzlfg:
j tnrdyuzwamfnkljrlac
rfnyiajqtnynivrijuf:
⇥
ufyortrxdjanvukursv:
j nacwjlzqlyrmxyckcma
lpdyayyztkcundszsrm:
j xamoarhyzrltyxymnad
nacwjlzqlyrmxyckcma:
⇤
⇤
⇤
⇤
⇥
klgryefaynbrapmaeih:
⇤
⇤
yqpoasfzvwuinnjaper:
⇤
⇥
⇤
mul %X %r %w
⇤
⇥
jrypznrrrariswwrlce:
j nyeaqaxonxpeumjrnkn
lsrtpnamwwbdxxqcpyv:
.end_macro
stack lw $t0
merge_row.macro merge read_half write_half $v0 $a0 $a1 $a2 $a3 $t0 $t1 $t2 $t3 $t4 $t5 $t6
jr $ra
merge_col:
.macro merge_col.macro %merge %Read %Write %v0 %A %h %w %c %d %X %Δ %a %b %i %j
j yyawjnpcnfbobmrmwak
fnrxecdunaylceqvuka:
⇤
⇥
byncmoafgnajklzhznr:
⇤
⇥
yxxrqnhveapnvonfsnu:
j bfqdbnczjegtrzqtayn
⇥
⇥
⇥
mihzkprefajwtyndqah:
⇥
⇥
⇤
xrnhjwvnowarjlryyzs:
⇤
prcivainyvntxmnlrtd:
rnkhoanbjyuwgdwwcvj:
⇤
⇥
⇤
⇥
⇥
⇤
⇤
j nbmbzccyaavnyvfovfr
acirtznwjypmohnwtyx:
j csjbmtyhrpaelagdntp
⇤
nbmbzccyaavnyvfovfr:
⇤
⇥
iyrpnndozqjrcahfrlj:
⇤
zaloyrnzirmannzrimn:
hihyzaaojxntlsxprgi:
⇥
⇤
fbmrjcmmauknwybyjqv:
⇥
⇤
j rhymyaanwybfildjras
urauonaefepelmyhpzm:
j koasgawxrwpynbxnadc
rhymyaanwybfildjras:
⇤
mul %Δ %Δ %w
⇥
⇤
⇤
j prvmhterykazrmokexn
⇤
⇤
ebewmrnlubxayryndsq:
jclugnnlcxrfcaoneoy:
⇥
j gzahzdqkarasxoyxkna
⇥
⇥
prvmhterykazrmokexn:
⇥
j peqixcfbyuwmrcankvq
gltvvtcnreykahpzylz:
j zavrukyoanxmswhlkxn
peqixcfbyuwmrcankvq:
⇥
⇤
⇤
⇥
⇤
⇤
roqmhaknaygvykcdxre:
⇥
⇤
uutlrrsrfujopeoanty:
⇤
j peyrtbrdinhutitsvap
waeagqmlunsulkjyxrn:
⇥
j rtznmauwkywhewodern
peyrtbrdinhutitsvap:
⇤
zhqywdxznrenryfpasw:
⇥
⇤
⇤
⇥
ohuysidydacnjvdlrxh:
if.end:
nuqksbaageryorxwitm:
⇥
⇤
⇤
mzxkuoazuunicrnsyox:
⇥
oyawpsbcirpenffrlnu:
⇤
lrhfrarynizdyplzbtf:
⇤
⇥
%merge %Read %Write %v0 %X %h %Δ %a %b %i %j
rqysqansyyfnrmvjnjc:
lptfrawvnucaebddzyr:
⇥
return:
⇥
⇥
jrvnafqjtncvfyaprzx:
⇤
⇤
tgebnjpfaagdkxyrwad:
ynhwrprtrzxtrabzvzj:
⇤
rhkdnbhjcsnxaxkyrnv:
⇤
⇥
⇤
⇥
gpzbaandfxpxnknuyrm:
⇥
⇥
⇤
xpalrlnffkmobazyajy:
kncitiyrvjfcouvkaam:
⇤
⇥
riatiawyskkdtmfmnys:
rubhgmgarkgkniijyin:
ymlfhwgrtjtjndsrsaa:
yjmnkeymiksfdaryuur:
irdecyaqniyfejfrfmr:
⇥
j oyuxohauerndnptcdgt
⇤
pjfrjjfaxnryyuliaze:
⇥
⇤
⇤
nzeoljeysqhzamvrmyi:
j krknxfbrnirennaysgp
yyawjnpcnfbobmrmwak:
j dnvarxcxyyrpiufvobp
krknxfbrnirennaysgp:
⇥
⇤
ynbsmervwtagbnyrnsy:
ybnekrmhsftpudyzazn:
⇤
⇤
⇤
⇤
⇥
⇥
nvywaliuhjusrhmdyos:
reoaejqlaimyzohnqvw:
⇥
⇥
tonokrywfaqemfqjaet:
⇥
qrejyxpspzjyrnaeiuy:
⇤
⇤
⇥
lzywsidofoaqnbdrmcr:
⇤
finvsvwsirjuakwvyds:
⇤
otuoekndafamnroryun:
luamuiyguffmxlbbryn:
⇤
⇥
⇤
ftbpatyqnpvyrivejjw:
⇤
teawlnpqcpvntjkyuyr:
rymteikawpyelfpnkfq:
⇤
rbzyautrlelkajcnbmm:
fmwrylngayaxxnthfbf:
⇤
sqarofgsirvarafnmya:
cntmdvcrfhtloazyrfy:
⇤
heqvyauogztvraaiiln:
⇤
⇥
⇤
validate_direction      %d %v0 return
⇤
⇤
yygahrnirxzdiuloeze:
⇤
knwhhnzayidrvswhiwd:
wawlervauwpqprpjyfn:
anqvzydxuxrdrsrrbug:
⇥
objqnkhdgueemayrcsq:
⇤
mjlwzryaazsorlmvnsr:
paxekmijazbxdyiyran:
xrtbyzvtnbvqroaojyg:
tnxarkbgyytiavnyaeg:
⇤
⇤
j ztnvrfzozlnewnabjzy
⇥
jnfqtwjrtylunsafymr:
⇥
j wipyjdynmnedfiacimr
rqzyveuyrnwzmvaxyro:
⇤
⇤
ggrnqecyglpqjeiytau:
⇥
⇤
zgorbknacfeuxypnayo:
⇤
⇤
dvnyxrafypjisbmqrzs:
⇥
⇤
⇤
⇤
wankqshnyrgxcaasosv:
ztnvrfzozlnewnabjzy:
⇥
⇤
⇤
⇤
⇤
⇥
execrryszaghkijudnr:
⇤
j zrzighasaqndtjuajiy
pyqufreptuvlapfuygn:
ngswaatymgwnilyrkjh:
⇤
j urauonaefepelmyhpzm
zrzighasaqndtjuajiy:
⇤
⇤
⇤
⇤
nwctxmrbalxrmfodusy:
⇤
xcrfqtxnaueqwxywovg:
bhqypmuvnsderuakeuj:
⇤
jwmayrklbdzdivdxzsn:
⇥
⇥
cgkhyxzoatdabsfvrnl:
yjngaprtzygwvmxynvc:
nwggyeupkirkcgabiay:
qyoxznqillrarkqkbiy:
⇤
wjrwndtzvvyarcyubsr:
⇤
⇤
⇤
⇥
⇥
⇤
pbtkqcyqldlnarkdbmy:
⇤
⇤
ntrrdfaiyaravmzqlpo:
j ynorwiawewlbdrnmtye
acjfeyzjherdnfwrorg:
j tpxrrgjynuazbzdwaxa
ynorwiawewlbdrnmtye:
⇤
bnvxgyxrqrnynsxvhah:
⇤
ubyrottbaattxgqbjnl:
aydohadycszangrroys:
⇤
⇥
⇥
⇤
⇤
ryqkpdajaufqrcapngd:
⇥
⇥
ufrqyalgnsrrfynqeck:
sfxrzasnkrmpocdynks:
⇤
vdkrqnywuywabjixdsr:
⇥
⇥
validate_dimensions  %h %w %v0 return
lkrmarrydqgfxbnuynq:
⇥
⇤
⇥
nuivrmpsgnzyxowawif:
validate_row_xor_col %c %w %v0 return
⇤
⇥
gyeybierxfboncxaguf:
rnbolnqyrknteiijaal:
⇥
⇤
⇤
⇥
⇤
⇤
pnksjnayhnqshcvfrqa:
⇤
nhncyprvyqapxzqsome:
⇥
⇥
⇤
⇥
⇤
vmkgoprwaeqnlhstybt:
phfgnvysgoaryncejzm:
j lmugyyzrnmszanxfjva
nqxyztapboteebypare:
⇥
⇥
j nodgyrdsicfapznqhbf
lmugyyzrnmszanxfjva:
⇥
bne %d 1 else
droylkraaglvfqlntha:
⇤
cozxgafduiyseadrnuk:
⇤
j yvmjmeooawcnrpkbzjd
natksxnnozxfvearkyz:
j ixweygnnhfdtokvwjra
yvmjmeooawcnrpkbzjd:
⇤
qeaqusytdxrnedgzngz:
yynppjamreaobwrhrfe:
qsdcgwurpaefzisynrf:
⇤
⇤
⇤
npjamydoccrvyonlsyd:
pbdksrylhoqahscifnw:
⇤
⇥
⇥
qafirgardxsonvajyod:
⇥
iamglyjzrnlwlkanyah:
naivzyzrofezsaeybek:
⇤
hawojcgmioiywrrtqnh:
cyyyhowcviaatrzbyqn:
⇥
deawmpyywicicnptrgz:
⇤
⇤
⇤
⇥
hsyrvnahpkidhwcrmuv:
⇥
add %X %c %c
⇥
⇥
nwrxanyiqohidwhamwa:
ziphpanheyecrhltgaf:
⇤
hmakamrolmjnvjsqyip:
⇥
⇥
⇤
⇤
ireffyxrrcrnpwskcar:
⇥
⇤
⇤
aupyqpgvsrkgunzrrin:
analrpnqugnflubybyl:
j tfilrrrtmexanypymnt
⇥
anubyfrocpazdlyrsrw:
⇤
vunwsyeyrbtmpqqmkal:
j dzozdjtawrnyiiamyyl
zcnpctprzhznfvrylka:
wtqbgiiatoqynslryod:
⇤
⇥
atjcqdfgtnysxarnabk:
sopcanyhguqwcranbfj:
tfilrrrtmexanypymnt:
⇥
zailtyjlsrralnfajnu:
hprstozlcqjotrgnpya:
⇤
hvefnpvdyjbrxazanfq:
frnyzucpmvgrybsayfm:
⇥
⇥
⇥
⇥
⇤
⇥
j abowermnaxeuexyytos
nhvaeghydelapgsruxr:
j djgesratysrnaicnwmj
abowermnaxeuexyytos:
⇥
⇤
⇤
⇥
xpodaoyypgyfdkernnf:
qlnrnuaapywturpnztx:
j zdsycdbngrxflxnuane
vxjvsanatfqdcyxgydr:
j arygnzxduhdvckekzfr
⇤
⇥
zdsycdbngrxflxnuane:
⇥
⇤
⇤
nwkryafdacnktryynqi:
⇤
⇥
homtcwmyvsweryjfjna:
⇤
j zaogjcyncwxrcapvgqz
⇥
rtznmauwkywhewodern:
j pyqufreptuvlapfuygn
nyraqvpzyrhpqrfbprx:
⇤
zaogjcyncwxrcapvgqz:
j tiqarynqwlsqvzevqeu
iragrejauokhqiayncq:
j waeagqmlunsulkjyxrn
tiqarynqwlsqvzevqeu:
⇥
⇥
⇤
sngygbxqrgazrisupni:
⇥
⇤
ohsukwvyfnnrcybqavq:
⇤
⇤
fnpqavsnhfvfyicjxjr:
⇥
catnmsbrpooynzbiuvz:
⇥
⇥
⇤
⇤
yarsljykyadkufjyoen:
j suhnorxrcyggcqzipua
tpxrrgjynuazbzdwaxa:
j wpbfzyyvlropvaodcnt
suhnorxrcyggcqzipua:
⇥
⇥
⇤
⇤
cwgnnvakzvvtzreykaq:
lzuyqvrancegpaytwmn:
⇤
⇥
nratuxgbsywmntfhufy:
⇤
⇥
⇤
⇥
⇥
bcinflwripmzjjftasy:
wyukqnwyxrrsgiawoka:
⇤
⇥
⇤
j jdxnakehyrhxaybshog
djgesratysrnaicnwmj:
j natksxnnozxfvearkyz
jdxnakehyrhxaybshog:
⇤
bhxbmmnmypprvdnynwa:
⇥
hsrnjmynjlatwyniiuv:
⇥
⇤
hwadukrninsynzkpcfx:
evzisaxrlakytatbhny:
uwwzayhnshrjntnymtn:
⇥
uqbmdonrvcyarluybhh:
aglbmjnjxxdqtrikhmy:
j kjoyjcdonmlfriyynra
nggmarxerkfyfzwapyg:
j jclugnnlcxrfcaoneoy
⇥
vtkpnxkybvtirvigaty:
yrlauoldjaqutnrpvyn:
⇤
⇤
kpnewmxxrzcfykzpanm:
⇥
ydscnaptvodgroblrsn:
⇤
⇥
⇥
⇥
⇤
bdkoabwtimdynrqcysn:
onfnrytgasdnfxrkyze:
⇤
ymkagahtlytuujngrns:
rapylzjnkqddyhrainv:
⇤
azirvnfhtuwqtdoaybn:
⇥
quaabrjhwyrkvqfenvg:
kjnyypdcpzccaqrwlwy:
⇥
⇥
⇤
kjoyjcdonmlfriyynra:
nkwaeoydiedjwhrxjhm:
⇤
⇥
⇥
⇥
meowdhyzeunbzdrarzr:
amrwdrlwyjaqznfllyc:
xuslenyahgkqmyageir:
⇤
⇤
⇥
⇤
⇥
nvdyanfwercukyjnyfo:
ucbfbenoyrkdqhzifna:
⇥
jbyaenaglqhhyrsnjqy:
⇥
autpseuiysznvrhthdb:
⇤
lkropsaknrynttywiyf:
⇥
⇤
iqckqfmlhqkrjvlandy:
j myyknqjwjvoajlrgtyr
⇤
⇤
eaiwwkzddwlanxpfryr:
j gpvomzalenazyrixyul
anrxoemyjisrfcklrss:
myyknqjwjvoajlrgtyr:
⇤
⇤
⇥
antxrulrdasartkisky:
⇤
⇤
⇥
j ywsnifolzlqnbpajodr
arygnzxduhdvckekzfr:
j bwndqafnrqlohctfupy
ywsnifolzlqnbpajodr:
wrynaeauqhdlxunwewh:
rnsyznndnxknampkxhc:
⇥
⇥
⇥
⇤
⇤
⇤
⇤
pe  %X %A
nyianfydmkxktrbzqgd:
⇤
j bnnvkarbmyfwwknnwyp
bfqdbnczjegtrzqtayn:
⇥
jjnyscxjzrjotifymia:
⇥
⇥
⇤
asnbixaewwbykreuaaq:
⇤
⇤
⇤
ysxfairjhnyfmwkcrar:
⇤
j arvydrssgfkjvxqocns
⇤
csjbmtyhrpaelagdntp:
j iragrejauokhqiayncq
⇥
⇤
arvydrssgfkjvxqocns:
⇥
⇤
j uotewxkadyaryosnrjs
wpbfzyyvlropvaodcnt:
j gltvvtcnreykahpzylz
uotewxkadyaryosnrjs:
⇤
xmiunkrawtzyrzwulxk:
⇥
mowynweztvozrtiwbae:
⇥
tpacnekgrjbqyjorqvk:
qngeaeyilrahdjpaoqe:
⇤
⇤
hxfnarpcvtihyzyikux:
⇤
⇤
⇥
vkyzrjdvylymnafjpha:
j nggmarxerkfyfzwapyg
hnuaceymowtjyheryar:
ahgamqrvqqvevlmywnd:
bnnvkarbmyfwwknnwyp:
⇤
⇤
wlnkdxxhgdjfahfryys:
⇥
⇤
⇤
⇤
⇥
arbjyvrrlmdsnbpmxrj:
vlwwjmqawfwyxnsmvmr:
⇤
⇤
ntyerqayllylxfxtcmq:
⇤
⇤
⇥
⇥
feafynafntuxqthbrwv:
⇤
amjoljanhbgcbvcvyyr:
jufnwbsdsybapcanprt:
⇤
mzysekbufyvnaqrdpls:
⇥
⇤
njptgyrranuwhhufqvj:
⇤
⇤
⇤
⇥
ranradexeibnyyhuqwf:
⇤
wmnjngbkyoaqscarpmo:
⇥
rnajpnqzyqbygibeqby:
⇤
yyxonymrahoesveilyr:
add %Δ %w %w
⇥
⇤
⇤
j if.end
alrmunackmayjmpcecr:
⇤
mucvlmlkrfonecykgaa:
kreagelbunagnbyqpfo:
else:
⇤
anztryireysaqhdjfqh:
etexrfnogywannmddfa:
j uhyzcyfyrafebpyyynp
tiyqcoyjnfcaraaqghy:
j nqxyztapboteebypare
uhyzcyfyrafebpyyynp:
⇤
wyngbnwnssjfwryahsp:
⇤
⇤
⇥
⇥
nxrtafxftzaryfrsyek:
qrwagytrdnxuxwogafb:
⇥
viyauxvvejvnraszbye:
ipjoadxnjqfyagyrwns:
⇥
⇥
⇥
⇤
yeclgtnzsmwlejrawgb:
⇥
emcanoqhscuyiatzryr:
⇤
⇤
mxtyrazjzcdsadxgbin:
⇤
fmnrybatcmqrbttqaun:
⇤
⇤
xnaybxgnlgfwbsjzqvr:
oenztbgndarubomnrhy:
⇤
⇤
hrgcayzfcxhnprdjyjj:
⇤
pqrifyxeycaeahunjgq:
⇥
⇤
⇤
yaynwjhpgwbjotjnraj:
nghtxmyvntvyareyjjf:
⇤
⇤
⇤
uacypstnvcqktfanarp:
ctlukdyrmreacjnjsaj:
⇥
⇥
⇥
⇤
⇤
⇤
vsajccykrwnbncrlgca:
mul %X %h %w
⇥
⇤
wlifnamqynarkadzwmj:
⇤
yheayddbrvsndqvayni:
⇤
nnzkrxzzmwyjueimwna:
⇤
nrhasyhwadyenwmxyxt:
⇤
vvmiirnpowylabsonbx:
ahklellnfrdvyyzkrza:
⇤
⇥
untadtvxazrnrstbmys:
yrfynwhzbmawxnzpdka:
⇥
⇥
caxnybarxcoibuwroyg:
qssfgaenrkbupysgyvp:
⇤
cqdvbrpolvayhxnxqme:
yxxnkrwyzrvxiqyajya:
⇤
mqkwskiannxmymlelnr:
⇥
lwylhndwnyadcoyvfrx:
hralybqfsaxqjrdfpzn:
⇤
⇥
xavcvsghnoxjewrwnyz:
⇥
⇤
⇤
⇥
⇥
⇥
syfordnucucaqkxsabp:
me  %X %w
fqamxyknrnyhaiqhgop:
⇤
hjrnrfyrmaywslxjxfh:
fddrzayorqegwntysyq:
⇤
vxeyturwfnwlrdpahyr:
cbmkxwyrcncwpoiifas:
rjyzdlmuanoybtdlvlg:
⇥
zobowhayaoxumrqqnhm:
⇥
⇤
⇤
aqzcpgxtekryyyvwunj:
j pbodhxkoptyyrxaccnc
⇥
gaqaxliyxxnyycmrhhj:
⇤
⇤
j tiyqcoyjnfcaraaqghy
⇤
pbodhxkoptyyrxaccnc:
⇤
pe  %X %c
j irylocatfxlvbdnsqqm
⇤
yeaninbkuahrjdpibrv:
gpvomzalenazyrixyul:
⇥
⇤
j ubxnaryprvdurzbhari
⇤
irylocatfxlvbdnsqqm:
⇥
⇥
⇤
⇤
⇤
⇥
gfdgkdfecqalavnrkay:
⇤
⇤
⇥
j rmondwnyalymtmjonmk
dnvarxcxyyrpiufvobp:
j nhvaeghydelapgsruxr
rmondwnyalymtmjonmk:
⇤
⇥
j yrvmfohjyqaxnntkvlw
nodgyrdsicfapznqhbf:
qnqqcyayigadzhanrje:
j anubyfrocpazdlyrsrw
yrvmfohjyqaxnntkvlw:
nyrapngllxhdepblial:
⇤
errdnayhfrztpofndwv:
yfrlohoyaiyykxnbtyt:
rejevntdzbiuaakgfmy:
⇤
baofhspnqkfnxyrvrbu:
⇤
⇤
⇤
rzmkqlsomrmjazbgmyn:
⇤
⇤
aoxaghhkylrypqntgyi:
⇥
dargtaontifatjoyyuu:
⇤
j gryasthstxhpwnoraaq
dzozdjtawrnyiiamyyl:
⇤
⇤
⇥
yulwdjoazurnpekyvhq:
jiysrrxfskmeinffxaz:
j jnfqtwjrtylunsafymr
ycsacokudnrgronoxgt:
⇥
envqxacwudrmkyaqeep:
ilutpzynefadfhprnqf:
pyiryfknkusrtaxoayj:
krmwyuarzywyqnjcrvw:
gryasthstxhpwnoraaq:
⇤
⇤
⇤
vdcmmaayxdklvnkzcnr:
bhanyhgorqeiocbcwin:
⇤
⇥
nufoabnyvromogfxdrp:
⇤
lbmkadnryjhnrlyucij:
ntkckwkyiufndaocvrc:
ewaaijubymniftgvrnt:
⇥
pznyhwlqngqryjtygqa:
nwrgvnaqdbsyujqzjql:
⇤
pxyezpnovarjpfegcya:
⇤
qimnaarbcsugnpkycxr:
⇤
⇥
oejwuauxczxyenpzrqg:
⇤
⇥
⇤
⇥
wafcengnwrraygyafna:
⇥
⇤
⇤
sbyjylewtaryshfqnnm:
⇥
grrfennoxxmzaljylou:
⇤
⇤
⇤
dpquvnjyycvncjrajay:
vipcayaorttnndlrfss:
⇤
eghpnxyrldibajsuzqa:
⇤
⇤
⇤
hreyanaxprwnurgiupq:
⇥
⇥
⇤
⇤
aurjphznybmkrbtaetj:
⇤
⇤
⇤
rpgoxnztfojjuayatrw:
mqrqantjyptbqnqoazr:
⇥
⇤
⇤
dzhtakjrzydqzonnhos:
⇥
j mexkicwjsnxgraaoxhy
⇤
koasgawxrwpynbxnadc:
j eaiwwkzddwlanxpfryr
uywruaqtyrnjxuwyskg:
⇤
mexkicwjsnxgraaoxhy:
⇤
ppmtarmnibgqmnypywy:
⇤
nxhxwbwrvyvlnnapjyu:
⇤
⇥
⇥
⇤
⇥
qryauotlgplnfuntnyy:
pbxyksdriawplnyvcdh:
⇤
lstsaeblxugennyraan:
jyrayuhkckocpjsncjc:
zalnbnyadlnlfqrhoax:
⇤
spzknsrupuygaqkcmbh:
uamuyamanebhrnfayzz:
rnaehulcgajcppdaymr:
⇤
nekrlqqnylngzajvsjm:
⇤
ljgfblitjzrrahnbnny:
xytmxqjaakscbrjqfyn:
afpumybrgnzpauyhwhr:
⇤
efhippaanttjdryfrya:
⇤
⇤
⇤
dlanplffrcfkfynifsg:
pe  %X %X
⇥
⇥
kthrhpaejrofyjnmaeo:
asyhsnqyhoahqyarukp:
oduaxojurnygghslwup:
⇥
⇤
anetabarvszqzrmmeyc:
⇥
yvtlqtunzpypadrniql:
⇥
rmrqhnnmantlpyaakzo:
inmsearaglzuayzrvth:
pe  %X %A
zrmynyjzaeotwrtdaur:
⇤
⇥
kvroeeejaydqxbaqsnl:
nrnhpygtmpvlbhxabqa:
⇤
⇥
j amghyzgxpfvrqjzelrn
zavrukyoanxmswhlkxn:
j vxjvsanatfqdcyxgydr
⇥
amghyzgxpfvrqjzelrn:
⇤
⇤
j faggwezvryoautlnfra
⇤
bwndqafnrqlohctfupy:
j acirtznwjypmohnwtyx
⇥
faggwezvryoautlnfra:
ijxvnlkszpayddcvrmy:
⇥
⇤
⇤
⇤
⇥
⇥
nxyniusacdpgtrrzcgo:
⇤
⇤
⇤
⇥
⇤
yndjwxbfvarmrvfzken:
nemjyxalrqysablcgyy:
⇤
⇤
⇤
⇤
⇤
⇤
j wgpyhbnnhsxcraadnbd
⇥
⇤
⇥
⇤
⇥
⇤
⇤
⇤
ajnirvxnmjywdiblria:
lcnfpnyryvrajfnvyox:
⇥
⇥
pdfynyukxwbapdpvrer:
⇥
j saasuyexeionjonkgkr
ixweygnnhfdtokvwjra:
j acjfeyzjherdnfwrorg
saasuyexeionjonkgkr:
⇤
⇥
⇥
⇤
⇥
⇤
⇤
lmvmarinxaymnejzmyh:
⇤
⇤
ngqltawtntwfrltayol:
⇥
⇤
choxntiuriezsyayenl:
⇥
jypupdnamrylujtlttf:
laaxbgynapnysrbswyu:
⇥
alqkgnyungxrudsnjrn:
⇥
gzahzdqkarasxoyxkna:
⇥
⇥
ctvaynyimrniobkzuuj:
yluaabbgrrgdjfnyilt:
⇥
⇤
rauudfsxkdnsquywqna:
maulaunyfyrbmzreymn:
nkywquszagjrqmzsfra:
zygzhxgqtiaajrienpg:
gcfwababcrnkufftapy:
j pjfrjjfaxnryyuliaze
aqkavqzjrejnfefiytl:
⇥
⇤
cnryaagxrygqbfcrwcy:
pnyydivprakcpcaqifl:
⇤
rjbqxhvqdnvhimoalyy:
⇥
fafbyvwprnnzqnhpwyn:
mrkhlgkdseyotnocxra:
⇥
htvydnarikcvekgqacy:
⇥
rnqtrulhujaatcpyvzn:
⇤
⇥
wudbyabnnaiorzsdbyh:
wgpyhbnnhsxcraadnbd:
wlanwdidwtmmnzarbqy:
⇥
⇤
j nndtwypzblrohutwgla
ubxnaryprvdurzbhari:
mrafppnxohnvmbcjlpy:
ykjahmuhrkncjrsxvyo:
⇥
j gaqaxliyxxnyycmrhhj
thdqpcgynerbavgraah:
nndtwypzblrohutwgla:
⇤
li %Δ -2
j rnkhoanbjyuwgdwwcvj
wipyjdynmnedfiacimr:
j fnrxecdunaylceqvuka
oyuxohauerndnptcdgt:
.end_macro
stack lw $t0
merge_col.macro merge read_half write_half $v0 $a0 $a1 $a2 $a3 $t0 $t1 $t2 $t3 $t4 $t5 $t6
jr $ra
shift_col:
stack lw $t0
merge_col.macro shift read_half write_half $v0 $a0 $a1 $a2 $a3 $t0 $t1 $t2 $t3 $t4 $t5 $t6
jr $ra
shift_row:
stack lw $t0
merge_row.macro shift read_half write_half $v0 $a0 $a1 $a2 $a3 $t0 $t1 $t2 $t3 $t4 $t5 $t6
jr $ra
start_game:
.macro start_game.macro %A %h %w %r1 %c1 %r2 %c2 %temp
j mrpkxyppmpnsharfvwf
isnwnggnyvgkbpvabrq:
⇤
⇤
⇥
tkrxmynylakhqwcpops:
⇤
xhnyersmyraveigwyxr:
yayyamryhwganhulkel:
⇥
⇥
⇤
⇥
⇥
toyylyptdbnihfaaqry:
⇤
⇤
bkxrnebgqdhjhwsayzl:
zowwsirylnnaagelndp:
⇤
⇤
⇤
ycaeynccseceupisrro:
dnhrrlytenobhlztaao:
chrokcwusiyuynyyazu:
⇤
⇤
xazmfnalecihryaunnj:
⇤
li %temp 2
wndyefqhyidadoudrxt:
aylyirmpzrqwnwlniza:
⇤
push %c1 %temp
vnyhsavlwjonlukdsro:
⇤
⇤
cebxlytamrkwngyjiap:
⇤
⇥
pdjnanxallvfqryrclk:
⇤
⇥
⇤
thabyjcfxznynrhpyjd:
fndtkvzjlvryrazyvho:
⇥
⇤
diizrwrhdnyzatltxyg:
⇤
xcphhynyjznbztarjrr:
j palrbdibzuynkbbylpr
⇤
yizlnodadqxgzbxcwfr:
j bwrxehzpayskiwvqntq
⇥
⇥
palrbdibzuynkbbylpr:
jal place
⇥
qrrrahyqwftgnjdsynj:
ptyurapkfzdhnnifleg:
soxsalimvxnlzryuiny:
⇥
⇤
kiayoyxdowpxplrntvg:
⇥
pqadnakoepyixrroyeo:
wyjvnqgkbgdzbaorykw:
qkomysieadmgbquatrn:
⇥
⇤
li %temp 2
⇥
⇤
⇤
rawfwawkezddwubhyrn:
⇥
j afdfoayycogorbsflnr
lbpdzwytaroofypznvu:
⇤
aymmfonnnaoceloyrya:
tohmzvepysnjvnaoygr:
dxnmekmydaydtqnlrar:
j lrfnnrkayxjzrsxefkp
afdfoayycogorbsflnr:
⇤
j nmayglrwmlqujhdsbvs
fedrrfwhyjneearipnp:
j apgnruoafsybvsxgsex
nmayglrwmlqujhdsbvs:
⇥
gymlkqydnrjsdmzzafl:
eedmzbeyrqjnxapshlz:
⇥
⇤
zxnuorrazdevbqyyzat:
gpeaybxeaonlcdpjern:
fmpacyznlkqewyvrsvz:
⇥
⇥
⇥
kyxerqbkgvajrcotnul:
⇥
hsmnkfarylnpsdmjdsh:
yuycnstpvoximauzrka:
⇤
j yszayixcqmdovbfnnhr
⇤
⇥
eswnqulizrfkceznayy:
fjbzfgvrrrayinlczuw:
j yanbhrrdzvhyeomhwfx
⇥
yszayixcqmdovbfnnhr:
⇥
qjvynysacohdayuvryg:
⇥
⇥
rktqnyiymtnknagzadv:
⇥
⇤
vrcnfybauvkrgixlgaw:
⇤
rnnsaveyalrmfonfanb:
⇤
⇥
⇥
⇥
⇤
⇥
⇤
j yjmtlrruqwvavwrpenj
ornnayvarulakroppji:
j yizlnodadqxgzbxcwfr
⇥
⇤
yjmtlrruqwvavwrpenj:
swtlonirusvzbavjkyn:
⇤
⇤
stack sw %c2 %temp
⇥
⇥
⇥
qfwatkjnyliajjnoreu:
bwuntafnawbzfravyin:
⇥
udyjaaydqabdnjnxurr:
⇥
bsqcgyzhknprugfdlar:
⇤
xlaxoarcnkoutyvfqbc:
⇥
rjtgdecjvannngmmhry:
⇤
⇤
⇤
⇥
dtuxaryadlpnshkdgoh:
⇤
nqwlyrpbayittwpvghu:
gyrnhicrtpygzuxleaa:
uiyfbqmrhneknyrsafy:
⇤
⇤
avbcvgrlnotxscecyvk:
⇤
qceakfbrowtyynjruid:
oftanqrhhihfraweyyp:
⇤
⇥
⇤
move $a3 %r2
⇥
kqzywvgndvtynvrarra:
⇤
jal place
kqynrptqjnaevtgiyoh:
⇤
inirbbacybatonuohau:
ihfnsxarposxygaxkcs:
⇤
⇤
tevcknrizfpbycrdafv:
⇤
fhurgjeanczhjybqcun:
ehbdqtydahyybbrnzia:
⇥
j ocxrdipwfrauermvjyn
rywbqnjaypqgduyknrf:
mzytjadfraaudlehnst:
j aiftwmeynjagmdxsnlr
xniwdvcalirnyishxsg:
⇤
ocxrdipwfrauermvjyn:
⇤
j rlzgzflfrnypastvgfr
apgnruoafsybvsxgsex:
j ornnayvarulakroppji
rlzgzflfrnypastvgfr:
⇥
eslpvaryvtyrhlmoneb:
saeqmryyiwnnjpavtio:
j gloogryncjvxaverexc
slepljnnsyadmoupnhr:
⇤
⇤
⇤
⇤
vnqaywerjenmbznwbwo:
qwctahfrazfrnovxwyj:
xalxuncvrzctjcyjqwi:
j qenxkaakmtgystkxmar
bwrxehzpayskiwvqntq:
j dxnmekmydaydtqnlrar
qenxkaakmtgystkxmar:
⇥
⇤
nyvnernodrjiuhhymva:
lqxszyeynlhrawvnzmr:
kzzquuymqzyayxrinnf:
⇥
uuwkpyridinyunnxjxa:
ckkqljjnabagrrzysip:
dtzsekygzkqggnvfrak:
ndrizgyyypxytanrqns:
⇥
nkhoryajmjygrlnawtb:
j nxaclekpryerlqangwp
gloogryncjvxaverexc:
⇤
yrrlueqgnlanvrqmgpi:
⇥
⇤
⇤
onkaweargfhrrouyvkf:
⇥
hfnomwwfwnryejpkpwa:
⇤
⇤
⇤
bjrnyrrwrckqjaeyuxf:
j idfrynyuwpkqcbsulas
uzxbbnkpqttamrylxan:
j fedrrfwhyjneearipnp
idfrynyuwpkqcbsulas:
⇤
⇤
kcygbgwalohorencybx:
⇥
ntvpwqodrsjydmadobh:
zvyotnprfayhwdogbzx:
⇥
⇤
⇥
⇤
tefqrffnartfyxvnhqe:
⇤
⇥
nlacjrdaiwqvfzgzjhy:
⇤
j panferamyfvhyjechmr
⇤
⇥
⇥
⇤
⇤
⇥
⇥
peajvnqmeosyxhgvrre:
khandwmczydnbnrhxxz:
⇥
vnimwfafewxtyqyrlkv:
vgakuytuncgaramckys:
rikalvzddydnfyglrqi:
⇤
rsonjebaybtxqpidvmv:
j bjbknhryyrzhsydarua
⇤
⇥
panferamyfvhyjechmr:
vfelmxyabzncsvhnuur:
⇥
pei $sp 8
⇤
⇤
return:
j awcuahlrbctoyiajzne
nhyvtaljsakroustilf:
j yylrrcdylfoxddajnhw
ypsdrnlrnbcyqrawndv:
j uzxbbnkpqttamrylxan
yylrrcdylfoxddajnhw:
⇤
j mzytjadfraaudlehnst
awcuahlrbctoyiajzne:
⇤
⇤
⇥
⇥
⇤
⇤
⇤
obpuuhyntjbtauurmlx:
⇥
⇤
bqnatzurycsxgkftrno:
j fjzhuantaygqwrxxmtw
nnstknxrbzaragabytj:
j zsvlnzqbvayjogyrazl
fjzhuantaygqwrxxmtw:
enigbrlazmruyexfthe:
⇤
⇤
giqulangeyrxdyzunup:
⇤
⇥
ncargjcaimhbqzygqja:
⇤
ylsavxrcnpjgpjcbayb:
jzjlnykovragcljdbzm:
⇤
cbylyraiamrlnnqkcpr:
⇤
flqwofrxgrsrnuqahby:
oymvxyrrlvlxdielnap:
uawiryuyenpezfhsgiu:
⇥
j jvearneylvbhvatains
⇥
⇤
ougtwhbchhgbazndryh:
⇥
⇥
⇤
⇥
⇤
⇥
⇤
boyorfadnrimwftwmzy:
awcrilonveaxxybkxpd:
⇥
⇥
⇤
⇤
⇤
⇥
rzdybwcugaatprnkaek:
⇥
⇥
⇤
⇤
⇤
⇤
dokgyrahtntsyykandp:
lsfnqzsmnbbythmriat:
⇤
wxwyduxacspvpgrnibf:
⇤
ntyfbyyrtyqbgeqdmna:
j ubyaajivenarhooakby
adnytoknkiswjeurfah:
j nyvnernodrjiuhhymva
⇤
ubyaajivenarhooakby:
⇤
j tdlfnyfneanymrheacr
mrpkxyppmpnsharfvwf:
j nnstknxrbzaragabytj
tdlfnyfneanymrheacr:
⇤
⇤
inedajayxcfxjgryihp:
rwemyaerlxsipezfonc:
⇤
⇥
validate_dimensions      %h %w $v0 return
j ihrycxbxacxnsdgkfyh
⇥
⇥
rdueyyanbyooatkcone:
⇥
cjszykiyurnbyyavvkw:
j adnytoknkiswjeurfah
⇤
rfjagqrygvjeodirynz:
ihrycxbxacxnsdgkfyh:
⇤
⇥
⇤
yhzjdanmejskrnxyvod:
⇤
qpceaaynnzygpalhrex:
qlapnkzyrarbltzrppk:
⇥
⇤
⇤
dmlcecreyebuaenylbg:
⇤
⇥
elripzneunaxwhzexfy:
⇥
⇤
⇤
⇤
⇥
⇥
⇤
⇤
jrqzjhgirjtapukyxun:
yzcunyjdjmshsqgrkda:
uydnrnwhaznwatagfvp:
⇤
dhcwkneiarwbikbivfy:
⇥
⇤
⇤
⇤
j nqypurvdkvszajyvagb
ngkamzzlrjiztnmeyfw:
⇥
kxzdrlymucuzmonjral:
airgqdnfgwaybaiungq:
⇤
j rafnyurrfkhjocjkbqb
⇥
⇥
nqypurvdkvszajyvagb:
xvfjrnnncrymxpnysah:
⇤
zjsksynfrasajthanru:
ryzhawrlhevfndynbya:
⇤
gprgtsiruvgyatpkymn:
clhwrajikyyanfcnqnl:
⇤
⇥
⇥
validate_row_col %r1 %c1 %h %w $v0 return
hsynmitvyogabnjrtrv:
cwararpeuwbnzeayzut:
⇥
gjhkasrmonnbcrxmyud:
ogksyoarxxlsjntnwda:
⇥
validate_row_col %r2 %c2 %h %w $v0 return
⇤
⇤
rkbonfjktyhaumsqhxo:
⇤
⇤
⇤
j cpudymurvslyaanyrnr
rafnyurrfkhjocjkbqb:
j vuywlranyxghyndzahn
nxaclekpryerlqangwp:
⇤
j ngkamzzlrjiztnmeyfw
myfisutmyawmmsnmrtl:
ruvniqozzubzymnhcba:
⇥
vuywlranyxghyndzahn:
⇤
⇥
aenvnghoueyurduwoto:
⇤
⇤
⇤
⇥
⇤
⇥
⇥
gerheqyiiltapxiycni:
⇤
j rsonjebaybtxqpidvmv
ylfysdeoynaqsytfurs:
cpudymurvslyaanyrnr:
⇥
bqoaybniznudkyradds:
qjiarywtlncopyokyai:
glynbtqkcruriybbara:
nsynqrkbvqcfvjxunva:
jal clear_board
⇤
⇥
⇥
⇥
⇥
⇤
⇥
j gjnsksxrnnuaeonhmmy
⇤
rmeuyavzwslvpdunsiu:
aiftwmeynjagmdxsnlr:
j eswnqulizrfkceznayy
ayqbesqontobsfynrxr:
nadzmmdruyydhtazkoe:
⇥
gjnsksxrnnuaeonhmmy:
eapjnxrumkjzlylvxay:
⇤
⇥
⇥
⇤
jxnhhrurkaorybhdaey:
⇥
j bkxrnebgqdhjhwsayzl
⇥
bjbknhryyrzhsydarua:
swxarfqhwabywwnrbry:
⇤
j ntyfbyyrtyqbgeqdmna
⇤
⇤
qaqzavwpynucgdnnrtq:
⇤
⇤
⇤
j wsaxsrncyrnscruryai
yanbhrrdzvhyeomhwfx:
iffegnblygdunaparjz:
ewwqpbylakwignvrxgw:
⇤
⇤
kzpognabhlrkvygpkhy:
⇤
j rdueyyanbyooatkcone
pnbayxxngzxsvycrcyi:
wsaxsrncyrnscruryai:
j rhlpohbsavktndayyjn
lrfnnrkayxjzrsxefkp:
⇥
⇥
j nhyvtaljsakroustilf
rhlpohbsavktndayyjn:
j ynaranhikfhldnfxdxl
zsvlnzqbvayjogyrazl:
j ypsdrnlrnbcyqrawndv
ynaranhikfhldnfxdxl:
j isnwnggnyvgkbpvabrq
jvearneylvbhvatains:
.end_macro
move $t0 $s0
move $t1 $s1
move $t2 $s2
move $t3 $s3
stack lw $s0 $s1 $s2
push $t0 $t1 $t2 $t3 $ra
start_game.macro $a0 $a1 $a2 $a3 $s0 $s1 $s2 $s3
pop  $s0 $s1 $s2 $s3 $ra
jr $ra
user_move:
.macro user_move.validated_call %func %fail
j zakcworojauuypnrmfw
zpzrsqvszgqaknyewwv:
⇤
gshblqroyjuqknmajnt:
⇤
fzksmwnyespbzparnwd:
j irovusjwxnmuykcawaf
opzepcfarydenjrmafg:
⇤
ygwjhbqadwncmlrdhiz:
j oykarfwwfnclxhadurf
irovusjwxnmuykcawaf:
j xanyrbtrzbwxctbzqsk
zakcworojauuypnrmfw:
j opzepcfarydenjrmafg
xanyrbtrzbwxctbzqsk:
beq  $v0 -1 %fail
⇥
koyagxfrgfnngmqucvd:
j wywvrrflhcwncaatwoh
daymjornuroovgzzasb:
⇤
jal  %func
j fzksmwnyespbzparnwd
oykarfwwfnclxhadurf:
j daymjornuroovgzzasb
rsvfxcnytywaykshewd:
j zpzrsqvszgqaknyewwv
wywvrrflhcwncaatwoh:
.end_macro
.macro user_move.for %shift %merge %fail %char %dim %end
j mccrayrgeyozozrnaan
cinrwrbgqcaribatify:
⇥
⇥
⇥
yiskdcetqhnmyrcawoh:
⇥
j jxtyegutsetavnwvrjn
xyzlysafknvtrghnnyc:
⇤
⇤
⇥
eznuyahqhzyputqrrqw:
yrrpcrylasncuuqushb:
⇥
⇥
praiuayjehcsjfnrgqf:
j zupvenytfaevggzddqr
kbrefyunhrzkavjnltd:
⇥
⇤
⇤
ylqkhasnpqxjqkytzrd:
⇥
⇥
dyrfnsadygegwlmpcqx:
iohbrakmearyydgahnm:
⇤
irrjjnramjazvtmsoyw:
⇤
⇥
⇤
⇥
⇤
⇤
⇤
⇥
⇤
nkhfoqfvrvsonjivaya:
raaicigvenelaanziyt:
j yqjigyagbvuqprnwugn
xgsxcvwwnralymwbnqy:
j klbefhuwqrfytnbgjma
⇤
yqjigyagbvuqprnwugn:
nhydrucnipgxqajeixy:
⇤
ptanfhrwvvsyilcjwtx:
⇤
⇥
⇤
wtpryhainaynygituhp:
jxtyegutsetavnwvrjn:
⇤
j dcrayaqntrdncclyhjt
rjmdbmcgnmcivujryea:
jnfpqsnryhtqmrgcamh:
j vhzxfqidaanwzrmyrae
dcrayaqntrdncclyhjt:
⇤
⇤
j okbsgydbocgwaejtran
tzutatinzwyryfjcngn:
⇤
ceyzgihxfvyaqqrnhan:
j xgsxcvwwnralymwbnqy
lnqsrlymrwnkkabxwbk:
ivyusasrvdzdkwafhnw:
okbsgydbocgwaejtran:
⇥
⇥
⇤
⇥
yiajxkrsepdxliapnbf:
⇤
⇥
⇥
irrscqutyrmtudaegxn:
⇤
fknqyryvajuobvjyqae:
⇤
⇤
rvfpmabbntyraxuoqte:
⇥
⇤
⇤
mxdyauatccfminhjrts:
j indqmleayrzuhorhsfa
⇤
⇤
⇤
⇥
⇥
⇥
wugisrasgdownnyxxqc:
⇤
nfplyrfzdgqmbhryjya:
⇤
wvthdailyercunxehkq:
⇤
j rmpzysedaeinprgwapa
⇥
nfaimlnakpkmrydyarz:
⇤
indqmleayrzuhorhsfa:
⇤
lyayrikzrhtfecgnusm:
⇤
yhyrsohndmvswaekjel:
j zyvinnmxxnyfraniyew
ulqoconqahjyrcppaoe:
j flybafjnodrrsatbfxa
zyvinnmxxnyfraniyew:
⇤
push $s0 $s0
voohwuhmndllbzrwyau:
ifhrcrwnioryurjyapc:
⇤
j hdrbvnituruclkoyqpa
⇥
oykymnagagufbtrpeqx:
⇤
yyrplvbagolnagnsprw:
⇥
⇤
⇥
rfdooacaiuancioryvb:
⇥
⇥
⇤
⇥
⇤
⇥
⇤
edehztruagyrornbnuk:
yvtqxornnjuacvooisi:
⇥
j yrrpcrylasncuuqushb
hdrbvnituruclkoyqpa:
⇥
⇤
j mofyqclyrysanrmtrnt
qyaattcnywbpkqgvrew:
gmqezpmynwgrapnuxlv:
j ulqoconqahjyrcppaoe
mofyqclyrysanrmtrnt:
⇥
⇤
raizwkmoupoizxqdryn:
⇤
lz   $s1
⇤
⇤
for:
⇥
qwcrcynfepcltyqajhv:
j zmjrswdczrpwycnbnad
j vbutpzrmtygimayvnra
zzygzknqxrgjuzvawvm:
j irntdfekqrncatpyirv
vbutpzrmtygimayvnra:
⇥
⇤
rmpzysedaeinprgwapa:
crjajavzkmbcdblyfyn:
⇥
⇤
eongxydswlddrtgaixo:
⇥
vldprajyeovrwlnxvrk:
uytrqlarntyckplcons:
orjreajxbanszednbyh:
vfoceywzruonnjtkiaf:
⇤
⇥
scwfgkdjndafyrfsyrn:
j vqelecrawyoqcuoarcn
⇤
⇥
ijnatyfnuarjgzfgoma:
⇤
⇤
j ahcsexpneiwsknruaye
⇤
vqelecrawyoqcuoarcn:
gnzyriuaeyvgnqbbnlb:
⇤
⇤
⇥
j oykymnagagufbtrpeqx
⇤
aeddqwerbrasnfiuykh:
⇤
⇤
⇤
⇤
⇥
⇤
⇥
⇤
sbhayniauvofhperqeb:
zmjrswdczrpwycnbnad:
⇤
j gclnkyftjpjlzrhyvam
aowpzrtnkcoofyrebfj:
⇥
rrsauemfiyprrxmeenp:
⇥
⇤
⇤
⇤
j ijnatyfnuarjgzfgoma
ahxplyylbilvyqsnmur:
gclnkyftjpjlzrhyvam:
ohajsdwbnrnzhytlpbc:
rmhmrhginnadcwzykao:
⇥
⇥
nagudqriihbpypkkyyu:
⇤
⇤
⇤
⇤
fgdahanyrcplrakgmuf:
⇤
xsnmixjrfmrywdnvhao:
⇥
move $a3 $s1
⇤
⇤
jwrhowlmanrycgesata:
zonukwjgtqkrpratyfb:
⇤
⇥
user_move.validated_call %shift %fail
⇤
⇤
⇥
nwqfnksrarryxbbbkxa:
⇥
⇥
ghakkzbunnduiymgrrr:
zexalywnmwrsymnwmiu:
⇥
j wuyywgnaqrqobtnodav
vhzxfqidaanwzrmyrae:
j ceyzgihxfvyaqqrnhan
j qdlnhctekrrawgijhyc
irntdfekqrncatpyirv:
⇤
⇤
j adykpurexndyleadrpv
qdlnhctekrrawgijhyc:
⇥
wuyywgnaqrqobtnodav:
user_move.validated_call %merge %fail
⇥
⇤
⇥
olradyibltntwzfruhc:
⇤
⇤
⇥
⇥
arvqzxygjtwngafalqj:
⇥
nevatqevyvozqmchraj:
rwrcnazodbjmdjypygf:
⇤
bavkndyllrwsfuotkce:
⇤
vnybgkhaapffrnwnard:
qbuxrbhauunnojivyza:
⇥
⇥
onnkzfbypercarmlymz:
⇥
mlrwxfyatxdwnollyiq:
⇤
⇤
tqgseyrfunbmjmnacly:
⇤
⇤
⇥
wioayarcnkdcmcvowbt:
⇤
⇤
⇤
user_move.validated_call %shift %fail
⇥
j bqrnkepdadctyfgusbs
flybafjnodrrsatbfxa:
wkmrippdginraqyocfv:
j zzygzknqxrgjuzvawvm
bqrnkepdadctyfgusbs:
j uyqatwlavgfnlskkrae
mccrayrgeyozozrnaan:
j qyaattcnywbpkqgvrew
uyqatwlavgfnlskkrae:
⇥
⇥
⇤
nvrgydkqnaxukbctxdl:
ygdobnraqbgvsnierfw:
irqgwscbbpnyhuzcazb:
⇤
reyqnfgjrhdnyuaxxbp:
⇤
knvylsyanryahyclorm:
⇥
clhtijrijhvrnnyfxba:
⇤
htrekkdudqancwylgts:
⇥
inc $s1
brwayyaraknhmqdmxks:
j ueptymnpdqaovsfrinw
⇥
⇥
⇥
okstmfnwrafdwwhyxhs:
j nfplyrfzdgqmbhryjya
ueptymnpdqaovsfrinw:
j uflgnordnmhyczvaxko
⇤
⇥
vaaqnyswqchhtykcrjr:
⇥
ncyezavmmwhganhoxrx:
apyltfnyplxlmewonrl:
j okstmfnwrafdwwhyxhs
uflgnordnmhyczvaxko:
xdhakglqxjnntimdyro:
j kdaijrtxnxapizyczjv
klbefhuwqrfytnbgjma:
⇥
j rrsauemfiyprrxmeenp
pipnnfayntrqvwxjnqn:
kdaijrtxnxapizyczjv:
j bmanajakrdwhjnumyde
adykpurexndyleadrpv:
j rjmdbmcgnmcivujryea
redzfatxpyuycpnfdyw:
bmanajakrdwhjnumyde:
blt $s1 %dim for
j cuqwmqeprydoaryarnv
⇤
fsczabaadfcnyydmrrs:
rwscbeypldsnsaigaar:
⇥
zupvenytfaevggzddqr:
yancghmwezqzzxcrulq:
⇤
⇤
⇤
⇤
bgncrqtayeulxmjbwyl:
j qongryawurjugsvsqoq
ahcsexpneiwsknruaye:
j apyltfnyplxlmewonrl
qongryawurjugsvsqoq:
⇥
kynyhvkconaprnwghaz:
⇥
⇤
⇤
⇤
ctrakkywsyntbnxsaxq:
⇤
⇥
etytmqrnramyvnvgkrb:
qbyvdamfnswrkqunrbe:
yixbrseakxqnxfanlro:
gchrpanmlkluzmwzyqa:
vriebzbnuuatnladbuy:
⇤
⇤
mraunxisorakkrzyhjv:
maytxtaynrxpxxyeanr:
ljxrwdcgqardqunynbd:
⇤
⇥
li   $t9 %char
⇥
⇤
nilssaajteylhxrmbop:
⇥
qnjuvklqnuyworgetac:
zaqnqjrfdlkacenryan:
zkaobgkmsyjqknsijra:
oewlyglrnsyfykeooah:
wspnnoajrwimyqvnlyj:
oyzzrrtxnhksimuafea:
⇥
aklrnaykwwlrnekktqg:
arhnnzmxurrcbpmyfog:
seq  $s0 $a3 $t9
⇥
fpryjvlrmfdriaunkql:
yoahnnjkrjrkrtlwhuw:
mavudxmrjvwoenyajkx:
⇤
⇥
j cinrwrbgqcaribatify
cuqwmqeprydoaryarnv:
.end_macro
.macro user_move.macro
j mlkraronynfhvtffxke
rwcpwexysjhvnpolxat:
⇤
⇥
⇤
akqttaznnsjlycowzra:
tarkknykepfnsraeudl:
⇤
⇥
⇥
uvagtsbpcnxraccrhsy:
⇤
nbjyrparrolfztzbifn:
⇤
⇥
iljumrjtntjcoaawsay:
⇥
⇤
rgryeencpwliaatjgjy:
yixpasiynbryyrvnvdc:
j jpxprlfdhphynqazfdr
nrfaeqmjykhnxcditla:
⇤
ypnepyyrkahcttaoksu:
anpawirresovhvywndt:
⇤
⇥
dirpgwjnulxkkystpan:
j ncecqxsuvcgrayvqxir
unpacewrsdqyqgtfasl:
jpxprlfdhphynqazfdr:
qsfurorylaznbxpajbz:
⇤
⇤
⇤
⇥
⇤
⇥
pjwfxlynaeurlmafftb:
bnpyuojmqyaaeabrjfh:
ebyjjibyrznmwgzweta:
xqayhrwdemjnjvmnquj:
⇤
reaymnfsnrrhyqimyao:
⇥
pairtuktrnychcuvipc:
⇤
madanygcdderhsjqotr:
⇤
⇥
lprfguyoxxgmuenrrka:
bwijwacgnkrmmmjayom:
rtuahjeyuzaxnhlrixb:
⇤
⇤
⇤
⇤
craxntdmngaxyfbkwrn:
bvjocryaknujrwfqjiu:
⇤
⇤
fruyvlrziqjpqnkdpca:
⇥
⇥
⇥
⇥
⇤
⇥
⇥
⇤
⇤
⇥
⇤
jynuyahshctxaqfrsno:
⇤
⇤
aebbhndyzyonicafrlw:
⇤
⇤
⇥
zaulorgawnecyseaucv:
⇤
⇥
⇤
⇤
bne  $a3 'R' fail
⇥
vcringgmqzwhcwalynq:
j tnanhxwzeryburlwrpt
ydbsargiobixrbnirjt:
⇥
j hnrmtvcpoomaymdwqfn
tnanhxwzeryburlwrpt:
⇤
⇤
ayzdmgrjwnvfzjuzojc:
⇤
zpzkysyaogrycmganna:
⇥
rqrglyowdnhivvmqazl:
gyvtbaetmrkamanrwxk:
⇥
zalyxbwmuagfaojornh:
⇤
j ogmtpyugnassumliyrb
⇤
dpeavkzdibcpjeniynr:
ankcenyuuwamofyrlja:
qnkgwmgnfvhyrgapgar:
⇤
⇥
⇥
gaqerovlyhxtbmqrybn:
⇤
⇤
⇤
⇤
⇤
⇤
⇥
atrwyecnckyntnerzqa:
⇤
⇤
pwkexhyqaoyolnbydyr:
j acqbmltnjqdunarucye
vramxqfironbyelutyi:
⇤
⇤
⇥
⇥
wpyzqyyknwawudtabvr:
nyuwgrumhodnatcsapw:
⇤
kazygahmjqabanryphl:
hypnfniiuyovpaiyrzh:
oxswayqcwlixscywsrn:
⇥
jiipcnyjrfabzvdanvx:
ctrzwknaykcrbpllryb:
⇥
⇤
⇥
⇤
⇤
⇥
ogmtpyugnassumliyrb:
⇤
⇤
wjrtanijimozssypjkp:
ntiphqxiydcnuayrmxe:
⇤
dwccqdajnwmxyzasrnu:
⇤
⇤
frnjzkgrupyhiaytakp:
⇥
⇤
idypvdrpamnartksxxn:
nzgvoinixarcyhovbrr:
⇤
⇤
⇤
⇤
⇤
mnirnoxrgyyaeebppny:
⇥
nhyniiuwzcsrpdkhadg:
⇥
yhpoqxnasmjrbjlsyqt:
imecwkzlrageznbhhyh:
⇤
⇤
⇤
⇤
⇥
⇥
⇤
j naqpmyfivthrjchydnm
nboqoadapqydyrynkbj:
nuacsnyyywwkzhdcrrg:
j zkgnxvazlirfxiyngoc
rudqvnlaraezhfympod:
naqpmyfivthrjchydnm:
⇤
⇤
⇥
⇤
j tnkbyzenkolmnhtrzaf
eyaeugcuryvfaanpsrp:
elyfnbrqnnsfzatxfdw:
j tviojunrngqawrzptdy
ofrtazneabewqoeyyef:
⇥
⇥
zsmryayoeslynwcepkm:
⇤
⇤
⇤
tnkbyzenkolmnhtrzaf:
⇤
qympopyalgrzkdnjslm:
⇤
⇥
horz:
joqnorpsyjarfiuoztq:
ncpsjrbyawybacvvwvw:
⇤
⇤
ggeiuzyanrzptaxqfqp:
alqbnkgxgermyakqize:
⇤
⇤
⇤
⇤
pcknidzwxaeyfrzmqmy:
⇤
⇥
lyyuyrcnoazrhrmhofb:
⇤
pknyjyfmayfrgzpurxi:
⇥
⇤
fnxyakpsrymrkahpcno:
⇤
⇤
⇤
varnirdbbmflujxyghn:
pkynrqbviapjyclqurm:
⇤
⇤
pfaxqnqorvakirydzyl:
⇤
tyvnngazllfqcinowlr:
⇤
⇥
bvpgbaatsniekcroysn:
⇥
⇤
⇥
⇥
⇥
⇤
⇤
yynrcijzrpfwkzcraba:
user_move.for shift_row merge_row fail 'R' $a1 end
rotfrackbshinzynfvr:
mnjrletxqvsgfowyago:
j kuzvyvjqfynrqrpahpa
tojrpyatsrsegqkzfon:
kzkyrxqevravbonlasi:
j ntifjnzgrartwlpykcy
⇤
xpqytjadjrxxgkynzbf:
kuzvyvjqfynrqrpahpa:
htnatyizgcstmuwronr:
⇤
arlorwpgqvyhbvaiong:
⇥
uokoayygonryacpicis:
ytyobqzsgnncahyarzj:
rnfqwoaynficzyumjyn:
⇥
⇤
⇥
⇥
⇤
redypzznxcupwayfaaq:
nstrpgffuwaqnybquvr:
⇥
⇤
⇥
yynmpyablsryrwpoeyr:
rgdiqeebnaompwxoygy:
⇥
ffdrxkmlgdrnuyricar:
j end
⇤
⇥
⇥
yxazulgclirmrqajany:
⇤
hcvkctamdyyrhqsuanr:
⇥
⇤
aflyhpnzryrarlkseul:
⇤
j vnafdreyyllozbfqvuy
dqxrhaflrcawhhipsny:
j hurmfjnkgrycnoalfdd
⇥
pnvyyfzavfabryjyqfb:
⇤
vnafdreyyllozbfqvuy:
⇤
nnjwryvpbavmbpzvnnt:
ucydwyrdambhknyladb:
⇥
athrtatanbstxbyepqy:
oxehbcqvlprriyateen:
⇤
⇥
⇤
mnewmaqoygnyqvrlgbi:
⇥
⇥
⇤
⇥
j pynkccmhcmrodaksgyb
sxxfryklwbgaxbkckvn:
j paiuwnjmqydrjfjgyvl
pynkccmhcmrodaksgyb:
⇥
⇥
⇥
lyhuhnrjdofeabwxoha:
j blyaryubnqgkxmbkbyk
⇥
⇥
⇤
⇥
ufwndtcxrjyolwawune:
⇤
⇤
⇤
j zzdgdpzaesyskvsjnar
⇤
⇤
⇥
blyaryubnqgkxmbkbyk:
⇥
⇤
rtcefjwunpdanazzycj:
⇥
⇤
⇥
⇥
phrnddriarnivsyytpp:
rebnhvyelckexprannn:
imroaonijsonykoenan:
⇤
⇥
syexahrgcpswfnqqrub:
mgrkwjanqqnyrgvywez:
agyotykrenfmabjloie:
⇤
⇥
j mqlarrmxypynalygkmu
ckrvrfrhhnoyslmhpar:
j nboqoadapqydyrynkbj
mqlarrmxypynalygkmu:
⇥
⇥
⇤
⇤
⇥
cnzkpvvgmrxmkmiayqw:
vert:
⇤
⇤
⇥
stgzyrbahnwiphdiugn:
⇤
⇤
ehhoijvyyrexkfpxbna:
⇥
⇥
⇤
⇥
⇥
⇥
user_move.for shift_col merge_col fail 'U' $a2 end
⇥
⇤
⇤
⇥
⇥
⇤
⇥
⇥
⇤
birxdnyoyflattcksos:
⇤
⇤
⇥
avndrgusaejgywidkrj:
amyegkqxrqijnrfdcls:
orijiiybajilohngevn:
⇥
bnzcoyaayrqxxiwywns:
⇤
⇤
nqnylryanvqkpzgfnlq:
⇤
⇥
⇤
⇤
⇥
⇤
⇤
kqhrcachdlnlcyqscse:
⇥
⇥
fumxpuhsnayhrbrrtoh:
nnmbihrapbnypwobahs:
⇥
kakzzczraynynmyymud:
⇤
ynzoaxeurmlktygyicr:
lafoukkarhsipyndbnl:
xyoabsftmrqnlzwtvrp:
⇤
⇤
⇥
⇥
grywbwcjnnfapazxpap:
plrwcciwvwpxgsyaynw:
xaatrvynqdvochmsnkx:
nwmryleieafxoafnkhv:
⇤
⇤
⇥
⇤
rezkiqkynyywaspuucv:
qmuyrpnvgaufvfnimuo:
⇥
gjuyoniajxdlhdnrrzf:
⇤
⇥
j nybnsglahyalrjdnrme
j uyocianzsnfykyreyps
uyavsbwpgfrgxnuqavy:
j sxxfryklwbgaxbkckvn
uyocianzsnfykyreyps:
⇤
vhtyeubsayocjnsrllb:
uvdybspngcviqaxrpmq:
⇤
srrnpyvrbmamubyzust:
j nrfaeqmjykhnxcditla
nybnsglahyalrjdnrme:
⇤
⇤
⇥
pahynohughxvalprfcu:
⇤
⇤
crnadzrngcwuayftwgk:
arobypyjlpffwnghzyn:
j lggdzmakmlnodrwttya
mlnhehhcnyjastrrdhz:
moyumulylkxnvjfarmz:
hurmfjnkgrycnoalfdd:
⇥
⇤
⇥
⇥
⇤
rantymbwxtaeahvnors:
jgdwjojhdrtylqyaafn:
j ufwndtcxrjyolwawune
⇤
lggdzmakmlnodrwttya:
⇥
ddoxkgcroguryzanqmk:
wdgiirndkjliklavyxn:
⇤
⇥
xkzapvbqswyfgqrfkjn:
⇥
⇥
rnaopzkykiuwcmyycnx:
⇥
⇥
⇥
ykrberziyloacuainbl:
gaolpryeynxslyxzkvt:
⇤
ivrnduztorxkzlazsyb:
⇥
⇥
rnrgyancnfomiwmtfyh:
end:
⇤
gnvyrwkwanudrtwtcns:
vmhjjdrjyxjacliulnr:
luovrrebckryraqcwvn:
⇥
⇥
fayfcjrnyfqivtvxjrw:
dxqrwunhwawxjyprmvn:
cexbantmifhgbjrndyf:
⇤
nktnwbtcrrzkvsasybu:
wyvrkqnnkafdiupqbhj:
⇥
j bmretonhnraenuupgny
⇥
mvboenfcyzrdjakfouy:
⇥
j ufrqnxynxbkskxgcaek
bmretonhnraenuupgny:
⇤
⇥
uycbmodhrniefjnfaek:
⇤
btadyrvlucrmojonakm:
⇥
⇤
⇤
⇥
rykzxgxmybnysakhocy:
⇥
⇥
obadrllysntywbacyhr:
⇤
⇤
cttjzsrbnofnbzzayek:
⇥
⇤
lxxruqyastmzlynlwjx:
kvkgbmurnuymdaciknh:
⇥
⇤
jal  check_state
nyissofftriabwftknm:
⇤
anfyiiajrenhkwcfwaz:
j uriytlklebamyncmorl
fhfwdnycpblaxyreqaw:
⇥
⇤
⇤
⇤
⇤
⇥
⇤
vmakvasrjpbfejwnoyu:
⇤
nniilqfjvaovhuqytvr:
acqbmltnjqdunarucye:
⇤
rnpfjpcwxymfhaanhbt:
⇤
⇤
⇤
⇥
nhzyzcovlrngnihtzaq:
⇥
⇤
⇤
xkuybpakrnnnechkwhi:
ingabwxihyfcmqhxrtq:
ihayrelrafenvnkrmhy:
⇤
⇥
⇤
axaeqavwfczyyrsysrn:
⇤
enarlyyzgllmulnfwzg:
vrlnyxroqoytygeonja:
⇥
zgfqkddmvytprfqangz:
⇥
⇥
hqqanbgykirxadkrnmp:
⇥
⇤
⇤
kknanloqgvyrwqwmpfz:
irnprvyxpbnnfbaxvqg:
⇤
⇤
ypxnaprahceieajtamm:
wvxptzqybojbdrnataa:
lbrsnynaayjvsvronfp:
beboutonamuiunyopkr:
aguvmnlybkfugccnzyr:
rtyjakdqakyknhqlisv:
j crnzhdqvymcmkwrrasi
⇤
⇤
⇤
j fubipcsrjyrgaanjjtx
muounbpewdcyjcarebr:
⇤
bnimjrodharsykdztbr:
j rbuxhajwyhodxbyajnk
fubipcsrjyrgaanjjtx:
⇤
⇤
cfaucljahgpeuyrkbnh:
⇥
vrbncuyxmqvldcoxdag:
vaubyardhzcbabynbxo:
aarwtwkaynmmklzuvyd:
⇤
⇤
⇤
uriytlklebamyncmorl:
⇤
wnbyypbuosajjxrzlky:
⇤
urpcxjkkwmlpzyndlap:
⇤
⇤
pbfwgyrdsagoijqfnsf:
bkajdrxznaavhmhnyhh:
⇤
tayftofuphnulkxnard:
cmmxrgrsicmbwwddayn:
⇤
⇤
⇤
wxevyfkwiugaqxofnjr:
j dvwcaitsmronrvywpvt
rbuxhajwyhodxbyajnk:
j iqagyfxorkoawudlnts
dvwcaitsmronrvywpvt:
⇥
⇥
⇥
⇤
⇥
⇤
⇥
ytahkrvrbwpnwlrfhjn:
⇥
⇤
noxiiqfallirpjbyfai:
peeqgbyklincyarzajn:
⇥
⇥
yzqqkadpaxrrrkynvva:
⇤
⇥
noygilhyracuvusxqww:
qdgqqgtntuxyunmarkg:
⇤
⇤
ynvfemcgirvatznymex:
sirhanafkrswyxxmszx:
rwkybiitmaqnhayucsy:
ixyuwabkqyxzxvrnyqo:
⇤
j rcyuigtaobffamanhlr
eqmbjmfnawauqdropyy:
upwnnravsuscbyaneex:
sfdzrbnmsafiykdnvnh:
⇤
j cmveteyavnyriiekaeq
⇥
⇤
rcyuigtaobffamanhlr:
⇤
⇤
⇤
⇥
⇤
⇥
hagxqyoytarqqwjlhtn:
⇤
wkjalpyeienqeauevar:
⇤
mfvixlkftbaxnlylrhg:
djydjingkmcxdabrvgb:
⇤
cvxphgjrddhqjnxyyoa:
⇤
tcrymlxtwaavuyyinno:
⇥
⇤
j bjcsprwdcawrgyxnkgw
ufrqnxynxbkskxgcaek:
kabmnrekiakyeyaianm:
j yunzcisabnqsdsyhbro
⇤
⇤
plbknnlyyercltawooh:
bjcsprwdcawrgyxnkgw:
⇤
⇥
⇥
⇤
uvcnyryrulbaahemkfm:
⇥
⇥
⇤
⇤
⇥
poaydqrnrtwkipuanyq:
unaxrnshuoouzmjywqd:
⇥
ycdahafkwjjnhkrvoca:
⇥
j nkspbyyrnpgwoswxjca
⇤
ncecqxsuvcgrayvqxir:
j mvboenfcyzrdjakfouy
yawzarrnwrjulkobqvw:
nkspbyyrnpgwoswxjca:
fqxwnnyqrclwrqgzalj:
⇤
⇥
⇥
⇥
j ygglnsndasntxebrazo
⇥
xxzwyrdrkanghgynbjp:
j yfjabyqfyradgonfvon
ygglnsndasntxebrazo:
⇤
⇤
thzdkotvyvmrmavnaya:
⇥
zeyutbtquaoouryasnt:
ifbxwlndrcrayrkhkwd:
anymsglydirhbcuhgxh:
⇤
⇥
⇤
srefhygdebfjnanyybt:
⇤
⇤
⇤
ivayynaiqkcjljnworr:
⇥
ybnwxfogharqryozvpq:
⇤
⇥
j acwnbyrabnaghtqapkq
gcylnazyfezmvdjrogy:
j ydbsargiobixrbnirjt
⇥
acwnbyrabnaghtqapkq:
⇥
⇤
⇤
yyisgmkaewlternyihb:
j jjaydirgncyhddgecws
vyqijnnnanrpyxajgos:
jsruqzynpfsfemobalm:
j gcylnazyfezmvdjrogy
jjaydirgncyhddgecws:
⇤
⇤
bzbzrntnwaubsribhuy:
⇤
⇤
qnzurupryajnnsocovq:
jtxkpkaapnnyujrubru:
⇤
jcsnrxqaikuhhvyputb:
⇤
imyntiaznkoysgurnaw:
move $v1 $v0
vyaraenxkxajgnykrnc:
⇤
⇥
⇤
⇤
uzvyhjrasoynpyttxbi:
j bitakdnnalvjccxdyrx
cmvdprnayazrvrbanni:
j eyaeugcuryvfaanpsrp
bitakdnnalvjccxdyrx:
⇤
⇤
wqaladerfhdlvnaqylk:
⇤
⇤
⇤
smirdzynacqrguxjonx:
⇤
⇤
qakibdnewhnnaynrfzn:
ycsaaribwxblpmeyngx:
inqldfkxxyrfirayzas:
⇤
⇤
⇤
alvarnceufvrvtgofym:
li   $v0 0
uiczfwdvfyvdavmayrn:
jptgidsajnorjctyxra:
cyfaqlaorvlhiueyneq:
⇤
⇤
⇥
⇤
⇤
j    return
⇥
j ciawyrboibvshniagai
tyaoeewforazyzqfrvn:
j ckrvrfrhhnoyslmhpar
ciawyrboibvshniagai:
⇤
⇤
⇤
⇤
⇤
rqjqnszndyanmyvwvaw:
fail:
⇤
yddyedfrrbhcalsspan:
⇤
⇤
bnatjchqgranejayddw:
jnruagatqnnybfuppze:
akqnegcngunjnylorpt:
fijuoaytnkkacqcmnrc:
⇤
⇤
⇥
hunyyeilllatnrieprl:
jsnatjvyfnlgiirhrnt:
⇥
ebnqiqoqujefaxryhvf:
⇥
⇥
⇥
⇤
⇤
⇤
⇤
aofxsertiwurascaiyn:
⇤
axzltdrpyudcnvrxygy:
khqaxarsmcyprgqnyra:
rufquuocrphukaklyon:
⇥
⇥
bqhwknyabqurphjhbiy:
⇤
⇤
⇥
laaayfyrnzmnullkaiu:
⇤
onzinamokyriuwqryib:
⇥
⇤
⇥
ujrmyxbfjydwpladcpn:
⇥
⇤
⇤
⇥
yrhhokkeyznrsucdzae:
⇤
⇥
⇥
hdzskwwnrqlyyngkjaq:
⇥
⇤
⇥
⇤
⇥
j vgnanlyrofrbmonodgu
ntifjnzgrartwlpykcy:
j srrnpyvrbmamubyzust
vgnanlyrofrbmonodgu:
⇤
⇤
⇤
basnnxryqsnikswznoa:
⇤
⇤
⇤
wlrnwioboriaywgtmyv:
⇥
⇥
wpzytoapnbfyrcidynn:
⇥
⇥
rnzjtslfbskfapuzwyl:
⇤
ancccqdyrchpwraivqv:
⇥
⇤
⇥
⇥
garwyvdydwkkndcrsyl:
xpjyuvnwbhingcyared:
alrycpyalbasangpwsz:
bluzribqnniymycyadp:
⇤
rffdyhrnklvnshukakf:
⇤
⇤
rdqnsyaflkbaqpmkcdi:
⇤
⇥
⇤
⇤
⇥
⇥
pjjiyzvsnsjywanrviy:
rqzxcapwcdnajxwyhls:
⇤
lblrhpikynajcdsjktm:
⇤
⇤
⇥
⇥
j rykaaenpnbagmaggdxb
njrnfabtmjcarrygnqn:
⇤
xnqrrgifykauadiuwus:
j tyaoeewforazyzqfrvn
rykaaenpnbagmaggdxb:
⇤
nlorbomklryaeqnzpym:
qljqwtxadynnyrzcfol:
li $v0 -1
⇥
klvsvronpuyzeaecono:
⇥
narucfljcmhavonyxeo:
⇤
li $v1 -1
oytncsnqoxacdrqwijh:
dcxuydqengatfkzreac:
⇤
⇥
⇥
⇥
⇤
⇤
zjywnplirnzmrwroawl:
⇤
⇤
hwvjraycztwyuaqandk:
return:
xcyqthbxalaalgqunrn:
bbdbhymauywtyqnrslp:
flprnzwpgaybgtkdpgl:
⇤
⇥
⇤
⇤
⇤
nogjqhnlkhqlcsazyra:
⇥
⇥
j wugpupbrnasxvuyatbn
⇥
⇤
⇤
⇤
jyeblbogzoraoodjnhw:
⇤
rvyyvzbnrstwvsdqzau:
alajomysrnvosjbggsw:
asmyiinerntspljltzn:
htanhmrjyhsadtdzytr:
nrlznzsddltzfzdaqyd:
j arymfhgwlfdrmkyvnwm
dtnrmjnhaymluqbrynw:
wyaodmsnivavhdrdyfi:
azonnmirrayphgovmin:
yrorzrkrvnjhatpgvnd:
⇤
⇥
lpeadrntrtpynzqrjzz:
yunzcisabnqsdsyhbro:
bzyirhfgaryezasldbn:
j dqxrhaflrcawhhipsny
⇥
⇤
⇤
rxncbjprdaoyjvnqycc:
qnaytxsxiybbqsrkjhv:
⇤
arymfhgwlfdrmkyvnwm:
⇥
tdbzvfmlnyuaordxydr:
⇥
ykwwracukdnvbxxzinf:
⇥
⇥
bjqyonvkrwahcagjgpe:
⇤
uroyngmmercamtweaae:
aefurlprzlvygnnosxn:
j lnbnrxyekracmwkxagc
qxypxfyadngrhjsylyn:
aowhmyramdtflygnmwb:
⇥
⇥
⇥
hnmgjjhahrzceyunaoi:
⇤
⇤
⇤
⇤
⇤
⇥
⇤
⇤
zjanytndpehsrkvyhho:
uafyxrbvjnrlgvyaipa:
⇤
ycxdybrnofjadswqrqj:
⇤
⇥
nohprvpeolxynrqeqam:
⇥
wugpupbrnasxvuyatbn:
yhfolgqehxtkracanlc:
wloywoqazdcdbrsnuym:
move $sp $fp
⇤
tyinwarwuyjvxmttdpa:
⇥
⇥
⇥
jyeqwavyhcruamrtncs:
vnylxzyoardqoevptij:
cdcrbqcozypqqayznpo:
⇤
nzopkrirtyacsjvaybn:
xnatxinaivpurnjzwpy:
⇤
⇥
plfdayrvwcnhcikruyk:
yyhxjynnsaktnlnsrxr:
⇥
acnmjrhsezneqyatcno:
⇤
gnhldacpwroawoyhweq:
⇤
xhynkglpdznrbtasysh:
jcfcmtaklwnstynztrm:
tehrypnkcracehytsfd:
⇥
halqaahaviryanhoucx:
⇥
j eonsuvieohparccygcz
mlkraronynfhvtffxke:
j muounbpewdcyjcarebr
eonsuvieohparccygcz:
⇤
⇤
⇤
⇥
nrvztqpykxxdkunyxak:
⇤
waaunsmufijkersfyzm:
⇥
⇥
j dpvrlpykyvnaiguzpre
vsgmvgbnbarwqtuefiy:
⇤
j tojrpyatsrsegqkzfon
dpvrlpykyvnaiguzpre:
⇥
⇤
azaryzoajolyvfbfxon:
kbrppnejqonyuwjnnca:
⇥
granplikrecxoyibadf:
⇥
⇤
⇤
loknsybmsreifwawhjn:
pop  $ra $s0 $s1 $fp
⇤
⇤
⇤
⇤
⇥
egnqaqraukykxherbsn:
⇤
nnrajkzlghynygujywr:
rytfwzntqunylwaqjgx:
⇥
⇤
⇤
⇥
pcjbozudkyayafnrezv:
rtdppsnwsmkkqxayvzn:
dkqaolvbrcneybaknya:
ijqlmnnwsayamoqrupb:
⇥
yawxusryvfdhypldhen:
⇥
teotryaxmdnswokpbcr:
⇥
j enrxmrranwjaptyweej
nfrstaxqpqjdyayhlar:
j uyavsbwpgfrgxnuqavy
rhzaslpnouuhyfqwyqa:
enrxmrranwjaptyweej:
drxzyorjvrecjnarxrd:
⇥
⇥
⇤
⇤
zoynmrcyzjagjtvevvs:
⇤
varatvdnyxnrryqmrnl:
⇤
⇥
ltpfqayhznxxrkxdqqu:
anrxsbksklzyutxoyzm:
⇥
rymnskydzbhurgaeayn:
⇥
ofhnqnwwrealgqjpyad:
⇤
⇤
⇤
⇥
⇥
wwswyhzsymdfrvynqap:
ykrewvdpxnpttppsaci:
⇥
nkyrbayfyitncwfuavg:
wayuioltrasungbjeos:
⇤
gbyrykuoytxynrmaynh:
⇤
j iejzulnpndthvrudyta
iqagyfxorkoawudlnts:
j eklyszrpaibrznjstcd
iejzulnpndthvrudyta:
⇥
yqdsxdlrvpbgpshnadr:
⇤
⇥
⇤
⇤
qfztqfqanulxylytrkt:
⇤
⇤
yqyjjjywtsbariagztn:
⇥
wmworuvapkpaewnuvyf:
sjzpyryinrsakblxswr:
⇥
pitizafhrpgsgtaydln:
⇥
⇥
⇤
nzggmiagssnyicjptxr:
⇤
⇤
zgkijwiigkarmnyfmuy:
tqblvfysyneakrivfni:
pzrdmplzanzaetbgayn:
⇤
ritfstnbdvnriyiarzl:
vbsmtslywyaynhbbmrg:
zznnkfwjalyrfarvlgv:
⇥
⇤
bexkntwwyruibbppaae:
j nreplbfracoyiydhmcn
⇤
⇤
⇥
cmveteyavnyriiekaeq:
j nfrstaxqpqjdyayhlar
nreplbfracoyiydhmcn:
⇤
⇥
lpiqsomnasawprzsxay:
⇥
ytirnahrbtbwfcalfzj:
gfnposrgbbhbywdyqxa:
⇥
⇤
qntccydkaaeoykrdzzh:
⇥
⇤
khnkwrmxpvcywdjfoya:
nvsxardzlswszmjeydp:
avkcqykbprnrdurdrzj:
⇥
dvcngrhyynioparcupf:
j mjgrthgakgycuawprqn
⇤
⇥
cizduwoenyerylahfdz:
⇤
⇥
⇤
zrmvltyrqvgvnqbatrp:
j mynvofwrmgaqkljgleu
⇥
⇥
⇤
azcbncqjtinypbfrdab:
⇤
⇤
⇤
⇥
oacdrvhntbduakgyqgs:
vnayrcraemnwoebhwwz:
⇥
wnagqymjkylmrboilry:
⇤
⇥
⇥
lnbnrxyekracmwkxagc:
⇥
⇤
⇤
msssrnheawysubzxybq:
⇤
j ptqnnzyzftmbqavywrw
eklyszrpaibrznjstcd:
j jsruqzynpfsfemobalm
ptqnnzyzftmbqavywrw:
⇤
⇤
prppximssqawrnxlejy:
j gaqerovlyhxtbmqrybn
⇤
ckrryeratdnymbgimfz:
⇤
⇤
nkbarnaejynsnclbmgx:
⇤
ywwvotfrwaaayngjxus:
⇥
j hnvmyvvvaxgzqgrardy
abhnqbcfmjyrdlyacnl:
⇤
j njrnfabtmjcarrygnqn
hnvmyvvvaxgzqgrardy:
⇤
qgnegjypyaqozwemrtn:
namhycultartrvyfsin:
⇥
bpmknenafrkskaynkjq:
yihygqjnpmrizgannfo:
⇥
⇤
⇤
rxbvymoaxkumvvyaxnh:
⇤
⇤
⇤
mynvofwrmgaqkljgleu:
⇤
cakhpdkrzcflkynqaeo:
nmybuzrppcbniqautrl:
⇥
vyswytgcaqfkvrgjnob:
⇥
⇤
⇤
⇤
nwqinhglaarrtoycyon:
⇤
⇥
⇤
⇤
⇥
⇤
⇤
⇤
syvtbrnomojgbajomnj:
⇥
⇤
⇤
⇥
rpohrpvcazytfnvpwtw:
⇥
fheycdpfmnyeoagkroy:
⇥
⇥
scnlktiayckcrnatvcb:
⇥
senanzhahymcyrrcuvl:
⇥
yuarnrmbefqoouncxas:
ukroydtnlmpvhxsjamj:
⇤
⇥
⇤
⇥
tmarqnyknlkvngfzffp:
⇤
lyerlqamnjairjcxbka:
lkeznjruakexuanzeyg:
⇥
⇤
⇤
⇤
⇥
⇤
⇤
⇥
⇤
⇥
crnzhdqvymcmkwrrasi:
⇥
⇤
⇤
⇤
srpnygafajlrvnaazzy:
cdnjnnknucwofkryoar:
push $ra $s0 $s1 $fp
gnlfnrusbbaywfjllgc:
⇥
⇤
⇤
⇤
bzhupsyjdriqaajfqan:
⇤
⇤
aouskurfnnyzmnnyczy:
⇥
⇤
⇤
⇤
⇤
⇤
⇥
⇥
ryzdrjajbmtyygntipe:
ongrnajgyevmswypfzt:
⇤
⇥
⇤
⇤
⇥
khbqteaaahenprypzrj:
⇥
ryanraczqxgbkitgacz:
⇤
⇥
⇤
⇤
rqghanqpgabuxepcqny:
⇤
⇤
⇤
⇥
mnembkqrpsylcapqmuo:
move $fp $sp
⇥
rocphaywirfbbnommjt:
⇥
⇤
⇤
kybyyqnlobtkyermaly:
⇤
pxufrenvoismaybmura:
grnhlgypupymiawdzrq:
j mxpdznszlmryaiiniae
j tvnrdjayjgemoyrgjqi
hnrmtvcpoomaymdwqfn:
j abhnqbcfmjyrdlyacnl
tvnrdjayjgemoyrgjqi:
⇤
⇥
zkgnxvazlirfxiyngoc:
yhqyidrxbyaeowvlpnt:
omyrgdahdnqioplvdnn:
j xxzwyrdrkanghgynbjp
⇥
mxpdznszlmryaiiniae:
⇥
⇤
ydalzxgoufyhatnrkim:
⇥
j athodrsseecaooyionw
paiuwnjmqydrjfjgyvl:
j vsgmvgbnbarwqtuefiy
athodrsseecaooyionw:
⇤
⇤
⇤
beq  $a3 'U' vert
⇤
ofjptmenseacpwydadr:
⇤
rianavasqpkhqrftthy:
uyvjeaqdyyttrgnoogm:
irsawlgefnviyjuvgzp:
⇥
⇥
⇥
awydwrralbzofhpsncp:
⇤
yjnzaxthnrqxnotseoy:
⇥
axxornaoofjvtbuzlyc:
⇥
⇥
hgnspqdkwayympanrni:
mytaglcrfknrwqomhnz:
⇤
nsymihrsjaxjvowssxa:
⇥
⇤
⇥
lylynsoybnarnxxprli:
⇤
rgyernjuwizzpyxigam:
⇤
⇥
⇥
⇤
dkjuwzydsjrinrmdhas:
⇤
⇥
freplyrknnanfvddmrn:
⇤
⇤
⇤
⇤
⇥
⇥
ktqnsgovrakbduvyyft:
qrnrtzkanveebnyvbca:
⇥
⇥
⇥
⇤
⇤
⇥
⇤
⇤
beq  $a3 'D' vert
⇥
j inowydautniybirwpmj
rurvnskkespuynmsayi:
tviojunrngqawrzptdy:
⇥
⇥
cyigpqynranwfkyyuue:
⇥
jdrtrbdtqyasnfahbnd:
uoyniaysvikawrlwgjz:
yunwwerhguclqigaivy:
⇥
⇤
fjnnwemoxryafvgkvmg:
⇤
⇥
knkgatopfhgmybnarqe:
⇥
j jyeblbogzoraoodjnhw
⇥
inowydautniybirwpmj:
⇤
jaufqmovnbrerlqpdhy:
eprvahzcjlafhlynzrv:
oxndywrdhgedyablnmr:
sorrzpzyyjagrcsanxa:
⇤
⇤
⇤
⇥
⇥
⇤
⇥
awdwwrrihtnavgwjqcy:
ahjqyjyhwhqknnypydr:
nbwutfvmydxadhywbrp:
xtqnbdyiyarftrdbvnv:
⇥
⇥
jwgxeasnkdajyiakurm:
dbornqekiupyrfnauqw:
ajqijabucwhnajaruvy:
bayrdtkprozolvnzoyr:
qlsaqymmhrifnnpzywm:
rnaqdeiquvbeeyrpnar:
yhgaelyagwrfquauynl:
baaieextxxbznrngqly:
jvnburluofnawryjxhy:
adxwyjkyrbmeyoanvbi:
⇤
ggdnwyeyenlroaulqco:
⇥
⇤
j vbykiocoyvefadwyfrn
zzdgdpzaesyskvsjnar:
yjbddnacrclkygwjxdc:
⇥
⇤
j cmvdprnayazrvrbanni
vbykiocoyvefadwyfrn:
⇥
⇤
j rqjlmakyhhrmooqdana
yfjabyqfyradgonfvon:
j eqmbjmfnawauqdropyy
gnyalwelaiwdjddnmxr:
⇤
rqjlmakyhhrmooqdana:
⇤
⇥
⇤
⇥
jsflanonoqsqkmrazyv:
nsrdwiibagnjaylynfb:
vxcmcaprtoqyeqbznhq:
beq  $a3 'L' horz
⇥
rtnyaisrpuwnuxdnrsm:
⇥
qwncntaxhaurysmdafx:
anfqymocnyjzmyxognr:
j rwcpwexysjhvnpolxat
mjgrthgakgycuawprqn:
.end_macro
user_move.macro
jr $ra
check_state:
push  $s1 $s2 $s3 $s4 $s5 $s6 $s7
.macro check_state.macro
j dnlyczyvbvnbbrefaac
corgmaymqyomnvkrrff:
⇤
lmosoyrnnfxircftqja:
sxoyzoqreimjnabrota:
⇥
pmggrwlyorbnasxrmyf:
mrxinitxuhokpakwjyn:
mvshnnueyjdgmqwrabt:
⇤
⇥
trmmbmsyssgujeazncm:
⇤
foqaxwdlrimsjeykaan:
ydrrrhefkadbsmxxngc:
⇤
⇤
⇥
⇥
bkyunwtduxhagxcidpr:
eowattavymjkntrdino:
⇤
⇥
yqbhrkgjayjutbnpzgn:
⇤
⇥
⇥
knaryinqxtksqkawiih:
snrlwearbmkbyhnvnuh:
⇤
j evdyshdvtzirnxkakod
⇤
⇥
kgamrrtrrancmrbooyt:
⇤
⇥
⇤
⇥
⇤
uuontancmnriysspnvy:
⇤
⇥
⇥
⇥
uwrhprvalyobqrmznyq:
⇥
nalnnqirazyxrqzysyp:
⇤
knanzfzcxqdajnfryya:
⇤
uizfkorxfshnehehayc:
⇤
⇥
ynoknyyfygaprwtzqwo:
rbbyppfnwjvdwarxrzx:
⇥
⇤
⇥
⇥
rtfisgjiiasdanyaygj:
kibnbrbixvhagejiyak:
⇥
⇤
j ztzybsayewuyrbsuwkn
⇤
⇤
rofyqlcreatvyqnjico:
⇥
⇤
avuadqrtyrngynnzmgr:
zivhrnkajbesfykqatf:
epiokinrvnwaogwfayr:
j tfamrcdnvnoepnydyao
⇥
ztzybsayewuyrbsuwkn:
⇤
⇥
⇤
⇤
zklgcgnlyqurleijawn:
⇤
⇤
qyurjtartmmyjisnzkb:
⇤
evrizntfepvyznratnp:
ypzrblpgnurrjyhpwan:
oosyuymwqjapyrnbnur:
onraxnyaspgpdwkyurc:
jypxlbnirrhrxcaajst:
aaewtknzbhyaryynxki:
vaapncojordyyzpoprl:
⇤
frkyacunwrdnomprsgi:
⇥
⇤
qqwlmayznpdiiqgrdzp:
⇥
vlhkyalgjgyryomrnuy:
arcujeryotrmgnannhk:
cifryrtaeoebzrxxeng:
ogpiiysrmgeyawinykq:
⇥
yofhkpanoofeanpziro:
ppuanzrcqanywjbsdnj:
⇥
nvierkcndfyuweaalwo:
jknymxsturtxauttyqa:
fsknpovikrdnyfacqae:
⇤
j vyumygdrinfjroiabrj
⇥
⇤
evdyshdvtzirnxkakod:
⇥
uailzryqngayvgsqrey:
⇤
⇤
⇤
⇤
kfcnsunvilgnsrwyhad:
⇥
⇤
famxctbnfwjrbycwbba:
⇤
j zximsyadwliconlrumu
fvyyzqldnjgarzneezs:
j yiabsnabfxthsslrens
⇥
zximsyadwliconlrumu:
⇥
⇤
⇥
aanvpyrotgilyscnbzf:
⇤
asbihiimrroeropinqy:
nplaiagunuyuwchgwqr:
qcbynirjsntbefazgbn:
yzuyibsraeyxsberbhn:
ufoimymnrradyprcpyy:
nrysrayhqaunozanucy:
⇥
⇥
⇤
cyfroapwqygdmucmvhn:
⇤
⇤
rwgrhosxqzquviyanhr:
gjnrxsmkmqvbyaurfzs:
tyjnvsrdcparzlothnu:
⇤
⇥
⇤
⇤
⇤
cqqnhuxdtpynrxksnaj:
⇤
uprxogknuqzawgocyfa:
⇥
⇥
⇥
najexzrrkwlynopgtlu:
⇥
j crbnfvxaynxrvwweyjw
⇤
lncjbmcfrlyommnaiqg:
⇤
oagytmursbepundbyzz:
qryddvrijajwraaznxo:
⇥
⇥
zwaxyfnrybnioxjqrjl:
⇤
⇥
rtajmcjrytnwskonaap:
⇤
kapianrtmkynzrksrjq:
lyrgvygdnhdxznkbnav:
⇥
⇤
⇤
jryxdnsxqktqwqafnax:
dsrnkriodytaleavhiu:
j hkysemeiqmmhbcnpvra
⇤
⇥
tocvrmlcjnfapyqynhv:
ubyygtqnwvodwarhqns:
⇥
ldnyzavdvanpumdrunm:
⇤
⇥
crbnfvxaynxrvwweyjw:
⇤
⇤
⇤
⇤
⇤
⇤
⇥
⇤
⇥
⇥
⇤
baoadayajxncbcbrrtf:
⇤
⇤
⇤
binalfgrxqifcpucrpy:
⇥
hurrtaitzyizgbacpnv:
blarrvtomvfyrnmrkne:
⇥
⇤
⇥
ngehbvcatlzrfnuqyib:
jnurkxynibiuqrpdeda:
jjadtokeehfdvywfrcn:
⇤
j aonrdajnjqknfnbxyhe
daxgbrfeuwnnlzkqryd:
j lolbxmmfkrngjaoybik
aonrdajnjqknfnbxyhe:
blt $s0 $s1 for.0.loop
⇥
tgtepaniromictvvyag:
bnrhdynxxlafxhymgmh:
⇥
⇤
⇤
⇤
⇤
⇤
fyrsajdanqzgfdotuye:
⇥
⇤
⇥
craoyqvlgjknyenhatq:
annaxcwdrhnyksgyrhs:
⇤
⇤
⇥
yyrakmvnzvzwatownyi:
puqangyklibptrbkuvl:
⇤
⇤
⇤
⇥
⇥
⇤
⇥
ynarcvwvnyzxqlvitil:
njbqrpmhythkotrpvra:
⇤
nnaynhuppwrtbpdaren:
lulvxdkyuacjalunfrl:
⇥
⇥
⇥
⇤
⇤
⇥
⇥
⇥
bnbhkiovtarawfyaxqr:
⇤
gnsrmnikzjaoxypvoxy:
ivupnonwupygzacmxra:
⇤
kgawguryrnytgklfaoe:
⇤
krqknzrfdpjogwyzoan:
⇤
⇥
ynevndgadkgyjhwrzgt:
⇥
⇥
rnoxycwqaydsamkjdra:
tfryjnnyrkwxhssfhua:
⇥
⇥
rqzdyylvwantutymqdm:
⇤
⇥
⇤
aasysaaggurapnkcjhd:
⇥
⇥
emuensyrbqyamrixakr:
ilndyofacrtzvrybusd:
adkmuakcnwprvgeymff:
⇥
⇤
⇤
neuhwjvialftrcgpiiy:
⇤
yotrilozccnurqnafwb:
⇤
snhlyiokrarzozmgewm:
vjironmasyvystrzlan:
⇤
radnrsxwsiyuwukoise:
⇤
nnvarufesdvgaanyclf:
⇥
nahvshgtwmtfshzyrgy:
⇤
⇤
jerpnyauoqalbsbpsiq:
vavpyenygtrymeoxjaf:
⇤
⇤
⇥
lrsynahbseacexrrutr:
⇥
⇤
ehlafejxkyrfjnrhday:
⇥
⇤
⇤
qqrgrmcojyaogwfnant:
⇥
⇥
nwbvgpypuwujsadprwj:
⇤
⇤
⇤
⇤
⇥
⇤
kapojsaiynawnzxxrca:
⇤
wpyorzmbweuayxnkytm:
sgairjjhgyzdywknhyz:
⇤
ynwanwrorjkutzbfhjh:
⇥
⇤
bebaygknezyzntrdoso:
szajkzqrzsaynnxeifu:
huxgudhmgypaxoonenr:
⇤
⇤
⇤
anwtrdoepdstrmnsysv:
⇤
ydrofvqaanxqfaycbha:
⇥
⇤
⇥
bmetrwrnntfmaasyduw:
⇤
⇤
⇤
oykuovlramxiznenxlc:
⇥
⇤
lprpjhlpilrjgyafbwn:
⇤
⇤
⇥
⇤
for.0.end:
⇥
⇤
⇥
mzntysfldragytqvnyo:
vmxwnafhbyuuhprormj:
uxlrwtwqylnruvonxaq:
hlcnmhsaolproryppnj:
⇤
rudiispbzwgnsofanys:
⇥
j npbwlhhourwadtmffya
arynwqipoiwmursxbix:
j darnrdvrnwgyjqwijjn
npbwlhhourwadtmffya:
⇥
⇤
ukjxbpzvznauwyrgvcl:
eqospsabgdmrjuxdyvn:
zvaqnswklljfunvjryl:
⇤
oiyabqodyramdnsqswb:
vhgnrucnanrnoyykncj:
⇤
⇤
qaaayijlotgsnrnxmdl:
zvlqvrywxkqitedakzn:
⇥
eextyyaswnnjhpaaerp:
olgpbonkeeyvewaaras:
⇥
⇤
qbzylyziwxnarvkrikc:
⇥
nxxhuqlrcfssnkytwda:
⇤
⇥
⇤
⇥
jmakmxjccwrgyrixynm:
lz   $s0
⇥
⇤
⇤
⇤
⇤
fycguzngcnczionjrab:
hnfusabrjdmrgmuyxya:
zgnyowanymywbwwgkfr:
⇤
⇤
qapraialxdbecesykin:
bayhgckbramgiubnihu:
iyykyquzymvalwnrnui:
⇤
⇥
⇤
⇤
afdtohzwwnyytunjxbr:
⇥
⇤
tizygrspfkufelnckai:
vxnitfsarospyxdnpyh:
⇥
rjuasnrpjyxhnttzcha:
⇥
⇥
eraqbhnerdyvizjxryy:
⇤
⇤
⇤
hddnffrajpdmydiazun:
auniactmyrnpeiygqhd:
nwyrlviamhtkzvvnonz:
⇤
⇤
zyyzpkjpbarrzwbepbn:
⇥
⇤
⇤
ynthxdhvyrijupfiyab:
⇥
⇤
⇤
⇥
rnmmdybbdrvgnbuaykj:
⇤
⇥
⇥
boxaaceyrtviztqpqun:
rwyqnvbuupnslqzasyi:
badskyhvnzwmybarjiy:
dkobzavynjaebwwlgsr:
⇥
⇤
yzyjnnoaxpyumcfuhrb:
⇤
⇤
⇤
⇥
xrnnawykaxjdzyonurw:
⇤
j buwroyqrkuypaajnkxv
⇥
caodrwjgyvxazlyonuu:
j lsduxnpryxaallqirdp
buwroyqrkuypaajnkxv:
⇤
⇥
tksgfvrnicenakvycvi:
⇥
⇤
vargnygbjsvdodvhjhx:
⇤
⇥
aopmyqacrnubxxdlrrt:
akuwnkmiggqbnyvdurb:
tudadrrnhsrrypakasb:
hdmzkhkgydpnrzblpav:
⇤
⇥
⇤
⇤
⇥
⇤
⇤
⇤
⇥
⇥
⇥
⇥
qbbndamdcrqrsuxyxjl:
⇤
aqcrynkvnzntuqtqgzt:
pcothssmkwnalrbykyt:
⇥
dprnnwzsozwwngumyaf:
eudrhkzwaowmtninyvm:
⇥
ynoaimddrerflnngwtb:
⇤
⇥
qdjrttkyyvagzaardnd:
⇤
⇤
⇥
⇤
⇥
⇤
⇥
⇤
⇤
⇤
tacngyquyrtuezfthyb:
⇤
⇥
⇤
agywallofnnruhjrvbn:
⇥
vamsnlyfnamkfqorrjr:
⇥
⇥
qczrnoawmrwzzqpywjy:
⇥
⇤
⇤
⇤
smbmdburvynyuanfspm:
⇤
unwdgjypnxmhroyqwax:
yktntmrayoabjdhxakt:
wrznqysekvoancoilrg:
⇥
rkjnfgrvtdosryngfda:
⇥
⇤
⇤
j xlyynldcuusayrfthtx
wsiyldnyravrcobwfrx:
j venvpdvhlarqnwyzvgo
⇥
xlyynldcuusayrfthtx:
prqfrlgnawnjoyzxjgj:
pjqrsqncpavvgicygzb:
⇤
tnvqarylakydihsijrd:
⇥
⇤
⇤
czmvgkylwwrwpanafyn:
⇤
xdaxpunbjzrrytjqmph:
⇤
golryxuxfembaljnxzh:
fldfscgcnaodvhbwrpy:
hwwatcwlpylraminanv:
⇤
⇤
⇤
qasuarludpigacyniia:
mzvpdunrsxpijsaavty:
⇤
rbzsnujylfqzapsyjyr:
⇤
⇥
⇥
marnmigypyreloqsbxh:
⇥
ncqqxflruiqifgygmak:
srvnvnaglycxprzixoe:
⇥
⇥
kfrtuzbfkcbsbfyknwa:
⇤
njmasjvfgvjrcbweyrc:
⇥
⇤
⇤
nledaovrpnylhzckemn:
⇥
⇤
⇥
⇥
⇤
⇤
hvayaogloytvbnnrevi:
zogfvzgvranoboaexyu:
diaakjdpnnqjyrscayn:
⇤
ucynhmrkfiupibhkyna:
lhaynrpfatotfnrmufd:
thjndgjlmrnpyaogwrt:
⇥
⇤
fanyrarnhlzetpiibwc:
j waxvbsozrdranriybgk
⇥
⇤
⇥
⇤
⇤
dgbturvyynevgiojcay:
⇤
j mhvnpvgxnynoxwarrkb
⇤
waxvbsozrdranriybgk:
⇤
⇥
niyjejafyhcdhyrgnjv:
addi $s3 $a2 -1
⇥
nystispknxeadqdrykf:
⇥
⇤
urpgwkraayygssdenei:
⇤
⇤
yaxmdqcrylmtnaniybf:
aibaaztiryoyrnqabcn:
⇤
⇥
onzzghvzvbartanozyr:
byakmtnlnsrstlugkly:
vzlysqjsnbmrqamkfdq:
⇤
⇤
bbaqnybsijncajhrlai:
⇥
⇥
⇤
⇤
⇤
qfztmrmyubualnxfwxa:
⇤
nbaurcfsofwcappriyq:
⇤
epqcrabhmuatqsnyxrq:
⇥
⇤
⇤
⇤
⇥
⇥
⇥
vxydweyrhbsdxvtrant:
⇤
⇥
kjncyrdrgtibnutnanj:
azjybrusvuywngucuzi:
⇥
wyrnirtcsuodrymatfd:
⇥
⇤
igybigporyesmnakenb:
⇥
⇥
⇥
tlymyaminzaffcrymon:
kapdijbmwsryipunrcz:
⇥
⇥
j umhuwrmavyonqjobjak
dzpcknzthryvacotvvc:
⇤
kjxokefjqniqauyslrv:
j wsiyldnyravrcobwfrx
umhuwrmavyonqjobjak:
⇤
nwiamiaobbzwujqoyrb:
⇤
⇤
⇤
⇥
⇥
gariyzxgzruagndfnuu:
⇤
orvxkkdrnuybxtmbnap:
⇥
⇥
⇤
⇤
xhjckpzcbryyganbrfj:
⇤
⇤
⇥
ywxlumndlgixagjxrpj:
rxyxtmakpngfnjdopjh:
⇥
⇤
⇥
⇥
nrxnarkyupqfbymacfe:
⇤
⇥
zurmaqnyxvzqacjhnpu:
⇥
⇥
⇥
⇤
⇤
⇥
pnfterayxqfilrrnoxa:
cuffanezriaaagjkbyx:
⇤
mul  $s4 $a1 $a2
⇤
mototykhiaxphyntmrg:
⇥
⇥
ynyoynihiqbnhcarofm:
jtzcayazycijradnafw:
awidncciwdadvdgjyfr:
⇤
⇤
⇤
⇥
⇤
vhkbyfijvqrytanfwqh:
⇥
⇥
apynrvjikorhfsryhnw:
⇤
ufiwlwraemfylbnaqgm:
⇤
⇤
⇤
shudsynruvjblaxmuma:
⇤
⇤
lpjprdsoynyczbqnbna:
⇤
nvkdywfriyhtvaimgyp:
⇥
⇤
⇥
⇤
mxymilnlvnygbfmrgav:
ztdxxxmbcraddoynuqe:
⇥
⇤
⇤
aacllholabnyakvlorb:
⇤
⇥
j kbnayrdcslgnrynusfu
ymahvypnkexoezdrwwu:
j tinrafcypelrhdwhqot
kbnayrdcslgnrynusfu:
⇥
ahgdabldnyvbetrrxcq:
⇤
⇥
zjnrzcsueaaybahbtqo:
asmpmvjgznlubidrmyy:
⇤
⇤
⇤
⇥
njvuiakvryfurjkzykc:
⇥
⇤
⇥
⇥
⇥
nktbhtyrpmixcyfstea:
⇤
⇤
⇤
kriqqaipiuyaqnakwja:
⇥
yyxxxnokqkfmkaenarn:
l1   $s5
rdzhmjyeawnlmqzrmyj:
⇤
roypqxidmqamlnvmgch:
⇥
⇤
⇤
qsosnkmryaorbeirrdk:
mjamubwnerararuuyvb:
nqysvfuxmjggazjiner:
⇥
⇥
⇤
⇤
xuuudyyrsnrapbzjhby:
⇤
xbeurwtransazywtswu:
⇤
⇤
nteuciyjxnagawmrbrr:
irpiogngijbrxjyaygz:
sgbbrwnyqmxyecpawcn:
⇤
⇤
⇥
⇤
loop:
⇥
⇤
yckrynzzvqmoprohuda:
⇤
jjnorofkqktazkuazay:
⇤
lffaaeiacnydpnyquzr:
⇤
⇥
⇤
duvmpkriyyarnfpazvl:
⇤
⇤
fabhpenrdxyaazvifzd:
⇥
⇤
⇤
dayauvsryuunrulrsvj:
⇤
⇤
mvwkfyynbrqlardlvau:
kknhdvadpuhawztryel:
adrnqinhlhrfrxsmoyj:
⇥
smudzbrwdamltcypnmx:
⇥
⇤
unavdfdazyryojkogza:
xyfnqsvgvrudgfyqaiq:
nnpbrkbvthbiuykheav:
druihvyfridnrjwaonw:
⇥
uvrntedtyjgktgjpaxd:
⇤
oajprykblynpvxleecr:
mybadqnsrgfeofdacdl:
⇥
⇤
pxvnraobrkbnxmzcwyo:
⇤
⇤
⇤
honuiygxarttmdarzqr:
asjwfzhzibitmprmwyn:
⇤
⇤
⇥
⇤
⇥
nnsraiimnrqdcoxrzgy:
⇥
⇤
⇥
⇥
⇤
⇤
j vwrecacyyfwfdnsvdrr
⇥
rophydgknthrktlulha:
j rumfrytaovuafgynxfv
vwrecacyyfwfdnsvdrr:
⇥
nrkvahnmmywdsgganzh:
gnleegkychehryaefdh:
rdqynygnylacnnbnfro:
⇤
⇤
mnaduvjndwsxvarbyvy:
bxyfnokaqrpryykuxlj:
⇥
⇥
elumnroaxjqnyeaakgj:
⇤
kliaoitxrehqvwdfnym:
znaahlxqduqroxdazgy:
hclnyhahftnvfsrdzkl:
⇥
⇤
⇤
⇤
ndcyajuatqhiiugmrue:
⇥
nmfjanbyaimqtsmrsro:
⇤
⇥
roldyclnikuahwmvakk:
zyyiawlporsrwmyncfi:
cciyplorfqmiasnoxhl:
⇤
edbinllnqkvhqdxreay:
⇤
⇤
yhnueyrpnqdrwojraxr:
⇤
⇥
obpybaxfgxpuiabrnxn:
⇥
⇤
ehrnydaygzjjrjynewl:
⇥
⇥
wfpfbrnwawuvrpnovay:
⇤
⇥
deyrufnbgytjznwjuax:
tkhndwgoypchrawcldk:
⇤
actprmwfmopwcnyqazu:
⇤
ezyfrnlehhecanrbwag:
amywrchnfyxsehxvurd:
⇥
rsntuapgyvatpasrkar:
⇥
yqmgwzyaqjrlefxnyek:
⇥
nktoxikryabnvhynlck:
rlvpvdfzanpmzdqzany:
xysdhyengnxfzurdaqu:
⇤
hqrhljdiasiirunwyiv:
⇤
⇤
⇤
cznpawlrdcrymakokeg:
⇤
⇥
uahfsetgnjcywmxhrtj:
zkwsarktajhidmqyunm:
⇤
⇤
⇤
⇤
⇥
⇥
⇥
eriaatbnjkshxyykrrm:
⇥
⇥
⇥
ybaniykbybcrgnyifha:
⇤
⇤
⇤
wbfleachuqrbgiokayn:
smzmfbryorxnkjpkqaa:
⇤
⇥
uuouuyciwshltrcwtan:
⇥
⇥
⇤
⇤
⇥
lhalurjrtmsjqdnelay:
tehduhisalyfpzerhun:
dauyxymdyjrrabuushn:
zqsqwyknaeeoqzwmrnv:
⇤
anxqpynrxwkdywcndce:
⇥
ylhgaznrdktxfkakrwn:
j ayenuarlnufrtywxvcd
⇥
nctzrmtyszmkzacrsna:
j xtrlqgjrqynpeuglena
⇥
⇤
⇤
⇤
ayenuarlnufrtywxvcd:
rnnkuthyxwouatoigaa:
j esaazryzpodaenykkhn
jlpjerafjyfpptncxhh:
j dsnngplyadarqyryzpu
esaazryzpodaenykkhn:
⇤
⇤
rnbtahxyoztnzzdfjop:
⇥
⇤
⇤
rumvbvjneufyajunsgt:
vpurnbzaxrbynngtqab:
zpnqjwwrhasuqizlexy:
⇥
vbpyjfkinbryaapykfo:
⇤
hxgpydyipaakggrnzot:
uazzknabrsvwnuykmka:
xfyclxcyafezpbnjrxa:
⇥
⇤
⇤
ayyodptrikaknmmnccj:
⇥
⇤
⇤
⇤
⇥
⇥
⇤
⇤
⇤
⇤
⇤
⇤
⇤
⇥
⇥
⇥
⇤
⇥
hbnofzyasutajpuramm:
wwyluqjarelnzijmymz:
⇥
iuvonhrglpzgeyakoda:
⇤
⇥
⇥
⇤
⇥
⇤
⇥
ahyxmpdnvdcslaprwat:
⇤
⇥
yxyuwyznirjaurgtlzz:
hcavkinrhyojngztbtv:
⇤
⇥
⇤
⇤
⇥
⇥
aadgpfrtvqygvmanixa:
⇥
⇥
⇥
⇥
voqasyndnntynttergl:
⇤
⇤
tkpsavhrygbbmnkthuo:
⇥
ilauxeyxyetracnyexi:
j miqwcztgynblaerreit
⇥
⇤
⇤
⇤
xqkpsdaanrlqsudyyfm:
fnwplbrfuanbnyauujr:
⇤
⇤
⇥
⇥
fqbzikqrxqqynaxaakb:
vemikrsassyjmslnhxi:
lanizvqzhrlqhxwzzyg:
⇤
njyriqpapfgalpwrxgx:
gbmaguyzcyaqnohvzri:
⇤
⇥
⇤
⇥
j mjulbnhbjgjsramayto
⇥
⇥
⇥
qcbzzrahnrtrhpunxky:
⇤
⇥
⇤
⇤
bphramzktyeshnwdvpw:
⇥
nvyzuzayizanrgwyrzf:
uhmyylnxqsazrylctiy:
⇤
yxzkaxbovwzpnjwajdr:
fazxxzmvfymrfjnytal:
rbqlxbgylannmarbydp:
axwprislvohysqlskqn:
⇤
ytlnozxsfjnajbdbraa:
⇤
ayawfnhbbwsllgrppfj:
⇥
tpyzrnyrantxcwareax:
⇤
⇥
⇤
⇥
⇥
⇤
⇥
⇥
⇥
⇤
miqwcztgynblaerreit:
⇤
murylnqrlunttcvqkab:
zrrapmdytoynwieyknl:
⇥
⇤
⇤
⇤
⇤
⇥
mul2 $s1 $s0
arkrxyfrpqahanxhryv:
dijyjwdrbnebnpkagua:
ytudakdssdbudpxnrsc:
ayrrxrrhxtzinnsaeyn:
⇤
⇤
xpncvvqesvrbnzwiazy:
⇥
nqeamurnyatziwyjwrb:
⇥
tnwrmaonpyufcnnwrve:
⇤
⇤
⇥
nvzrdhmdyenxvajiruz:
dpiangezfiwalrncvyo:
⇥
⇤
⇤
⇤
⇤
mlqryucdsqyualjvjan:
tgrdzllnuxyreaiymol:
⇤
⇤
j jqcxnahyozyecsrpfcd
vftdsaysrnyvaxtgqij:
xtrlqgjrqynpeuglena:
rirvvrninnykusaolcd:
drchbdaurwennynajiv:
vxonaccjywvtlrnpkoa:
j pncnpxgrybpxnzraxnc
⇤
⇥
⇥
yqglffbtuayrwnncpey:
mrisiaboybspyhinona:
jqcxnahyozyecsrpfcd:
⇥
⇤
⇤
⇥
lnoxuiyjduanrnehuic:
tyrmrxynameymjpqrzp:
⇤
⇤
⇥
⇥
⇤
⇤
⇥
wrsczmrrdlgahyuanjl:
aeumrgznoqwtzoewymh:
veamniagkgrnyfbydrn:
⇥
⇥
⇥
⇤
⇥
⇤
⇤
mkenlfesekanrvewydc:
gtpnqrycfolrmasqrad:
⇤
ucepxfagyrqvlmmgrng:
⇤
⇤
⇥
⇤
⇤
⇤
⇤
aylcqvvyyhfenbrkdfp:
akpaumsfntbyrpfpovd:
⇤
⇥
⇥
fylffnfrixoctdsfsan:
xkurtarpiazqxctnngy:
⇥
⇥
⇤
gkhnrkdtqaiylbypyqn:
kkqyqzulgrxvplaznxq:
⇤
xcdllbynbnrpsdnwzda:
yaznrhwrvjrzsxhqnrk:
dopnyupetvfawtosfqr:
fbzquoayisfvunxdwgr:
qikhaicnlrbvarohnly:
mnfmhvtryyoffpgytxa:
sguvrubaxywnrkeggkd:
erqupyyefwnxnwvsaro:
mfryntmqzoayopfpbdy:
vynrtpjqprclvagsvgr:
j aipgyferlruenylovyg
⇤
noccnxqvfkqabrblaly:
dnayzknlbdobrhdtstv:
j ierbyrwcaheflkeayan
aipgyferlruenylovyg:
add  $s1 $a0 $s1
⇥
⇥
⇥
lh   $s6 ($s1)
ranshozbdizfebuhymt:
⇥
⇤
pyvizrjdneyuzoehatm:
⇥
⇤
⇤
⇤
⇥
⇤
⇤
⇤
⇥
⇥
⇤
hucarmkonnntlpxkvay:
⇥
j yvuerxhfrqyrgnaecsn
⇥
emdrkpktwhaalnybkqc:
gdybaezsfjgaunpryvr:
⇥
axypbfwftrtyjnysehu:
⇤
⇥
iaonrpoocylbcxpmbae:
⇤
miyxmjcrqotxaknmytg:
⇤
gynkqalrxtererdirfc:
ofrmrfnyrfyaqdcrnqe:
j bimvrgvwfxnyirfsdga
⇥
yhuqnfglxnvwrbawwhu:
cankdycxfmsycsbudrl:
⇤
⇥
yvuerxhfrqyrgnaecsn:
ylqrwygaaadaoeenowh:
⇤
cuiitiylcnrbgonzkna:
zgxkalbyryhprbthmne:
⇥
⇥
⇤
⇥
⇤
⇤
⇤
⇥
nnllwgygfdtzosoaera:
⇤
ppqeznbufaypyukmran:
⇤
⇤
azyfbglyznapuufjrvd:
⇤
nyykhnnbyprasbhaiys:
⇤
nsktstvgramlyllrtbm:
⇤
⇥
⇤
veqaakzonbrjubqpyvp:
⇥
bblarrjcnqntayvcndt:
j juykasseadnarzgrefe
gamltynchrqgkyhrsuu:
⇥
j esekngtmeqkgyiadvre
⇤
⇤
yinalxnegazutnrwyna:
⇤
⇤
⇤
⇥
brtdujaadmnpyaefgyr:
⇤
⇥
⇥
juykasseadnarzgrefe:
⇤
⇤
aornjhxuslzyxbznvir:
aeflsdibcrulnecypqk:
⇥
rzsydgwrnnvsaxblwgq:
⇥
gwnimbbpsvrawyzvhar:
⇥
⇤
zrfururnvgywatjqnhu:
⇤
byanufrduopskivcnvx:
⇤
⇤
⇤
⇥
⇤
⇤
dtyzrmarfxmonwfzeta:
⇤
lnjyceaeamrghkmrbya:
⇤
⇤
⇤
qzzjaexucalzlvrdnyt:
⇥
⇥
hpypkmjddngdrixbkza:
⇤
ravxjuhrvouoqquynoh:
gvwderbmnyaatadqvrt:
⇤
⇤
vefyxnpyahbatrzwsrs:
⇤
hrmvsbdwrhjzypndanc:
oiygybaaycrlwaygner:
xhoeywkyraxzpwsyjqn:
⇥
⇤
⇥
raludimdhndtisirsqy:
olmsvjrnyarcgygqvbn:
kmbswzwvlyygpajnnro:
lntotoduygemngagpmr:
⇥
arhcqcrnmfrigsxwyhp:
⇤
⇤
xragtiyntibgnxugxqy:
⇤
⇥
nuyyeatntinrmyappjh:
⇤
⇥
atgjomxntycqwrstrpx:
⇥
bkpnhiraweviryepqtr:
⇥
yasreojuzdbjiacnkbu:
⇤
⇥
⇥
⇤
⇤
⇤
xcynndrsesaoqvkarxn:
⇤
⇥
⇤
⇥
yogdsyqjpypynnrhxda:
qchunoijwynraktiuzh:
⇤
⇤
⇤
rakgnsuvtchtdyrcczh:
⇤
ftrnydwypyemnlnadar:
⇤
⇥
rakvngzdolkyojjqhhf:
⇥
⇤
⇤
⇤
mmspyjdbbinafvtroau:
⇤
bskdninpzyfqaluxtrq:
ygxnaiyrciqzfbklwrd:
⇤
⇤
⇤
⇥
⇤
puxvohcifhfcwnfaydr:
nrlsnnapvdefxswfiyu:
⇥
fyseujrdjaaarkitinr:
⇤
⇥
arryvdylanfuyibhsxo:
⇥
⇤
⇤
⇤
⇤
yvsjgmnzjkresyxspab:
⇥
vvywhaznaayodsrjvke:
aysvayntburdnwcnhyr:
naznxfmtbjadriyylnj:
⇥
irymtncggdnnaxvdxmq:
⇤
⇤
yzaktnvvqydquyyqrng:
ilsytajxjixrntdfrrg:
ncljskwrynyslyaawwb:
⇥
⇤
⇤
⇤
urvwpvwnxrktknaaryw:
⇥
⇥
puvuorocyxjgxgcznfa:
⇤
⇥
⇤
⇤
⇤
⇤
⇥
⇤
⇥
mmyxytjjzaxyrysvncp:
⇥
⇥
⇥
rkpkyaayjnxnvjbnlzq:
⇥
lfgruujryraynykzmfy:
pycroamzowksspdxnou:
⇤
⇥
yxnrasutmroogyjklwe:
jzzscnlqkxargzerlpy:
⇤
⇥
agefovlajnxfrqrybgn:
byjnabpoqxuzrgtozrg:
⇤
⇥
⇥
xzyaxnfpiwpposnqrio:
⇤
⇥
⇤
gdyxnjvonnynavripbs:
⇤
grcatbsniyenrpzadfq:
⇤
⇤
⇤
rqxfgnpxxgtzysasfyy:
⇥
pe   $s0 $a2
ofrjalvzpolynfkbnhw:
ynmvdldnwaiklvqorzd:
⇤
⇤
⇤
⇤
⇥
dpfanimhnwraecaryyn:
⇥
wtrgfyzpclacoyfpznq:
⇥
⇤
⇥
nyarjzifgozvwvdiilr:
⇥
⇥
⇥
bge $s0 $s4 else.2
⇤
axnnarkcszrzfxphyie:
awqlqeavsynvmafrifl:
⇤
ckugptcwjgoarlymona:
⇤
⇤
⇤
⇥
jzrrejfahrcsoxuyneo:
⇤
⇥
⇤
⇤
⇥
rqqjnahielwnoatowiy:
rrsjneayezdtxcnenio:
xiqnrmybxblranwojlp:
yjakusmiaikmrimnade:
⇥
⇥
⇥
⇤
⇤
⇤
hmcuacmnjhoawebyinr:
nozvpayozrfkwyxpyzl:
hgaalddlwtrcnsuoryy:
⇤
⇤
⇥
serbnodysuantmajbqv:
⇥
⇤
osabsmcnyrxgoakgwpj:
⇤
⇤
frahdfyayatqsctexnr:
⇤
rlvhryyawdfylhoymnn:
qeancwmoztzqyeiozrp:
⇥
flckrjlsrjnkalytxbc:
⇥
⇤
⇤
⇤
⇥
⇤
meirovhlqarbqogfkny:
cnagxlhrzyyumddrzbp:
⇥
⇥
⇥
⇥
⇥
nhairiyxnyzybtcezhf:
fnyvgrnutnhiabxisdm:
⇥
cavrqetnvyarzmjrlnu:
⇤
⇤
rycmmlbpjoydeadlahn:
⇤
⇤
⇤
⇤
⇥
rmnmgazayyixmcutwrn:
⇤
⇥
⇥
xfhcivdceprknynaqjr:
⇥
⇤
darymfrdnjucanopqxb:
ramhcryvfrqwnqhaokl:
⇤
⇥
⇤
nypypjaiqorupgunzkk:
obyssziddknoctardde:
riwkfyaupnozmlqajgg:
ndrsxalgrgakapyobzd:
⇤
jvzaglejajyurndtssk:
⇥
wcnlbumcawkuspiywry:
⇤
⇥
⇤
bvpmvflbuoauxnrgcyy:
⇤
nyzfhyrjdcnrgtpzart:
⇥
znmybndnroewwyaynfw:
⇥
oayipqhhekrztxenhcr:
⇤
pardhogljxaoygnrahy:
⇥
ixhwbpnaahrylwztzym:
eesamrlunwywmgwfnle:
⇤
ciarpydeanyfzmbrsoc:
nrcbrjgjykfztdpnfna:
j eumekhnzgyzcnjvbyar
vngzsarruwzzpcbgyyk:
xaagorrryccdijyvjne:
j sfnrzuzdwklxyqnwina
yophzrugfualiugntob:
⇥
⇤
⇥
⇤
⇥
⇤
⇥
⇤
eumekhnzgyzcnjvbyar:
⇥
anbyraqnlahjvydsghh:
⇥
rbaxlacjsmvnmgyfrfd:
⇤
njxqwebnnzqkysahkrr:
⇤
ctryxvbyafyvzexynrz:
pnybnyrtuaahyovqwkb:
yjpignarixvwywzonjt:
⇤
ljlhkzngrrakwymzduo:
ztnlqhtyxafngoeyvrw:
⇤
mdjymcgusfkarrnhzrs:
⇤
xaswstvraycvunqkflf:
⇥
elmynfawgrxdnfnceft:
wydpfrgtadjtwnanolr:
⇥
⇥
j kawnvtrresiamtlytta
⇥
esnmzaajgcwnrypcako:
⇥
j lbyrsdaqaonxbyfyipc
⇤
⇤
⇤
kawnvtrresiamtlytta:
⇥
⇥
yloslyazelrqqnmfaji:
⇤
bnaqhzlyokqexhrfsew:
qnkvrhxmydqyagwkzqj:
⇥
⇥
⇤
⇥
⇤
⇥
nyigamwfgcvrkmoaukz:
⇤
⇤
ahyvhrbhafjlgrrrrnb:
⇤
⇤
bqqhvagncntreowzyea:
opfealruvlotddnnuya:
⇤
⇤
⇥
njmyrndhagbrmisazyo:
⇤
⇤
⇥
⇤
eywqagldxldkribrifn:
⇤
⇤
⇥
⇥
biczvtomnfxenritayd:
dugamenrxmqjljdjays:
hwafojnoisgyrptjepp:
⇥
⇤
ehssfdrakmsbyfffnqr:
⇤
⇥
⇤
neanrzhedvrylhwahya:
⇥
⇤
xdgebdwtnadmyrfrhrk:
kracnawvyupgvjrcvyi:
⇥
⇤
ayfqdimrakrwcrgthtn:
⇤
⇤
⇤
⇤
⇤
zhnmrcapcpahvkheymw:
decrsfbrwygyxnccazo:
zagnwbwsyfaitfriyoa:
⇥
rnfaincoaxysetopfne:
msfspaxruarmnxdricy:
psdmijraywwbyqyntgo:
⇤
xlrdloeqyjaoerhznra:
nxctlknnacharhkeydp:
⇤
atjbserwhpetaunycfq:
⇤
⇤
⇥
⇤
⇥
⇤
⇤
arjajnwccsfayrlfsxb:
ykenxntyrvaveewvrin:
⇥
⇤
nzerzjnalnwjpxylndt:
hekwdnyojbpirnalrhf:
⇤
⇥
⇥
⇤
awwaypnrzjokpgawtoy:
⇤
⇤
ojausynxbonpzyogvrg:
⇤
⇥
⇤
⇤
⇤
⇤
⇥
nlurqfysaizksahifcj:
⇤
⇥
rzngwrryajwanyicebg:
dfyprwansfdajkgccdy:
⇤
⇤
ftgtdnytkjpwedpakrz:
⇤
gxtxfhtrnklrbajytns:
lwqnjlzuovyrnfbilah:
njabdygxiygrbpftaja:
⇤
⇥
yarsvxrwxbyoebvhhnm:
⇤
⇤
⇥
⇥
cnkbroanbjmvnscpkay:
⇤
⇤
giurwrcyxddaqancbrw:
⇤
⇤
⇤
tqcrjqyidlnabiuyotq:
kjwaknlqafyrridnzwu:
⇤
⇥
⇤
ncbwwxyrahbneymbfnf:
⇥
wanrpjmrajexxvyyalc:
⇤
⇤
jtzfrynsnlxbwdyjaes:
⇥
zaawrodnzkmnyvsyjca:
⇥
⇤
⇥
⇤
⇤
axpqhrirypsnbsswrgi:
anrunfhtnynlfsefnfw:
⇤
⇥
deuoarujnczylntyern:
xgyvvnunkufgafanjer:
⇥
hjcndrqeaidjoqkqtym:
⇤
nrcrfoyfarunohpmwcg:
yvqylnlkdxnirraazia:
⇥
ywruhsnkixqiyosunca:
hplanjnvjayrrzukebk:
⇤
eneqrmuyatygqlmniju:
⇥
⇥
⇥
⇤
⇥
⇤
⇤
bdyzgymqoanohdmriil:
⇤
⇤
qhvijyskkuacnewoyru:
⇤
awrwganabyvwkanwnfj:
⇥
⇤
⇤
⇥
j yimlpaayanylrffydur
nplcagkkolicxynjblr:
j uwceirnecwyukhayufr
⇥
yimlpaayanylrffydur:
⇥
⇤
⇥
⇤
⇤
hiymxnavcqurlexuxjm:
oatnrcrjzaeymamdpns:
⇤
mul2 $s1 $s0
⇤
⇤
⇥
⇤
⇤
⇥
⇥
⇤
fkvuerhkpkznnaynvkx:
mbexrwnyybwfdnfsawh:
⇤
⇥
lkppayxfprmeydlnrso:
azczvsodkrgadvyvxnk:
⇥
orgljykrnuajylrtwzy:
⇤
⇤
⇥
⇥
ztonnfsclgclacyryyb:
⇤
⇥
⇤
rarbqypxtenywflmzfu:
ydaeeunnurehdayrrwh:
⇥
⇤
ucrnjmyxalwtlsothpq:
⇥
lwyelrvsmvdanrmrfls:
⇥
⇤
crngzuoayatcsprjiok:
⇤
trqfrnrjgqjmamxylat:
⇥
kfjlcwafaulsrlenynk:
⇥
ayigvsiygrcduntrhir:
clknakwemakjhcbrzys:
j mungsfoobeayncavrgk
nnwpptkornlsyadovgo:
j dgygrjudyrnayvraaru
mungsfoobeayncavrgk:
⇤
tdtrxpwadrtanjojumy:
⇤
⇥
⇤
hlbbpdllorknybrnawd:
⇤
⇤
⇥
⇤
oavyrqnabjkrmnpvxxe:
⇥
⇥
⇤
yfwysltmwnyaybnotri:
⇥
⇤
ruonytapptyhfsrozsr:
lqnkiynrxywuhebayub:
⇥
⇥
arzxwwirfdvcynonyap:
⇤
⇥
⇥
⇥
⇤
⇥
⇥
qwpayqmwlntrtcwcgnb:
⇥
⇤
j ranqmepnaxgtaxrvyrl
⇥
jyzpiyoarunnwanezqs:
j dnayzknlbdobrhdtstv
ranqmepnaxgtaxrvyrl:
⇥
⇤
⇤
koqjgncaryeigmmenog:
jpqyovtrvajmxhanavn:
⇤
⇥
⇤
⇤
⇤
rnzswnopapaezxygahs:
ysjxgharwqgyhafnjvn:
rsebsnrsawyyrgcnfva:
xfthdnerbrzrsuaayzo:
eudzyrggnnvayagjvqw:
⇥
⇤
eeygsctikcxyahnrflc:
⇥
⇤
⇤
agcrwolpqmnyyubhrdn:
⇤
⇤
arjyhuodskowusjnwmm:
⇤
⇤
⇤
⇤
⇤
yrvvwawfvmwywavyunx:
⇤
⇥
⇤
⇤
⇥
⇤
⇥
⇤
pranvyejywmdyqtucnz:
knxfnyckrjzodwqunpa:
add  $s1 $a0 $s1
⇤
sdndgalxyrapyxvlzii:
ylvjjgawsnabrylyakm:
⇤
fykyrkbxfzdovlalabn:
⇤
⇤
⇥
⇥
⇥
ysygenacxjchryagcrd:
cynarwcbhlrsqwrwftk:
⇤
jynlofyeofivanrkkrt:
⇥
⇥
⇤
⇤
bnrnkyhozlpusakljyd:
⇤
gxeayniveturxcwvzfd:
⇥
zkadykrpoqrjyvoztnb:
⇥
⇤
⇥
⇥
⇤
frgaojwzsznypucbkgg:
⇤
frauobzbunwpvblhnyr:
pruwxanmjxtlnyrhgxq:
⇤
byybnoakyegtnfrzgos:
⇥
⇤
lzynaxasubppadypryu:
⇥
⇤
⇥
⇤
⇤
⇤
⇥
admvrwkwybpbncwvsmw:
fxacxbchzhmvexbjrny:
⇤
⇤
⇥
⇤
⇤
⇤
⇥
⇤
⇤
ntpafhpwdjdryampvja:
⇤
gwpkzkknvywnjmhazrp:
yypbiayanfkoeraejve:
⇤
⇥
⇤
dauycnfsracioicfxcj:
⇤
⇥
⇥
yupaklptpdniojryopw:
⇥
⇥
rafyngkfmnnxgwmhatf:
mtadnacgryrwbqemexq:
yjznodvfarxoagditou:
⇤
⇥
⇤
ualrnnuhdyaxzirnxzh:
⇤
nrzylsmhciwacfaacdy:
qxspnzaiyiramangwgz:
⇥
cmvifyyrgnadsristta:
cbhyanytaxhrozzcffr:
unrxiyhjgydeandoaxr:
xanpjxahjkffypqknwr:
zcyrnwqblnyhwyrrraf:
gmcynpdrrqgsjksrarm:
⇤
⇥
bjjydranqassjqmkors:
⇤
⇤
⇥
⇤
⇤
nabvrpmdfrptqaypbhi:
⇤
rgyrzgamdpnumlnbrfh:
flrneavddeapzytrikp:
⇥
⇥
⇤
irrhgvryhvyygfypanh:
⇤
⇥
tdtmawybchlsehrpnyd:
⇤
zjzdyfjjoypqyarzfcn:
ziszrswvwaynafzasmr:
⇥
xnthjaxpwgjerkeznyb:
pmnratbuhzmjyyldpek:
⇤
⇤
⇤
j oacrtxlgymxdtvcncrj
wfvdrmzynfwafnisusf:
j egnzplnxxwyauotiitr
oacrtxlgymxdtvcncrj:
⇥
⇤
j jzxtryzfpeniixyvfwa
lrybnupugawxedzmrdd:
uyznbarbvxnwnydaotc:
nuayvomylmmhrpirkxw:
j nabalyyaudqatqczkro
jzxtryzfpeniixyvfwa:
owrvnsvboflywqfluah:
⇥
dgaaqdnnfrstyqbrfvt:
⇤
ayyizrzjniwctfuuqzr:
rnkminxgahrimrfyetj:
⇤
⇥
mivykyinrcfsvyaeffr:
j nhvlljvqpjyratuvykv
lbyrsdaqaonxbyfyipc:
⇥
j nnwpptkornlsyadovgo
⇤
bjuadyorfnyaizuyrte:
nhvlljvqpjyratuvykv:
⇤
rqefxcxunkrnyjkahgq:
anbcdlbyqaurqhyjzig:
⇤
⇥
nbwiyjykvaoywlqkaor:
wywhhkwsmvaerslrnci:
⇥
j nyfdpimnrreameaybcn
jsaayprtshcqdyvnrwx:
⇥
⇤
⇥
yrvybjcujanqncwvjrb:
⇤
⇤
⇤
fffrvhjdknbrzoyabgs:
⇥
⇤
⇤
yyaaznvynvtuqriybdg:
soyglpdnlhdaramatvb:
⇥
okviweyvrdahqcnnwwf:
j bnjbpiymntgoapehyre
xtznsfigyprjbaaspjn:
⇤
nyfdpimnrreameaybcn:
⇤
kfyodavjwonbzrwyrrr:
aujyqtepakjvanrsnht:
⇤
⇤
vzkrdaxtracrfzgywvn:
⇥
⇤
npfrcorlgavxinfayxi:
syznmayawtscqzcfrnu:
⇤
⇥
qosearxumpwhsnycdtx:
⇤
⇤
crywsyejzolrkbanmqc:
⇥
dztkoxysmifaechvrnj:
rppfokdcbpnnvyalpqs:
evxvrulnnkinyfyatnj:
⇥
apnjwiourdjndyfxwup:
nfbtrjrrkyugmqaanqd:
⇥
qxiqfrxmocvxaydwnic:
pngqflgnmokknajaayr:
⇤
⇤
qgeykmdnnorfvbgddau:
⇥
⇥
⇥
⇤
⇤
sqafqnujdtgyloyirrn:
⇥
⇥
⇥
⇤
⇥
⇤
⇤
assrtamugmdyrndltwr:
zgajaurbfomypcaldnd:
hrxytjccajnoxwquxat:
⇥
⇥
⇥
sgkdxreynyaleannmeo:
narbyjvgutnvllxnmtn:
⇥
vwmlsykwfarqyonbnou:
⇥
⇥
bntwnrhlzndhmlfywba:
nfafarsarxivrbvyipl:
⇥
⇥
⇤
facryxerkbgycyonndo:
⇤
⇤
orbkkkfwarjvdntqvyy:
⇤
⇤
peyrmclngqwahxrjomy:
⇥
⇤
⇤
⇤
gyznyabwpqvhavjayrr:
pvlybcbenmofyiirbxa:
⇥
⇥
⇤
yxqnnwyawrffdgmtckh:
⇥
drrhjkepiaiyhklngaq:
⇤
j ynvcjeumdnffkayrjfa
⇤
fmcroaozsrnwcpyjiif:
⇤
pmnrlrynprpwpallnas:
⇥
jbyzvhqvpfauqraxbtn:
j gamltynchrqgkyhrsuu
⇥
⇥
⇤
ynvcjeumdnffkayrjfa:
⇤
⇤
⇤
⇤
⇤
krnjarasnqehykhwmqf:
⇥
femnddadngnpsaynwrk:
pizeeropnyuaaonmecf:
fjanehjyqbcgrgxpruf:
⇤
⇥
⇥
⇤
⇤
⇤
tsljoaholrmnrberyah:
czrtofgaavrsxajyern:
⇤
cdpglrbjekjydpsuank:
inhsryraiaevkbbficp:
⇥
⇤
ngfotrzcslzkyqucmha:
xyennwcaekcgtnqruwd:
⇤
ozysnprjbfwlonoklaq:
fpgaanbedylrgahhhrj:
qanryupsafwvlidozfo:
⇤
j wcahykhnvqivlfrbyeh
fzruejapynkqamualso:
j leiyuolbrcanovhbbxy
⇤
wcahykhnvqivlfrbyeh:
⇥
⇥
⇥
⇤
bjnorgfusyckmmvadam:
xoyaeatlgdrrbeylzon:
⇥
⇥
⇤
psfhwrfvvousyyuwzna:
bntidhazlzgpbeyrfcg:
⇤
⇤
tikypqdvlacnrxdvgbo:
⇤
jqrnypnjrynzaytzotr:
⇤
⇤
⇥
⇥
rbjkzdnjvlyrsaqqhet:
bqrheeglxzbatcyonjz:
vyvnnufxrzraxobxfte:
⇤
kbsyrnytpeamwgnpywp:
apfuxulihjtayarzhni:
j ajuverspqlwayphndhx
apcajerinymohcnuwws:
j zysnhdrvchlglrjyjag
⇤
⇤
gahywinvwvakcralncb:
⇥
ajuverspqlwayphndhx:
xfsevasdryrjnuzfoen:
⇤
⇥
⇤
narvrlglqfyvxxvbhcc:
urczvnyvrayyzjldwqg:
wxyaanasdyehyebirtl:
⇤
nnlnrygbmvxmguruvaw:
⇤
⇤
nyatapdyfynrzoxrxxi:
⇤
⇤
nhzhawxortcayayrjly:
⇤
⇥
⇤
yqcarccsunzvpdpntts:
⇥
nhmaiokulcbcarstlyu:
⇤
⇤
yuanrrqytoeueagnpva:
⇤
⇤
raptunlyvwgdiozpesl:
⇥
⇥
⇥
⇥
wvmitamryzvbnuznndz:
⇤
⇤
ynreaeoakgoqwanyipl:
lcuxpaylryqrhkniwnd:
⇤
⇥
⇤
⇤
tahiylcobzyrlwynyqx:
fsymraljonlqmiarvst:
⇥
⇤
⇤
⇤
⇥
⇥
duogxxanyzshjknbrzw:
lh   $s7 ($s1)
⇤
⇥
⇥
j akrcooaajmnwyfqazcz
ernwvwagruaylrncnvk:
j apcajerinymohcnuwws
akrcooaajmnwyfqazcz:
⇤
⇥
⇥
bpaylyyugooprbrrcnn:
qkcxyvfrfzknwkamkcb:
⇥
⇤
⇤
⇥
⇥
⇥
ybnennaxwofnovccrwv:
hjnpcazwfyrjlpydsze:
⇤
iyrmakutcirtmmnralx:
⇤
rhneazhwyxgqcheocpk:
⇤
ynfzgnqhjhzferhatly:
doiqlnmadxyrpjxlmag:
⇤
tzcraeqtkagrkgnbyny:
urzqpuouyunntaaoszy:
xukoykmsrwuasbyuone:
psaarsclnhxqnikhvyw:
⇤
⇤
⇥
tjqkrghodcwdnafdsgy:
fhnuvparcohtmiywhyr:
⇤
ovlbtbejlurxnahydqu:
psasahojqogrpmrfysn:
axopiqrikbydncewkwl:
⇤
yrdwacuelsnldndpnfr:
kohaayjnwcaqfbrtkrx:
rgfdtymaniraztycdur:
cyxyzqvrxpxxcgnazag:
xpndscrdklmyihajbpt:
⇤
⇤
⇥
⇤
⇤
vaeoalsjwneuvrxawyr:
hcwvyzzrntdtkvnayed:
tpeoxynmayojrzfmjme:
scrrmyldigbnfahrduh:
⇤
naenqgaojvkdyslsrrj:
acnzrhikqlypfymbrxp:
uxruhosgbroynbbczaa:
⇤
haryuznnkicahueinwb:
⇤
⇤
⇤
⇤
⇥
j yzvtnblltnurnrmlmar
⇤
tfamrcdnvnoepnydyao:
j xaagorrryccdijyvjne
⇤
thqirsmdynmxgqxafsr:
⇤
yzvtnblltnurnrmlmar:
⇥
⇤
⇤
glasarynqsmscukarkb:
⇤
⇤
xinzparhgtirslxkeyc:
⇥
⇤
⇤
dbqzpuzyibcreozxzna:
⇤
j mtjoryodpablmfszznm
thrnrwedylvufnintan:
ptycpihzbfaplhngnrj:
ngsigejawytthsiymar:
cyinbxoocvsaksrqnnn:
⇤
j yagetyltvcagnrnslmr
edlnarscqjnagyrwohd:
aimsrlaaiaxutmnqlye:
lcvsvrssmoaskzaneyd:
ynjxujekaooofevyrpv:
⇥
⇥
⇤
⇥
⇤
mtjoryodpablmfszznm:
⇤
⇥
yyypwdnphqfrshaduqy:
ckjqjusnpanqmrdakyb:
nrqrcarvwlvumrzkmay:
aihpanetrzkjlyrykkx:
⇤
yxrzsqnjjhhatndzmah:
⇥
⇥
qrayolrjawhnyyprgdr:
zrwljohyrlvbaweanww:
izontbfvajrynjjdfih:
⇤
xwyseqbhefmyfnjjarw:
⇥
nmrtnvhgwajskhywbra:
qtzwbcynmdvysrglahi:
⇥
⇤
bne  $s6 $s7 else.2
⇤
aupyeejonxdavyznlir:
⇤
rwpnmateyynmdizylhp:
⇤
⇤
⇤
⇥
zxenaktnwrulsfqtnyc:
⇤
⇤
⇤
⇤
krmvxynfapyauorcglk:
nsaahhlykrkzusruznm:
⇤
⇥
⇥
ahbknedersayyropgou:
⇥
ntybuyrazpyrmargfdx:
⇤
⇥
⇥
⇤
osvrncgugzbynmruadx:
ozjdesqreppfhaitynp:
⇥
⇤
⇤
⇤
nlqylayclrzltzmlllg:
⇤
rhvdnxeqsfnaniblysw:
gpqdykxymwssqnazdrn:
⇤
fqdnmczbhmeljtnwyar:
⇥
srxhzweryjqufctnkah:
⇥
⇥
gftsnwgfuvyztadgraa:
⇤
nrryqsnssahnwhsdqyu:
yrwpndfupkzezkczakg:
⇤
⇥
⇤
⇤
kopmrzdnxfsauzuyayn:
⇤
⇤
⇤
snkynzbjtjarvbqhnwt:
bkjsebpypkwajymxryn:
⇥
⇤
rhqhbfyfudtknrdatva:
⇥
⇥
⇤
⇤
njflewavvafwreryhcx:
reytgxpraadnnzgauqx:
⇤
⇥
rnkabkhygoxkujfqbws:
⇤
⇤
⇤
ozsofcluyahkaynrrmk:
⇤
⇤
nivcyrbhkaqgxniwrlr:
uyankcgfupjrdnstvdi:
revntdaiyitkdktwdaa:
⇤
⇥
⇤
li  $v0 0
⇥
nxeycrkvhtuuhpzcxaw:
rannnzpxpyouqrbuytg:
⇥
⇤
⇤
thznamynirdapfdsnmg:
⇤
⇥
⇥
⇤
yaskezarrykpuokgvnt:
fxidphvaynfmprmaqpa:
⇤
⇤
⇥
pigaeyonytedlarkuyj:
⇤
yrcrabtxafdvynxnjjo:
⇤
⇥
bslmyrynfclqirpeard:
⇤
xnryqsgzumasjjyqxlp:
⇤
⇤
qgaunrqbgjgytrrxnge:
j   return
zwuyvxhreetanjjreiw:
⇤
⇥
braakndzyemhgktsysp:
⇤
ykxorutiajxvniajllm:
⇤
⇤
⇥
lalravpnphrnasblysn:
⇤
xbinnkygfarxqxidfnr:
⇥
⇤
⇥
⇤
xojgicyapyqtymtrvyn:
⇤
ncejfqauwypkinvqurz:
efckpclehvarnyugqla:
⇤
⇤
⇤
⇤
⇤
naihsaryigsyvymmqfx:
⇥
⇥
ramjauuykhxkrriymna:
lnulzygrerjwqjbtarv:
⇥
yohdxaevnrgnewhfpvu:
ylkctwzmvmkkrenznla:
kvilrruyirdlnzzadpb:
⇤
⇥
⇤
⇥
njgzssysarffeopdnus:
xycnnmhjzdsoycsrasa:
⇥
znauxytbytrwfevunrz:
mqvptnirosjapyoarqx:
⇥
⇥
⇥
caxxscjnryhmqgiborr:
pkrjgsjnaehwiwahdyp:
⇤
nydzroszgncakaumznc:
⇥
⇥
asdnnqidyyvivwinrbb:
⇥
akelxdewyvqcbdftrpn:
⇥
⇥
⇥
nywsaawaqrywgtnqlqn:
⇤
ahnrvyjuywlgpivvmkp:
⇤
⇤
⇤
yuvaygrmlfevnrtbwwh:
arybqnagcqwgudfolva:
⇥
⇤
agvyyvrhunbdxbfbkfw:
rpiuanleqqxkxmooyid:
⇥
⇤
hataxgydnbhybrulkyb:
zynsunraokwsvxkoyzv:
⇥
vyylkiamsrqceansmny:
suvdoyormficxoblvan:
⇤
⇤
⇥
⇥
⇤
⇥
⇤
parrcoeforuyryallyn:
⇤
⇤
⇤
⇥
actrainjtyluwkukqxv:
uanrojgtrjkaylrblpg:
⇤
⇤
xqcrcyuwznmloyyuavn:
⇤
⇥
⇥
qtjwaryrbnybjppvbav:
⇤
⇤
⇥
⇤
ajpxynnyndcudyairkr:
qaajzprwwsyxwhnumde:
fgnyxeuhwswyanegdqr:
⇥
⇤
⇥
⇤
⇥
⇥
⇥
⇤
omdryqxykgajskynnhc:
jrtazfkylonxnwlvewp:
⇤
⇥
⇥
zdryaouqpndyixalrzq:
⇤
⇥
⇥
⇥
⇤
vtuwcmtmscnqiycarnr:
⇤
⇥
⇤
j drodwaecytkrhreynya
rwatdloirqinwmldnyr:
urcjfsmpmymahddnlaj:
j pgmnrsbqaynkqiaduoh
drodwaecytkrhreynya:
⇥
nblgqkraaniyeiqbchc:
⇤
hlynvrrnxmwrqaymbcs:
⇤
⇥
⇥
lmyfcpjqyvranbdylwy:
rrqwyuarnnrnvgzyuyb:
⇥
aadnspqnbytgegtorjl:
⇤
⇥
⇥
⇤
⇤
iltynjmdkexfranjsnk:
⇤
rdrkdanrxhkvniygeal:
rwvcemzjjanohkygcaz:
yyarjspajmhtrfneezr:
⇥
nfyzqnoyrnfahwarmme:
lyxagqcnqwlewggsjrt:
⇥
⇤
⇤
qzjeynvfgygdarbkvub:
⇥
sysiqrzraarcjnwwyfl:
⇤
azzrryzkpjkzoevrndn:
qcnzuqialwfxqybpryk:
yauulwhyrnmywgggkbc:
⇤
nqognirpeakhovzqmay:
⇤
⇤
rgmkocsrarjybiznhhr:
aetegpotwndaosqyrql:
hgtmnuuygprelagoynr:
⇥
⇥
naggdjkfnyddrrfftac:
⇤
⇥
⇥
rajrosmlwqylcwhpntk:
⇥
⇤
yaqpjcrpefkkypgszen:
⇥
⇥
⇤
onyqzmarrmoojkyhrsr:
⇤
⇥
⇥
⇥
hqoarcwxhyvyqczqune:
⇥
⇤
ynatzjapwntkpdtzrhh:
⇤
⇤
⇥
⇥
rdoydwqaptnnyapghvy:
zzurnmqbnibjxwawydm:
axgcncbyvxrgzrrvrsv:
⇤
⇤
⇤
⇤
⇤
wfzqyuirfmzcafnhtiy:
⇥
⇥
⇤
⇤
⇥
⇤
⇥
⇤
bhfyrrxhjpeympanumv:
oedadjievrwhgznyzbi:
⇥
⇥
⇥
⇤
⇤
⇥
⇤
⇤
⇤
⇤
ppzyasehrjpslnsfdgv:
⇤
⇤
j clagjlnoedrohnayknz
darnrdvrnwgyjqwijjn:
j tduqzlylznoaqyryama
clagjlnoedrohnayknz:
⇥
snrjzyztwrerasxxoai:
else.2:
⇤
⇤
⇥
xpzinygwazmbsjvvrar:
⇤
⇤
⇥
⇤
⇤
⇥
ernsffsazkpvyanqtww:
⇥
ijmcvprwaiayngnxqmw:
pczvyngdxwyrfwzbvya:
sedyjaeubstrmnjzdmq:
ghfqnxzvoyjhenguayr:
⇤
⇥
fmxnfsyrrcuymfasdzy:
⇤
anurkfzyoaknoyqgnuz:
⇥
⇥
⇥
kptytrdmziiwcegnnwa:
⇤
⇥
⇤
bdvkzvmaukyxxuntrfi:
⇤
⇥
rxebybcclfyceuanzcy:
⇤
⇤
vaskwttvfyqnmywfkfr:
⇥
⇤
⇥
nuyibomjoogcacskrnu:
hsyebgalnprkfmmffyj:
⇥
ndiwmyryrssiroqiuao:
⇥
sylibfrrlyqaebjljwn:
⇤
azwurnnitigrgiyzzwe:
⇤
lnxuiunrzsryyyljahx:
⇥
zjwsbpaontoiyprkqay:
⇥
⇤
ynuzyrmezzjnmjzakqi:
⇥
⇤
⇤
⇥
tawyqepnjyrnlaozkra:
aysonqmlwahrxjfegsl:
⇥
dxrekuasnjorywnewop:
⇤
⇤
wcsqarkulcqtrenyazn:
zqapjxaalknyrzwcytn:
⇤
⇥
⇤
⇥
qnarazrkmwixnyarzap:
⇥
gbagdmylnrnhpmnigvk:
sygoqatzwlniaanierg:
⇤
⇥
⇥
⇤
⇥
⇤
⇤
⇥
wipwcrdyxnndyzuhapn:
⇤
⇤
ypyoqjkuawrdadnvwcr:
⇥
armfpqkusnwyueubfrh:
zzcqckenrysvoavdnyn:
meanhtgckhymbupryol:
⇥
⇥
⇥
⇤
⇥
⇤
jbjzygyrjgmaaranuaq:
nyuxruhdeancygcobja:
⇤
⇤
⇥
ysoonqbrydbtmyqaowv:
⇤
⇤
qryboqywakysynrfabi:
⇥
⇤
⇥
⇤
rzwkovcgunjarzxoyzc:
vrycgogapyeyblayfkn:
⇤
irwynvwppkopbxnamsq:
⇥
xrxunbqmrpzfotcjcay:
⇤
⇥
me $s0 $s3
nvrirwrfvcyhahzmvge:
⇤
⇤
⇤
⇤
⇤
⇥
⇥
⇥
kmkjfcnaryzlaxilrij:
⇤
gaufjjyyginjgxcinzr:
⇤
⇤
ozuvrqsafarmjysnmcn:
⇥
ulnysdzxfagurknculs:
⇤
⇤
⇤
⇤
uhnwfrakbgxrfldtxvy:
⇥
yallnrvwdebbmqajtna:
⇥
⇤
smrrbcwvzqclanbuzry:
⇤
wznlmubfsaeaedrnyys:
⇥
⇥
eqrjgjmgcrmymanpmix:
raqxmkahwonyogpdgao:
⇥
rspaypkcgzbngywrvju:
⇥
⇥
lrprzapvliglnjyiadf:
⇤
⇤
⇤
oeeugqreohuarcjynsc:
rudnhzevbkydrwapoao:
⇥
ofneyzxiurnpanpjlth:
⇥
⇤
nraivkabyntsrwqnbqx:
cyqddlkaramwynuyvxx:
⇤
⇤
⇤
⇥
rocabavevnfyjjibgas:
⇤
ypoelfyneijvahrmaes:
ewrsnbhjnmhauwynuuy:
⇤
⇥
⇥
asyrkqlknviijyrvzka:
⇥
⇤
udmakdgjfrynvbtutwb:
xlpayzqwosawrthuxnb:
sbwgcayabbjwlhgrnka:
xyzdxvnohtptroakbuv:
⇤
⇤
⇤
argsvwbrglshnfrhsya:
⇤
⇤
⇥
⇤
⇤
⇤
tuqcmranpkbvyolinry:
⇥
⇥
⇥
⇤
⇤
yyujabbllrtofdeqnch:
⇥
nkhylakubrdxafdypyr:
⇥
⇤
⇥
⇥
⇤
⇤
⇥
ngyscpjizcesbraidyr:
⇤
⇤
pgaszhzgwypierpyabn:
⇥
⇥
ufgkrjeygmuyaaenkyx:
vgxrrywtyonlbvnljya:
vqznjxdpraykdrdejfi:
zupipmanabbnrvjnqmy:
hytrfkmlnaikxjhcgpn:
⇤
rdzlysbvaxrxvndialm:
⇤
⇤
⇥
⇤
⇤
⇤
qkacsvapeocyfrfmnyo:
⇤
⇥
nevklsrlqknaxqqttvy:
⇥
arjvbthiuzccvuhnhsy:
⇥
nxgrytslbvalnpzaejr:
⇥
jddwyqdjalinjdcvrmi:
duorxehvbzgrnygavqw:
⇥
⇤
ibwrenhezhatzqhbisy:
⇤
voxegalvfynqfguksrj:
twpnguyojnaplgerxku:
zadkcnsnuyqwlrkkxyg:
⇤
⇤
j gxrmyzhwkgplsnabaqy
⇤
rumfrytaovuafgynxfv:
j rwatdloirqinwmldnyr
gxrmyzhwkgplsnabaqy:
⇥
⇤
uxfrbrprykzsansofur:
⇥
⇥
yovkareprkhmgnnexqr:
⇥
⇥
gtxxmmtpacklryydann:
⇤
crhlgglcvpnamrrpyck:
⇤
rjosqqghtujnhpuyhab:
⇤
⇤
⇤
⇤
nuyztrgxlxbknigsora:
abhfyjduuynyorakrmq:
⇥
⇤
⇥
⇥
wyheryfganzplyrlleu:
uydkeuraodrnpfiacla:
zrlkhyadbyfhlpdzurn:
⇤
⇥
jqoyaajnswainwoqirp:
yyiwaylvctgdlaumdnr:
⇥
⇤
⇥
⇥
ycranwajkctyanereoz:
⇤
hanjztfaunoylfzgeor:
⇥
⇤
⇤
⇤
kedrwurbnyuiabyodrw:
⇤
⇥
uduknonqrarmmybytru:
j iakminppgyiuonrmwig
afyxrapntlsierunglk:
j dfydaqfcrajvknhknbg
iakminppgyiuonrmwig:
⇤
⇤
⇤
⇤
ayutvxoqnjgigkfrqjr:
nalgyxgsxydulzlreac:
⇤
⇤
⇥
⇥
kedayrdbsubpknqnnra:
atuioytjsurnntreiyr:
jayhrmisbmowgpwgeln:
⇤
⇤
umbnirtnysajxejmtkw:
⇤
⇤
⇤
nxrqrtanyoqyoquckda:
ysikisaztakwrtnujnv:
⇥
⇤
⇤
⇤
npnlgqmnaavyrerpgpe:
tdqzfjnaqjyxnhqcqsr:
ffnlxrdcykdydkaarpj:
mfuvyrrahldfsnvevsb:
⇤
armllzfgozyqqavnyyo:
rhacngofzyxdezgcmis:
⇥
⇥
⇥
mrpoeqnsigdapaepdyy:
⇤
⇤
⇤
⇤
⇥
⇤
⇤
⇥
⇥
⇥
⇥
xowxqtopaaedysnrnab:
⇥
⇤
⇤
⇥
⇥
naacgnirctwslnwkyhr:
qufsamnhlyowakjyrla:
⇤
bmepmnyuywisxrcjuaz:
⇥
⇥
⇤
⇤
yratpnozwbcmlzvybhp:
yqvkpywopjkrzafunjh:
locfysfzdubnyvazerq:
⇥
j yoaennaftuokeqbryei
ucktmingjsqireyoxap:
nvdrkgenfynpfuplamn:
j cuanvyjrieqaytbygnk
yoaennaftuokeqbryei:
⇤
⇤
⇤
⇥
caeuxyauvnnozhjhrth:
⇤
tnsgyxrbajjmlneqywp:
⇥
awuryhaxqqzxdxhpnan:
fkmlrljkfvsyaandcov:
xnqhvngruaajzngydzt:
yynxaasorkwxssecxbn:
⇤
⇤
⇤
ihlaapkirnnjqhwpyhh:
zwqbbymapnuqelycdnr:
⇤
⇤
⇤
⇥
yrraxahvyureikrnmhm:
⇤
⇥
⇥
⇥
⇤
⇤
⇤
⇥
yxygupzncoxhkzdragb:
raoygvmnarozrsrflww:
nqsqyjvmcrrkaeaflnu:
⇥
wpuvytanqxerldbwlir:
⇥
⇥
⇤
⇤
⇤
fyminfinpnglrjrcafx:
cenikqudryahrwqzgnc:
yrtfgcymapwxjonqgir:
⇤
vkrkyacfinwztakrshl:
⇥
nlcvuryflnoahdbrvtn:
⇥
dgrzrwenrapfcohywpf:
⇥
⇥
ijueapjyngexsahirav:
iyrtlbqadrlenpipodn:
⇤
⇥
⇤
⇤
⇤
gnrhfcviwaaunzidqky:
⇤
⇤
⇤
⇥
⇤
⇤
⇥
nyggpxwrfuguuygahcr:
nnpquhydfkagwrnkalt:
⇥
⇤
fzmwtrnhknjoatyxygn:
⇥
anxvaizsydwlyygrytj:
⇥
⇤
revaorqknjgseydfvlg:
akdknpdpyfhoafrqrdi:
⇤
vqanirsbvtyhgxqprdi:
⇥
⇤
aglyltravgoflrrpnxy:
⇤
j brfirajphbvnnwayngv
awrsimdzpeysrnzxcyp:
iytzxqnakciezirmsfh:
j nrvgsuqgxnayyjyagtd
brfirajphbvnnwayngv:
⇥
wznmeagpqnksrfcthiy:
⇤
wzvhnmbwznanhrycgty:
⇥
⇤
qhhysyxrvtrknctwahm:
⇥
⇥
anicgyryggzvopxrhlv:
⇤
rudjrnexuqvjhanyjxt:
⇤
⇥
⇥
⇥
gcrjeuplyzuntaqzyza:
zrvdavyqmantdccrfpr:
⇥
⇤
⇤
jqumnrijakkatfychtg:
⇤
⇤
rcruzfaonkoyzebcnin:
⇥
gxvqrypaajngkcbhubk:
⇤
⇥
ygamoigoorlbgnizzac:
zynofnucgamkxnrkkye:
qsnlrayntzgbpxpssyt:
⇤
⇤
j nnriwnvafaewxgldysd
probmrznqiswgannsfy:
j nyolecavrnuzlyplise
nnriwnvafaewxgldysd:
⇤
brdpvsyoypkotqbctna:
yybyhbuafraxlnpcyrc:
⇤
⇤
nepbtcwrvaylrdyqima:
cnzesakcvbqnyeomrrb:
⇥
⇤
orzzvhkliooyhuajank:
wsbrqfrbptoenoafyjg:
jzmlewanqkymuunkerj:
⇥
⇥
⇤
oaynqryxayxnnpsuypa:
enrrsaqiznkqvtswyml:
⇤
nfahyuqmaehlereekbo:
⇤
⇥
⇤
canjoizyiqtktsiorid:
⇤
⇤
⇥
⇤
⇤
arnchpydxjimlosqoph:
⇥
yevyafmgkvnrsnwnitr:
⇤
aorqfrzjiinbtllagyh:
bvappyvnclradcyqucq:
⇤
aakplrodxenynybplfn:
⇤
cagxrmrnhyecrhbbpyz:
⇥
xcrtvdhtnbpqlzauggy:
urynzexaknyiaomvwgc:
⇤
⇥
srjetydszharcwzecng:
⇥
unzhkjgxgmpralnbyxp:
ozofnpaypxsnpruwlcs:
⇤
⇤
⇤
⇤
⇥
⇤
hnimyrtulbqrrianscz:
krlnzltiylnorquvkha:
⇥
⇤
⇤
⇤
⇤
⇤
⇥
⇤
⇥
iirqtwaomamwhxntiyc:
usckduoaijkonrdtyak:
⇥
tixotnyxgrarawaxsbn:
vcyjjltnziqhdasqhrp:
⇤
⇥
⇤
⇥
⇤
⇤
⇥
⇤
yerjqfdzkoamyesncrc:
⇤
⇤
fnnsjzgrdnujppwyarx:
lkhqrvyjmnhadqjozyp:
⇤
uknbrqnyfguymztladv:
⇤
⇤
⇤
⇤
⇤
hnbdkwurroudpagfwyj:
⇤
⇤
pffrwdjhckjanfxpamy:
⇤
⇥
⇤
⇤
⇥
⇥
⇤
⇥
⇤
nwmhkaqiyaprrmuncsz:
⇤
⇤
trhlsgrdvaqdyypnmia:
⇤
⇤
⇥
⇥
⇤
yanrmsncwwobapesaqe:
rrqgftyvlvtnyluxcap:
⇤
xnvhaycioksxffurmdf:
mzjhasmijrdryzvvwnz:
whargqgtiardsijnyjh:
⇤
⇤
⇤
⇥
qnckukhtwuybpzoxzar:
oandqsavlztbrwyedht:
⇤
⇤
nrzgxlacysaywpnrfws:
gwylcoeznyzjzurlifa:
j nmldianoroykyntznfd
⇤
⇥
nyoxcpoxbexntnnmayr:
⇥
⇥
⇥
whngnyrskkahganojuh:
⇥
lqbeaygrpiacbgbkadn:
⇤
oiryycwkxlcaojwjlnw:
injnmuaepsxyigrbyvr:
jzanuayquerdpykxbkz:
⇤
⇤
⇥
ayejdmrrrvkefgrnpus:
xyngnkzprsdrhuvdjai:
icoekijryfxankasxop:
j hbyaxmkpmnrhdconvto
⇥
⇥
⇤
⇤
⇤
⇥
nrwhbuznjyomjaidkle:
⇥
⇤
eydgzbikgadtevbrfnw:
isayxxmgdsjqrmsiynq:
nmldianoroykyntznfd:
j yqpnadaoorpttbaynfe
qwtynqgwakcdaqraoxa:
⇤
j pyknflovcjragdhfybl
irvysaislnnnegyoqxb:
⇥
yqpnadaoorpttbaynfe:
⇤
⇤
⇤
⇤
⇥
⇤
⇥
rjihlptxpnyklavyfrb:
⇥
kyxfrvunufarioanpau:
⇥
⇥
rwbvyctapunonfyqnvv:
⇥
⇥
⇥
jyamjnerphwkdffazwl:
tennaujrycyjakbsrjr:
crzengpysaowuhfvzzr:
⇥
blt $s0 $s4 else.3
hxcdyrnkfycofcwwaim:
⇥
⇥
qzxafymhcribhhfrznt:
⇥
⇤
necpsemsweybzqfryqa:
⇥
⇤
⇤
gayguprlhjnnhbxoqlf:
dxlppmsfrymiandhpur:
zxharzgthwmynpelvqp:
⇤
prkqyaqgynzzibpzawr:
dkhynvgaqdtnkayytlr:
⇥
⇥
⇥
efuamfsaoyfhnrkyejy:
bnkvmykoakjdgyarwla:
⇤
⇤
⇥
⇥
⇤
ynaitunyaivgrouytza:
⇤
hadypbyivkrnofxvnfu:
⇤
nnbjlnnabcxyrttnkso:
⇥
natemwziutlhnlfrfay:
hlnbhzrluxahsmlnvoy:
⇥
⇤
svbayromlgeylmyaefn:
dsacibnbcybxwrnvwsp:
rbnjuynjvkbqhhezyca:
tmrfislrfhxnkabylzn:
⇥
mptniooxlhlaiyarnwm:
rlyrkbazmozxxpgiunr:
⇥
eaqsnmztyqkerrlygmc:
⇤
rqvmjmqfrnyiqzattrz:
⇥
⇥
⇤
rtmakhrfsqogcgawnty:
hqhapfjynabtbrhmobi:
⇥
⇤
mjarzyxndyralxvymzq:
hibyzcdnastnlasyrin:
moarhafniykmpnylbck:
⇤
⇤
⇤
npiggtyrscfvhkaxkza:
⇤
xlawdrryuyqbdywdned:
muryvgfagynwzkazlgn:
⇤
⇥
afjtqdavnncervavyjl:
⇤
grjthccwvdgnyeabhhj:
nzrobvppmytlarihoxx:
li  $v0 -1
⇤
rzngqxyysgknxyctana:
nwifyngikpalienjrsh:
ycorrbfwdoyynbrjeoa:
⇥
yfeuxtuihrfdlainohk:
⇤
laqybnoxiynkcjrtcwa:
⇥
⇥
groanthhgphwypgtrna:
⇤
nrpwynwhmwzoenzczoa:
⇥
⇥
awynkovvvothltrivhs:
⇥
⇤
⇥
hcuverjfrmnlrnwalyg:
xvceyvhkrxnelukmanm:
lyeutvnslswdqtjrfta:
nqrqxvasagywegayuez:
avitybzibzmwamyjntr:
⇤
⇤
⇤
⇥
rcaqnmuwpfhivnivhzy:
yxowabkacvbnmqivrel:
fqvrzsabnakihyotpnq:
⇥
⇤
⇤
⇤
⇥
⇤
⇥
bpcyhjatrfcwnvlzfni:
⇤
j return
coylbdpalhdfalxntdr:
⇤
xmraysrjrkmnyxyumur:
⇤
⇥
⇤
⇤
⇤
rybafncxmmdyukoazgz:
⇤
⇥
⇤
⇤
yoppykenorvundvadwj:
vadkyrfyyzoncbghxna:
gcgadpbzcjenyvvbrrm:
⇤
fnckjoceffywyagajrj:
⇤
⇤
aupzsanynmskynafxyr:
⇥
nxwjgfwdsabhzrjypyj:
snkrhgwnrxfmvmcgzay:
⇤
⇤
amhrzvlywgnagixvbyo:
⇤
⇤
⇤
xrnynydwayzapcsehxk:
⇥
pbkbrivzgraknykbjlu:
⇥
qticztknxkamkutstyr:
⇤
⇤
⇤
fifyelrtzoxthnnapnl:
⇤
zmghreznjlcufenyoka:
⇤
rasaiyxnrbgyxqygrel:
⇥
⇥
smturynzyscornagnjl:
jmaausobkprhgypxkun:
tohqgmhrsbaveyhcnpj:
⇥
⇥
j iyhoaatngtqirfadenm
rtayxqtuaranygrdvmr:
⇥
wvuldevnljalhrpkity:
⇤
ifnhwzatbxbxyjobfrz:
j lqbeaygrpiacbgbkadn
⇥
⇤
⇥
iyhoaatngtqirfadenm:
⇤
⇤
⇥
⇤
⇤
⇥
⇤
⇥
⇤
⇤
⇥
⇥
⇤
foatvacbigkrqydppan:
⇥
⇥
tfbyafrfnuoashxwdlp:
⇤
rgdvnsygaabhgfsiqyh:
⇤
⇥
iaoisnryrcqyawyrqca:
yftncqejbunaklwrtaf:
⇤
⇤
⇤
hypcjshsuaeelclprln:
⇤
⇤
⇥
⇤
nyoonqkbjkfnrvysana:
⇤
⇤
inneuvuamqkyterwppt:
⇥
⇤
⇥
⇤
⇥
nmncmnqnlbyrfxerjsa:
ovidbbgyirbavgxenpl:
⇤
⇥
⇤
else.3:
j ypqpcarihnotfbuuymw
lolbxmmfkrngjaoybik:
⇤
⇤
j caodrwjgyvxazlyonuu
ypqpcarihnotfbuuymw:
⇤
⇤
⇤
j vflnyornstjovyasqvw
dnrsmhyirsmkibzixwa:
⇤
⇤
iorxxoftslyxblqnsea:
bnjbpiymntgoapehyre:
⇥
⇤
⇤
fhzlyyjostnnririxay:
⇥
j rxnergoadjzzehzyrrx
dfydaqfcrajvknhknbg:
tzyfnohrvqjadavgrrv:
j ygzemqrncgagavcmjoy
⇤
rxnergoadjzzehzyrrx:
⇥
⇤
⇥
lladnyxsmvcprancmnp:
tgisergazakndoarpyo:
⇥
j emdrkpktwhaalnybkqc
⇤
vflnyornstjovyasqvw:
yvcradiwndpemensekr:
dnbfahyrexnrcpyzcaz:
afxdbrwqtzpjvehnpyu:
⇤
⇤
ikngthymcqwyarmrgak:
⇤
ncwyunvwyabbvrcownk:
⇤
⇥
⇥
sadjbmvmanaydgrwpcf:
⇤
⇥
beq $s5 $a2 else.4
⇤
j fpynmzrppgtcnjblxar
mcyqavjrvzlyanrrplu:
j aryntvdaslvpzmsqpjm
fpynmzrppgtcnjblxar:
⇤
⇤
⇤
⇥
qcfqwjvjwrmaqyvnunj:
⇥
⇤
⇥
⇥
ivmsnbrysnmlikbaqyz:
⇤
qxyrwacrikjuacdmckn:
yyyarlgbllgbnmoisvb:
⇥
vrffqhjryslnnaaayyb:
⇤
⇥
⇤
⇥
aubtnymorrqekwefksr:
⇥
⇥
⇤
nvmyzdhhztawreeyklf:
qykcmuraohnhhlstxsn:
ihkirownqmaniayjcni:
⇤
⇥
wfdyngsztpasrxowaun:
⇤
wyoxnllkusdlroapkhg:
⇤
gnyhgxbhazrlsfnqptr:
j gysngmujlfqvyaaevzr
⇤
zysnhdrvchlglrjyjag:
j jyzpiyoarunnwanezqs
gysngmujlfqvyaaevzr:
dmasufatfyshlcrjngs:
⇥
⇤
⇥
ayrnexyccwnmhjbevra:
okpiezxjdymntaapnyr:
⇤
rvnxaeefjitnydielyn:
ypsttvfstawimansvra:
⇥
⇤
axxrdneittwwyvuczrn:
⇤
vwnvytnpamfrzxspnlr:
⇥
vrbwfqqfkposytqanbr:
⇤
⇥
⇥
⇥
⇤
⇥
⇤
xallmvtqygxchrartnn:
⇥
nadphyzjzmrukjshthd:
cqarapzthurlonqnlyr:
⇤
⇥
⇤
azbdjcsyupncnokzurh:
j hxwahyaxqinrgdexlpn
qeqannavirbqkouyyma:
⇤
avsdrgmapryawrgansv:
j fcfonryonnayesunbel
dgkbxnbrrdvamyupknq:
hxwahyaxqinrgdexlpn:
⇤
krepcteeyzqbgnumaor:
scozrayjdcbnywnkhnn:
⇥
⇥
⇥
⇤
⇤
ymrfhbmzzpsnblnbarn:
nfbilwrzyjabqjcssbq:
⇤
⇤
eroqslthtlngvalkykb:
⇥
⇥
⇤
⇥
avotjqqxodunfsglayr:
inyujwknrhipburpnqa:
gmabyzncnxwirmabywf:
⇤
⇥
sqotastijprtanmyywh:
tdixzhyajbqberncnha:
⇥
⇤
gncjieiczqkrylvareb:
⇥
⇥
⇥
⇥
⇤
yphqxzwcraonzrsnlst:
⇥
⇤
lkhfnhmipsxzdbyorao:
⇥
⇥
⇥
⇥
⇤
⇥
ammyfrsnbfoyamueiny:
ealxzfcucwyrjnvptkk:
bwgxynvfjxcrzahluct:
⇤
bapildvdjqmfnkqybrs:
⇤
⇥
otnrsywaakyoaylojyw:
⇤
⇤
⇥
brygouqoalknqnntrve:
⇥
jlairwyhoyhnuizjnka:
⇥
⇤
hyxpmrpdmniakvarytb:
⇤
⇤
⇥
⇤
gjrukynkaokejapyxbn:
gmlnyvhdiiekcandurk:
⇥
⇥
⇥
goqkugiynqmwzwvkaru:
⇤
dizcheyakacnqrnjkoj:
⇥
⇤
nfsgdcvncdsauxqrhcy:
⇤
vagrtnfqxwepvxrsybf:
⇤
aoplybdfnasrkycsdoh:
scicofrdvsayynlgniy:
⇥
⇤
⇥
vsewfrpnyukifhmqtca:
⇥
byyfeddwnbnrzresaqi:
⇥
rpheznayfyrqigmnrzj:
⇤
tojabbhnyapzabalqrw:
⇤
xxazmlmngrxrandnyar:
⇤
⇤
nfrvjywjugmajyrrujj:
nyxwlaylttuxepvprda:
⇤
⇥
⇤
⇥
⇥
⇤
⇥
⇥
trtmfyvrdngmyoawicr:
anedktnryeglkuyqsae:
rtszlaxoangrhydheda:
⇥
⇥
⇤
⇥
⇥
dwxgvbjreyonbuwaveg:
⇥
⇥
smyvmanawrlsugidkmh:
⇤
klrbyziaunryamtbfqy:
nxfzybgrensynazjzpb:
⇤
⇤
⇤
rjoyzerynxdxluxhanq:
⇥
⇥
qjdlchnnyaqerpdairb:
⇥
⇥
⇤
⇤
jligxmzzfhqyabrnybt:
ppmtnharseggwfaayed:
j ernznrzrazxilejyfxe
hkysemeiqmmhbcnpvra:
⇤
j rnnwyfblsmgalrpdvyc
⇤
ernznrzrazxilejyfxe:
lxcxryiwqtrmcjunjqa:
cmyvawhdaaajrnofkmi:
j pufbxakhpdcrecoanky
dgygrjudyrnayvraaru:
j qwtynqgwakcdaqraoxa
pufbxakhpdcrecoanky:
⇤
⇥
⇤
⇤
⇥
⇤
⇥
jrqydsbndankrnjevrc:
⇤
⇥
⇥
⇥
⇤
fqqfhzkyayfjjnarsda:
azizpryjrmfcpbenemm:
⇤
eyreqbagrmvnzsetaed:
roxgpdgyxmtuntronsa:
aoiislnizrhrfzuyltf:
awunyinujbwrdvhpesj:
⇤
⇤
nrbzyfpafcqayqdmhbr:
⇤
iywicnrausdoesoicrd:
nringfvawsyssnamycb:
⇥
yaqnnnfbgtioercyyyd:
j ntfxsiyyjyckmavmhnr
otyofacuyedwujrjndc:
j rophydgknthrktlulha
ntfxsiyyjyckmavmhnr:
⇥
⇤
⇥
yfwigrdggakadbdnddc:
ckmnmuwxevadihxynrw:
⇤
⇥
lshyysnoxyvaqesrzgu:
⇤
uanmipfxcyrsrcsqtcl:
⇤
⇤
axthondwhpydvmyjzzr:
⇤
⇥
cabrryzilaynczxgunm:
⇤
inc $s5
ivkuoaxbcygpdrirunr:
j oarayldfyniqzfbzmno
⇤
pncnpxgrybpxnzraxnc:
⇤
j nplcagkkolicxynjblr
oarayldfyniqzfbzmno:
⇥
⇤
⇥
⇥
prfxvyqgbheaqftndia:
⇤
lcjjbtkqemgnapryuga:
eydmjabrwtmnartgvxy:
j iptwklvayorcifakikn
znqcfiyavfqenrcpyxr:
⇥
bvnvbsziqoyrnppwaam:
⇤
⇥
⇥
⇥
⇤
uavbyszpdiafyrcnmfw:
efxcfnnupecradeltxy:
⇤
szrjaaqhinnnrgajuvy:
oxqnxnkxnhrafjvsyqg:
jwtaamycxrxcyfpring:
⇥
⇥
⇤
⇤
⇥
⇥
j vrhwelocntcxyxtxauf
iptwklvayorcifakikn:
⇥
⇥
mul2 $s1 $s0
imlllydarnfviesdnlp:
⇥
yyyzbcvkanfubtyrqda:
⇥
⇤
⇥
⇤
⇥
⇤
zbkphbnhbryfrklbjar:
wdngesakuehrtmrnyyf:
cyclpornmraighjhngo:
⇥
⇥
⇤
niasyymanjurnowapsl:
wilxdnwyzkrbwaaafhw:
⇤
ztanzqqicavrewfmynl:
⇥
spknrxdqheynguaqdso:
⇤
⇤
⇤
raebnvnttxjjwzrwlby:
⇤
⇤
xnkfetukaruakmpsygh:
rssbrvavnvfdyhlcczr:
fnejlyyqhyyarxuconw:
⇥
⇤
⇤
hoaqnptyfncgzpdsrzc:
ipnpqyjfgrmyjtqjwea:
⇥
⇥
zyvaskanevyyrdccedn:
⇤
tajehyrlrsniqkilldx:
qyurjcrlihanyxedxok:
hqoplnadnelscxgrpmy:
xhnytigrywecabqojxi:
iyszmrwwyxgeapnijuj:
⇤
⇤
⇥
⇤
mnyasflnaemrrmurguw:
⇤
qrrbqgyfankxkkhypqc:
⇤
⇥
⇥
⇤
⇥
⇥
⇤
j aowfmrcaijtpegbnyye
nlxatkpyrryfyvysmyf:
rczeqajczyiymabdhln:
lzghydaprorrrauqsnz:
⇤
⇥
j nctzrmtyszmkzacrsna
aanzyjbzncdrbkrupkf:
⇤
anywmjwmippqrtecsrd:
⇤
aowfmrcaijtpegbnyye:
⇤
⇥
⇤
⇤
rzerbjeahnqfpkyemac:
owoytsnapimrbvuelya:
⇥
⇥
⇤
ndmzbiviaanrfnymiqr:
⇤
⇤
⇥
rasiayvoasnnuzrwhbm:
⇤
⇤
⇤
⇥
⇥
j ygaryplwarlpkrtnnmd
tinrafcypelrhdwhqot:
j jbqyywvadwqngwkrivf
ygaryplwarlpkrtnnmd:
⇥
coxsvanxaaytsacaerz:
qyarzyabirddczczawn:
vtprfyansoynmausnxv:
⇤
⇤
ivgkjpxyymarznifkcd:
⇤
⇥
⇥
ziaywabicergpqfdsnv:
rzfnnarbbwyyvmlmxyg:
⇥
zwkznyayptshgxbrgms:
kezexnrpeamfxpptzyc:
⇥
pxlnfyfqzzhryxftlla:
⇤
fpubuynhnryzazaaveg:
⇤
⇥
⇤
⇥
rjnzqafkhpzfrhmqygg:
aacnnoqluxfdhyswzzr:
mnayvbaruxkbqsizsqb:
⇤
⇤
iazjwwrycvnjqoknucn:
bncqzfaboyjrunaexvn:
⇤
⇤
⇥
djyzuraqzbngywznfjv:
⇤
add  $s1 $a0 $s1
⇤
mhafhqincybddsntvrr:
cnhcjryxzaimiuvtnni:
⇥
nyodkosyshcsrwqozay:
⇤
⇥
⇤
⇤
⇥
⇥
jrbgjhkabnnmxoeyrwk:
⇤
nyjwaywkrvgvpcbndqd:
⇥
wvxxrlonwiordrypkva:
⇥
uwpynfvrapxadrplnud:
⇤
xgiecnsaxkxzginpyry:
⇤
⇥
⇥
⇤
tfhtjkycgfufnzurkqa:
snvtrtyvyrzkjmadtxu:
⇤
⇤
⇤
⇤
⇤
⇤
oleraumxatdjslnysve:
⇤
⇤
⇤
⇤
⇥
ugyrskhfiiupfxwinak:
onyraynbaemrszpehtu:
⇥
⇤
⇥
⇥
⇤
⇥
⇥
⇤
kgsoajmynzhsxraccru:
⇤
⇥
⇤
huhpugukzxihayrlafn:
⇥
j lvipyhnraleccndagfi
tduqzlylznoaqyryama:
j fvyyzqldnjgarzneezs
lvipyhnraleccndagfi:
⇤
⇥
nsyashnarsxvkympvpv:
xfmfcafzxnsfdaqfryi:
⇤
uanryxczdkxrfrqegxv:
dvroabunlweyytcurca:
⇤
smnkrjcqndqdgrryaay:
⇤
⇥
⇥
⇤
rdbmnurftynbxpphgac:
⇥
lbeugzoyziynimnmarg:
⇥
yfklntmxsravfryncrv:
ngverstiuyallaxjhzh:
⇤
⇤
⇥
⇤
abrmuyumrnwafwiboyt:
⇥
⇤
rufnxdqyfeqabamxavt:
⇥
budrhaqfmayxjxtvnea:
⇤
⇥
⇥
⇥
⇥
⇥
⇥
ruyopmnlghblzzxqawm:
⇤
⇥
⇤
⇤
⇤
⇤
⇥
⇤
⇤
yalxnknmcarkdapfswi:
rmxtyaafynkwebhamzv:
⇤
⇤
⇤
⇤
⇥
bkpjedkopiynnlrdeax:
⇤
⇥
⇥
akrnbknlepbhxyhnyws:
⇥
⇤
⇤
⇥
⇤
nlkqxycnopzkmargdua:
yyqgtrgbdbpcknnajhy:
pyaurbpaqjgrqnrmhvk:
⇥
j qxfvmauiklfscrnenuy
⇤
leiyuolbrcanovhbbxy:
⇤
⇤
⇤
⇤
j ernwvwagruaylrncnvk
qxfvmauiklfscrnenuy:
⇤
⇤
⇤
yamfunbwsplqoroyxea:
⇤
ntqfqncbebiyarwoamb:
⇥
⇥
ghjrrfyrtemwnhyolca:
avvnntqrxaryoavrnny:
⇤
⇤
⇥
⇤
rcjyxpfavkgmmrxnxlc:
⇤
⇤
⇥
⇤
⇥
⇤
paipawvkjrxttnqbusy:
yoaynrnnackwifmduuj:
⇤
j qyllxnxypwzkrjgnawc
aryntvdaslvpzmsqpjm:
j probmrznqiswgannsfy
qyllxnxypwzkrjgnawc:
⇤
⇤
⇥
vrqdinaiemqcwygbpmb:
⇥
kvrrmbyycanxxlhrrok:
paelttnhfcnihuybjnr:
⇥
⇤
⇤
njapqjpkojqkryfxyts:
sfsyjpmsmjvfyeaugrn:
txhvvdkderzbnhuiyya:
⇥
gonhrxnsbaoefkojyyg:
wjkkzfyskdrsanuison:
ybpkhprrybnccafkbcr:
bfarsyuhfrofiqcmsna:
⇤
rlaqorfpmaulqkdasny:
igvuiyoungreaowxrrn:
⇤
lh   $s7 ($s1)
⇥
sdyqdzcnovkusophmar:
⇥
aymfrvepgnyonsngnka:
⇥
⇥
⇤
⇥
agmcvryeatlgivvnyrl:
⇤
⇤
⇤
⇤
lxxzgybrapqanruxqln:
tvanoaczyrmndfxhlor:
⇤
⇥
⇥
⇤
⇥
chenzfsivaxyrjyskgl:
⇥
⇤
⇤
j gcrjqlyblfcanteddao
⇥
pgmnrsbqaynkqiaduoh:
j arynwqipoiwmursxbix
gcrjqlyblfcanteddao:
⇥
aioyvasrfyrwmmyaonb:
aqmfkhmyqhjbjorkkrn:
⇥
eoecrcptgidygsnpall:
rrkxuensakwjoyvdrxg:
⇥
⇥
rmmzydnquqbatxkdvrl:
⇤
⇥
⇥
plwyrhadkutydginhcp:
enrwkdnmyzrpwnswuaj:
xnahyaojnrebrknxfdx:
⇤
⇥
⇥
⇥
⇤
⇥
⇥
nluozdygsicgrzhrazv:
yjuesnxthrhpjkbqape:
⇤
⇤
ruydlwanfpqmfyugoyg:
⇥
qbniwbqayyarasgfydk:
⇥
ldnrhyafafdgpbaecgs:
⇤
⇤
⇤
⇤
⇤
rajaybstnxrddolvcea:
⇥
llshnatqxuroodypjng:
⇤
⇤
⇤
ravybonwefjvysabpcn:
⇤
⇥
dozarbsocelrynduikc:
⇤
harnloemyyppcrrmjoo:
⇥
ykrynwmgflndicxbvay:
⇤
atowahdemykpxyngrya:
⇥
⇥
tldpmutancusicrjtry:
gpnuvybadoohhirxrcr:
ecdpxrjjignakrpyeox:
⇤
⇥
xsrfyciivhianowfniz:
⇤
⇥
⇤
⇥
⇤
⇥
mggbzevrgandxsyoehr:
⇥
bne  $s6 $s7 if.else.end.4
⇤
⇤
⇥
onvwraaooyczmyetvib:
⇥
rnqragbskbqmgqyhyst:
⇥
cywjahgrvrwconmkjqw:
⇤
⇤
⇥
⇥
⇥
⇥
⇥
drrpoyrdwakrsxainzd:
⇤
ghiclyzcrowwnouahas:
⇤
⇥
pshucxvxksnayvrkrop:
⇥
jaiagynraheywmmymuj:
hrwnvdunyayanfzmocd:
qycyenrmjvalskangox:
⇤
⇤
⇥
⇤
⇥
vjvuhuypcgnajjnrmrt:
azzkuytearmlnnxsvyg:
pohyyzrnusynrdafuqr:
⇤
⇥
⇥
izxkyraqenurkysjoov:
⇤
⇥
nrkyhupsrnianownnti:
⇤
⇥
rmyindaclyvmansrryf:
avoqmmkkriyobkenpzf:
⇤
ftnfycgachsahfrnjut:
luauyjrwrcuyznfxrov:
⇥
pucpnvqkbkjrtormamy:
⇤
⇥
zxayjybvhqundlkudhr:
⇤
kwyuuaynfxielqwscbr:
ygdlsmhphvlbwearnsx:
⇤
⇤
⇥
⇤
⇤
⇤
⇤
⇥
ineideqjrzcawrnyyra:
kfaurvwhwinkpjysfsx:
⇤
bnyfumpralvnymulrva:
⇤
⇥
⇤
onabfhbkamwmyqnsbrr:
⇤
⇤
⇥
nyrkfisuypvdnwonair:
⇥
⇤
⇤
nqdzyusuhfnubawgrlk:
⇥
ysknymlorondaehlzds:
⇥
⇥
⇤
⇤
asrejnqndbfapbyzixn:
aetghredgmxmnoslgly:
iknraloykwsajnfljnh:
⇥
rarbfocyqqhdqnahhbz:
anynysshyryzprkawmc:
⇤
epnmpqrdthyainfuqfy:
⇤
ynxbrrugvskhutcamgp:
ralpsyqlaxaykrneavj:
⇥
⇤
sdrjsnxylllunakqfyl:
zvnrhbvnmyaxorclasp:
⇥
luouydngalyearmydrt:
wolsnulyggvaraozixx:
dtqdfasnrwhzyxcwvru:
vrrvkaonahyempnefus:
⇥
⇤
svrdeaneymhnzavfqio:
⇥
⇥
apxrbmzytgsnwylykrr:
ugejnqcnplqqrauwyvn:
⇤
pdnrrbzvfavuynhxbcp:
⇥
rexanaxzumyuuevuesq:
sfaukuzieyrnydmlikm:
ryeqozdlebhnninueua:
wsravkgqntrckaqezby:
⇥
⇥
⇤
⇥
⇥
gndjyfgzynarrdmauak:
⇥
jxkfnbrlefaxcyxrxjq:
⇥
⇥
vwywpwagynhtvrbsaei:
rxweaucvjaslwyngtsj:
vsafyqonyorzrnqgija:
⇥
vnylhdlvdbayrgjaqak:
nlsmkryfyrifawnalqo:
⇤
⇥
⇤
⇤
⇤
⇥
⇤
⇤
⇤
⇤
dasqctdvwrrkcyzgjno:
dyfimvknacdjcrmximw:
⇤
⇤
⇥
⇤
opwkoounyravinargia:
kycnvslkaacwbleyprp:
⇤
lavetdzakxpysfnrend:
⇤
⇤
⇥
lsfcczsdanjnrmyryha:
⇥
⇤
⇤
uncxurcmyebwvvanpgl:
ykqaldmnmlzrjfcwrbg:
⇤
⇤
⇥
nloyerrzabvdulqsyvn:
hfrcyeajihjayynolwv:
⇥
⇤
⇥
zznurywxatnsynldykb:
ctjyasyuprnuuwpffey:
⇥
jrvcycrsasqrtvnxicz:
j barrnaryijicncnwdtf
dsnngplyadarqyryzpu:
j nvdrkgenfynpfuplamn
barrnaryijicncnwdtf:
⇥
⇥
⇤
rvkdaoxrpgcnrhyzzid:
freatbdqdflzzynyqau:
loorupwxayniaxyvbrm:
parqhqavzpdrrhxywnh:
⇤
⇥
gwaxndgyjqqxrniicjq:
⇤
⇥
⇤
⇤
⇤
wkcaotqiulqvyrrnllb:
⇤
yieyapwewmnehrzqaig:
⇥
⇤
⇤
⇤
⇥
⇥
harccyyyeerjqznugjj:
tssxwavdrmymnedvzed:
hvarngtraufbyzqknty:
ryqqonnpafaeucvbxdo:
myngalpmbyrnljfmvbe:
haqpjitlnnyucogrlnb:
sdgrehmwgrnaybwldum:
yewdywrlltbqaqnsxbz:
⇤
⇤
⇥
⇤
pcalhgeidwzniyyurvm:
⇥
omprplsygnhepuuzjaz:
⇥
yjjrqlafdmqenionyfj:
⇥
yiapcpbnwvjarhywqak:
⇤
⇤
⇥
⇤
⇤
wyaqynzcbbbtrtywsnz:
⇤
⇤
⇤
⇤
⇤
⇥
⇥
aqprqrffuuynznwcxwl:
kvlhxorlgnpolgybbay:
⇤
⇤
⇤
⇥
⇤
⇤
⇤
⇤
⇥
cnuusctciynasdabrcy:
ncuwyiayyjrkfteovqz:
vfyjjagndyjnturosbd:
⇤
⇥
⇥
⇤
⇤
⇤
⇤
nwxanrcywoakufpymrl:
⇤
⇤
⇤
⇥
⇥
⇤
⇤
⇤
nynbakibcdpnnrorhlu:
xixyhrbwilfgipmnwna:
⇥
⇥
seonyjqbvuvaurimudw:
⇤
lanympzybvxoaqrzlxm:
yyakafnmoraiseuiint:
⇤
⇥
j wldlywwnqrapcrhumgf
zcybucaqanbrcrnjqfq:
⇥
unfnuagfkylihpjfojr:
j fzruejapynkqamualso
wldlywwnqrapcrhumgf:
⇤
li   $v0 0
⇤
⇤
hrayyeonvinweuruzxy:
⇤
makmcjfadxyrvsaynnm:
⇥
⇥
ftjkvrnpfaobwtwnyas:
urorynaxznssdyltvbd:
⇤
gfyvjuzrhxemyymtabn:
⇥
⇤
eoiknajjybrmabhwzqd:
⇤
dnhybxmyxqyvrbdvsaj:
⇤
ovtrzezqvrdavrhlynw:
⇥
⇤
yqjczaexbjgnxgtrnip:
⇤
bayjrqwdynrjfoqbues:
tknyofvzyzimaygrnfr:
⇤
⇥
⇥
⇥
⇥
j ybktrbmaxdnpbtaygof
⇤
⇤
⇤
⇥
qqaeswhnlyglnzfyddr:
⇤
⇤
⇤
⇤
⇤
mpmraogazyhbqnqwbnh:
bnvgdddnyfxainqoqtr:
⇤
mkyeerywbyfhnwvatyk:
⇤
⇤
fzfdyufamcrfvenyfjx:
⇥
anvyzmzdjscwyurocdi:
djhabwcbbmbrbyctsnv:
whunmqlovxgyfalqhjr:
ajwmuipfngiglypfrfk:
⇤
uabvyrefvbjirenpamn:
⇥
mzzbsryysanihbwhacw:
rhhksnjiswamftmnrny:
yrtqizbsebnzcytnfka:
vztjynlpntftaybrsar:
j ayjyifvqiajppnwzsgr
⇤
⇤
gybunrjlvnyopsavsuo:
⇤
⇥
⇤
⇤
⇤
quqluynprnmaaybtzcj:
rytywrnhvfavexlsooa:
nhidysaardbbloxwvpr:
irparulbemhmbxnaydb:
⇤
oivyepaovoskmqwjnrj:
⇤
nffwngalrxkurwlpfyy:
⇤
⇥
⇤
⇥
⇤
jervrjanacoupbhyxwm:
⇥
⇥
⇥
nqgmphaorgqrypbgynb:
⇥
⇥
clainureaevyqhkcrkf:
⇤
grdgajtfccyywnzytgq:
zgkpuapxzjreyerofnk:
⇥
ybktrbmaxdnpbtaygof:
⇤
ocanxcvqbnraioyiklr:
⇥
⇤
nbyvrnyuetmagcdajxs:
nzyjhazhamlvykxeyrr:
⇥
⇤
⇥
dvzfygbraydsbjganom:
ztwprqtanwclihyknyp:
krmanypwwyzelneumcw:
wasgqfyadgngedwrcad:
⇥
⇥
⇤
cqnzrvmthnicbarvyjy:
nnnywfvyhcfqaruifuv:
aroujmnxmbyocpexpzn:
⇥
yndvolbzjmoyiahzura:
⇥
⇤
⇥
⇤
⇥
⇤
iernyqirzaqewyyodyb:
⇥
⇤
⇥
⇥
pgmtkrribnyvasyrnhn:
nyevxrwheszjaahtfgx:
⇥
yrywnxuryzipxjhjaro:
⇥
avsxqnagullkfyyzjra:
⇤
vupatyrqvytusnqyvat:
yetnomfwrevazunwqea:
⇤
⇥
⇤
rbnpnaobyhyejhavzvk:
⇤
⇤
⇤
⇤
⇥
hlzyoaajwnmedmhxrca:
⇥
fcoruxsnnxzltthoyna:
⇤
⇥
⇤
gkualbvfzyszrjjantm:
⇤
⇥
⇤
⇤
jfnuypbysramafazkny:
⇤
⇥
⇥
⇤
⇤
anucekjsgusybcsirsp:
⇤
⇤
eywnkjsjtbeaksmzepr:
⇤
⇤
frayeaafiruajfnhnun:
mzwftkwkwvuyrauanlm:
⇥
⇤
⇤
yarzouozsxmgcyxnhoz:
amptyrcuuievqhucern:
afoozdavrvneqvgyiwu:
hrnrxkyghhrhcaoghfj:
fhfryejaqmurnrshcab:
luzrxwnyoiktiksuiwa:
cajbwacgfzyonbpbacr:
⇤
⇥
⇤
⇤
awlixfryxnbgdignhyd:
⇤
⇤
wcabpvqyeufaanyrfvu:
⇥
⇤
⇤
⇤
vdrrzafnffarynnrnme:
⇤
ryystnpjiewjxixlaet:
⇤
ynlynjwrxfqmsyagstn:
⇤
kqvdagoysraagyyqvnd:
⇤
⇤
mvuwadhicayqmukumnr:
hlxyiysnmofaraeljcu:
⇤
⇥
kkertvnzgqeayxvsctd:
⇥
uohyreskqxnynnrahug:
⇤
⇤
⇤
wcwnyyrguypeqfbiamd:
⇤
⇥
⇥
ubptsrmrasjgyzancwr:
⇤
rmtnvxybocqnbvjvayd:
misohrfxfnzxyfqacym:
j nnylrsegypjbarwuwiu
⇤
nabommxrykmzrhshiqt:
⇤
nqaxamcyyrzchtfikqr:
⇥
rrbvdddnsnzyaqicpuc:
⇤
czimbtkarjptylfnkth:
ywllypudorsygbnqaka:
⇥
⇥
⇤
⇤
⇤
⇥
ymcmdzyganqmssyfrmh:
⇥
syjnynuacarnwdsnegs:
⇤
gywhnytyamrhnupknlk:
qdndzyaqrecdbvxebkd:
⇤
⇤
⇥
⇥
⇥
⇤
npgaqsagyzfwglvvrhd:
⇥
xdhrdppughftyfasnix:
wmgivaunysdxglrypam:
⇤
⇤
j mkictbygaqdggcuyynr
⇥
⇤
rcnsvnqicuqnoyhaaow:
yptmeercwhcusyynnaz:
⇥
irbnhrroamdrmuyfctn:
⇤
zwjdxyneyomabrlmine:
ceolhkmderytunoeapc:
apnzlfrmcjngsfyivnc:
tvyzxbhirqykanlnryp:
⇥
vyugwmjrgznutacagsr:
⇥
svuuayoruqinnmvnenm:
ylvngabmerxrkjlqvel:
⇤
yvcwpntaxnwrkbdrqkx:
plofgsgkxgibnsyzrai:
⇥
⇥
⇤
otqqsovnzrbeanylwat:
⇤
⇤
odzlpawocgzbrygdnnt:
⇥
uxoargnnzyweozkuyxa:
skcnahynlrwayxfbher:
⇤
⇤
⇥
⇤
⇥
⇤
⇥
⇥
⇤
jdabbcrfyflnbjxduvr:
⇤
⇤
nhrkdyqxbmkafaggxpd:
⇥
⇤
⇥
⇥
⇤
⇤
⇤
⇥
dgvjasrlpdnxdzadtyh:
⇤
ljmyantgoenjogfrrfg:
haodywzedfgvmaefnnr:
krbamplabnhrymrbutl:
aymgcjxnelgzibruwhy:
⇥
⇤
zynvrakykevsuyhzvtp:
fodyjanharrhdylhfyt:
⇤
j yaegnorxypczfgjbcpf
nadfkuqsbrhryykbdbu:
⇤
⇥
⇤
fcfonryonnayesunbel:
⇤
nhaiiybarvcfqhgxaea:
j avuadqrtyrngynnzmgr
yaegnorxypczfgjbcpf:
⇤
mnlvhcjaakuyfrbzvmx:
⇥
⇤
⇤
zreeqjqgndnxiyahcjl:
⇥
⇤
xyjdnaaxkpzrynaxdij:
pthnrupedyjojafraxn:
jnnlrefcancybaghybe:
xnnxrdyuabdrxgbhaok:
⇤
⇤
⇥
cyqkpwwysbcursnyaae:
ikamzqntyggznaurwni:
syfsbqjryiqnaaaypan:
⇥
⇥
⇤
uzwohgvevayicerfrdn:
⇤
ymwtpayeadfdikpfnri:
⇥
⇤
⇤
⇤
⇥
fjraksacjwtudbhynyt:
⇤
⇤
nlqnfryiakrbmuajjoa:
pyjnjmcnqtcxwrmawzd:
⇤
⇤
ambgurhbtxnadkukykw:
⇤
pjpypzrzlquuknppdaw:
zrbyokdbticaqnhqrnl:
mefsttrlnenegyibaga:
amqxvhjhuajrilytznc:
vowyptciakxbuunaohr:
⇤
raxsnzzylmruzjecnxb:
⇤
⇤
vjkyxdvntmrralwinyv:
vndnsvkhtnlssvbyarb:
⇥
nnylrsegypjbarwuwiu:
⇤
⇥
j awnoyauhdrbvtoyropl
⇤
⇥
nlcmlzqwlwrqgvyaywe:
⇥
⇤
⇥
⇤
bimvrgvwfxnyirfsdga:
j rtayxqtuaranygrdvmr
⇤
⇤
⇥
yecmganrapqinswgwej:
⇥
⇥
nrnygakpgwjnoybecmv:
⇤
awnoyauhdrbvtoyropl:
⇤
⇤
qgmzzrnvppgadxayhcq:
⇤
⇥
⇤
⇤
⇤
⇥
aqybsyenwbkkyugmxbr:
lurgokhnooyblivdarb:
⇤
⇥
mnisebddawvrdnmmmyw:
yvpjrhgdpvyezxgznba:
⇥
⇤
⇤
wdrtrysugmmjeapwnll:
rclcjmunuqncraiylur:
⇥
⇥
⇤
⇤
j erjntbdwwalodsymsig
⇤
ihabythfgrmerpmknnv:
⇤
j aeyfuorfmppxnnslgjy
nyolecavrnuzlyplise:
j misjfxhjyenranrcraz
aeyfuorfmppxnnslgjy:
nalfyvrapnriisbadcv:
⇥
oankavrppqlwynfmsri:
uwceirnecwyukhayufr:
j avsdrgmapryawrgansv
⇥
erjntbdwwalodsymsig:
⇤
aqnrnmjrqmyprqrvmzr:
⇥
⇤
⇤
⇤
⇥
⇥
⇤
⇥
wfhfranmraxchrhyxkp:
⇥
fonoyysnwtrabwxpuxi:
znsywidrhxzyrnhmina:
⇥
⇤
⇥
⇤
⇤
⇤
⇤
uwnecotcwsrzyffrfla:
⇤
⇥
iyyxyaxavkunhrcjpue:
⇥
⇥
⇤
⇥
⇤
⇥
⇥
nfanyzarredhjeskeum:
izynjpjujqrgakgynal:
⇥
⇤
⇤
⇤
⇥
⇤
wrzjhwboqcdapnyflqa:
tlntcagobsnxbyerhnv:
xomrntapfriwenarqmy:
numabrmrursuhlvgybt:
⇤
⇤
podhpjymcskaxgnrsyq:
onbdaukrygqspvgmjwu:
⇤
ntyyyejhqtojrmadlhg:
⇤
rvyaqspmnfqfvuxjywx:
ywleoabffpbljfnmcrb:
⇤
lalrazfnyyvgyscnsai:
⇤
⇤
bjmasfnqvvmwyfonpnr:
⇥
⇤
⇥
⇥
⇥
⇥
⇤
uxeairoankrbxaywzts:
ngoyzkykqxrrvahimwl:
mpdjxrinogrgjaluynm:
cpfwykoaaqgqrudnzvi:
⇤
⇤
⇤
kxtardgrhesynwwexyn:
enjrryqxysalxioyahg:
⇥
⇥
⇥
⇥
⇤
⇤
⇤
j xreyrtvzntscogtbaym
nrzdkbbyjumoviadzhg:
yujrflilredbxiaagrn:
j lrybnupugawxedzmrdd
xreyrtvzntscogtbaym:
⇤
⇤
⇤
⇤
yxmabnrnwrunvacasvl:
⇤
⇥
⇥
pbhsuaafoxunyrejysr:
⇥
⇤
⇥
olgyazbnbtliarqeqib:
spkyizaghhrnoowvpyv:
anarbyiplbmjtuldmqq:
⇥
lbixbohayrlepnsnvla:
⇥
⇥
uabalnhheizyqfrhsqc:
tnouodabkyctrrwaqgj:
⇥
yyarvkdwymjarzsznkg:
⇥
jrrangqqxnawmggtmyw:
hghryttadeknddatpey:
⇤
rwuafcnjrspkrbbsnby:
⇤
⇤
⇥
⇤
⇥
rtyfpbhiarnqeoylajt:
wgznyrynuryoggreaff:
iyngkataiwybqryyine:
⇤
tyjmagphyhxkrnazvuy:
⇥
⇤
⇤
j    return
wayqqomuamsglnjrkgn:
⇤
ucnjenmrbayiyagecvq:
yferzduckbvsnkhftao:
⇤
ntfjareaklwfoppnyas:
mlarjrkzmocfjrnuncy:
⇥
⇥
wqxnrmaicaltkdydkml:
unhrfyhadirryqanyng:
⇥
⇥
eymrvgbajtuvneqycra:
haryzknlyqumjdrrzui:
rshacmeenaykwxydevk:
⇤
else.4:
⇤
⇥
⇤
⇤
⇤
jfeyrxjlzonlehusamq:
⇤
⇥
avmkzryazrvtohuqkbn:
⇥
⇤
yapjxqrrewnawucoysr:
arswkylfwkvzdjnpyzn:
⇤
⇤
⇥
ogtejacqnhjspybytrl:
⇥
avhcxrtydjsfnqoxrps:
ryryabhkddqnualkfyf:
⇤
j wrupnyhjcjreplsarrx
⇥
⇤
⇥
iconbjwappmpyrqgpci:
xogbdaitpshyognpdrd:
tpnqzinhnanyobrpnlb:
⇤
⇥
almrnrqeyhamiriaobu:
⇤
⇥
⇤
⇤
qcfivnskrypsapedsgr:
adnjunhpdkeywzfmfrs:
⇤
j yyaaznvynvtuqriybdg
wrupnyhjcjreplsarrx:
dnxudvqtbtaqwhyrhdr:
⇥
⇤
⇤
⇤
⇤
⇥
nmjayrgjkbnffymvajr:
orfbwwfsreyrahenogt:
⇥
yalhyjabwhmigrntrll:
ebfdaranbrdohycxtup:
fwnjtycpqrjacnirsne:
⇥
⇤
⇥
⇤
yrkxouklbpxzsoynkma:
⇤
nrqhraprpxltrntcyqg:
⇥
⇤
⇥
⇤
gsnnrzvahwyjlyieknr:
apievyngvauftnltwrf:
⇤
nwtxqrhoptfysmkjlba:
⇥
lyamrgblieqyfyeqnns:
⇤
bbnukqktyprlyrejxra:
⇤
njrryarolhcdxvgdwln:
ywdjptvsryjbksnanyr:
kabnoeariyejhjcpahn:
⇥
⇥
⇥
xpxrvuxnopnixzyyaiw:
⇤
gpmnjyzkankqavronik:
⇤
cmmsaehrlntpvtseyoy:
⇤
rrjdhhlavlbskanqbny:
⇥
⇤
suetngypfrsuazcwkqv:
⇤
⇥
iehlmrqvqtimamnoyov:
⇤
⇥
⇥
⇤
⇥
qgyhaxltnqrjtfkxjen:
yeggznclydathccqgrn:
lkbsgsbobaaoejxynyr:
dynrcnzpuldnbooawjj:
⇥
⇥
vrbrlhyylankrfshpvk:
stsptnhkrixybfbygah:
⇤
⇤
⇥
⇤
tdaiwnarpxyiqzycrkf:
arybgnbvrdiyiygbtca:
⇤
rcvhqcakadybzcxnjhs:
gerxoguuduyftbaogna:
⇥
mgdnviuvwrugraorryl:
j blxnycgygpafkcurmhc
nabalyyaudqatqczkro:
j iezaagumjdygrwfxuny
blxnycgygpafkcurmhc:
⇥
⇤
⇤
⇥
rjniftdsrkyzgaexfkc:
⇤
⇥
moakuryqyypmkrsfnzf:
⇤
⇥
⇥
⇥
rdiohragancbauuryre:
dmqmulrpqkaprvjynwx:
⇤
⇥
j ecnyhohgalxicfirlfh
⇤
⇤
eualjnhrntkglufmayx:
lsduxnpryxaallqirdp:
j esnmzaajgcwnrypcako
ecnyhohgalxicfirlfh:
acrmsywzgrlnasnjkav:
⇥
rltvjszffynwacfygie:
⇤
acrymqnrxyymyqccbhc:
⇥
⇤
⇤
vakyspyqcruksefunej:
⇤
unrbpqhvzbafryzrehe:
ofogrkwalcnaniyowpi:
⇥
⇥
⇥
rjunmckayanqoltrakm:
⇤
mbrynpisrbbkpnfoakw:
⇤
⇤
⇤
⇥
⇥
kaufgkqmynfooeerlzd:
⇤
⇤
⇤
asssvlfargmunribkmy:
⇤
irvreroarownrwyebnd:
mrnzaswctylwkekskhg:
⇥
⇥
⇤
mfwnygtdkhisnisroqa:
⇤
⇥
⇤
⇥
⇥
⇤
⇥
⇤
⇤
⇤
⇤
mdegpapvyihnkwmarui:
vjniraiznyvaepiygwg:
rsnatwyfsfouzrhzxrm:
⇥
⇤
fkrocjmszbeanygvykc:
⇤
rkdhtqcycnaprvruxar:
⇤
⇤
wqclgxjsndwrwyanaex:
⇥
rkxgbtnalufdcyfkmnr:
yrabsrcrinxnehbcyhu:
⇥
⇤
j rinyusbjalctxbvngzg
yiabsnabfxthsslrens:
j wfvdrmzynfwafnisusf
rinyusbjalctxbvngzg:
⇤
roncycxnfnxrcvzblja:
⇥
uradidyqynhucaelgmi:
⇥
cadnyqvqihjnbrewvkf:
dercyvmtkhtowfbinal:
⇤
⇤
⇤
⇥
⇥
⇤
⇤
⇤
arytbualknfrbycqqdr:
⇤
⇥
rcyydiwnocsbhxvuzaz:
⇤
⇤
⇤
⇤
skbfzdrnjqeayeagnjj:
⇤
⇤
⇥
wlzvofcyinfftrancdu:
knxvzgybhirarjabvap:
⇤
nfjmyndrncphgdyahlq:
uuyvakgfiiyrpgaakhn:
⇤
⇤
yrglyhenlbrdtpbqxaw:
⇤
dysckouctgjbnzrpawo:
ejnarirvgdarhygnwpz:
hanryukllnyrnmscwbt:
arvxdmnrmohnybaaysn:
⇥
gcnbbfxkabrxyagtanu:
jaxkchhrqoyuwnwuyqi:
hhcnmaekujjfftsyrer:
⇤
⇥
⇥
l1 $s5
⇤
ndcurgwyrtektnzamsv:
adkrzqireerxaogynhj:
⇥
eurlipynwawcrlqusck:
⇤
eyrnznucrkxjnqyyanc:
nzrnhsgilubvfvpyasa:
⇥
nlcfopjkmatvyklrtke:
⇥
⇤
mkceersrnwyaxzojhuu:
⇥
⇥
⇥
etvwatylarnyysdnmdr:
⇤
gjknudfgkeglroaytpr:
⇤
⇥
⇤
⇥
⇤
⇥
⇥
⇥
ahniqrmxfawwzlautzy:
fxzhofuxwadaurynvep:
⇤
⇤
ahmflxjvnurlycrczow:
fnwihrqayapirinnvpf:
⇤
⇥
⇤
enqarvqrbpbnkdzuyzb:
⇤
pnicaswapryiraumbnw:
⇥
⇤
⇤
aspnyuarbzydsgwfjzw:
jgayrjaxfhlnxyrrcfp:
⇥
uakhcryhnxnpqynzykj:
if.else.end.4:
nunmrtadgusyuxjywpo:
tdaywfkskjndmapbyrn:
⇤
⇥
bqvonirkuwiivvmayps:
⇤
⇤
⇤
⇤
⇥
⇤
⇤
xrhtragbqsyyvkneyjv:
⇤
⇥
⇤
⇥
⇥
⇥
brsbnzhzfuatlfspwly:
⇥
⇥
⇥
⇤
⇤
⇤
⇤
⇥
⇤
vyyghrilnauuhrscaaw:
⇥
⇥
⇤
vmuinmaygierrnnvbko:
⇤
⇥
vntbyarqthhshuhxoum:
⇥
wclmrsjdeayyhssrpnm:
⇥
j loop
puzsnpryzsmhpsajxsn:
niblnryxkghsacwrbst:
⇥
⇤
j xrhbquamtpoyjgymtne
rqfpkaovbzkponyeyto:
j ppwnffacsmelkbryrri
xrhbquamtpoyjgymtne:
gqceyynardldeggsneq:
⇥
⇤
ayxjgrhzufngcrzajrc:
yrduuaqztltpepizyjn:
⇥
⇤
⇤
rduluzcqynzalbthenq:
⇤
⇥
⇤
utnibcrtneyqayeubvx:
⇥
⇥
⇤
⇤
ayaqluctpecknxurjea:
⇥
⇤
amjryqycwfnnlvlhklp:
⇥
⇤
⇤
ynydtaqqkfehakernwk:
⇥
⇥
pnuevuddxnqyjfaoxrm:
⇥
⇤
ioarhhuvnzrmrcabwyz:
⇥
⇤
⇥
akfuavjvljrsgeyhoqn:
nwlkbgjparnyykztvrc:
abhznsryuagwqbkksrs:
xwygajualaszrcmzven:
nxlrduaxtrpkriyvdqa:
⇤
⇥
alnlplgxpjyqwoiispr:
⇥
⇤
rnleaykrxecvdsvmipj:
⇥
⇤
⇤
⇤
ncbtbzvogqmraafwyye:
⇤
⇤
⇤
xkgppziuzrcakthydnm:
yagnelxwdrjznayckzy:
⇤
oqdnyddyianyrewmwxe:
rldpgvairjanarnqayh:
ruohxcnrfazvuywrsca:
drofyiedyrlajuunnpa:
⇤
⇤
⇥
zaumnlmsfqcpdyytirf:
nikdearrwakfbpymobk:
⇤
⇤
qrtnqqyfuhcwbsvjhar:
⇥
ybdjbuwrcaepnbzaqpt:
pqpfajnjtrndvdyokix:
⇥
⇤
⇤
⇥
⇥
⇤
hyxlokijnmprwxtaaqz:
mgmptwaibgrzrolnjfy:
⇥
⇤
⇥
⇤
⇤
⇤
pnvrzdvtjyqdtifursa:
⇤
njsklqrzjanbirdsywz:
riebmyynbeyayzptlro:
⇤
⇥
mryweynfhzzrjakaqgr:
lbnaiqhdsynwidktarn:
leyonrbwkntspaauxdi:
⇤
⇤
⇥
⇤
⇤
einmivvrxbeaoayzorl:
yemngarkmpqkebxaalw:
⇥
⇤
⇥
⇤
⇤
⇥
jaqfxvnlrmzluamseyx:
⇤
nolvyipmuwroddrrdea:
⇥
sorcafmbkrnilhlybjn:
⇤
⇤
⇥
⇤
wcvnktupiwwrarpyher:
⇤
⇥
⇤
⇥
⇤
rthnqzsobagyenyicdp:
⇥
⇥
tmthymnsrbvataiutdp:
rjqplkrsbxvywndaere:
⇤
⇥
⇥
⇥
sjmstyzeyrrckuenack:
ansxnrlgrzajqdyezem:
⇥
⇤
gnnadrjidlzkyuogklh:
⇥
⇤
⇤
ykfhtharhkkgwjncune:
⇥
raganbgjpszjzyfaoyb:
kjvrenhnavattrswryd:
⇥
hdkayrawzygbzywyfnz:
⇤
⇤
return:
⇤
pop $s0 $s1 $s2 $s3 $s4 $s5 $s6 $s7
azmbyrfcqpnwngczrup:
cgnxurqeuhynxadknsn:
⇥
hshlxvocyiilnrawyvu:
⇤
⇥
ewefaklbvhnqwrrpyjr:
⇥
vaekbrcchlynuxsdabz:
⇤
kdfjzgzyfarfwbynigo:
takatjvntryzgjotmvr:
⇤
⇤
⇥
fzugiqvwnudgayrxxqs:
⇤
warllvncczyocevyfyb:
⇤
⇤
⇤
jiypycycpzbnarjohnn:
ronbacbnncymscladkx:
⇥
rylcuqawctrpyzfqzrn:
ayrctjtpynyjnrtjarl:
⇤
⇤
⇥
⇥
⇥
⇥
⇤
⇤
⇥
⇥
⇥
lleeaansuzynwwrgcro:
tamjynsyefwsrfldyqj:
kngahfruovlbqkrvtyr:
⇤
⇤
rranptnaahpsrpjyqhs:
hwgvhjcntralshqnyie:
⇤
⇥
djbnwmabwwdvlyjftru:
⇤
fhtzwwaszyzhhhmnpqr:
⇤
⇤
⇥
⇥
fsdyriofxnhyiaxwhfk:
⇤
hgzagryzlyivaziqnxm:
⇥
⇥
awkyzjfihanoyaavvrx:
tyrmavsnccjzkrqwyhi:
⇤
⇤
hklvyyrkzsnqajztnbr:
⇤
⇥
uhtuyxqjqanmacgikrj:
j jhprryxiyaxljegnato
xybfuatggotrntjdafr:
sseekpavpwmnuduprby:
sfnrzuzdwklxyqnwina:
j qryddvrijajwraaznxo
jhprryxiyaxljegnato:
dfztmefvyoawxchybrn:
⇥
⇤
⇤
⇤
dvgurpuaszvfvcgyncb:
⇥
nadrryfnyajmwvumhea:
⇤
⇥
bxwfybnkubvtzacaran:
⇥
⇥
⇥
yanxyyrdroktglncrok:
wuxbpeypjlcfdsroacn:
⇥
⇥
⇤
⇤
⇤
frpfpxqnlyrynyprarr:
⇥
⇥
tkmnqaznerwngqoftwy:
⇤
⇥
qubpdrasxsydwbzexna:
⇤
⇥
jnezcnwrgrynaluachv:
⇥
⇤
znyjmurkxtaxcmanrbq:
⇥
⇥
hgatmlblqpryqrobnra:
zikslyinvsntrjovqav:
nxpglptarflxaygkbgb:
⇤
ljluybezhrkkaunleya:
⇤
⇤
⇥
⇤
⇤
eyhajqvdqnlauhirrya:
rwknmdzlfracplkrnye:
⇤
⇤
nayialdfctarzwzqntw:
⇤
⇤
yjkjddarlovaqmnwrjf:
⇥
⇥
⇤
rvblmrvywoyekzvvtan:
⇤
⇤
riwzaydirxbnrapoynp:
gncjfadymtarxzrwizb:
lhzlriagkckrnfytpsr:
mwqwpnviudzyaytrhvn:
aijgcoohporytntnxnk:
⇥
⇥
⇤
⇤
qljfgodainlkdyynhrg:
croizvnnkogxarjhylx:
vqaxoaiizxmzrcynutd:
⇤
⇤
ynurtlessxyhsrcllwa:
⇥
⇤
⇥
⇤
ymbdgrelftnaroqalqu:
kazirvvdjmbxtycnyyv:
⇤
⇥
dvklarlcnnavcnchuyj:
⇥
⇥
⇤
⇤
⇤
⇤
⇤
⇤
⇤
⇤
tirkjsayqadlnefpvyv:
aizrlrranrfdqbmtgxy:
ucngoiincmchacyrtvu:
ndrmtzndutyxmannitt:
⇤
⇥
⇥
⇥
⇥
⇤
⇤
rlaqlgrbqcodfonryor:
⇤
bopzqfaxxyrdnrxoduf:
⇥
⇥
⇥
⇥
⇤
cvkaadrngqkfyemrnta:
⇤
⇤
chuejrjwpyxavnihkon:
⇤
⇥
⇤
⇥
⇥
nvyagfavalabuqrjoel:
gcjyqyaxygorkneocrn:
⇥
⇤
⇤
nymnzatefdfladropst:
⇥
⇥
hiefxvsnnrlybaunecb:
indchtlpygrnckkmbpa:
wajjgyutbccagmerinm:
orufonwkxapnmddbyyi:
⇤
⇥
⇥
tyysrayxrfchlnltzky:
cazgaqkypsnnfjsbrvy:
⇤
⇥
dbimdymfbpnrntpapvk:
⇥
⇤
danurndqoygjyhpugrt:
⇤
⇥
⇥
⇤
⇥
⇤
⇥
tmigauiqdwynqbrcrnk:
⇤
⇤
⇤
drhacytbbaogskmgxnw:
cvmnznprbxyqubikfas:
⇤
⇤
⇥
⇤
arxxejzuyanybqkuajb:
uxwnsyqsrizifarujgx:
⇤
⇤
⇥
jr $ra
j jdbyknrrqagdynydevn
⇥
ndyijycrifyanlzneog:
mkictbygaqdggcuyynr:
⇤
⇤
⇥
itaenffmlrjtthyzmsx:
⇥
⇤
⇤
vymltzpmxjfxarnsexo:
ndyeqhdlpknmivuojra:
nzbepnawxfozwqyrgyj:
⇥
hnanpumtyirbfawrdro:
yxhwdazllhyrgdjinvh:
⇤
⇥
⇥
mrjaznadnwnwywgyvnr:
qprrstgyqndjaguqidq:
⇤
⇤
mafnwaybrtonavcgujv:
ilrftfuedbnaygkbhyz:
⇥
mul  $s1 $a1 $a2
⇤
⇥
cqersahrnnvzjvaygzi:
xbrdxnqzkomefazydna:
⇤
⇤
ypktenqvfywpntyarzd:
zunaeimgrjfqyngilfw:
uryvhwqhaltptbzrran:
⇤
⇥
⇤
⇤
nousnjsyoyqaazkrxcp:
⇤
mxwyaqrlbqlnstlbwtw:
⇥
qxmmbazeytxfgrxnfro:
ymndrybprnucgkfacjl:
⇥
⇤
jrvolaadykevnknqdja:
⇤
⇤
⇤
⇥
vsympanvfsgsrhypyxj:
⇥
cdsxyukwdqarhntratj:
uaygfrfwwbeusuxnwnc:
⇥
⇤
⇤
rkwhunnayzahnbhkqfl:
⇥
apnewnoeirsxwtylypj:
ndfxtgrabfevpyxiqyn:
rwrblkrcdatnbrypgks:
krwnnnahbjhzstlvwgy:
mzfhlrgxvjsjaysylsn:
rvrcpgfawcjynwhtnnp:
zgagrrwjyngqrdavjxy:
nrminrcbztpxwtoyadf:
⇥
⇤
⇥
⇤
⇤
⇤
⇤
⇥
⇥
⇥
⇤
vnfpylcrnluaoqzrqis:
vespnsdoknuyraxnyqu:
⇤
⇤
⇥
xbozbasyydrkjtnzblo:
xjldrhcavsldjnxwyya:
gabqymorverawprtsyn:
⇥
⇤
dslrnjomahynttxlbxh:
rpakynryskadtlreqzm:
⇤
⇤
⇤
dridlxkwdmseunyrnaa:
⇤
j illjraxtpywgondpxfv
⇤
qkkrzagfoyaqxthshrn:
ewqqriiewprkgypdnfa:
j jlpjerafjyfpptncxhh
nszpfhbcmyxwiadarhx:
illjraxtpywgondpxfv:
⇤
⇤
⇤
⇤
zrmlnenaqjpfzyytefc:
⇥
⇤
j mzpkvxcnqyhhcqaxzrs
j wgurdyycxhawqwntnbr
gnfmgymozunepmrcwoa:
venvpdvhlarqnwyzvgo:
j nlxatkpyrryfyvysmyf
wgurdyycxhawqwntnbr:
⇥
⇤
qcagztqngrfylonruyt:
⇤
vzfbaftcyxcnaajrstt:
qypqaqygvvnrxyryvia:
uojpyenczhdivcearey:
j uavbyszpdiafyrcnmfw
⇤
⇤
mzpkvxcnqyhhcqaxzrs:
trmpefalzryncrohepv:
⇥
vdykktsnutldryjtaap:
⇥
⇥
⇥
⇤
⇤
mul2 $s1 $s1
⇤
mafhdhelrpdqanyzoys:
miytjmqvyynqxtlkmra:
⇤
hcrxbwuqygfgavnkxol:
arapabkrjynnxqzdxpd:
⇤
⇤
⇥
⇥
aimxdfxnkdodurckbyv:
xpahrnuwqtqynehhvaa:
⇤
rnfgfmnqhbciibayzmi:
gpsarkzioiuumznqity:
⇥
⇤
⇤
⇤
j hormwnebgurdazipyoo
iezaagumjdygrwfxuny:
j nzntmawauspjdtymfrd
⇥
hormwnebgurdazipyoo:
auurndcnrnjvzomcgyb:
⇤
jgurdradbedhunwvbny:
eqnmzprymmarkpapyfi:
⇥
⇤
xpnzryoxorlxtsbaazf:
juwfvasafeqnkgykrhx:
vgnyszvhabaajrwfsqx:
yylenrjwdyatjfapebr:
yrnrsxmqdooavlxpbjy:
rymclpcankjbzhjaevt:
⇤
⇥
⇥
⇥
vznfndoayhniysdanor:
hkvswawzraanyhhmnvi:
nysvaherspphxyjwavj:
⇥
⇤
eadrdgknryftnapktoq:
ygpiaatfpnniclrwvno:
⇥
⇤
⇥
⇥
nmlckwybvjnnlatrnqa:
hgkmxnlhkoinaayxusr:
⇥
⇤
⇤
⇤
⇤
⇤
⇥
vqrlqrhypyawnmyuyub:
⇤
⇤
⇥
⇤
bbarhknpkvrvkywyjdl:
⇤
ysfhwrvxgnnccayrytv:
⇥
⇥
dgnoznkqgornhywaeuc:
⇤
fygulnjaoielmzzrczf:
avzaanmhjalhsxircpy:
⇤
⇤
⇤
⇥
vrbzyvnsaqazdmxhwpv:
⇤
⇤
⇥
⇤
⇤
⇥
⇤
lbrpcmchcekramsapny:
⇤
uopydtrumqaifnnxazu:
⇤
orgummaanhwnmzyewig:
⇥
⇥
⇤
⇥
add  $s1 $a0 $s1
⇥
⇥
⇤
⇤
⇥
hsaohmtjnnilriduyby:
⇤
⇤
rnokhtfiqolyfayfpck:
hrdgnvmwjxtbbawauyy:
⇤
rxajsneiwehscdaqefy:
⇤
⇥
kwrtrovdyaxlxlqhnbj:
unageukpnreomlynshs:
⇥
⇤
⇥
⇤
⇥
zckqwwnvnbzaixyrvnu:
nampdsfeaircrmyadcx:
⇤
⇤
gaynxmecsdmbarhulcn:
⇤
⇤
nyrzjaclysovlbiyhys:
⇥
move $s0 $a0
⇤
dynmdlcqrfgkdllasyy:
nemqbreyguwlpaxunsu:
⇥
sqfyyrikducfafnechy:
⇥
ynmgnxwswgsemmfsrma:
⇥
ffafoyafrvomnnqnntd:
j fysrinbwtlupawuwinx
ygzemqrncgagavcmjoy:
ajqnvvwdxrypsczgnml:
j rqfpkaovbzkponyeyto
fysrinbwtlupawuwinx:
⇥
rhyvaaxtyinjpeyukae:
xvynwzioroupbjvnane:
⇥
⇥
nyyyunimahbravjnoan:
⇤
ioiyatnmfcnswxliurr:
⇥
akrnkheipyrbvpkiket:
wwxiypqmmxgnajmdrgl:
ingizeadigfgxrlaybf:
xaypnismmwqaprznmcr:
pggwywawyreawnyowbu:
⇤
etiprnezwnmersyyeam:
⇤
⇥
⇤
fsmayktomnhnyyyvrms:
⇥
⇤
⇤
rncnezownhjwzsamnry:
gbbffsnnroaiyhvnops:
⇥
rvhyjjralkaeeiencxc:
⇥
⇥
⇥
myaeqjarzpajhnyjnyy:
rnzxidwnynpvgavjqnj:
j yarcrypnjhivxetgtgb
nfjzzvhgcshrxytdsao:
j afyxrapntlsierunglk
⇥
yarcrypnjhivxetgtgb:
⇤
rnxgdjqwazlkygqvujw:
fsnkuamyxsasqwrrnza:
⇥
ytmlpwiabanbvxcodvr:
tdplcxacplyarrynewo:
⇥
⇥
⇥
⇤
⇥
bzedyhtamqdonhgmzrf:
⇤
⇤
pwmdanrtlxnyjnynssu:
⇤
gbagtgyrdxiicnslenf:
⇤
⇤
⇥
⇥
⇥
phhnaltprhnoyherhed:
nxfyrmzulakozmlfckr:
⇥
lrnafzkeldkeecpnisy:
⇤
⇤
⇤
⇥
gulnafrfyvjdqsuvulx:
⇤
hmpaohwvaywiiyjnbyr:
⇤
jispoxyarjfmhoqpmny:
j qfdvpfewddhexnlgayr
bnscwnqoavaiomfxywr:
⇥
qxanhypyyrqwzikivvy:
⇤
⇤
ecdfryoyannmailczje:
⇤
arlugnjgwsycptsezpa:
j mmpwxandkwarrwydbwf
⇤
atzybniaatrrrggdbof:
⇤
⇥
vrhwelocntcxyxtxauf:
nhsliwyugaybxrkwoqn:
⇥
⇤
⇥
⇤
⇤
j nqtznkcfunnyapartug
⇤
⇤
rxnaswvayjjanonndrf:
xwgmlreznycufvgzvar:
remlnkdryqgbjiljrka:
mmpwxandkwarrwydbwf:
⇤
roqygnivimrolppndad:
⇥
⇤
⇥
vohftrtieadungycstc:
ypdkagmpcshnanxhgrs:
⇤
⇤
⇥
⇤
rryfdenzafdmgxkzyhb:
nyuripmckxkorqhamif:
⇤
amykqdrcmfihrznnrqk:
vmaotcndmmqrwfyexcu:
rbmaqypkorlmnirbngo:
⇤
ayjyifvqiajppnwzsgr:
⇤
⇤
⇥
⇤
⇥
yvnrwhagapwenanbgla:
⇤
yrsoqljqdmomfomnyas:
qinewicjyanxcuomrna:
⇤
⇤
moyzpzbaavnmhfgwrba:
pvmyindgfeabsrbrlin:
⇤
dtetzxhnijpomgprapy:
⇤
⇥
⇤
⇥
rxstfoltnhpasyyvgsc:
aypqotztzxubjroudtn:
⇥
enrdelnhounubmlayha:
ezlaqtqrwiqmiyaufnm:
ldyyluafbdnsrzaywpr:
⇥
akqpageryoqzpnybkms:
mnanvtzpyubrhegwyku:
⇥
⇤
rpsrverftaymhnmdxlm:
bwfkwxifnomyvazdvro:
axyzksemjwnkrjuqsma:
⇤
⇤
jxrryjjaynrcnywqrks:
⇤
dialxyxythmttprjgqn:
yfjdarfpdgnnukkqert:
⇥
⇤
⇥
⇥
erowptynmvcllrakbaf:
tcynvosooznxnrrbjxa:
⇤
⇥
⇥
⇤
⇤
⇤
⇥
⇤
gcjynmsiczserbrhaha:
zjnblmaayychamarnog:
xunhvwdqsgabrwcsyvc:
iqvnaybnfmyydwrrmyz:
⇥
⇥
twdhnnykruzdvhhfgva:
⇥
⇥
⇤
j czimbtkarjptylfnkth
⇤
fxmueryonvnyaygmura:
rppodnflxdyejhndqas:
timdrbrasygyawnudto:
⇥
grueioxzyvyraevntkw:
wbvqxariyuliygpmsvn:
⇤
⇤
qjdmehttrefayhrnajn:
⇤
⇥
⇥
⇤
trjcrpzsabnynuiwqcy:
tcjvrapjkpytnhjmksm:
⇥
⇥
⇤
⇤
⇥
hhinysayilzacrwiifp:
nyrybpgpxcjmahfgexn:
⇤
⇤
⇤
⇤
⇤
⇥
pryanidkeaktgeqjbnl:
⇥
maenrxiyfdrtpanltjy:
⇥
⇤
crnuqjlrihrgeyarydz:
⇥
joryadqykdcwfzrgnxt:
⇤
⇤
⇥
hvwzqymnzargtmaoynt:
⇥
⇥
⇤
⇤
⇤
rnmuvadryfovyviawti:
ckkcfeswndbryoaamne:
⇥
lguhqnmhwoeyqayrmza:
jnkzikhrirvaynldxhj:
⇤
vhriaayiwvskendhlac:
rnbqelyyjqazhxucazb:
⇥
swjpnarryvnaluoomeu:
ueyskfakuvvagnruean:
⇤
ayjonjwofaaizvbbrnw:
irnpoereelaxoyaxuqw:
⇤
⇥
⇥
nrnarbymriyptnyqvtl:
⇥
qfpakszwnvgjxpntyer:
shnnfnqlfycmarmtbra:
⇤
mhpnnyqkfrtdwvtauyy:
gcawbsxyvermenwyunf:
⇤
⇤
qfdvpfewddhexnlgayr:
nrcwazbfearclynufyx:
⇥
acreenyorgycxpiuvha:
rrsdunzyvlwqarzxhxc:
onnsklawyjknyuzsrtz:
⇤
ugkxxoirnryxttxaanv:
⇥
⇤
⇤
⇤
dhoirshanjzaylryxfy:
⇤
⇥
uyaoramwuieakknamnn:
oymbthbnxqgamarpfsr:
foysjsakroyjhaknxcm:
⇤
⇤
⇤
⇤
⇤
⇤
muirsofyrbqfannraku:
j ajcolfyyrbnigxghutq
tfptolddlarnlgcywah:
⇥
nrvgsuqgxnayyjyagtd:
j almrnrqeyhamiriaobu
⇤
⇥
⇤
ajcolfyyrbnigxghutq:
⇥
⇤
twnmkyhsnftzrbzajaf:
⇤
⇤
⇥
⇤
⇤
nyxesarctqoayinmfdi:
⇥
⇤
⇤
fcknuglrkdehuyyairg:
⇥
hyqacfnysxmxgtnwjrd:
j znbmaacsraayenkcoht
ppwnffacsmelkbryrri:
j daxgbrfeuwnnlzkqryd
⇤
znbmaacsraayenkcoht:
⇤
⇤
zapwcnvaqaoreptxbyk:
⇤
⇤
iszzfawscweybytrtnj:
⇤
⇥
⇥
pkremaebuupbtsxsngy:
ogypeqyvypqrvkqlanv:
wzznhorbdamnpytxuaa:
byatdfijmkprlilhnuk:
⇥
lqarnrdfxljounyaegb:
kwnrcyaryxzyvouhvbp:
obyrhhhomhkenankcsy:
⇤
⇥
ukvxojydpkrnwfqutha:
⇥
⇥
⇤
nerpxswaaaynlybddrs:
⇤
⇤
⇥
⇥
⇥
qyprmgganwjxctnntwv:
ayqrkhoxcipjwanadda:
crwoqoziylughnlatzb:
⇤
yanbycxsrneqhubnakr:
⇥
⇥
⇤
⇥
hfrarcmcxyncqkjhodc:
⇤
azjvqgxenasmrmuyykq:
nybrypuyyakhvaxkrbf:
vetldljctvynmsaerry:
⇤
⇤
⇤
vdnynrrpqpnymeqnzwa:
ycaagymnzrffudfcklr:
⇤
bge  $s0 $s1 for.0.end
nnwqyaadaxoqdskscur:
⇤
⇥
⇥
⇤
zjbswkxcjarhdrnrywu:
⇤
cyojvzgdegbanfrngfi:
⇤
⇥
⇥
⇤
juyitvnexavyourngry:
⇤
⇤
⇥
mddisafloyyrfufyxno:
⇤
⇤
⇥
pfnqhgeyfyqawyopozr:
⇤
⇥
ynowfvrbxflgmnmhaqq:
ckdhfsumgyrutaiknnl:
unrauycnwhppxjncvjx:
j yamktloraodbfnvzwql
misjfxhjyenranrcraz:
j otyofacuyedwujrjndc
yamktloraodbfnvzwql:
⇤
fnoyrwmroiyqgatnzgc:
upanzwzdlnnpxqrsyuz:
j nlmrcsrznrvcbfuyvaa
daoyxybkraantyarggq:
yagetyltvcagnrnslmr:
wxbribwhkqxroapaney:
j ydruokycvdmpawuyurn
⇤
⇤
⇤
⇥
⇤
droplsktynluiwliayt:
nlmrcsrznrvcbfuyvaa:
⇤
⇥
⇥
⇥
⇤
⇥
sioxjejdksunfyeqavr:
⇥
⇥
mtbwyvagiaeniqfrswa:
⇤
hsxbfbnjunyrrnhvxan:
⇤
⇤
⇥
⇤
auqvuhosyanmchderwn:
⇤
tqgvednyluaqhaakirw:
ssyafkibarnlppdzceu:
⇤
objtrfdfynjjxaoprmb:
rxpbprsytgvnyjdxaai:
⇤
⇤
⇥
⇤
⇥
⇥
⇥
lyehwxtkjnansktryri:
frcshyyglvnwaonniju:
⇤
vbdbdqrobsyfakagnan:
⇥
ohysbilndatmdzrptar:
⇤
ubonjnvvyyrkczzuyag:
⇥
⇤
gurbfwzlmausyvcabpn:
⇤
⇤
⇥
⇥
⇥
orvfriczyqapazdhhnq:
argwnncdeinfyohxyzy:
curjyymrjzygfyknwau:
⇤
⇥
⇥
⇥
⇤
⇤
⇤
⇤
paunseawpbroyyqwyrm:
kvkamzcfynoinjtveur:
⇤
j drybwresenbyqkinabr
⇤
efkaobnyrvasqnsbupj:
⇥
⇥
⇤
xrnpswmaeygnlnuthxi:
cneqzwrtvnynlscaxvl:
j uwfripztjictbyhnaan
avmympxanqtfirgxmax:
⇥
⇥
ysmryxnrojayihyzjir:
ynturqkfprwmactztxj:
⇤
⇥
⇤
rnnwyfblsmgalrpdvyc:
⇤
⇤
⇤
lvxksdwgyfmncarguxm:
⇥
⇤
j nkmhcbzrfynmtymmgna
⇥
uwfripztjictbyhnaan:
lsraoeacnlsyrcgyazc:
⇤
⇤
dlfyrazojsnofsiunqt:
⇤
⇤
⇤
⇤
⇥
⇤
fryiaiafiqdquwoghon:
j cyinbxoocvsaksrqnnn
drybwresenbyqkinabr:
⇥
pwhrnptfqacsodyaisj:
⇤
⇤
gyeavwhblssdndhsrer:
eyuaztvvrrgwcadknya:
⇥
⇥
⇤
dunnqzyrowcwtraycmy:
⇤
⇥
⇥
⇤
⇥
⇥
zckslkmratrnogyiava:
lzmvxahbgjsnryydxme:
rykgepyzpbqdezxqanj:
⇤
⇥
wmyptahnntrhnbzvavd:
⇤
mrbbtyaucnceaohrnsk:
eykaniaioedlergkjnx:
rzuedbsynacimnwlrye:
⇤
⇥
vrtatmtcfhiajkcsfny:
rfinohanyurpqvbjiry:
⇤
zyyfxarfmehalxnaych:
⇤
nnxeyfaarhgermbfmyj:
⇥
⇤
⇥
⇥
⇥
⇥
rsmuwiaoamnytgoixon:
j rupmyqoghonrthaqcad
uuuavwycwrymyenknaw:
esekngtmeqkgyiadvre:
j cneqzwrtvnynlscaxvl
rupmyqoghonrthaqcad:
⇤
⇤
auvjsanylyzufynirxi:
⇤
⇥
⇤
zamwytpsryywnjpszjx:
trznlpyrvxaynwmjlaz:
ufynxwxyudtxrjvzyoa:
⇤
⇥
⇤
⇤
⇤
cbnyhrjbakobxxahcyp:
upntnrroggwygwqwnaa:
⇥
⇥
⇤
ndnceltuyvweaudarpv:
⇤
⇤
j iweyyueafbyflrdnolm
⇤
vtjtarlyuwubmtxnumy:
ucybyizmhaxwaqerron:
⇥
nmztryfiamzpkuyanto:
⇤
⇤
⇥
⇤
⇥
⇤
⇤
⇥
⇥
j fsknpovikrdnyfacqae
⇤
⇤
lwlsqdrndlyyrcajtni:
⇥
⇤
⇤
⇥
kbcanxjxrunldurqyyo:
avxjyjahlnyvntwhwro:
harxlfzkvnavijbryiz:
⇤
grexnkeadaaikrnemyi:
⇤
lcyasrnxyinofplxbhw:
qyxgsndksndrhkimasy:
⇤
⇥
⇤
sjakslrfafhjarysnbz:
⇤
⇤
aoypjysaogmpohorpna:
⇤
⇥
⇤
⇥
⇥
⇤
ynokirtwluuehyaluua:
nwlauryambbsayxinrk:
yhtvorrvvhwgahhnraz:
⇤
⇥
⇤
qckdseayxnaksbdrypc:
vjoyyyrczyrtasrenqt:
⇥
iweyyueafbyflrdnolm:
⇤
lzoxkrxndcexwoytwal:
npwduaqkgrelfnemyhj:
⇤
⇥
⇤
ffrcablfyfnccnwyvre:
spncpyicakwlzbqrlqr:
nchxbvrabkfuahdtwry:
znyscubruefhaoqywky:
⇤
⇤
⇥
⇥
oebaswfnesfxeirygka:
dwtxnawksuwsztfryph:
⇤
⇤
⇤
for.0.loop:
⇥
⇤
sgbpkrmxydipncvyaxq:
⇤
ywhhoqhnarpiiojbjch:
yaqzankaluryxveoone:
⇥
aubsuaymmcvopnhgyrc:
deopglhqyrklqfnanba:
⇥
rxqhtabaronfkyvxpva:
⇥
qztnbaodgfcprmzyeaq:
⇤
⇤
j konyppkeagpyukrkrvo
jbqyywvadwqngwkrivf:
j mcyqavjrvzlyanrrplu
konyppkeagpyukrkrvo:
⇤
sffetearewsnyipuidx:
⇤
xqakontcatzyyfevdrm:
ayrkfaktauykoedwkon:
⇤
⇤
⇥
⇥
⇥
nrgkyleidvtaagerane:
lcskawnonoamryqcfve:
⇤
⇤
qfperhknotrtqczyyay:
j ablryvdkflrrhnjfcza
⇥
nkmhcbzrfynmtymmgna:
anlzvrpopyaomaiqayg:
j pmnrlrynprpwpallnas
⇤
ablryvdkflrrhnjfcza:
⇤
⇤
ofcfgaykldsdybkrnai:
tnyereyvzvuygadcysu:
⇥
ianjocunygvyurvjgzy:
⇥
⇤
⇥
⇤
yyokqacrprkjyvinxag:
aarxiylnyrfxkhhnbfn:
⇥
⇤
uaurwicsxcvyxvbznhs:
⇤
⇤
⇤
fqgjyymdtiawineurpu:
⇤
⇥
⇥
prddrmynanhgkuyterg:
⇤
pjurnbsvunaywhwwkgb:
⇥
⇤
wunurnyaflmlxnotvae:
rnrfityawgnoknyrppp:
⇤
⇤
⇥
⇤
⇤
pitbndqeagnrkryzeyg:
rcvubcvxasqyobnkpry:
⇥
ruknfstelrekzehacfy:
rnjezjjcjixzevanvys:
yakqonyhrnnotcwcykx:
⇥
⇥
⇥
⇥
⇥
obwaeyyyfhdlanrhaer:
jpmgwndlkxryalxgjin:
rwvistihywnkvnaiczh:
⇤
jzaybhrsntrxqnrcuzn:
⇥
kpxnslrolgxvayjoyyw:
⇤
sfygvmaonchjdtpranm:
⇥
oirbyxkfasebtaaozng:
⇥
⇥
bkydhcacigknbgxryad:
⇥
⇤
vdvatxihfrnmjaeyrza:
⇥
⇥
xcuzbkwrivyrnsxrhaa:
xynrduanmjfmxtaznvi:
⇤
⇤
gxpzurjlypuawrgynaf:
⇤
⇤
qpmsihicqayrnbvvdsg:
ynurimhizinvuarjrqv:
⇤
⇤
yanygeguobrjthrifjb:
wwwnrzxzoyfycahvyhw:
⇥
⇥
⇥
⇥
lvssrijzpwsnyatcsry:
⇥
⇤
fxaxeqivotverkxhnys:
⇤
⇤
⇤
⇤
⇤
xmqneamfatpfcryyryn:
⇤
cfeubyonyurnyjnajaf:
fuhwvyajnqycoryfcuw:
aflwgqniqymudppjrin:
⇥
rcnjwcogtnawkyvjtfm:
⇥
⇤
vonirymtojmfkurayha:
⇤
qbvnqqcjjaaymrjcrre:
zdshouaeorvayrenybe:
nooxyvyauguctqmrvvx:
⇤
j yaadarbfmucnuwayyga
nqtznkcfunnyapartug:
⇥
aelryxlvhlyeudnnxqa:
⇤
⇥
whlpknhfyazyakrymrm:
ovtliryalibchanrzws:
⇥
j fnwplbrfuanbnyauujr
yaadarbfmucnuwayyga:
⇤
xgljixhpvhyanykwwar:
j orapsevtfmmixuymnkz
mhvnpvgxnynoxwarrkb:
j kjxokefjqniqauyslrv
⇤
⇤
⇤
orapsevtfmmixuymnkz:
⇤
⇤
mpbfyjyajdjuarifnad:
⇥
zfzdiuxnyvgmrdccfaf:
⇤
wlrnoxkavtusldnaygh:
dgjyvuzivbnravipflc:
⇥
⇥
⇤
nrhbmdkfdkscgaykylj:
⇤
mmnajyurzjinwxocemw:
⇥
⇤
⇥
⇤
⇤
⇤
ubxvueqyrdnzvrmqzia:
wmnjyywwhnjljiujnra:
ndsjkawcrndbpxyrykx:
⇥
grunzoxxwyiaxakxukk:
⇥
oordwyvrsavjcjyengd:
⇥
⇤
⇥
xdvrcrcuaczyelxanit:
⇥
gtmzrgnfyzfamwxanoy:
⇥
⇤
lndyiryagzgyncpnyuw:
nadmprrpqltzrngpjcy:
⇤
ysqgpgbznrbjfcqzfma:
fsmmzurlmyfuaytnwmr:
oamrxefsyaanyrarrjm:
⇤
gvobravndaymnhohmnl:
haypreaqpnsglebcdqo:
cauntxarjheyqemypdt:
⇤
⇥
nseyxqdqrcyopkazvyu:
⇤
trwidrjqynaiyohxatp:
⇤
⇤
⇤
⇤
vjlmsrryauqkmfnfyrq:
naingtkczoyruoylvor:
⇤
iprnejfylqswalbuqrc:
⇥
⇥
⇤
drmmpannsyysenmrznb:
⇤
⇥
⇤
⇥
⇤
sainagyrudytjphidgg:
ornarpmnplyranuriap:
⇤
⇤
nzfewqanyydrtejywba:
⇤
j yqlgysanqbltsmoumrs
⇥
ierbyrwcaheflkeayan:
uydrunuraynszphutas:
⇤
yxjaisrcaiuukzxyins:
⇥
j dgbturvyynevgiojcay
thrtyabwnxqnutxfvfa:
yqlgysanqbltsmoumrs:
⇤
lqviaqaoswqpyirntxn:
⇤
npradyyiumyjylcqwnj:
⇤
nxsddlhyhiwpkkorpna:
⇥
⇤
avnjwkqviranxyddmad:
⇤
fadxrmnstelipdnrfny:
⇥
⇥
⇥
qccgharniqovswynpzj:
⇤
⇤
naahwyspugxrvrcgznd:
ardjyyiufkxxngszaih:
nkrazccyyaunlidwqqy:
maakrqnmdmoatyrkvjq:
gndahytfpryqunrkflc:
⇤
⇤
xhqniyloowkcgraperu:
rnaprqtocjdhtyazrnn:
cnszixxyiatiuresvln:
⇤
⇥
⇤
⇤
⇥
⇤
auzsctcryngarzqjfwa:
carpinwlqbnrjldvrby:
mcahrnvcluwndjqyuuq:
wbkknibrfajxccnxymg:
radahnizvrtqryordpb:
⇥
nwfrtpqwtamrgyhgxrz:
jrebhayaqswnubuhpci:
⇤
⇤
⇤
⇥
mknfraylvxmopvkgyqu:
⇥
dqcyraudnlofvzyswbh:
⇤
⇤
⇤
okfbruolmranwunyhgy:
⇤
eeyyrwlwnmbacrcjekf:
⇤
⇥
⇥
jywlnaduarmrjoddszn:
⇥
⇤
⇥
uyjmammifaybrrfgtnh:
⇤
kbcnsqkrrbryvmvodpa:
⇤
⇤
⇤
⇤
acxeewdvhnrxyjhlinj:
⇤
⇥
tlrghwociyapayynbix:
wqsvqwuaoenmhnferyv:
⇤
uaodlebyozisiscarnc:
⇤
⇤
pnxnptywfgujvardeac:
dxjfhqsrboaanybyqea:
⇥
⇥
sqlfyrbjaadrhlikwny:
⇥
⇤
⇥
jnebaepxrraycytvjnh:
nnuffjbydzawimjtrjf:
⇤
dnxohiyvwytenjdrpao:
aatrgrwybbqnrraomgp:
uergevbanoklvkkbsyp:
⇥
j oscziafvmubwrynmbzk
⇥
⇥
⇤
⇤
cwnmlwyzaryjhhyxrzq:
⇥
ydruokycvdmpawuyurn:
ncjlraroryinkfavheh:
qymrvynyrfxrpcumyna:
j iytzxqnakciezirmsfh
alhbgwqnaijsynsrreg:
⇥
ekkndryjebielbaprif:
⇥
oscziafvmubwrynmbzk:
demmjhgieikanukrybv:
⇤
uiybsetducinxrvadpc:
⇤
⇤
ytfmanuacdesskeckrc:
⇤
ntyjqackwrhipjvtewo:
⇥
fnafyrpuuanzcueljsl:
hiuarkzqkycmxlawnlp:
lh  $s2 ($s0)
nfjzzzxtysjjrvndalr:
⇤
sycqgvstnbcxsahsery:
⇥
⇥
⇤
⇤
ickykawsczcpojanfrx:
⇤
⇥
nncohaxjwqrysnfpyfu:
ufiwmtrnksstceyblau:
pknjvrldasfynfjgwfs:
⇥
⇤
⇤
⇤
ynayornaawwrxtlirjx:
ixqfupgneawryfvxlrb:
⇤
⇤
⇤
rwaxmachnrlygxzqzky:
⇤
nnrfzdrnuzbldanlyoe:
⇤
ajldpamdrpndkfzkrdy:
⇤
⇥
⇤
fklyhnthaoskzlzxqri:
nzxaytprhqasgmdyjkm:
⇥
mxoymnantmdagqcksqr:
⇤
⇤
zmsnrddgsfdnyknqhai:
nefqfsoayjcgnbrucfu:
adtqdyizpnnlcazmrat:
rzckiawgynznaohjuul:
⇤
⇥
dbydvfyaniyytsbfrni:
nfxsihamrorpnfkmoey:
yrwsrlbbebndyhyjbat:
⇤
⇥
⇥
⇤
⇤
⇤
⇤
⇤
⇤
⇤
⇥
⇥
vjqkyaarafhxntssjkw:
adthcxrrxfycraraznf:
⇥
⇤
⇥
hncefycfngaherajcoz:
pnfaremrydioqrmqfzz:
⇤
⇤
kenapdrkastfyunbvya:
⇤
jquysfergnwhvhritza:
⇥
bavzyufrefnnkjqzcyn:
⇤
nyrxetaerymkgfsyrna:
bne $s2 -1 else.0
ytkaafeyljwgvdanrdg:
⇥
tylvkqawvndzrkbdfyb:
⇥
⇤
⇤
⇤
⇥
⇤
⇥
hkzjvyhtrntxlaasqld:
⇤
⇤
ycmiorrkddqxrafnuaj:
zyujnoeckfabprnqnxk:
⇤
snjagpycrhenynnzqqa:
jnuaztixkwkcgynrybg:
⇥
rakyrinueshfzumsdls:
⇤
⇥
huquflfpnxryuflmrba:
⇥
⇥
⇤
⇤
⇤
zrrdyrarnpctziwoyzg:
⇥
kdrasnzzxrnlnyycbqy:
nwompqrnozayedgtgue:
ibxrcbuytrzaytgnmsy:
⇤
ntpryjsvaxnwnltlega:
ofrfnflbylesyardqnp:
⇤
⇤
⇤
jwutuyrnpkuryardhrb:
⇥
noemsoirafkatysrgay:
⇥
⇥
orfaufwfxolnbnafyks:
⇥
vzrlxjnbupymyyamdnk:
grxdyqrxaummqwjrntu:
⇥
⇥
sqqgbyhkibneqajdrsn:
qxhlzkponaqubwiryrq:
⇤
⇤
azrirlswyvhspcnhkjc:
ljorauvypthbmnfivnn:
⇤
⇤
wsewpgqafyirwqpnjae:
⇤
qnwmovhzjyhlqqafrtb:
⇥
⇤
⇤
⇥
⇤
li $v0 0
rnsshyfealgpxrjblpe:
dpphjywerxaigrbwnua:
oahgrdtphfupyevbnfo:
⇤
⇤
⇥
⇥
⇥
wnxrwyifwxpyirwdaaw:
zxcpnpfymrpghzatalm:
⇥
⇥
⇤
⇤
ahrrynwphkjsclegrqz:
hcktyeqgkntahrtaetr:
unecjvanjgyreyfyglj:
grfkvntvvlnryahuymf:
⇥
fmashnqjjuxgykcptre:
asipwvzyzwcznlsqrpb:
⇥
hwabahadbnryyxetdvr:
⇥
hcdjnqoioyybapinrmy:
nhabbxtdlyorkqdwqsr:
⇤
fjuzasmmaylhtdaruon:
⇤
⇤
aqnonuerhpuonuccyho:
⇥
⇤
⇥
⇥
⇥
⇤
⇥
⇤
fntkryphhqnjalbajpp:
⇥
⇤
jnkwetswaqaqyvorddr:
yngrdjaslgralvydyol:
⇤
razwgmsfunfyrrclntu:
⇥
⇤
⇥
hkbzwzxtjyrhyvjpaon:
⇥
⇤
okynpcbjrttonaxeiuc:
⇥
raymdhsekxxbeytqnxa:
⇥
⇤
⇤
wdwerwzezgmajnxakiy:
izrpawnbakygwstsrcg:
⇤
⇤
njargtalyustahvyjmo:
⇤
⇥
⇤
⇤
⇤
⇥
⇥
⇤
⇤
⇤
sejahywtazxyhrvvnvv:
⇤
⇥
jzfyarefncukvkiangf:
ntlwyzkdfrxankwaxvc:
⇤
⇤
⇥
dazrwaukuenyzryaznj:
⇥
vynrreuqbsrsavanlcj:
⇤
qqrevzzeyjqagnqntsr:
⇥
yubfndrqmnhsgqaxjrm:
fngyklqfljnnacwmryc:
⇤
⇤
yrwdfantdrychknhhgc:
⇤
jfszxhvdnyradbzrjod:
imfcrywbnraaawmazim:
⇤
j tguvrgyvsjkranlnzcy
dnlyczyvbvnbbrefaac:
j xmrgpliutancyeqwdyc
tguvrgyvsjkranlnzcy:
⇤
⇤
pfrrbgqttawjqznevyd:
⇤
zlalgritdhjygnuvxfq:
⇤
⇥
⇤
xautyyyxuznryxclcih:
⇤
yjzxgbfmaomjmnrtnrc:
zjapwgnpnzyksosnrjv:
hhnseknlyrbargcykhp:
⇥
⇥
⇤
nlrwzagbuxrzdacoryz:
⇤
⇤
⇤
nyfcaqriksyfizzxaiu:
yanerqfolnebbjknmxi:
⇥
⇤
⇥
bjzygnnnzkuaarmuqsm:
ydenrdfurvteaimpsqr:
⇤
⇤
⇥
⇥
zzxgdlrwwnbhyjrklha:
agiohysrnqehjgsawzl:
⇤
⇤
tympvfnzqsuapprrohy:
ymuonamrwlhazcuojeu:
⇤
dbseqoxnapapapyznrd:
⇤
⇥
⇥
krdnvynghenwhpzrxax:
j zknagqntqryawkezciq
⇥
⇤
eudnsaadmszohnryqda:
wyeqnjcqahyfvrajrsq:
rtcyztfzmiofskuanqd:
ryxopsaggdeasvrqnel:
vyumygdrinfjroiabrj:
⇤
⇤
lyhwrxiacakakalshbn:
⇤
uhraokgyukeznysboqy:
tasdruwbyadwsftlmtn:
⇥
⇤
fiwbraycydyvwntkwnk:
⇤
⇥
⇥
⇥
⇤
⇤
⇤
exhsnrayocpbhlvybrw:
⇤
ympqrnbpftzgugnrxad:
⇤
ncjgwvwgbrjvveigaxy:
⇤
j qqaeswhnlyglnzfyddr
⇤
⇥
⇥
⇤
zknagqntqryawkezciq:
⇥
auyyzvntfgawlrlgbuf:
⇤
ssnzbggrskowysbojaa:
bjeyglxrnbotanosdqu:
xzntkzrbahygcbsuzfy:
anlkwournuraojppsvy:
⇥
kdddatgrzngfymlrtin:
cmpinaxnneytqrattjq:
hmeyulraqrtuynlwpds:
⇤
ngasjjytrocllyduhkr:
⇤
⇥
⇥
⇥
⇥
arxenaarhjcjocatqyh:
⇤
⇥
⇥
dhnamrfyxrajrvqsmgz:
lhgpnrqwydjnudobabr:
⇤
⇥
⇥
⇤
⇥
⇥
⇥
⇤
⇥
⇤
aarmcdndfyukgxyhigw:
⇤
⇤
⇤
⇥
⇤
⇤
⇥
meynzerqlvyskarvrev:
⇥
⇥
⇤
⇤
⇤
⇤
⇤
⇥
⇥
⇥
j return
kxrjqnkhcaoftftaehy:
⇤
⇥
⇤
⇤
ajrlaxemthrzyknnggr:
⇤
⇤
⇤
ydknyuicvbaalrraqln:
⇥
⇥
aatddszryuejozdudfn:
⇥
nbyrmoylxtctiuaxrro:
⇤
irtynetpfamtgwkhncy:
whrxqpystqalqirkntz:
⇤
⇥
⇤
⇤
amgzyonqrqoksxxshya:
⇥
⇥
j yboqfwanrqjsgkobadf
egnzplnxxwyauotiitr:
j onjownrroosyrapyvgu
yboqfwanrqjsgkobadf:
⇥
nphyaurrsnnjxpktodm:
yuyvlwrnzxfawamkmrt:
rfxucqanysnrgntscec:
⇤
⇤
⇥
dxrywiyksnppfrjaflx:
⇤
nthmshrqqzzjaonrxyy:
⇤
⇥
⇥
ymbmuglftuxavwinurt:
⇤
⇤
⇥
⇤
ynnynhmldrgjeqpacyr:
cytrgbnwonhfaggrnhz:
⇤
⇤
⇤
⇤
⇤
⇤
⇥
uawfaqlqlqmfynslakr:
j zarstqkaavzynbfzjsz
cuanvyjrieqaytbygnk:
⇤
ojrpxartekpyccnmony:
j zcybucaqanbrcrnjqfq
zarstqkaavzynbfzjsz:
⇤
⇤
oonanrxgkrsttdbeujy:
⇥
⇥
⇤
⇤
⇥
ohyirnbgupitasrcfky:
zqceyjnbbrwqaddvpor:
rgekgdyfalwtxncrich:
⇥
⇤
xybqdrhynbqnsqypiya:
wxfrikbxauoaynryhld:
⇤
ltmjamrtzongypgiamz:
urriueupawnyeowgzlq:
⇤
⇤
ajwrpjjynlgnainawwb:
⇥
⇤
⇥
⇤
⇥
⇤
rdnneonamyjkdrzonga:
⇥
rkfqjkicndicpeykazr:
⇤
⇥
⇤
⇥
⇤
xumwiahmwyfrrgnjawr:
⇥
⇥
ulvqldyrntjjlyaumvs:
⇤
rbajohxnxsnqhmbhamy:
else.0:
⇥
⇤
⇥
⇤
⇤
jzmhlaorapdgedykrny:
⇥
j cnqypjrdrayywpnbgvd
ngolirdaraldfhfymhv:
j ymahvypnkexoezdrwwu
cnqypjrdrayywpnbgvd:
⇤
mrcbynkmvealawreuma:
ytsrknenstdcaderrpo:
⇤
suahonfgicbrncdyrds:
⇤
⇤
aexgayjnolsxrreidwp:
hnhemynbylrqonaaxyn:
⇤
wnyywzneorrsktayqdr:
⇥
rofyehwnbsdtvacibwm:
⇤
⇤
⇤
⇥
zyzkqyyadneriqyamyv:
⇤
jbyunykhcrpaiamxdpi:
⇤
⇥
⇤
⇤
jcrhzwaewayuneirvyr:
⇤
njegwxaamqnwrergnyn:
⇤
alxntansyvoqziorsbn:
⇥
⇤
lcypidrnvcwukabygry:
ephjodbumlzxnzyreha:
⇤
⇥
⇤
⇤
⇤
rxcqhrpndgybanchmvs:
kchruxcgqykaigsnnnh:
⇤
imyyrywtoafhngqnlva:
⇤
⇤
natpsursugylgarfkly:
⇤
wyxhyhtckrbndrvlvfa:
⇤
⇥
⇤
⇤
⇥
⇤
⇤
novirkquudghmypapcr:
⇤
⇥
⇥
⇤
j rsazulnygvjsssatcam
⇤
⇤
⇥
⇥
dqbrayznlreekalqmup:
⇤
⇥
mjulbnhbjgjsramayto:
⇤
⇥
bpaaemwrxninurxoypx:
emanjytrhwtsrfkpgau:
j ucybyizmhaxwaqerron
ravgsykvubgxtnjxurt:
rsazulnygvjsssatcam:
⇤
⇤
⇤
⇤
iqcgkhzyrrannkyrgkr:
xpewilbyxnfxjaiiyjr:
itgzneyrwzcljrcdavq:
⇤
⇤
⇤
⇤
nlasyercmoinnbyylkf:
⇤
⇤
⇤
nycnhcrzahfdspguybw:
hrsnkjawfyhdpaynads:
⇥
blt $s2 2048 else.1
⇤
ykxadfxbhcrjgyrnnph:
⇤
⇤
xfaoanaavaysxrfnsoy:
⇤
⇥
ynzyrrzhzwuanycydha:
⇥
⇤
tvrhfqtryydacnzkinc:
ntndzvganvjjnqirlys:
li $v0 1
hngbetjvprauwrvygnl:
⇤
ryvzfxozvsvynrapkiq:
⇤
⇥
⇤
fpzycjyrynkmelarpft:
⇤
⇥
lenrnikprihvoaznyts:
⇥
⇤
⇤
⇤
⇤
⇤
csyntscnehraktgfymq:
sxiuaenoyvgjrnsdere:
⇤
wkvrhyiesxudafisfdn:
⇤
tobnafyswsnwfhvgruw:
⇥
⇤
fwtgovywcnrqabrbmlx:
⇤
vtbyhryntadmlourxni:
⇥
⇤
⇥
⇥
xaybavkbmtynrxjrchj:
⇥
⇥
lzrgwbyyxnfzrofqacy:
⇤
⇤
tngiayramowngljthwm:
xvjpzelaqgcrnmxdsvy:
⇤
bufoqavodzcrxrnbycr:
⇤
⇤
⇥
⇤
⇤
⇤
⇥
ylvtafscakldvlwnsrz:
⇥
⇤
⇥
⇥
⇥
igqwnlurgymlahoaklb:
⇥
⇤
⇤
hnljxnsemnkirfaprvy:
nyagpvywbpgjcsrdsla:
wpavwrgnfckzyszrkym:
chysgxrwdhknrwameyy:
mrtdeokrzkjtcnqhaxy:
⇤
⇥
⇥
rjjhyknmnqarmzyiqwa:
⇤
qzuogdvtpoyijnaorvf:
wutnlxzurusavyeytry:
⇤
⇥
⇤
⇥
rtqrnbcufyltgoxhaoy:
⇤
⇤
⇥
⇥
⇤
⇤
⇤
cyiokywawxrnvjotnyx:
⇤
⇤
⇥
awydehifivitghnmrog:
⇤
jspcraytojtgaltshnv:
tksaivuvyuijqxarnlb:
⇤
rolcajqspctywrgndvj:
⇤
enysjlomyrdjjoarulx:
wzsoqrqbasmyefggene:
banaulyelzrhambngmd:
jynuvucqkjlmrbhpwva:
⇥
⇤
⇤
hrvmrodraywifntodan:
⇥
⇤
⇥
⇥
⇤
j return
⇤
rdnhyrleltjejgtxadr:
⇤
⇤
fagnzphyombubrmajix:
⇥
bwanxawkbwaxcdrryiq:
uxtmymrimnpaiodznsa:
⇥
yuqxujameqbnhpxaorq:
⇤
⇤
⇤
⇤
⇥
⇥
xytvjfoexdprnnaruko:
rbjzbyanscwooklzpyr:
⇤
⇥
mrfniflmybeykaqzsyj:
⇥
⇤
ntiinbrxrkyazukeeuv:
emirpbjuydguunpcjta:
⇤
vrlcfjerxanqnahxybz:
⇤
⇤
vpaarvsklqdjsxanuzy:
⇥
⇤
⇤
dwhvqruycysagldsxnz:
j mxnfyayrlkrgbcyojzy
onjownrroosyrapyvgu:
⇤
j yujrflilredbxiaagrn
mxnfyayrlkrgbcyojzy:
⇤
panlyhynrxgwisikzgh:
⇤
⇤
⇤
⇤
⇤
⇤
ysczlnytcaeldmrdncy:
⇤
⇤
rypyncdcaeyjufrnnfu:
⇤
⇤
⇤
⇤
⇤
⇤
rnxhgnyesagvajmxiyu:
⇥
ajwigtlpjcsarznycnl:
⇥
keonslxaosmrylztgzz:
⇤
manrrbpbykqttprjsyg:
⇤
⇤
eurniclsunyrrtlaxys:
⇥
⇤
⇤
⇤
byrqnieefgqqyrnaqnw:
aluwrtafdydqbacsadn:
cnlllttpcvsoaryapds:
uyfsnpmaymlcmltujrx:
⇤
⇤
⇥
aelaycqjvlnrjcifayc:
⇤
tskyrgoenaxhcmgehix:
yylimbfniwxotahyizr:
ahlytnfjmsnnrfazoco:
⇤
⇤
⇥
⇤
neezdarawovtqoixjny:
⇤
j dlntrzfalayowxninqd
xmrgpliutancyeqwdyc:
j ngolirdaraldfhfymhv
dlntrzfalayowxninqd:
⇤
⇥
llyhzbucrnsfalsrnto:
yujparowqfnagtvhezs:
⇤
⇥
⇥
⇥
⇤
jpnycynrnwvbbarswlt:
⇤
oroanwfoksygnfeaess:
⇤
ypnacgogxkqicmiufpr:
⇥
⇤
⇥
⇥
kickarmxionstiavyye:
essrnjahrvsmwymriyx:
vtkyadprnnfqygajtka:
⇥
⇥
nasqbarcxrqvnwxzucy:
⇥
asahloqobvyndrazday:
⇤
hymqirkracaalsnggzt:
qyomxninxrtcuyaecto:
vzydnhlravvcchfbqwj:
⇤
⇥
⇥
npenmtkxryyvkahyibp:
⇤
arcfgvnbbubnnweiyti:
⇥
⇥
⇤
⇤
⇤
⇤
ptxynzrvasolwdfimah:
⇤
sgeylrtpavtaaevnkjn:
wfnvmtuumgafbrxyfga:
gnyrpsgqamxatmzfdvu:
⇥
ryaprnnltjednyznjeu:
dwxtvwfryjedfnahzyt:
⇤
ptzkzscwoayryxxvsnm:
lazneaepdwzdrnskkyl:
⇤
⇤
dutayvaupdesntthbwr:
⇥
⇤
⇤
⇤
⇥
rhssryhnfdcacojoqag:
⇥
⇥
crnyilsavfwflljnnpn:
ueonajsgbubknwrhzyf:
⇤
⇥
rgbjynrdbyyazbazhox:
dakxbnyygnoarpkxnyd:
⇤
⇥
⇥
⇤
ktgnymazeyrdmlqgffc:
hmiqoxnqvpfawykurms:
sdymyfeuuhrglgpainf:
⇥
⇥
⇥
ryaqonmxinaegmlnzee:
⇥
mgflayynxdqukdnmwri:
yzdxfkgannofgruhuzn:
⇤
⇤
yzrbcnbyidccaiyytyu:
⇥
⇤
⇥
⇤
fawkynymuaxtwqfrrkv:
⇤
⇤
dnokhvctwyrnayrzdym:
⇤
⇥
⇤
hwcsqfzuanvcoytrokq:
⇤
naryoglpkbjrzyyhglc:
⇥
rpfmniqdahbgyiatwrk:
nbmdecyjnkdxagcacrp:
mpesssoaxpnyardenqn:
wichnazcmardcyxnlzo:
hauxmgayfuunrjsimdg:
sesdppgdnwpghafrsyr:
⇤
nzvjknavrobnjatnpyo:
zhrynjqhlczsapsarfn:
lmpnvrqyntdxahziena:
yjkrmwhxndtqukyvaku:
⇥
rqnecrauyibvppslnfa:
atpgjkywlnutjbkykkr:
⇤
⇥
⇥
miuacntfykylkrlwryn:
⇤
⇤
⇥
vwzoyzcndbdcwmjavar:
⇥
⇤
⇤
else.1:
bayrpueydvkqtylynaw:
pyqjqhmmudsntwodxar:
⇥
amubndafynprybakfnx:
fcmqyudngqbekroahuc:
fypvmlaungztqrwwczy:
srnhjeotjyojrlbvvap:
⇤
⇤
⇥
hprehscgmseknsjaycm:
⇥
⇤
foouuaryppcnhtirdqr:
⇥
hybrhykbnibleafvkfh:
⇤
⇥
⇥
majoazywahindjfusrn:
vfrilzjhjhqgenarywa:
⇤
⇥
⇤
tcrawpvjuoinlrhadyj:
hfyaqynryllwmylnzvy:
aniknkattjbzxwoyrme:
⇤
⇤
⇤
⇥
⇤
⇤
⇤
⇤
⇥
⇤
laaisiukownwxreyqrg:
⇤
eqwdtaygnagrrpeertn:
ufyzvmrnifbgasdhare:
⇤
xbzpahdnndxtlktyyrs:
⇥
mrnykargxdqjjbyyobm:
vudtfetnaexyatecrxc:
prwyxslrpunoyscaket:
ouixykmjdcnrxtiaded:
⇤
⇤
⇥
⇤
⇤
⇥
⇤
⇤
debmilyquuvionyirab:
⇤
⇥
⇤
yvwdrcaqrbnkzravdbh:
⇤
⇥
iafrrznwkyduwobnyca:
⇥
mykranupvevjqnnffkz:
⇥
⇥
⇤
⇥
⇥
⇤
nzlanrjfgfrewbrywtn:
lyazezrntvxxxreyupy:
ialhawmpogwmhnzrypp:
zrrtjyngcaxrmakjlly:
⇥
⇤
⇥
⇤
⇤
⇤
dodbdxrpslanylanabr:
qkmchnrtdosyvbwajtp:
⇥
⇥
⇤
wybrtkytjixrdarzntj:
⇥
j inajfmsnvoviyhnraof
⇤
⇤
⇥
nnarbylkkwbsnpcbvku:
⇤
⇤
⇤
⇤
⇤
misipioytznarfyakfh:
hbyaxmkpmnrhdconvto:
nxydirreftgrqayleup:
j qypqaqygvvnrxyryvia
⇥
⇥
⇤
⇤
gxqnpyybheatzarurif:
⇤
⇥
udfyzawxukhctyrzihn:
⇤
⇥
⇥
mdonydhuhhqcdgasiri:
yvbhuiwuaryngcdiqet:
hkhrvkalbxkgqnbnypv:
swnzbhrpyahzaeasgdy:
inajfmsnvoviyhnraof:
⇤
⇥
⇥
⇥
cjgiacsyywomrwmnngu:
⇤
nmjaltvwrepgapnpnyb:
⇤
xvqnbgtabmniyrxnyqu:
⇥
j srwzzfijarqxccnnmay
nzntmawauspjdtymfrd:
j nfjzzvhgcshrxytdsao
srwzzfijarqxccnnmay:
⇥
⇥
cbyacmnasqrkvleblfr:
⇤
xtraknwjobysgdpcsqn:
yaqlhmbrbooiadehnmv:
⇤
⇤
⇤
⇥
⇤
⇤
⇤
gidtpvfanrsyklnyxav:
⇥
⇥
⇥
qmdhqyztjndnrbqaavh:
yfghnirapzgqgykpdmt:
⇤
⇤
⇥
gajnbrzlsynqzlacvjw:
⇤
⇤
⇥
⇤
kchxnaazbyzrnnyxzzs:
⇤
⇤
nreprqxskesyltlnaxn:
⇥
⇥
xzyenuruapalrvfsryx:
⇤
⇤
anneiikaqylugduwwrf:
⇥
⇤
⇥
⇤
⇤
⇤
⇤
bloszwrdcajnyjarmmg:
⇥
nncidymnbuzkutrkpla:
⇤
bpgaragpzgyjnjopcpj:
⇥
zsijyhyrgbnhnauwxom:
⇥
⇤
⇥
aypjsndrrekftzsbwdb:
⇤
⇥
rvxhfasgvdnwyamqnxd:
apukgrliudgfkrclnyo:
jdyjgsaavryxcnhydki:
⇥
⇥
⇤
⇤
lipprdydjavrrgpfdon:
pei $s0 2
⇤
pyufetyamzarggvvnba:
⇥
⇤
j laogbynbdoqpnnyzqrd
pyknflovcjragdhfybl:
⇤
j ewqqriiewprkgypdnfa
laogbynbdoqpnnyzqrd:
⇥
⇤
⇤
⇥
⇤
⇤
⇤
⇤
⇥
⇥
⇤
⇥
⇤
⇥
⇤
eoraqhrtyyoynayrxxx:
esyfzidwgvwmwaznsir:
⇥
⇥
⇥
⇥
cuzadlxydznadnrgjut:
⇤
aaxnefwymdgpiprrsfa:
⇥
⇥
ajacaagriwyhcghdjne:
⇤
j corgmaymqyomnvkrrff
jdbyknrrqagdynydevn:
.end_macro
check_state.macro
functions.end:


'''
coade='''


▶ editDistance £str1 £str2 £m £n
    blez £n exitWithNegative1
    ⓘ blez £m
        exitWithNegative1:
        ⮐ [li ◊ -1]
        ⮐
    ⓧ
    #
    pstrl "m:"
    pint £m
    pstrl ",n:"
    pint £n
    pstrl "\\n"
    #If first string is empty just insert n
    ⓘ beqz £m
        ⮐ £n
        ⮐
    ⓧ
    #If second string is empty just remove m
    ⓘ beqz £n
        ⮐ £m
        ⮐
    ⓧ
    addi £n_minusone £n -1
    addi £m_minusone £m -1
    #if the last chars of the two string are the same ignore the last char of each
    ⓘ beq [rba ◊ £str1 £m_minusone] [rba ◊ £str2 £n_minusone]
        ⮐ [ ∘ ◊  = ƒ £str1 £str2 £m_minusone £n_minusone]
        ⮐
    ⓧ
    #if last characters are not same
    ∘ £insert = ƒ £str1 £str2 £m £n_minusone
    ∘ £remove = ƒ £str1 £str2 £m_minusone £n
    ∘ £replace = ƒ £str1 £str2 £n_minusone £m_minusone
    #
    #calculate minimum:
    move $v0 £remove #v0 = insert
    ⓘ blt £remove $v0
        move $v0 £remove # if remove is less than v0 set v0 to remove
    ⓧ
    ⓘ blt £replace $v0
        move $v0 £replace # if replace is less than v0 set v0 to replace
    ⓧ
    inc $v0









'''
code="""

▶ add £a £b
    ⮐ [add ◊ [add ◊ £a £b] £c] 

▶ mult £a £b
    ⮐ [mul ◊ £a £b] 


"""
None
# region COMPILER:
from r import *
# Current language has no understanding of global variables!
def get_mips_temp_var_names() -> list:
    temp=lambda x,n:[x + str(y) for y in range(n)]
    return temp('$a',4) + temp('$s',8) + temp('$t',10)  # In ascending level of desperation: ['$a0', '$a1', '$a2', '$a3', '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7', '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7', '$t8', '$t9']
def get_mips_invalid_temp_var_names() -> list:
    return space_split('$v0 $v1 $at $k0 $k1 $gp $sp $ra')
mips_temp_var_names=get_mips_temp_var_names()
def is_valid_pseudo_mips_namespace_body(s: str) -> bool:
    return all(str.isalnum(c) or c in '_$£' for c in s)
def is_valid_pseudo_mips_namespace_prefix(s: str) -> bool:
    valid_pseudo_mips_var_name_starting_chars='£$'
    return s in valid_pseudo_mips_var_name_starting_chars
def get_pseudo_mips_var_names(body: str) -> list:  # Returns a list with only unique elements. All pseudo-variables denoted with £
    body=body.split('\n')
    for i,l in enumerate(body):
        if '§' in l:
            body[i]=''
    body='\n'.join(body)
    out=[]
    ⵁ=False
    for c in body:
        if is_valid_pseudo_mips_namespace_prefix(c) and not ⵁ:  # Prefixes can be used inside the variable names. For example: £Hello£Goodbye is treated as a single variable name.
            out.append(c)
            ⵁ=True
        elif is_valid_pseudo_mips_namespace_body(c) and ⵁ:
            out[-1]+=c
        else:
            ⵁ=False
    out=[x for x in out if not x in get_mips_invalid_temp_var_names()]
    return list_set(out)  # Get rid of duplicates but preserve order
def remove_mips_comments(body: str):
    pass  # Implement me for things like get_pseudo_mips_used_temps so that $t0 in a comment doesn't matter!
def get_pseudo_mips_used_temps(body: str) -> list:  # Usually for registers. WARNING: Will look in comments right now! Returns a list with only unique elements. All pseudo-variables denoted with £
    out=[]
    for temp in mips_temp_var_names:
        if temp in body:
            out.append(temp)
    return out
def mips_varname_is_register(mips_varname: str) -> bool:
    return mips_varname.startswith('$')
def mips_push(mips_varname: str) -> str:  # mips_varname could be a label or register
    if mips_varname_is_register(mips_varname):
        return "push_registers " + mips_varname
    else:
        return "push_labels " + mips_varname
def mips_pop(mips_varname: str) -> str:  # mips_varname could be a label or register
    if mips_varname_is_register(mips_varname):
        return "pop_registers " + mips_varname
    else:
        return "pop_labels " + mips_varname
all_mips_function_names=set()

functions=dict()  # The global dump of fucntions
# def pseudo_mips_to_mips(line:str): fw

class mips_function:
    def __init__(self,function_name,argument_names: list,pseudo_mips_body: str,dont_preserve_temps=False,manually_unpreserved_temp_names=[]):
        # fansi_print(manually_unpreserved_temp_names,'yellow')
        self.function_name=function_name
        if 'ℳ' in function_name:
            self.function_name=function_name.replace('ℳ','')
            self.macro_args=[]  # Will be added to
            self.macroized=True
        else:
            self.macroized=False
        # pseudo_mips_body=pseudo_mips_body.replace('ℳ','macro')
        # pseudo_mips_body='\n'.join([x+"\n ⇥" if '.macro ' in x else x for x in pseudo_mips_body.split("\n")])
        # pseudo_mips_body=pseudo_mips_body.replace(".end_macro",'\n ⇤ \n .end_macro')`
        pseudo_mips_body=pre_process_pseudomips(pseudo_mips_body)
        pseudo_mips_body=pseudo_mips_body.replace("ƒ",self.function_name)
        while "\n\n" in pseudo_mips_body:
            pseudo_mips_body=pseudo_mips_body.replace("\n\n","\n")  # Completely un-indent it
        self.pseudo_mips_body="\n".join(x.lstrip() for x in pseudo_mips_body.split("\n"))
        self.argument_pseudo_mips_names=argument_names
        self.argument_mips_names=argument_names
        self.used_registers=[]  # Will be replaced by make_mips_function_definition
        self.mips_definition,self.argument_mips_names,self.mips_to_pseudo_mips_dict=make_mips_function_definition(self.pseudo_mips_body,self.function_name,self.argument_pseudo_mips_names,dont_preserve_temps,manually_unpreserved_temp_names=manually_unpreserved_temp_names,function=self)
    def mips_call_code(self,args: list) -> str:
        assert len(args) == len(self.argument_pseudo_mips_names) == len(self.argument_mips_names),"Mismatched number of args: " + str(args) + " on calling function '" + self.function_name + "'" + ";  expected " + str(self.argument_pseudo_mips_names)+"; args = "+str(args)
        out=[]
        # for marg,arg in zip(self.argument_mips_names,args):out.append("swap "+arg+" "+marg)

        if self.argument_mips_names: out.append(correct_swapper("swap_right" + summation([(" " + arg + " " + marg) for marg,arg in zip(self.argument_mips_names,args) if marg != arg],'')))
        if mips_debugger_mode:
            out.append('print_str_literal "\t\t\tPSEUDO MIPS DEBUG|"')
            out.append("functionCallCounter.inc")
            out.append('functionCallCounter.printIndent "->" "" ')
            debugger=['''
                # print_str_literal "PSEUDO MIPS DEBUG: $sp = "
                # print_int_register_as_hex $sp\n'''
                      + """print_str_literal " FUNCNAME: \"""".replace("FUNCNAME",self.function_name)]
            debugger.append("register_debugger")
            debugger.append("println")
            debugger='\n'.join(debugger)
            out.append(debugger)
        out.append("jal " + self.function_name)
        if mips_debugger_mode:
            out.append('print_str_literal "\t\t\tPSEUDO MIPS DEBUG|"')
            out.append('functionCallCounter.printIndent "<-" "" ')
            out.append(debugger.replace("ENTER","EXIT "))
            out.append("functionCallCounter.dec")
        # for marg,arg in zip(self.argument_mips_names,args):out.append("swap "+arg+" "+marg)
        if self.argument_mips_names: out.append(correct_swapper("swap_left" + summation([(" " + arg + " " + marg) for marg,arg in zip(self.argument_mips_names,args) if marg != arg],'')))
        return "#Function Call: " + self.function_name + ("(" + ', '.join(args) + ")") + "\n⇥\n" + "\n" + indentify("\n".join(out),"") + "\n⇤\n"  +("\n#(End function call)" if show_end_function_call else "")
# END
# END
# END ⇥ ⇤
# END
# END
# END
def make_mips_function_definition(pseudo_mips_function_body: str,function_name: str,argument_names: list,dont_preserve_temps=False,manually_unpreserved_temp_names: list = [],function=None):
    """
    :type dont_preserve_temps: boolean that specifies whether the function should be allowed to modify $t0, $t1, $t2 etc, or any other temp variable.
    """
    assert not function_name in all_mips_function_names  # We should have a unique function name
    local_mips_temp_var_names=get_mips_temp_var_names()  # Don't include any temps that are originally used in the code because we don't want to overwrite them

    nargs=len(argument_names)
    if nargs<4:
        local_mips_temp_var_names=local_mips_temp_var_names[:nargs]+local_mips_temp_var_names[4:]+local_mips_temp_var_names[nargs:4]# Put the remaining argument registers at the end


    pseudo_mips_local_var_names=list_set(argument_names + get_pseudo_mips_var_names(pseudo_mips_function_body))
    unpreserved_temps=[]  # Will be overwritten if dont_preserve_temps
    if dont_preserve_temps:
        unpreserved_temps=get_pseudo_mips_used_temps(pseudo_mips_function_body)
        # fansi_print(unpreserved_temps,'cyan')
        for temp in tuple(unpreserved_temps):  # Make sure that we DO preserve any $s registers used! # tuple(used_temps) so the for loop doesn't do weird things when we remove things from that list
            assert isinstance(temp,str)
            # fansi_print(temp  ,'cyan')
            if temp.startswith("$s") and temp in get_mips_temp_var_names():  # This code is DIRTY: need to refactor this logic throughout the program!
                # fansi_print(temp,'red')
                unpreserved_temps.remove(temp)
        for used_temp in unpreserved_temps:
            local_mips_temp_var_names.remove(used_temp)
            pseudo_mips_local_var_names.remove(used_temp)
    for nam in manually_unpreserved_temp_names:
        if not nam in unpreserved_temps:
            unpreserved_temps.append(nam)

    end_definition_label_name=function_name + '.end_definition'  # llows for nested, local functions (just don't expect them to return lambdas with memory etc)
    #
    mips_prefix=['j ' + end_definition_label_name,function_name + ':#(' + ', '.join(argument_names) + ")"]
    # mips_body_prefix=['#Prefix: ']+(['#Unpreserved registers (might not be restored after return): '+', '.join(unpreserved_temps)]if unpreserved_temps else [])  # Where we save all used variables by pushing them to stack
    mips_body_prefix=[] + (['#Unpreserved registers: ' + ', '.join(unpreserved_temps)] if unpreserved_temps else [])  # Where we save all used variables by pushing them to stack
    # mips_body_pushes=["# Assume we got here via jal"]
    mips_body_pushes=[]
    # mips_body=['#Body:']+pseudo_mips_function_body.split('\n')
    mips_body=[] + pseudo_mips_function_body.split('\n')
    # mips_body_postfix=['#Postfix:',function_name+".return:"]  # Where we restore all used variables by popping them from stack
    mips_body_postfix=[function_name + ".return:"]  # Where we restore all used variables by popping them from stack
    # mips_body_pops=[(mips_pop('$ra')if not "$ra" in manually_unpreserved_temp_names else ''),'jr $ra']# 'jr $ra' isn't a pop, but it should come directly after mips_pop('$ra')
    mips_body_pops=['jr $ra']  # 'jr $ra' isn't a pop, but it should come directly after mips_pop('$ra')
    mips_postfix=[end_definition_label_name + ":"]
    #
    pseudo_mips_names_to_mips_temp_names=dict()
    for pseudo_mips_name in tuple(pseudo_mips_local_var_names):
        if pseudo_mips_name in get_mips_temp_var_names():
            pseudo_mips_names_to_mips_temp_names[pseudo_mips_name]=pseudo_mips_name  # It is it's own name
            pseudo_mips_local_var_names.remove(pseudo_mips_name)
            local_mips_temp_var_names.remove(pseudo_mips_name)
    for mips_name,pseudo_mips_name in zip(local_mips_temp_var_names,pseudo_mips_local_var_names):
        pseudo_mips_names_to_mips_temp_names[pseudo_mips_name]=mips_name
    mips_argument_names=[None] * len(argument_names)
    mip_names_to_push=[] if '$ra' in manually_unpreserved_temp_names else ['$ra']
    mip_names_to_pop=[] if '$ra' in manually_unpreserved_temp_names else ['$ra']
    mips_to_pseudo_mips_dict=dict()
    for name in sorted(x[::-1] for x in pseudo_mips_names_to_mips_temp_names.items()):  # This can be rearranged with any method you'd like: order doesn't matter. It's just for aesthetics.:
        pseudo_mips_name=name[1]
        # fansi_print(argument_names,'magenta')
        mips_name=name[0]
        if pseudo_mips_name in argument_names:
            mips_argument_names[argument_names.index(pseudo_mips_name)]=mips_name
        if not pseudo_mips_name in manually_unpreserved_temp_names:
            # mips_body_pushes.append("#"+mips_push(mips_name)+"# "+mips_name+" ≣ "+pseudo_mips_name+(" ⟵ Argument "+str(argument_names.index(pseudo_mips_name)) if pseudo_mips_name in argument_names else ""))# (Not using .eqv)
            mips_to_pseudo_mips_dict[mips_name]=pseudo_mips_name
            mips_body_pushes.append("#" + mips_name + " ≣ " + pseudo_mips_name + (" ⟵ Argument " + str(argument_names.index(pseudo_mips_name)) if pseudo_mips_name in argument_names else ""))  # (Not using .eqv)
            # mips_body_pops.insert(0,"#"+mips_pop(mips_name))
            mip_names_to_push.append(mips_name)
            mip_names_to_pop.insert(0,mips_name)
        else:
            mips_to_pseudo_mips_dict[mips_name]=pseudo_mips_name
            mips_body_pushes.append("#" + mips_name + " ≣ " + pseudo_mips_name + (" ⟵ Argument " + str(argument_names.index(pseudo_mips_name)) if pseudo_mips_name in argument_names else ""))  # (Not using .eqv)
    # region #  More efficient: use push and pop macros that handle them in bulk:
    function.used_registers=mip_names_to_push
    mips_body_pushes.insert(0,('push_registers_silently 'if allow_silent_pushpop and '$ra' in manually_unpreserved_temp_names else 'push_registers ') + ' '.join(mip_names_to_push))
    mips_body_pops.insert(0,  ('pop_registers_silently ' if allow_silent_pushpop and '$ra' in manually_unpreserved_temp_names else 'pop_registers ') + ' '.join(mip_names_to_pop))
    # endregion

    mips_body=[search_replace_simul(x,pseudo_mips_names_to_mips_temp_names) for x in mips_body]

    mips_body+=mips_body_postfix  # +=['print_word_array.return:']

    if function.macroized:
        function.macro_args=['$v0','$v1'] + list_set(get_pseudo_mips_used_temps('\n'.join(mips_body)))
        macro_arg_string=' '.join(x.replace('$','%') for x in function.macro_args)  # '%a0 %a1 %a2 %a3 %v0 %s1 %s2 %s3 %s4 %s5 %s6'
        mips_body=[".macro " + function_name + ".macro " + macro_arg_string,"⇥"] + mips_body + ["⇤",".end_macro",function_name + ".macro " + macro_arg_string.replace("%","$")]
        mips_body=[x.replace("$","%") if x is not mips_body[-1] else x for x in mips_body]

    function_mips_code='\n'.join(mips_prefix + ["⇥"] + [x for x in (mips_body_prefix + mips_body_pushes + mips_body + mips_body_pops)] + ["⇤"] + mips_postfix)
    # if function_mips_code.count(function_name+"."+"return") +function_mips_code.count("ƒ"+"."+"return") <=1:# It's silly to have a return label if we don't use it. No other function should ever attempt to use it; so, remove it to make the assembly output more readable!
    #     function_mips_code=function_mips_code.replace(function_name+"."+"return:\n","")
    while "\n\n" in function_mips_code:
        function_mips_code=function_mips_code.replace("\n\n","\n")
    return function_mips_code,mips_argument_names,mips_to_pseudo_mips_dict
def apply_indents(s: str):
    '''iteration_via_for_loop_test.end_zii:
    ⇤
    #End of for-loop n3l
    ⇤
    #End of while-loop M1y
    #End of 'if' branch
    ⇤
    #End of if-else branch zii
    increment_register $s0
    ⇤
    j iteration_via_for_loop_test.while_hu3
    ⇤
    j iteration_via_for_loop_test.end_RlN
    ⇤
    iteration_via_for_loop_test.else_RlN:
    ⇥'''
    '''
    A
    ⇥
    B
    ⇥
    C
    ⇤
    D
    ⇥
    ⇥
    E
    ⇤
    F
    ⇤
    G
    ⇤
    H
    '''
    # ⟱
    '''
    A
        B
            C
        D
                E
            F
        G
    H
    '''
    i=0
    out=[]
    for l in s.split('\n'):
        if l.rstrip().lstrip() == '⇥':
            i+=1
        elif l.rstrip().lstrip() == '⇤':
            i-=1
            if i<0:
                i=0
        else:
            out.append(indent * i + l)
    return '\n'.join(out)
def parse_automips2_to_mips(s: str):
    macro_flag_hash=random_unicode_hash(20)
    source=s.replace('\\','\\\\')# Otherwise it would break when copypasting the source code back in again
    data_section_lines=[]
    prefix=s[:s.find('▶')]
    s=s[s.find('▶'):]
    ans=s.split('\n')
    ans=list(map(bracket_breakdown,ans))
    for i,l in enumerate(s.split('\n')):
        if l.lstrip().startswith('⮤'):  # Run it as a command via exec
            if l in ans:
                ans.remove(l)
            exec(l.split('⮤')[1].lstrip(),globals())

    ans='\n'.join(ans)

    hash=random_unicode_hash(10).replace("▶",'')  # This fizzazz is to help you comment out ▶ definitions without it giving errors such as 'you have duplicate function names'
    ans='\n'.join(x.replace('▶',hash) if x.lstrip() and x.lstrip()[0] == '#' else x for x in ans.split('\n'))
    ans=ans.split("▶")
    ans=[x.replace(hash,"▶") for x in ans]
    # ans=[x.replace('ℳ',macro_flag_hash+"\n",1) if x.lstrip().startswith('ℳ') else x for x in ans ]
    ans=([Q if isinstance(Q,list) else Q for Q in [Z[1](Z[0]) for Z in list(zip(ans,[eval(x.split('⮤')[1],globals()) if '⮤' in x else identity for x in [y[0] for y in [z.split('\n') for z in ans]]]))]])  # Apply all the ⮤'s from string to strings or lists
    ooo=[]
    for x in ans:
        if isinstance(x,list):
            ooo+=x
        else:
            assert isinstance(x,str)
            ooo.append(x)
    ans=ooo
    for i,x in enumerate(ans):
        x=x.split('\n')
        for u in range(len(x)):
            if x[u] and '⮤' in x[u]:
                x[u]=x[u].split('⮤')[0]
        ans[i]='\n'.join(x)
        # for x in ans:
        # fansi_print(x,'red')
    ans=[x.split("\n") for x in ans]
    ans=[x for x in ans if len(x) > 1]
    ans=[[x[0],x[1:]] for x in ans]
    ans=[[space_split(x[0]),x[1]] for x in ans]
    ans=[[x[0],'\n'.join(x[1])] for x in ans]  # [[['f', '£A', '£B'], '    print_str_literal "g: A+B"\n    print_int_register £A\n    println\n    print_int_register £B\n    println\n    add £C £A £B\n    print_int_register £C\n    println\n\n'], [['g', '£A', '£B'], '    print_str_literal "g: A*B"\n    print_int_register £A\n    println\n    print_int_register £B\n    add £C £A £B\n    print_int_register £C\n    println\n    ∘ f £A £B\n']]
    ans=[x for x in ans if x[0]]
    # print(ans)

    def ofx(ans):
        thing=(' '.join(ans[0])).split('~')
        thing2=(thing[0].split(' '))[1:]
        if len(thing) > 1:
            thing3=thing[1].split(' ')
        else:
            thing3=[]
        thing3=[x for x in thing3 if x.lstrip()]
        # fansi_print(thing3,'cyan','bold')
        return thing3
    fprinted=lambda x:printed(fansi(x,'blue'))
    def modd(thing):
        # thing == ['£A', '£B', '~', '£A', '£B', '$ra', '$t99']
        out=[]
        for t in thing:
            if t == "~":
                return out
            out.append(t)
        return out
    ans=[mips_function(x[0][0],modd(x[0][1:]),x[1],manually_unpreserved_temp_names=ofx(x)) for x in ans]  # list of functions
    fdict=dict()
    for f in ans:
        assert not f.function_name in fdict,"ERROR: Duplicate function names! Duplicate name: " + f.function_name
        fdict[f.function_name]=f
        blist=f.mips_definition.split("\n")
        for i,l in enumerate(blist):
            if l.lstrip().startswith('Δ'):  # Run it as a command via exec
                blist[i]='#'+l.lstrip()
                data_section_lines.append(l.lstrip()[1:])
        f.mips_definition="\n".join(blist)

    function_names=[x.function_name for x in ans]  # In the order they were written; NOT alphabetized ['mod', 'quotient', 'factorial', 'zmain', 'reverse_string', 'print_word_array', 'string_length', 'read_byte_array',.......

    for f in fdict.values():
        assert isinstance(f,mips_function)
        lines=f.mips_definition.split("\n")
        newlines=[]
        for line in lines:
            # print(line)
            if "∘" in line and not line.lstrip().startswith("#"):
                originalline=line
                # "	    ∘ f $s0 $s1"
                # print(line)# "	    ∘ f $s0 $s1"
                line=line.lstrip()  # '∘ f $s0 $s1'
                line=space_split(line)  # ['∘', 'f', '$s0', '$s1']
                line=line[1:]
                fname=line[0]
                fargs=line[1:]

                output_registers=[]

                if "=" in line:  # "	    ⮐ f $s0 $s1"
                    # fansi_print(line,'yellow','bold')
                    if line[1] == "=":  # Remove the first 2 things WE HAVE 1 OUTPUT
                        output_registers.append(line[0])
                        del line[0]
                        del line[0]
                        # fansi_print(output_registers,'cyan','bold')
                    elif line[2] == "=":  # Remove the first 3 things WE HAVE 2 OUTPUTS
                        # line==['$a0', '$a1', '=', 'multiple_return_test']
                        output_registers.append(line[0])
                        del line[0]
                        output_registers.append(line[0])
                        del line[0]
                        del line[0]
                        # fansi_print(output_registers,'cyan','bold')
                    else:
                        assert False

                F=fdict[line[0]]
                fargs=line[1:]
                assert isinstance(F,mips_function)
                newlines.append(F.mips_call_code(fargs))

                if output_registers:  # "	    ⮐ f $s0 $s1"
                    # print(output_registers)
                    # output_registers[0][:3]in get_mips_temp_var_names()# A hack to prevent an errr Idk where it came from all of a sudden $s2ength from £length
                    output_registers[0]=output_registers[0][:3]
                    if len(output_registers) == 1:
                        if hilo_mode:
                            newlines.append("\tmfhi " + output_registers[0] + "#Retrieving the output value: " + originalline)
                        else:
                            if output_registers[0]!='$v0':
                                newlines.append("\tmove " + output_registers[0] + " $v0" + "#Retrieving the output value: " + originalline)
                    elif len(output_registers) == 2:
                        if hilo_mode:
                            newlines.append("\tmfhi " + output_registers[0] + "#Retrieving the first output value: " + originalline)
                            newlines.append("\tmflo " + output_registers[1] + "#Retrieving the second output value: " + originalline)
                        else:
                            if output_registers[0]!='$v0':
                                newlines.append("\tmove " + output_registers[0] + " $v0" + "#Retrieving the first output value: " + originalline)
                            else:
                                newlines.append("#"+"\tmove " + output_registers[0] + " $v0" + "#Retrieving the first output value: " + originalline)
                            if output_registers[1]!='$v1':
                                newlines.append("\tmove " + output_registers[1] + " $v1" + "#Retrieving the second output value: " + originalline)
                            else:
                                newlines.append("#"+"\tmove " + output_registers[1] + " $v1" + "#Retrieving the second output value: " + originalline)
                    else:
                        assert False


            elif "⮐" in line and not line.lstrip().startswith("#"):  # "	    ⮐ f $s0 $s1"
                # print(line)# "	    ⮐ f $s0 $s1"
                line=line.lstrip()  # '⮐ f $s0 $s1'
                # fansi_print(line,'yellow','bold')
                line=space_split(line)  # ['⮐', '$s0', '$s1']
                # fansi_print(line,'yellow','bold')
                fargs=line[1:]  # ['$s0', '$s1']
                # fansi_print(line,'yellow','bold')
                # fansi_print(fargs,'yellow','bold')
                assert not len(fargs) > 2,"ERROR: Can only return 1 or 2 registers! Problematic line: " + str(line)
                if len(fargs) == 0:
                    newlines.append("j " + f.function_name + ".return" + "#⮐ Exiting this function")
                if len(fargs) == 1:  # If 1 argument, sets 'hi' to the return value. WILL NOT JUMP TO RETURN IF NO ARGUMENTS ARE PRESENT!
                    if (hilo_mode):
                        newlines.append("mthi " + fargs[0] + "#⮐ Set first output")
                    elif fargs[0] != '$v0':  # That would be redundant; allows for macro based ⮐ syntax so I can say ⮐ $v0:
                        # else:
                        newlines.append(("move %v0 " if f.macroized else "move $v0 ") + fargs[0] + "#⮐ Set output")
                if len(fargs) == 2:  # If 2 argument, sets 'hi' to the first return value and 'lo' to the second. WILL NOT JUMP TO RETURN IF NO ARGUMENTS ARE PRESENT!
                    if (hilo_mode):
                        newlines.append("mthi " + fargs[0] + "#⮐ Set first output")
                        newlines.append("mtlo " + fargs[1] + "#⮐ Set second output")
                    else:
                        if fargs[0] != '$v0':
                            newlines.append(("move %v0 " if f.macroized else "move $v0 ") + fargs[0] + "#⮐ Set first output")
                        if fargs[1] != '$v1':
                            newlines.append(("move %v1 " if f.macroized else "move $v1 ") + fargs[1] + "#⮐ Set second output")
            else:
                assert isinstance(line,str)
                newlines.append(line)
        f.mips_definition='\n'.join(newlines)

        #region  Protection against § and ~$ra conflicts with silent_pushpop
        if 'push_registers_silently' in f.mips_definition and 'push_registers ' in f.mips_definition:
            # assert False,'WARNING: You probably used § and ~ $ra at the same time;'
            f.mips_definition=f.mips_definition.replace('push_registers_silently','push_registers')
        if 'pop_registers_silently' in f.mips_definition and 'pop_registers ' in f.mips_definition:
            # assert False,'WARNING: You probably used § and ~ $ra at the same time;'
            f.mips_definition=f.mips_definition.replace('pop_registers_silently','pop_registers')
        #endregion

    outcode=[]
    for f in ([x.mips_definition.split("\n") for x in [fdict[name] for name in function_ordering_method(function_names)]]):
        for line in f:
            outcode.append(line)
    outcode='\n'.join(outcode)
    main=main_name
    if main in fdict:  # Main method is special.
        main=fdict[main]
        assert isinstance(main,mips_function)
        if not main.argument_mips_names:  # Has no arguments
            outcode="\n⇤\n" + (("#" * 200) + "\n") * (3 and super_safety or not super_safety) + "\n#Exiting macro-world...\n#...and entering the wonderful land of functions, starting with " + main_name + "!\n" + outcode
            max_number_of_args_in_any_function=max([len(f.used_registers) for f in fdict.values()]) if not super_safety else len(get_mips_temp_var_names())  # Safest: len(get_mips_temp_var_names())
            outcode=pushers_and_poppers(max_number_of_args_in_any_function) + '\n' + outcode
            outcode=new_swappers(max_number_of_args_in_any_function) + "\n" + outcode  # Add enough swap macros to be useful
            outcode+="\n" + main.mips_call_code([])
            if mips_debugger_mode:
                outcode=debugger_registers() + '\n' + outcode
            outcode=default_macros + "\n" + outcode  # Only include the macros if we include our main method ⇥
            outcode="#Entering macro-world...\n⇥\n" + outcode

    indent='\t'
    # outcode=outcode.replace('⇥',indent)
    # outcode='\n'.join(list(map(correct_swapper,outcode.split('\n'))))
    outcode=prefix + "\n" + outcode

    #region add the datasection from Δ
    data_section_lines=list_set(data_section_lines)# Remove any identical duplicates that might be caused by ⮤ on methods
    if data_section_lines:
        data_section="\n########################## DATA ZONE ##########################\n.data \n ⇥ \n"+"\n".join(data_section_lines)+"\n ⇤ \n.text \n"
        outcode+=data_section
        #endregion


    outcode=apply_indents(outcode)
    outcode='\n'.join(x for x in outcode.split('\n') if (x.lstrip().rstrip()) not in ['','swap','pop_registers','push_registers','push_registers_silently','pop_registers_silently'])
    if show_source_code:
        outcode="############################ SOURCE CODE ############################\n"+("# Gist: "+((shorten_url if gist_url_shorten else identity)(gist(source,'Pseudo-Mips Source Code'))+"\n") if post_gist else "") + indentify(source,'#\t') + "\n" + outcode

    if strip_comments:
        outcode=comment_strip_attempt(outcode)
    outcode='\n'.join([x for x in outcode.split("\n") if x.lstrip().rstrip()])
    atlas,all_macro_and_function_names=code_atlas(outcode)
    outcode+=(atlas).replace("%","").replace("£","").replace(", ",",").replace(",",', ')
    if obfuscate:
        macro_arg_names=[]
        temp=""
        for char in comment_strip_attempt(outcode):
            if temp or char == "%":
                if char in ', \n()"\'':
                    macro_arg_names.append(temp)
                    temp=""
                else:
                    temp+=char
        macro_arg_names=list(set(macro_arg_names))
        #
        label_names=[]
        for line in outcode.split('\n'):
            if '#' in line:
                line=line[:line.find('#')]
            line=line.lstrip().rstrip()
            if ":" in line:
                label_names.append(line[:line.find(":")].lstrip())
        macro_arg_names=list(set(macro_arg_names))
        label_names=list(set(label_names))

        if strip_comments:
            outcode=comment_strip_attempt(outcode)
        for func_name in sorted(fdict.keys()) + all_macro_and_function_names:  # random_name_homograph
            outcode=outcode.replace(func_name,obfuscate_hash(func_name))  # +random_namespace_hash(obfuscate_length))
        for macro_arg_name in macro_arg_names:
            outcode=outcode.replace(macro_arg_name,"%" + obfuscate_hash(macro_arg_name))  # +random_namespace_hash(obfuscate_length))
        for label_name in label_names:
            outcode=outcode.replace(label_name,obfuscate_hash(label_name))  # +random_namespace_hash(obfuscate_length))
        outcode='\n'.join(['\t' * randint(obfuscate_random_indent_max) + (x.lstrip().rstrip() if obfuscate_unindent else x) for x in outcode.split("\n") if x.lstrip().rstrip()]).replace('.end_definition',obfuscate_hash()).replace('return',obfuscate_hash())
        o22=outcode
        o22=o22.replace("\n",' ').replace("%",' ').replace(")"," ").replace("_"," ")
        # for q in o22.split(" "):
        #     if len(q)>9 and 'macro' not in q and 'end' not in q and 'word' not in q:
        #         if is_namespaceable(q):
        #             outcode=outcode.replace(q,obfuscate_hash())
        if obfuscate_with_spaces:
            outcode=indentify(outcode,' ' * 1000 + '\t' * 100)
        outcode="\n".join([x.replace('"','') if x.count('"') % 2 else x for x in outcode.split("\n")])
        outcode=outcode.split("\n")
        for i in range(int(len(outcode) * obfuscate_decoy_label_proportion)):
            outcode.insert(random_index(outcode),obfuscate_hash(random_namespace_hash(20)) + ":")
        outcode='\n'.join(outcode)

        for old,new in zip(get_mips_temp_var_names(),shuffled(get_mips_temp_var_names())):
            outcode.replace(old,new)

    if every_line_should_have_a_comment:
        outcode='\n'.join(x + "#Every line should have a comment..." if not '#' in x else x for x in outcode.split('\n'))
    # outcode=' '.join([x[:3] if x[:3] in get_mips_temp_var_names() else x for x in outcode.split(' ')])
    return outcode
def correct_swapper(s: str):
    # region The theory behind it:
    # from r import *
    # a=space_split("1 4  2 5  4 3  7 6  3 7  5 1  9 8  0 10  10 9")  # ['1', '4', '2', '5', '4', '3', '7', '6', '3', '7']
    # tuples=list(zip(a[::2],a[1::2]))  # [('1', '4'), ('2', '5'), ('4', '3'), ('7', '6'), ('3', '7')]
    # firsts,seconds=list(zip(*tuples))  # [('1', '2', '4', '7', '3'), ('4', '5', '3', '6', '7')]
    # assert len(firsts) == len(set(firsts)),'All arguments must be unique, but are not'
    # assert len(seconds) == len(set(seconds)),'All arguments must be unique, but are not'
    # out=[]
    # thingies=[]
    #
    # while tuples:
    #     thingy=[tuples.pop()]
    #     while True:
    #         new_thingy=[x for x in tuples if x[1]==thingy[0][0]] + thingy + [x for x in tuples if x[0]==thingy[-1][1]]
    #         for thing in new_thingy:
    #             if thing in tuples:
    #                 tuples.remove(thing)
    #         if thingy == new_thingy:
    #             break
    #         thingy=new_thingy
    #     if thingy[0][0]!=thingy[-1][1]:# Close the loop: [('2', '5'), ('5', '1'), ('1', '4'), ('4', '3'), ('3', '7'), ('7', '6')] is unclosed
    #         thingy.append((thingy[-1][1],thingy[0][0]))
    #     thingies.append(thingy)
    # print(thingies)
    # endregion
    try:
        swap_type=space_split(s.lstrip())[0]
    except:
        return s
    if not (space_split(s.lstrip()) and swap_type == 'swap_right' or swap_type == 'swap_left'):
        return s
    a=space_split(s.lstrip())[1:]  # ['1', '4', '2', '5', '4', '3', '7', '6', '3', '7']
    tuples=list(zip(a[::2],a[1::2]))  # [('1', '4'), ('2', '5'), ('4', '3'), ('7', '6'), ('3', '7')]
    if not tuples:
        return ''
    if len(tuples) == 1:
        return s
    firsts,seconds=list(zip(*tuples))  # [('1', '2', '4', '7', '3'), ('4', '5', '3', '6', '7')]
    # exec (mini_terminal)
    assert len(firsts) == len(set(firsts)),'All arguments must be unique, but are not'
    assert len(seconds) == len(set(seconds)),'All arguments must be unique, but are not'
    out=[]
    thingies=[]

    while tuples:
        thingy=[tuples.pop()]
        while True:
            new_thingy=[x for x in tuples if x[1] == thingy[0][0]] + thingy + [x for x in tuples if x[0] == thingy[-1][1]]
            for thing in new_thingy:
                if thing in tuples:
                    tuples.remove(thing)
            if thingy == new_thingy:
                break
            thingy=new_thingy
        if thingy[0][0] != thingy[-1][1]:  # Close the loop: [('2', '5'), ('5', '1'), ('1', '4'), ('4', '3'), ('3', '7'), ('7', '6')] is unclosed
            thingy.append((thingy[-1][1],thingy[0][0]))
        thingies.append(thingy)
    return '\n'.join([s.count('\t') * '\t' + swap_type + ' ' + ' '.join(c[0] for c in Q) for Q in thingies]) + "\n\n"  # +"#"+s+"\n\n"
def code_atlas(x) -> str:
    x=x.split("\n")
    o=[]
    all_names=[]
    for i,l in enumerate(x):
        l=comment_strip_attempt(l)
        assert isinstance(l,str)
        if l.lstrip().startswith('.macro'):
            name=l.lstrip()[len('.macro'):].lstrip().rstrip()
            if not ('pop_registers' in l or 'push_registers' in l or 'swap_right ' in l or 'swap_left ' in l):
                o.append((i + 1," m: " + name))
            all_names.append(name)
        if l.lstrip().startswith('j ') and l.rstrip().endswith('.end_definition'):
            name=x[i + 1].replace(':#','')
            o.append((i + 2," f: " + name))
            all_names.append(name)
    mln=max_line_number_digits_length=len(str(max(list(zip(*o))[0])))
    out=["\n########################  CODE  ATLAS  ########################"]
    out.append("#       'm' stands for macro, 'f' stands for function.\n#")
    for u in o:
        out.append("#" + str(u[0]) + ' ' * (mln - len(str(u[0]))) + u[1])
    all_names=[x.replace("("," ").split(" ")[0] for x in all_names]
    return ('\n'.join(out)),all_names
def debugger_registers(registers=list_set("ra sp v0 v1 a0 a1 a2 a3 s0 s1 s2 s3 s4 s5 s6 s7 t0 t1 t2 t3 t4 t5 t6 t7 t8".split(" ") + [x.replace("$","") for x in get_mips_temp_var_names()])):
    out="""
    .data
    .word\n"""
    for r in registers:
        out+="register_debugger." + r + ":0\n"
    out+="""
.macro register_debugger
    ⇥
    push_registers $t9"""
    a="""
    lw $t9 register_debugger.sp
    bne $sp $t9 sp_new
    j sp_done
    sp_new:
    print_str_literal "sp="
    print_int_register $t9
    print_str_literal "; "
    sw $sp register_debugger.sp
    sp_done:
    #
    """
    out+='\n'.join([a.replace("sp",R) for R in registers])
    out+="\npop_registers $t9\n ⇤ \n .end_macro"
    return out

# region Good, beautiful code: bracketed expression evaluator (rather smxy algo)
def bracket_snippet(line: str) -> tuple:
    # ⮤ bracket_snippet('ABCDE[12◊ABCDE[12◊34]FG34]FGABCDE[12◊34]FG')
    # ans=('12◊34',14,20)
    assert has_bracket_expression(line)
    snippet=''
    for i,c in enumerate(line):
        if c == '[':
            snippet=''
            open_index=i
        elif c == ']':
            assert '◊' in snippet,'Error: Parenthesized expression must a temp output register, denoted by ◊, in it. But it didn\'t: line = "' + line + '" and snippet = "' + snippet + '"'
            close_index=i
            # noinspection PyUnboundLocalVariable
            return open_index,close_index,snippet  # If this line gets a PyUnboundLocalVariable error it's because '[' came after ']', which is wrong, like )this(
        else:
            snippet+=c

def has_bracket_expression(line: str):
    return all(x in line for x in '[]◊') and not line.lstrip().startswith("#")

def bracket_breakdown(line: str) -> str:  # Don't have comments on the ends of lines with brackets; it will break them if the comment also has brackets in it!
    if not has_bracket_expression(line):
        return line

    # bracket_breakdown('pint [add ◊ £a £b]')
    # ans=  # region Bracketed Expression: pint [add ◊ £a £b]
    # ⇥
    # add £Ƭ1 £a £b
    # pint £Ƭ1
    # ⇤
    # endregion
    #
    # ⁠⁠⁠⁠
    # ⁠⁠⁠⁠                           ⎧                                                                             ⎫
    # ⁠⁠⁠⁠                           ⎪      ⎧                                            ⎫                         ⎪
    # ⁠⁠⁠⁠                           ⎪      ⎪                    ⎧                      ⎫⎪ ⎧                      ⎫⎪
    # ⁠⁠⁠⁠                           ⎪      ⎪      ⎧           ⎫ ⎪         ⎧           ⎫⎪⎪ ⎪         ⎧           ⎫⎪⎪
    #   bracket_breakdown('pint [add ◊ [add ◊ [add ◊ £a £b] [add ◊ £c [add ◊ £d £e]]] [add ◊ £f [add ◊ £g £h]]]')
    # ⁠⁠⁠⁠                           ⎪      ⎪      ⎩           ⎭ ⎪         ⎩           ⎭⎪⎪ ⎪         ⎩           ⎭⎪⎪
    # ⁠⁠⁠⁠                           ⎪      ⎪                    ⎩                      ⎭⎪ ⎩                      ⎭⎪
    # ⁠⁠⁠⁠                           ⎪      ⎩                                            ⎭                         ⎪
    # ⁠⁠⁠⁠                           ⎩                                                                             ⎭
    # ⁠⁠⁠⁠
    # ans=  # region Bracketed Expression: pint [add ◊ [add ◊ [add ◊ £a £b] [add ◊ £c [add ◊ £d £e]]] [add ◊ £f [add ◊ £g £h]]]
    # ⇥
    # add £Ƭ1 £a £b
    # add £Ƭ2 £d £e
    # add £Ƭ2 £c £Ƭ2
    # add £Ƭ1 £Ƭ1 £Ƭ2
    # add £Ƭ2 £g £h
    # add £Ƭ2 £f £Ƭ2
    # add £Ƭ1 £Ƭ1 £Ƭ2
    # pint £Ƭ1
    # ⇤
    # endregion
    #
    # ACTUAL DEMO: Recursive fibbonacci thing:
    # region Bracketed Expression: [add ◊ [∘ ◊ = ƒ [addi ◊ £i -1]] [∘ ◊ = ƒ [addi ◊ £i -2]]]
    # ⇥
    # addi £Ƭ1 £i - 1
    # ∘ £Ƭ1=ƒ £Ƭ1
    # addi £Ƭ2 £i - 2
    # ∘ £Ƭ2=ƒ £Ƭ2
    # add £Ƭ1 £Ƭ1 £Ƭ2
    # £Ƭ1
    # ⇤
    # # endregion

    out=[]
    out.append("#Bracketed Expression: " + line.lstrip())
    out.append("⇥")
    counter=0
    def counter_to_temp_var_name(n):
        # if returner:
        #     if n==0:
        #         return '$v0'
        #     else:
        #         n-=1

        return '£Ƭ' + str(n)
    while has_bracket_expression(line):
        open_index,close_index,snippet=bracket_snippet(line)
        counter+=1 - snippet.count('£Ƭ')  # The number of evaluated temp brackets the snippet has
        assert counter >= 0,"If this fails, it's due to an internal logic error OR some input case I haven't considered. Input: line = '" + str(line) + "'"
        temp_name=counter_to_temp_var_name(counter)  # £Ƭ0，£Ƭ1，£Ƭ2 …… etc
        out.append(snippet.replace('◊',temp_name))
        line=line[:open_index] + temp_name + line[close_index + 1:]
    out.append(line)
    out.append("⇤")
    if show_bracketed_expression_end:
        out.append("#(Bracketed expression end)")
    out='\n'.join(out)

    if try_to_optimize_return_brackets:# Just a bit of optimization; now ⮐ [li ◊ 25] is equally efficient as li $v0 25
        aoisdu=space_split(line.lstrip().rstrip())# ['⮐', '£Ƭ1']
        if aoisdu[0]=='⮐':
            del aoisdu[0]
            if len(aoisdu)>=1:
                out=out.replace(aoisdu[0],'$v0')
            if len(aoisdu)>=2:
                out=out.replace(aoisdu[1],'$v1')

    return out
# endregion

'pint [add ◊ [mul ◊ £a £b] £b]'


def comment_strip_attempt(s):  # To be safe wont strip comments off of lines with " or ' in them because they might contain strings with the # character in them
    s=s.split("\n")
    out=[]
    for l in s:
        assert isinstance(l,str)
        if l.lstrip().startswith("#") or '#' in l and not ('"' in l or "'" in l):
            out.append(l[:l.find('#')])
        else:
            out.append(l)
    return '\n'.join(out)
def new_swappers(n):
    def swap_right(n):
        out=['.macro swap_right ' + ' '.join('%' + str(i) for i in range(n))]
        if n:
            out.append('⇥')
            out.append('sw %' + str(n - 1) + ' swap.temp')
            for i in reversed(range(n - 1)):
                out.append('move %' + str(i + 1) + ' %' + str(i))
            out.append('lw %0 swap.temp')
            out.append('⇤')
        out.append('.end_macro')
        return '\n'.join(out)
    def swap_left(n):
        out=['.macro swap_left ' + ' '.join('%' + str(i) for i in reversed(range(n)))]
        if n:
            out.append('⇥')
            out.append('sw %' + str(n - 1) + ' swap.temp')
            for i in reversed(range(n - 1)):
                out.append('move %' + str(i + 1) + ' %' + str(i))
            out.append('lw %0 swap.temp')
            out.append('⇤')
        out.append('.end_macro')
        return '\n'.join(out)
    out=[]
    out.append(""".data
swap.temp:.word 0
.text""")
    for i in range(n):
        out.append(swap_right(i))
        out.append(swap_left(i))
    return '\n'.join(out)
# region pseudo_terminal definition
from r import make_pseudo_terminal
def pseudo_terminal(*_): pass  # Easiest way to let PyCharm know that this is a valid def. The next line redefines it.
exec(make_pseudo_terminal)
# endregion
def swappers(n):
    def swapper(n):
        n+=1
        out='''.macro swap'''  # ⇥ ⇤
        for i in range(n):
            out+=' %a' + str(i) + ' %b' + str(i)
        out+='\n⇥\n'
        out+='\n⇥\n'
        for i in range(n):
            out+='sw %a' + str(i) + ' swap.a' + str(i) + "\n"
            out+='sw %b' + str(i) + ' swap.b' + str(i) + "\n"
        for i in range(n):
            out+='lw %b' + str(i) + ' swap.a' + str(i) + "\n"
            out+='lw %a' + str(i) + ' swap.b' + str(i) + "\n"
        out+='\n⇤\n'
        out+='\n⇤\n'
        out+='''.end_macro'''
        return out
        # print(swappers(10))
        # #         .macro swap
        # #         .data
        # #         .word
        # #         .text
        # #         .end_macro
        # #         .macro swap %a0 %b0
        # #         .data
        # #         .word
        # #         swap.a0
        # #         swap.b0
        # #         .text
        # #         sw %a0 swap.a0
        # #         sw %b0 swap.b0
        # #         lw %b0 swap.a0
        # #         lw %a0 swap.b0
        # #         .end_macro
        # #         .macro swap %a0 %b0 %a1 %b1
        # .....etc
    out=""
    out+="\n.data"
    out+='\n⇥\n'
    # out+="\n.word\n"
    # out+='\n⇥\n'
    for i in range(n):
        out+='swap.a' + str(i) + ':.word 0\nswap.b' + str(i) + ":.word 0\n"
    # out+='\n⇤\n'
    out+='\n⇤\n'
    out+=".text\n"
    return out + '\n'.join(swapper(u) for u in range(1,n))  # not 0,n cause i hang coded a faster version of that case
def safify(s: str):
    if not '§' in s or s.lstrip()[0] == '#':
        return s
    assert s.count('§') == 1
    s=s.split('§')
    middle=s[1]
    vars=s[0].lstrip().rstrip()
    vars=space_split(vars)
    l1='push_registers ' + ' '.join(vars) + "#§"
    l2=middle
    l3='pop_registers ' + ' '.join(reversed(vars)) + "#§"  # MUST leave the § symbol on if you want it to not read these like it reads registers from comments
    return "\n" + '\n'.join([l1,l2,l3]) + "\n"
def pre_process_pseudomips(code: str,label_hash_length: int = flow_control_hash_length):
    code='\n'.join([safify(x) for x in code.split('\n')])
    idt=lambda x:indentify(lrstrip_all_lines(x),'⇥')
    """
    :type label_hash_length: Will generate code such as ƒ.while.DZC7B iff label_hash_length=5, or ƒ.while.OA5 iff label_hash_length=3
    """
    # Example: NOW:
    # code = """
    #   Thing
    #      Cat
    # ⓘdonkey kong
    #       swiss cheese
    #   celery
    #       ⓕmips
    #  do
    #       ⓧ
    #
    # potato
    # """
    code=[x.lstrip() for x in code.split("\n") if x.lstrip()]  # Completely unindent code and turn it into a list of lines
    special='ⓘⓔⓦⓕⓧ'
    code.insert(0,['ⓧ',[]])  # Make the first line an endpoint for intuitive completeness
    def bundle_code_into_chunks():
        nonlocal code
        for i,s in enumerate(code):
            if isinstance(s,str) and s:
                if s[0] in special:
                    code[i]=[s[0],space_split(s[1:])]
        i=0
        while i < len(code):
            while i + 1 < len(code) and isinstance(code[i + 1],str):
                code[i].append(code.pop(i + 1))
            i+=1
    # Now: code == [['ⓧ', [], 'Thing', 'Cat'], ['ⓘ', ['donkey', 'kong'], 'swiss cheese', 'celery'], ['ⓕ', ['mips'], 'do'], ['ⓧ', [], 'potato']]
    def process_chunks(chunks: list) -> str:  # Turns chunks into a string: converting py2mips to mips. These chunks must be (for example) from an ⓘ to a ⓧ with (maybe) an ⓔ in between, but no other special characters (for example).
        get_hash=lambda:random_namespace_hash(label_hash_length)
        out=[]
        if chunks[0][0] == 'ⓘ':
            if chunks[1][0] == 'ⓔ':
                assert len(chunks) == 3  # ⓘ ⓔ ⓧ
                # Illustration:
                #    ⓘA==B        beq A B ƒ.if0
                #       C          j ƒ.else
                #    ⓔ            ƒ.if0:
                #       D      ⭆      C
                #    ⓧ                j ƒ.if0.end
                #    E             ƒ.if0.else:
                #                     D
                #                  ƒ.if0.end:
                #                     E
                label_hash=get_hash()  # Might be like AIg5G or something like that
                label_if=random_namespace_hash(10) + label_hash
                label_else=random_namespace_hash(10) + label_hash
                label_end=random_namespace_hash(10) + label_hash
                if not obfuscate:
                    label_if='ƒ.if_' + label_hash
                    label_else='ƒ.else_' + label_hash
                    label_end='ƒ.endIf_' + label_hash
                #
                chunk_if=chunks[0]
                chunk_else=chunks[1]
                chunk_end=chunks[2]
                assert chunk_if[1],'ⓘ should recieve more than 0 arguments but did not: ' + str(chunk_if)
                assert not chunk_else[1],'ⓔ should recieve 0 arguments but did not: ' + str(chunk_else)
                assert not chunk_end[1],'ⓧ should recieve 0 arguments but did not: ' + str(chunk_end)
                args_if=' '.join(chunk_if[1])
                body_if='\n'.join(chunk_if[2:])
                body_else='\n'.join(chunk_else[2:])
                body_end='\n'.join(chunk_end[2:])
                #
                title="#" + (chunks[0][0] + ' ' + ' '.join(chunks[0][1])).replace("\n",'')  # ⓘ blt £j 3

                out="""#Beginning of if-else branch label_hash:
⇥
title
args_if label_if
j label_else
label_if:
⇥
body_if
j label_end
⇤
label_else:
⇥
body_else
⇤
label_end:
⇤
#End of if-else branch label_hash
body_end"""
                out=search_replace_simul(out,{
                    'label_hash':label_hash,
                    'label_if':label_if,
                    'label_else':label_else,
                    'label_end':label_end,
                    'args_if':args_if,
                    'body_if':body_if,
                    'body_else':body_else,
                    'body_end':body_end,
                    'title':title
                })
                out=out.split('\n')
                out=[x for x in out if x.lstrip()]
                return out
            else:
                if if_as_if_else:
                    assert len(chunks) == 2  # ⓘ ⓧ
                    assert chunks[1][0] == 'ⓧ'
                    # Illustration:
                    #    ⓘA==B        ⓘA==B
                    #       C              C
                    #    ⓧ            ⓔ
                    #       D          ⓧ
                    #                  D
                    #
                    #
                    chunks.insert(1,['ⓔ',[]])
                    return ["#Beginning of 'if' branch (turned into 'if-else' branch with empty 'else' body:"] + chunks
                    # Easiest implementation: Turn it into an if-else statement where the else segment has no body.
                else:
                    assert len(chunks) == 2  # ⓘ ⓔ ⓧ
                    # Illustration:
                    #    ⓘA==B        beq A B ƒ.if0
                    #       C          j ƒ.else
                    #    ⓔ            ƒ.if0:
                    #       D      ⭆      C
                    #    ⓧ                j ƒ.if0.end
                    #    E             ƒ.if0.else:
                    #                     D
                    #                  ƒ.if0.end:
                    #                     E
                    label_hash=get_hash()  # Might be like AIg5G or something like that
                    label_if=random_namespace_hash(10) + label_hash
                    label_else=random_namespace_hash(10) + label_hash
                    label_end=random_namespace_hash(10) + label_hash
                    if not obfuscate:
                        label_if='ƒ.if_' + label_hash
                        label_else='ƒ.else_' + label_hash
                        label_end='ƒ.endIf_' + label_hash
                    #
                    chunk_if=chunks[0]
                    chunk_end=chunks[1]
                    assert chunk_if[1],'ⓘ should recieve more than 0 arguments but did not: ' + str(chunk_if)
                    assert not chunk_end[1],'ⓧ should recieve 0 arguments but did not: ' + str(chunk_end)
                    args_if=' '.join(chunk_if[1])
                    body_if='\n'.join(chunk_if[2:])
                    body_end='\n'.join(chunk_end[2:])
                    #
                    title="#" + (chunks[0][0] + ' ' + ' '.join(chunks[0][1])).replace("\n",'')  # ⓘ blt £j 3

                    out="""#Beginning of if branch label_hash:
                    ⇥
                    title
                    args_if label_if
                    j label_end
                    label_if:
                    ⇥
                    body_if
                    ⇤
                    label_end:
                    ⇤
                    #End of if branch label_hash
                    body_end"""
                    out=search_replace_simul(out,{
                        'label_hash':label_hash,
                        'label_if':label_if,
                        'label_end':label_end,
                        'args_if':args_if,
                        'body_if':body_if,
                        'body_end':body_end,
                        'title':title
                    })
                    out=out.split('\n')
                    out=[x for x in out if x.lstrip()]
                    return out

        elif chunks[0][0] == 'ⓦ':
            assert len(chunks) == 2  # ⓦ ⓧ
            # Illustration:
            #  ⓦbeq A B
            #     C
            #  ⓧ
            #  ⟱
            # ƒ.while:
            # beq A B

            """
            beq A B ƒ.while
            j ƒ.while.end
            ƒ.while:
                C
                beq A B ƒ.while
            ƒ.while.end:
            """
            #     C
            #     j ƒ.while0
            # ⓧ
            # OLDER Illustration:
            #  ⓦA==B
            #     C
            #  ⓧ
            #  ⟱
            # ƒ.while0:
            # ⓘA==B
            #     C
            #     j ƒ.while0
            # ⓧ
            label_hash=get_hash()  # Might be like AIg5G or something like that
            label_while=random_namespace_hash(10) + label_hash
            if not obfuscate:
                label_while='ƒ.while_' + label_hash
            #
            chunk_while=chunks[0]
            chunk_end=chunks[1]
            assert chunk_while[1],'ⓦ should recieve more than 0 arguments but did not: ' + str(chunk_while)
            assert not chunk_end[1],'ⓧ should recieve 0 arguments but did not: ' + str(chunk_end)
            args_while=' '.join(chunk_while[1])
            body_while='\n'.join(chunk_while[2:])
            body_end='\n'.join(chunk_end[2:])
            #
            title="#" + (chunks[0][0] + ' ' + ' '.join(chunks[0][1])).replace("\n",'')  # ⓘ blt £j 3
            # New version saves a single clock cycle every loop
            if optimize_while_loops:
                out="""#Beginning of while-loop label_hash:
⇥
title
args_while label_while
j label_while.end
label_while:
⇥
body_while
args_while label_while
⇤
label_while.end:
⇤
#End of while-loop label_hash
body_end"""
            else:
                out="""#Beginning of while-loop label_hash:
⇥
title
label_while:
⇥
ⓘ args_while
body_while
j label_while
ⓧ
⇤
⇤
#End of while-loop label_hash
body_end"""
            out=search_replace_simul(out,{
                'label_hash':label_hash,
                'label_while':label_while,
                'args_while':args_while,
                'body_while':body_while,
                'body_end':body_end,
                'title':title
            })
            out=out.split('\n')
            out=[x for x in out if x.lstrip()]
            return out
        elif chunks[0][0] == 'ⓕ':
            assert len(chunks) == 2  # ⓕ ⓧ
            #   ⓕA;B;C
            #       D
            #   ⓧ
            #   ⟱
            #   A
            #   ⓦB
            #       D
            #       C
            #   ⓧ
            label_hash=get_hash()  # Might be like AIg5G or something like that
            label_for='ƒ.for_' + label_hash
            #
            chunk_for=chunks[0]
            chunk_end=chunks[1]
            assert chunk_for[1],'ⓕ should recieve more than 0 arguments but did not: ' + str(chunk_for)
            assert not chunk_end[1],'ⓧ should recieve 0 arguments but did not: ' + str(chunk_end)
            args_for=' '.join(chunk_for[1])
            assert args_for.count(";") == 2,'ⓕ have two semicolons in its arguments ( ⓕ A ; B ; C ) but did not: ' + str(chunk_for)
            args_for=args_for.split(";")
            args_for_0=args_for[0]
            args_for_1=args_for[1]
            args_for_2=args_for[2]
            body_for='\n'.join(chunk_for[2:])
            body_end='\n'.join(chunk_end[2:])
            #
            title="#" + (chunks[0][0] + ' ' + ' '.join(chunks[0][1])).replace("\n",'')  # ⓘ blt £j 3

#             out="""title
# ⇥
# args_for_0
# ⓦ args_for_1
# body_for
# args_for_2
# ⓧ
# ⇤
# # ⓧ
# body_end"""
#             out=search_replace_simul(out,{
#                 'label_hash':label_hash,
#                 'label_for':label_for,
#                 'body_for':body_for,
#                 'body_end':body_end,
#                 'args_for_0':args_for_0,
#                 'args_for_1':args_for_1,
#                 'args_for_2':args_for_2,
#                 'title':title
#             })

            if shorten_for_loops:
                out="""#Beginning of for-loop label_hash:
    ⇥
    title
    args_for_0

args_for_1 label_for.loop
j label_for.end
label_for.loop:
⇥
body_for
args_for_2
args_for_1 label_for.loop
⇤
label_for.end:



    ⇤
    #End of for-loop label_hash
    body_end"""
            else:
                out="""#Beginning of for-loop label_hash:
    ⇥
    title
    args_for_0
    ⓦ args_for_1
    body_for
    args_for_2
    ⓧ
    ⇤
    #End of for-loop label_hash
    body_end"""

            out=search_replace_simul(out,{
                'label_hash':label_hash,
                'label_for':label_for,
                'body_for':body_for,
                'body_end':body_end,
                'args_for_0':args_for_0,
                'args_for_1':args_for_1,
                'args_for_2':args_for_2,
                'title':title
            })
            out=out.split('\n')
            out=[x for x in out if x.lstrip()]
            return out

    # Get a chunk from 'code':
    def grab_chunks():  # Will NOT warn you about unbalanced keywords: aka ⓘⓘⓘⓧ  is analagous to ((()
        starters='ⓘⓦⓕ'  # Things that queue us into looking for ⓧ's
        enders='ⓧ'  # Things that queue us into looking for ⓧ's
        nonlocal code
        first_index=None
        # noinspection PyUnusedLocal
        last_index=None
        for i,chunk in enumerate(code):
            if chunk[0] in starters:
                first_index=i
            if first_index is not None and chunk[0] in enders:
                last_index=i
                return first_index,last_index
        return None,None  # Nothing to be grabbed

    while True:
        # fansi_print(code,'yellow')
        bundle_code_into_chunks()
        # fansi_print(code,'yellow')
        first,last=grab_chunks()
        if first is not None and last is not None:
            chunks=code[first:last + 1]
            # print(first)
            # print(last)
            ccc=process_chunks(chunks)
            # print(ccc)
            code[first:last + 1]=ccc
        else:
            break

    assert code[0][0] == 'ⓧ'
    assert len(code) == 1
    join='\n'.join(code[0][2:])
    join='\n'.join(x.replace('¶','\n') if not x.lstrip().startswith("#") else x for x in join.split("\n"))
    return join
def popper(n) -> str:  # generates a pop_registers macro for n registers
    '''
        .macro pop_registers %0 %1 %2 %3
        	lw %0,0($sp)
        	lw %1,4($sp)
        	lw %2,8($sp)
        	lw %3,12($sp)
        	addi $sp $sp 16
        .end_macro
    '''
    out="""
.macro pop_registers_silentlyA
B
.end_macro
.macro pop_registersA
\tpop_registers_silentlyA
C
.end_macro
"""
    A=''
    for i in range(n):
        A+=' %' + str(i)
    B=[]
    for i in range(n):
        B.append('\tlw %' + str(i) + ' ' + str(4 * (i )) + '($sp)')
    B='\n'.join(B)
    C='\taddi $sp $sp ' + str(n * 4) if n else ''
    from r import search_replace_simul
    return search_replace_simul(out,{'A':A,'B':B,'C':C})
def pusher(n) -> str:  # generates a pop_registers macro for n registers
    ''' .macro push_registers %0 %1
            sw %0,-4($sp)
            sw %1,-8($sp)
            addi $sp $sp -8
        .end_macro
    '''
    out="""

.macro push_registers_silentlyA
B
.end_macro
.macro push_registersA
C
\tpush_registers_silentlyA
.end_macro
"""
    A=''
    for i in range(n):
        A+=' %' + str(i)
    B=[]
    for i in reversed(range(n)):
        B.append('\tsw %' + str(i) + ' ' + str(-4 * (i) - ((n-1) * -4)) + '($sp)')
    B='\n'.join(B)
    # B=B[]
    C='\taddi $sp $sp ' + str(n * -4) if n else ''
    from r import search_replace_simul
    return search_replace_simul(out,{'A':A,'B':B,'C':C})
def pushers_and_poppers(n):
    out=[]
    for i in range(n + 1):
        out.append(pusher(i))
        out.append(popper(i))
    out='\n'.join(out)
    out='\n'.join('\t' + x for x in out.split('\n') if x.lstrip())
    out='''#region All pusher and popper methods for the memory stack:
\t#Equivalent to pop_register %0 ; pop_register %1 ; pop_register %2 ... etc (but faster because we only change $sp once)
\t#Equivalent to push_register %0 ; push_register %1 ; push_register %2 ... etc (but faster because we only change $sp once)\n''' + out + '\n#endregion pusher and popper macros'
    return out
# endregion
# region DEFAULT MACROS:
default_macros="""#region Register Macro Adapters (Addresses carried as $registers, shifts carried as int literals): r2a r2sa r2l r2ls r2las
	#region r2a
	    .data
	    .word
	    t0temp:0
	    .text
        .eqv r2a apply_register_macro_to_address#register [macro] to %shift %address
	    #with 0 arguments:
            .macro apply_register_macro_to_address %register_function %address
                sw $t0 t0temp
                lw $t0 (%address)
                %register_function $t0
                sw $t0 (%address)
                lw $t0 t0temp
            .end_macro
        #with 1 arguments:
            .macro apply_register_macro_to_address %register_function %address %a
                sw $t0 t0temp
                lw $t0 (%address)
                %register_function $t0 %a
                sw $t0 (%address)
                lw $t0 t0temp
            .end_macro
        #with 2 arguments:
            .macro apply_register_macro_to_address %register_function %address %a %b
                sw $t0 t0temp
                lw $t0 (%address)
                %register_function $t0 %a %b
                sw $t0 (%address)
                lw $t0 t0temp
            .end_macro
        #with 3 arguments:
            .macro apply_register_macro_to_address %register_function %address %a %b %c
                sw $t0 t0temp
                lw $t0 (%address)
                %register_function $t0 %a %b %c
                sw $t0 (%address)
                lw $t0 t0temp
            .end_macro
	#endregion

	#region r2sa
        .eqv r2sa apply_register_macro_to_shifted_address#register [macro] to %shift %address
	    #with 0 arguments:
            .macro apply_register_macro_to_shifted_address %register_function %shift %address
                sw $t0 t0temp
                lw $t0 %shift(%address)
                %register_function $t0
                sw $t0 %shift(%address)
                lw $t0 t0temp
            .end_macro
        #with 1 arguments:
            .macro apply_register_macro_to_shifted_address %register_function %shift %address %a
                sw $t0 t0temp
                lw $t0 %shift(%address)
                %register_function $t0 %a
                sw $t0 %shift(%address)
                lw $t0 t0temp
            .end_macro
        #with 2 arguments:
            .macro apply_register_macro_to_shifted_address %register_function %shift %address %a %b
                sw $t0 t0temp
                lw $t0 %shift(%address)
                %register_function $t0 %a %b
                sw $t0 %shift(%address)
                lw $t0 t0temp
            .end_macro
        #with 3 arguments:
            .macro apply_register_macro_to_shifted_address %register_function %shift %address %a %b %c
                sw $t0 t0temp
                lw $t0 %shift(%address)
                %register_function $t0 %a %b %c
                sw $t0 %shift(%address)
                lw $t0 t0temp
            .end_macro
	#endregion

	#region r2l
        .eqv r2l apply_register_macro_to_label#register [macro] to %label %shift
	    #with 0 arguments:
            .macro apply_register_macro_to_label %register_function %label
                sw $t0 t0temp
                lw $t0 %label
                %register_function $t0
                sw $t0 %label
                lw $t0 t0temp
            .end_macro
        #with 1 arguments:
            .macro apply_register_macro_to_label %register_function %label %a
                sw $t0 t0temp
                lw $t0 %label
                %register_function $t0 %a
                sw $t0 %label
                lw $t0 t0temp
            .end_macro
        #with 2 arguments:
            .macro apply_register_macro_to_label %register_function %label %a %b
                sw $t0 t0temp
                lw $t0 %label
                %register_function $t0 %a %b
                sw $t0 %label
                lw $t0 t0temp
            .end_macro
        #with 3 arguments:
            .macro apply_register_macro_to_label %register_function %label %a %b %c
                sw $t0 t0temp
                lw $t0 %label
                %register_function $t0 %a %b %c
                sw $t0 %label
                lw $t0 t0temp
            .end_macro
	#endregion

	#region r2ls
        .eqv r2ls apply_register_macro_to_label_shift#register [macro] to %label %shift
	    #with 0 arguments:
            .macro apply_register_macro_to_label_shift %register_function %label %shift
            	sw $t0 t0temp
            	.data
            		.word
            			r2ls.0arg.temp:0#Is replaced
            	.text
            	la $t0 %label
            	addi $t0 $t0 %shift
            	sw $t0 r2ls.0arg.temp
            	lw $t0 ($t0)
                %register_function $t0
                lw $t1 r2ls.0arg.temp
                sw $t0 ($t1)
                lw $t0 t0temp
            .end_macro
	#endregion

	#region r2las
        .eqv r2las apply_register_macro_to_label_address_shift#register [macro] to %label %address %shift
	    #with 0 arguments:
            .macro apply_register_macro_to_label_address_shift %register_function %label %address %shift
            	sw $t0 t0temp
            	.data
            		.word
            			r2las.0arg.temp:0#Is replaced
            	.text
            	la $t0 %label
            	addi $t0 $t0 %shift
            	add $t0 $t0 %address
            	sw $t0 r2las.0arg.temp
            	lw $t0 ($t0)
                %register_function $t0
                lw $t1 r2las.0arg.temp
                sw $t0 ($t1)
                lw $t0 t0temp
            .end_macro
	#endregion
#endregion

#region Register Macros
    .macro ensure_zero_is_zero
        sub $zero $zero $zero#In-case somehow $zero isn't 0, which from what I understand it doesn't have to be
    .end_macro

    .macro register_plus_equals_int_literal %register %i
        addi %register %register %i
    .end_macro

    .macro register_equals_zero %register
        li %register 0
    .end_macro

    .macro register_times_equals_int_literal %register %i
        sw $t0 t0temp
        li $t0 %i
        mul %register %register $t0
        lw $t0 t0temp
    .end_macro
    .macro register_equals_register_times_int_literal %ghuiopbnm %register %i
        sw $t0 t0temp
        li $t0 %i
        mul %ghuiopbnm %register $t0
        lw $t0 t0temp
    .end_macro

	.macro register_plus_equals_register %registerA %registerB
        add %registerA %registerA %registerB
    .end_macro

	.macro register_minus_equals_register %registerA %registerB
        sub %registerA %registerA %registerB
    .end_macro

	.macro register_times_equals_register %registerA %registerB
        mul %registerA %registerA %registerB
    .end_macro


    #REGISTER_PLUS_EQUALS_LABEL IS A MISTAKE WHEN WE HAVE r2l

    .macro register_left_bitshift_equals_int_literal %register %i
        sll %register %register %i
    .end_macro

    .macro register_right_bitshift_equals_int_literal %register %i
        srl %register %register %i
    .end_macro

    .macro register_left_bitshift_equals_register %register %i
        sllv %register %register %i
    .end_macro

    .macro register_right_bitshift_equals_register %register %i
        srlv %register %register %i
    .end_macro

    .macro register_and_equals_int_literal %register %i
        andi %register %register %i
    .end_macro

    .macro register_or_equals_int_literal %register %i
        ori %register %register %i
    .end_macro

    .macro decrement_register %register
        register_plus_equals_int_literal %register -1
    .end_macro

    .macro increment_register %register
        register_plus_equals_int_literal %register 1
    .end_macro

    #region Stack Pointer Macros:
        .macro decrement_stack_pointer
            register_plus_equals_int_literal $sp -4
        .end_macro

        .macro increment_stack_pointer
            register_plus_equals_int_literal $sp 4
        .end_macro

        .macro push_register %x
        	sw %x,($sp)
        	decrement_stack_pointer
        .end_macro

        .macro pop_register %x
        	increment_stack_pointer
        	lw %x,($sp)
        .end_macro
    #endregion
#endregion

#region Printing Macros
    .macro print_int_literal %int_literal
            sw $v0 tempv0
        sw $a0 tempa0

        li $v0 1
        ensure_zero_is_zero
        addi $a0 $zero %int_literal
        syscall
                lw $v0 tempv0
        lw $a0 tempa0

    .end_macro
    .macro print_char %register
        sw $v0 tempv0
        sw $a0 tempa0
        li $v0 11
        move $a0 %register
        syscall
        lw $v0 tempv0
        lw $a0 tempa0

    .end_macro
    .data .word
        tempa0:0
        tempv0:0
    .text
    .macro print_int_register %register
        sw $v0 tempv0
        sw $a0 tempa0
        li $v0 1
        move $a0 %register
        syscall
        lw $v0 tempv0
        lw $a0 tempa0
    .end_macro

    .macro print_char_register %register
        sw $v0 tempv0
        sw $a0 tempa0
        li $v0 11
        move $a0 %register
        syscall
        lw $v0 tempv0
        lw $a0 tempa0
    .end_macro

    .macro print_int_register_as_hex %register
            sw $v0 tempv0
        sw $a0 tempa0

        li $v0 34
        move $a0 %register
        syscall
                lw $v0 tempv0
        lw $a0 tempa0

    .end_macro

    .macro print_int_register_as_bin %register
            sw $v0 tempv0
        sw $a0 tempa0

        li $v0 35
        move $a0 %register
        syscall
                lw $v0 tempv0
        lw $a0 tempa0

    .end_macro

    .macro print_str_label %str
            sw $v0 tempv0
        sw $a0 tempa0

        li $v0 4
        la $a0 %str
        syscall
                lw $v0 tempv0
        lw $a0 tempa0

    .end_macro

    .macro print_str_from_address_via_register %address_register
        sw $v0 tempv0
        sw $a0 tempa0

        li $v0 4
        move $a0 %address_register
        syscall

        lw $v0 tempv0
        lw $a0 tempa0

    .end_macro

    .macro print_str_literal %str
        .data
            print_str_literal.label: .asciiz %str
        .text
            print_str_label print_str_literal.label
    .end_macro

    #region println macros
        .macro println
            print_str_literal "\\n"
        .end_macro

        .macro println %print_method %print_arg0#Adapter macro used for one-lining println methods
        	%print_method %print_arg0
        	println
        .end_macro

        .macro println %print_method %print_arg0 %print_arg1#Adapter macro used for one-lining println methods
        	%print_method %print_arg0 %print_arg1
        	println
        .end_macro

        .macro println %print_method %print_arg0 %print_arg1 %print_arg2#Adapter macro used for one-lining println methods
        	%print_method %print_arg0 %print_arg1 %print_arg2
        	println
        .end_macro

        .macro println %print_method %print_arg0 %print_arg1 %print_arg2 %print_arg3#Adapter macro used for one-lining println methods
        	%print_method %print_arg0 %print_arg1 %print_arg2 %print_arg3
        	println
        .end_macro
    #endregion
#endregion

.macro lw_lAl %label %address_via_label#A====AddressVia. loadWord Label AddressViaLabel load word: from label(address) to label
	lw $t0 %address_via_label
	lw $t0 ($t0)
	sw $t0 %label
.end_macro

.macro lw_lAl_reversed_args %address_via_label %label #A====AddressVia. loadWord Label AddressViaLabel load word: from label(address) to label
	lw_lAl %label %address_via_label
.end_macro

.macro sw_lAl %label %address_via_label#save word: from label to register(address)
	lw $t0 %label
	lw $t1 %address_via_label
	sw $t0 ($t1)
.end_macro

.macro sw_lAl_reversed_args %address_via_label %label#A====AddressVia. loadWord Label AddressViaLabel load word: from label(address) to label
	sw_lAl %label %address_via_label
.end_macro

.macro sw_ll %labelA %labelB#save word: label label
	lw $t0 %labelA
	sw $t0 %labelB
.end_macro

.macro lw_ll %labelA %labelB#load word: label label
	lw $t0 %labelB
	sw $t0 %labelA
.end_macro

.macro la_ll %labelA %labelB#load address: label label
	la $t0 %labelB
	sw $t0 %labelA
.end_macro

.macro label_plus_equals_label %label0 %label1
	lw $t0 %label0
	lw $t1 %label1
	register_plus_equals_register $t0 $t1
	sw $t0 %label0
.end_macro

.macro set_ri %register %int_literal
	ensure_zero_is_zero
	addi %register $0 %int_literal
.end_macro

.macro lll_array_access %label_array %label_index_words %address_via_label_handler %address_via_label_handler_param0#TESTED :) label=label[label] array access TAKES CARE OF WORD=4*BYTE
	.data
		.word
			lll_array_access.temp0:0
			lll_array_access.temp1:0
	.text
	r2l lw lll_array_access.temp0 %label_index_words#lll_array_access.temp = %label_index_words
	r2l register_left_bitshift_equals_int_literal lll_array_access.temp0 2#Works :) lll_array_access.temp0 *= 4 Multiply it by 4 because 1 index = 1 word = 4 bytes
	r2l la lll_array_access.temp1 %label_array
	label_plus_equals_label lll_array_access.temp0 lll_array_access.temp1#temp0+=temp1
	%address_via_label_handler lll_array_access.temp0 %address_via_label_handler_param0
.end_macro

.macro str2int_Arll %str_address_via_register %int_out_label %goto_on_failure
	move $a0 %str_address_via_register
	li $v0 84#atoi
	syscall
	sw $v0 %int_out_label
	bnez $v1 %goto_on_failure#is -1 on failure to conevert string to int
.end_macro

.macro str2int_lll %str_label %int_out_label %goto_on_failure
	la $t0 %str_label #Optimized (instead of using additional safety variable): This is safe with current implementation of str2int_Arll because str2int_Arll doesn't use $t0
	str2int_Arll $t0 %int_out_label %goto_on_failure
.end_macro

.macro str2int_Arl_squelch %a %b
	str2int_Arll %a %b str2int_Arl.return
	str2int_Arl.return:
.end_macro
.macro swap
.end_macro
.macro swap %r1 %r2
	.data
		.word
			swap.temp:0
	.text
	sw %r1 swap.temp
	move %r1 %r2
	lw %r2 swap.temp
.end_macro


.macro crop_word_to_label_liil %label_word_in %crop_bits_from_left_int_literal %crop_bits_from_right_int_literal %label_word_out#Used for selecting certain bits out of a word
	# Tested :)
	# crop_word_to_label_riil rcode: let crop_word_to_label_riil ==== f
	# 0xABCDEFGH 8 8 --> 0x00BCDEFG  NOTE: All letters are digit-wise variables
	# 0bABCD 1 1 --> 0b00BC
	# 0bABCD 0 2 --> 0b00AB
	#...etc
	lw_ll %label_word_out %label_word_in#label_out = label_in
	#println print_str_literal "HELLO"
	#println r2l print_int_register %label_word_out
	#println r2l print_int_register %label_word_in
	r2l register_left_bitshift_equals_int_literal  %label_word_out %crop_bits_from_left_int_literal
	r2l register_right_bitshift_equals_int_literal %label_word_out %crop_bits_from_left_int_literal
	r2l register_right_bitshift_equals_int_literal %label_word_out %crop_bits_from_right_int_literal
	#println print_str_literal "HELLO1"
	#println r2l print_int_register %label_word_out
	#println r2l print_int_register %label_word_in
.end_macro

.macro crop_word_to_register_riir %register_word_in %crop_bits_from_left_int_literal %crop_bits_from_right_int_literal %register_word_out#Used for selecting certain bits out of a word
	# Untested O.O
	# crop_word_to_label_riil rcode: let crop_word_to_label_riil ==== f
	# 0xABCDEFGH 8 8 --> 0x00BCDEFG  NOTE: All letters are digit-wise variables
	# 0bABCD 1 1 --> 0b00BC
	# 0bABCD 0 2 --> 0b00AB
	#...etc
	move %register_word_out %register_word_in#label_out = label_in
	register_left_bitshift_equals_int_literal  %register_word_out %crop_bits_from_left_int_literal
	register_right_bitshift_equals_int_literal %register_word_out %crop_bits_from_left_int_literal
	register_right_bitshift_equals_int_literal %register_word_out %crop_bits_from_right_int_literal
.end_macro

.macro crop_word_to_register_rrrr %register_word_in %crop_bits_from_left_int_literal %crop_bits_from_right_int_literal %register_word_out#Used for selecting certain bits out of a word
	# Untested O.O
	# crop_word_to_label_riil rcode: let crop_word_to_label_riil ==== f
	# 0xABCDEFGH 8 8 --> 0x00BCDEFG  NOTE: All letters are digit-wise variables
	# 0bABCD 1 1 --> 0b00BC
	# 0bABCD 0 2 --> 0b00AB
	#...etc
	move %register_word_out %register_word_in#label_out = label_in
	register_left_bitshift_equals_register  %register_word_out %crop_bits_from_left_int_literal
	register_right_bitshift_equals_register %register_word_out %crop_bits_from_left_int_literal
	register_right_bitshift_equals_register %register_word_out %crop_bits_from_right_int_literal
.end_macro

#region For PseudoMips Debugger
    .data
        .word
            functionCallCounter:0
            functionCallCounter.temp:0
            functionCallCounter.tempB:0
            functionCallCounter.indentBCount:0#Gets set to max(functionCallCounter.indentBCount, functionCallCounter) all the time
        .asciiz
        functionCallCounter.indent: "> "
        functionCallCounter.indentB:"  "
    .text
    .macro functionCallCounter.printIndent %indent %indentB
        sw $t9 functionCallCounter.temp
        sw $t8 functionCallCounter.tempB
        lw $t9 functionCallCounter
        lw $t8 functionCallCounter.indentBCount

        blt $t8 $t9 functionCallCounter.updateIndentBCount
        j functionCallCounter.prewhile
        functionCallCounter.updateIndentBCount:
        sw $t9 functionCallCounter.indentBCount
        move $t8 $t9

        functionCallCounter.prewhile:

        sub $t9 $t8 $t9
        functionCallCounter.whileCheck:
        bgtz $t8 functionCallCounter.whileBody#bgez for an extra space between pseudo mips d
        j functionCallCounter.whileEnd
        functionCallCounter.whileBody:

            bgt $t8 $t9 functionCallCounter.doIndent

            functionCallCounter.doIndentB:
            print_str_literal %indentB

            j functionCallCounter.squanch
            functionCallCounter.doIndent:
            print_str_literal %indent

            functionCallCounter.squanch:

            decrement_register $t8


        j functionCallCounter.whileCheck
        functionCallCounter.whileEnd:
        lw $t9 functionCallCounter.temp
        lw $t8 functionCallCounter.tempB
    .end_macro
    .macro functionCallCounter.inc
        r2l increment_register functionCallCounter
    .end_macro
    .macro functionCallCounter.dec
        r2l decrement_register functionCallCounter
    .end_macro
#endregion

#region Int literal macros
    .macro l0 %register
        li %register 0
    .end_macro
    .macro l1 %register
        li %register 1
    .end_macro
    .macro l2 %register
        li %register 2
    .end_macro
    .macro l3 %register
        li %register 3
    .end_macro
    .macro l4 %register
        li %register 4
    .end_macro
    .macro l5 %register
        li %register 5
    .end_macro
    .macro l6 %register
        li %register 6
    .end_macro
    .macro l7 %register
        li %register 7
    .end_macro
    .macro l8 %register
.end_macro
    .macro l9 %register
        li %register 9
    .end_macro
#endregion
.macro post_increment %output %input
    move %output %input
    increment_register %input
.end_macro
.macro post_decrement %output %input
    move %output %input
    decrement_register %input
.end_macro
.macro pre_increment %output %input
    increment_register %input
    move %output %input
.end_macro
.macro pre_decrement %output %input
    decrement_register %input
    move %output %input
.end_macro
.macro exec %function_label

.end_macro

.macro read_word_array_rrr %out %arr_ay %index
    muli %out %index 4       #out  = index * 4
    add %out %out %arr_ay    #out += array
    lw  %out (%out)         #out  = *out
.end_macro

.macro read_byte_array_rrr %out %arr_ay %index
    add %out %index %arr_ay    #out += array
    lb  %out (%out)         #out  = *out
.end_macro

# .macro write_byte_array_rrr %arr_ay %index
#     .data
#     temp:.word 0
#     .text
#
#     add %out %out %arr_ay    #out += array
#     lb  %out (%out)         #out  = *out
# .end_macro

.macro call %func
    push_register $ra
    jal %func
    pop_register $ra
.end_macro


.macro print_int_register_as_hex_digit %i #only works for 0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F. Does nothing on failure.
    beq %i 0  print_int_register_as_hex_digit.0
    beq %i 1  print_int_register_as_hex_digit.1
    beq %i 2  print_int_register_as_hex_digit.2
    beq %i 3  print_int_register_as_hex_digit.3
    beq %i 4  print_int_register_as_hex_digit.4
    beq %i 5  print_int_register_as_hex_digit.5
    beq %i 6  print_int_register_as_hex_digit.6
    beq %i 7  print_int_register_as_hex_digit.7
    beq %i 8  print_int_register_as_hex_digit.8
    beq %i 9  print_int_register_as_hex_digit.9
    beq %i 10 print_int_register_as_hex_digit.10
    beq %i 11 print_int_register_as_hex_digit.11
    beq %i 12 print_int_register_as_hex_digit.12
    beq %i 13 print_int_register_as_hex_digit.13
    beq %i 14 print_int_register_as_hex_digit.14
    beq %i 15 print_int_register_as_hex_digit.15
    print_str_literal "?"#Failed to write digit
    j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.0:
        print_str_literal "0"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.1:
        print_str_literal "1"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.2:
        print_str_literal "2"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.3:
        print_str_literal "3"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.4:
        print_str_literal "4"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.5:
        print_str_literal "5"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.6:
        print_str_literal "6"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.7:
        print_str_literal "7"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.8:
        print_str_literal "8"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.9:
        print_str_literal "9"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.10:
        print_str_literal "A"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.11:
        print_str_literal "B"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.12:
        print_str_literal "C"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.13:
        print_str_literal "D"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.14:
        print_str_literal "E"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.15:
        print_str_literal "F"
        j print_int_register_as_hex_digit.return
    print_int_register_as_hex_digit.return:
.end_macro


.macro print_hex_byte %register

    .data
        .word
        phb.temp:0
    .text

    #DOESN'T do it in a confusing way

    sw $t5 phb.temp

	crop_word_to_register_riir %register 24 4 $t5
	print_int_register_as_hex_digit $t5

	crop_word_to_register_riir %register 28 0 $t5
	print_int_register_as_hex_digit $t5


    lw $t5 phb.temp

.end_macro
.macro datadump %label %length_literal
    la $s0 %label
	lz $s1
	blt $s1 %length_literal  loop
	j end
	loop:
        add $s2 $s0 $s1
        lb $s2 ($s2)
        print_hex_byte $s2
		inc $s1
		blt $s1 %length_literal loop
	end:
.end_macro

.macro move_byte %a %b %temp
	#If you're willing to sacrifice a temp variable's integrity you can gain a little bit of speed
	lb $t0 (%a)
	sb $t0 (%b)
.end_macro

.macro move_byte %a %b
	mthi $t0
	move_byte %a %b $t0
	mfhi $t0
.end_macro

.macro dialog %msg
    #%msg is str literal
    .data
        msg: .asciiz %msg
    .text
        sw $v0 tempv0
        sw $a0 tempa0

        li $v0 50
        la $a0 msg
        syscall

        lw $v0 tempv0
        lw $a0 tempa0
.end_macro
3
#region MACRO EQUIVALENTS
    # pl = printline
    # pint = print int
    # pinti = print int immediate
    # phex = print hex
    # pbin = print binary
    # pchar = print char
    # pstr = print string
    # pstrl = print string literal
    # inc = increment = '++'
    # dec = decrement = '--'
    # pe = plus equals = '+='
    # me = minus equals = '-='
    # te = times equals = '*='
    # tei = times equals immediate = '*='
    # pei = plus equals immediate = '+='
    # muli = multiply immediate
    # rbei = right bitshift equals immediate = '>>='
    # lz = load zero
    # l0 = load 0, l1 = load 1, l2 = load 2, ... l9 = load 9
    .eqv pl println
    .eqv pint print_int_register
    .eqv pinti print_int_literal
    .eqv phex print_int_register_as_hex
    .eqv pbin print_int_register_as_bin
    .eqv pchar print_char_register
    .eqv pstr print_str_from_address_via_register
    .eqv pstrl print_str_literal
    .eqv inc increment_register
    .eqv dec decrement_register
    .eqv pe register_plus_equals_register
    .eqv me register_minus_equals_register
    .eqv te register_times_equals_register
    .eqv tei register_times_equals_int_literal
    .eqv pei register_plus_equals_int_literal
    .eqv muli register_equals_register_times_int_literal
    .eqv rbei register_right_bitshift_equals_int_literal
    .eqv lz register_equals_zero #This one might be so sugary it might be a bit toxic...doesn't save any redundancy...
    .eqv rwa read_word_array_rrr # %out %arr_ay %index
    .eqv rba read_byte_array_rrr # %out %arr_ay %index
# endregion




"""
# endregion
#region Main:
fansi_print("WRITING MIPS CODE...",'blue','bold',new_line=False)
tic()
mips_code=parse_automips2_to_mips(code)
fansi_print("completed in "+str(toc())+" seconds",'blue','bold')
if run_code:
    for i,line in enumerate(mips_code.split("\n")):
        fansi_print(" "*(4-len(str(i+1)))+str(i+1)+" ⎸",'blue','bold',new_line=False)
        print(line)
    if isolation_test:
        some_random_ass_directory='RandomAssDirectory_'+random_namespace_hash(5)+'/'
        asmdir+=some_random_ass_directory
        shell_command("mkdir "+asmdir)
        fansi_print("ISOLATION TEST: "+asmdir+asmfile,'magenta','bold')
    else:
        fansi_print("OUTPUT FILE: "+asmdir+asmfile,'magenta','bold')
    string_to_text_file(asmdir+asmfile,mips_code)
    fansi_print("RUNNING MIPS CODE...this could take a few seconds. Output will be printed in console once it terminates.",'blue','bold')
    tic()
    fansi_print(shell_command("java -jar "+marsjar+" "+str(max_steps)+" "+asmdir+asmfile),'yellow')
    fansi_print("completed in "+str(toc())+" seconds",'blue','bold')
else:
    string_to_clipboard(printed(mips_code))
#endregion
#region Old MIPS Code
# code="""
# ##############################################################
# # Homework #2
# # name: Ryan Burgert
# # sbuid: 110176886
# ##############################################################
#
# .eqv pl println
# .eqv pint print_int_register
# .eqv pinti print_int_literal
# .eqv phex print_int_register_as_hex
# .eqv pbin print_int_register_as_bin
# .eqv pchar print_char_register
# .eqv pstr print_str_from_address_via_register
# .eqv pstrl print_str_literal
# .eqv inc increment_register
# .eqv dec decrement_register
# .eqv pe register_plus_equals_register
# .eqv me register_minus_equals_register
# .eqv te register_times_equals_register
# .eqv tei register_times_equals_int_literal
# .eqv pei register_plus_equals_int_literal
# .eqv muli register_equals_register_times_int_literal
# .eqv rbei register_right_bitshift_equals_int_literal
# .eqv _dec post_decrement
# .eqv _inc post_increment
# .eqv inc_ pre_increment
# .eqv dec_ pre_decrement
# .eqv rwa read_word_array
# .eqv rha read_half_array
# .eqv rba read_byte_array
# .eqv wwa write_word_array
# .eqv wha write_half_array
# .eqv wba write_byte_array
# .eqv lz register_equals_zero #This one might be so sugary it might be a bit toxic...doesn't save any redundancy...
#
# .include "HW2/hw2_examples.asm"
#
# #region HOMEWORK FUNCTIONS:
#
#     ▶ verifyIPv4Checksum £header ~ £header
#         #Tested :) ✔ (after refactoring)
#         #Optimized :)
#         #Returns 1 value
#
#         #Get the sum of all half-words in the header
#         lz £sum
#         ∘ £header_length_in_words = get_header_length £header
#         add £header_length_in_halves £header_length_in_words £header_length_in_words
#         add £header_length_in_bytes £header_length_in_halves £header_length_in_halves
#         add £end £header_length_in_bytes £header # ⟵ For optimization
#         ⓕ move £i £header ; blt £i £end ; pei £i 2
#             # pe £sum [∘ ◊ = read_half_array £header £i] ⟵ Was since optimized because this was a bottleneck
#             pe £sum [lhu ◊ (£i)]
#         ⓧ
#
#         #Now to do the carrying stuff for the sum as seen on Wikipedia...
#         #2¹⁶ = 65536 (I'm not sure why bge didn't work when I used an int literal; but this seems to work too)
#         ⓦ bge £sum [li ◊ 65536]
#             andi £overflow £sum 0xFFFF0000
#             rbei £overflow 8
#             rbei £overflow 8
#             andi £sum £sum 0x0000FFFF
#             pe £sum £overflow
#         ⓧ
#
#         #Flip the bits of the sum then return only the second half-word of the result
#         ⮐ [andi ◊ [∘ ◊ = bit_flip £sum] 0x0000FFFF]
#
#     ▶ get_header_length £header_address ~ $ra £header_address
#         #Second 4 bits of the 3rd byte of the first word of the header contains the header length
#         lw $v0 (£header_address)
#         crop_word_to_register_riir $v0 4 24 $v0 # assert ∃ .macro crop_word_to_register_riir %register_word_in %crop_bits_from_left_int_literal %crop_bits_from_right_int_literal %register_word_out#Used for selecting certain bits out of a word
#         ⮐ $v0
#
#     ▶ get_total_length £header_address ~ $ra £header_address
#         lw $v0 (£header_address)
#         crop_word_to_register_riir $v0 16 0 $v0
#         ⮐ $v0
#
#     ▶ print_packet_array_test £address
#         # This is just a test to see if I understand how the packet arrays work in this homework. It just takes a packet array, such as pktArray_ex3 from hw2_examples.asm, and prints the string contents of the whole thing.
#         ∘ £total_length_in_bytes = get_total_length £address
#         ∘ £header_length_in_words = get_header_length £address
#         pl pstr [add ◊ £address [muli ◊ £header_length_in_words 4]]
#         pl phex [lw ◊ (£address)]
#         add £next_packet_address £address £total_length_in_bytes
#         ∘ ƒ £next_packet_address
#
#     ▶ processDatagram £msg £M £sarray
#         #Returns 1 value (sarray.ℓ for success and -1 for failure)
#         #Started writing this method at 9:01pm, Oct8
#         #Finished writing (about to test) writing this method at 9:26pm, Oct8
#         #M≣Desired ↈbytes in string
#
#         #Step 0: Assert M>0
#         ⓘ blez £M
#             ⮐ [li ◊ -1]
#             ⮐
#         ⓧ
#
#         #Step 1: Set msg[M] = '\\0'
#         sb [li ◊ '\\0'] ([add ◊ £msg £M])
#
#         #Step 2: Replace all '\\n' characters in string to '\\0', and add each index to £sarray
#         # move £i £msg # Used as a char pointer
#         # add £end £msg £M
#
#         ∘ write_word_array £sarray [li ◊ 0] £msg
#         l1 £j
#
#
#         ⓕ l1 £i ; blt £i £M ; inc £i
#             lb £char ([add ◊ £msg £i])
#             ⓘ beq £char '\\n'
#                 ∘ write_word_array £sarray £j [addi ◊ [add ◊ £msg £i] 1]
#                 sb [li ◊ 0] ([add ◊ £msg £i])
#                 inc £j
#             ⓧ
#         ⓧ
#         ⮐ £j
#
#     ▶ printDatagram £parray £n £msg £sarray
#         # Started writing at 9:30pm Oct 8, finished 9:56
#         #Returns 1 value (0 for success and -1 for failure)
#
#         # Step 1: Call extractData, and return -1 if its first output < 0
#         # Also, set £M to extractData's second output for later use
#         ⓘ bltz [∘ ◊ £M = extractData £parray £n £msg]
#             ⮐ [li ◊ -1]
#             ⮐
#         ⓧ
#
#         # Step 2: Call processDatagram, and return -1 if its first output < 0
#         ∘ £sarray_length = processDatagram £sarray £M £msg
#         pstrl "sarray_length ="¶ pl pint £sarray_length
#         ⓘ bltz £sarray_length
#             ⮐ [li ◊ -1]
#             ⮐
#         ⓧ
#
#         # Step 3: Call print, and return -1 if its first output < 0
#         ⓘ bltz [∘ ◊ = printStringArray £sarray [lz ◊] [addi ◊ £sarray_length -1] £sarray_length]
#             ⮐ [li ◊ -1]
#             ⮐
#         ⓧ
#
#         ⮐ [lz ◊]
#
#
#     ▶ extractData £parray £n £msg
#         #Tested AND optimized :) ✔
#         #Returns 2 values
#         #Assumes each header is 15 words long and has a header length of 5 words
#         #NOTE: Don't forget to assert checksums!
#
#         #Make all checksum assertions before proceeding to modify msg: Will ONLY modify msg if all the assertions are successful!
#         move £header_address £parray #header_address is changed several times while going down the array
#         ⓕ lz £k ; blt £k £n ; inc £k ¶ pei £header_address 60
#             #First, assert not verifyIPv4Checksum(header): (from HW description) "returns … (-1,k) on failure … k is the first array index with a checksum error."
#             ⓘ bnez [∘ ◊ = verifyIPv4Checksum £header_address]
#                 ⮐ [li ◊ -1] £k
#                 ⮐
#             ⓧ
#         ⓧ
#
#         #All checksum assertions were successful; proceeding to write to msg
#         move £header_address £parray #header_address is changed several times while going down the array
#         lz £M #M ≣ msg_length = ↈbytes written to msg
#         ⓕ lz £k ; blt £k £n ; inc £k ¶ pei £header_address 60
#             addi £payload_length [∘ ◊ = get_total_length £header_address] -20 #My debugger let me see this was commented out and thats why it was borking! Get payload length in bytes
#             addi £payload_address £header_address 20 #payload address = header address + 20 bytes
#             pe £M £payload_length
#             ⓕ lz £j ; blt £j £payload_length ; inc £j ¶ inc £payload_address ¶ inc £msg
#                 lb £char (£payload_address)
#                 sb £char (£msg)
#             ⓧ
#         ⓧ
#         ⮐ [lz ◊] £M
#
#     ▶ printStringArray £sarray £startIndex £endIndex £length
#         #region Input Assertions:
#             blt £length 1 ƒ.error
#             bltz £startIndex ƒ.error
#             bltz £endIndex ƒ.error
#             bge £startIndex £length ƒ.error
#             bge £endIndex £length ƒ.error
#             blt £endIndex £startIndex ƒ.error
#         lz £out
#         ⓕ move £i £startIndex ; ble £i £endIndex ; inc £i ¶ inc £out
#             ∘ £string = read_word_array £sarray £i
#             pl pstr £string
#             pl
#         ⓧ
#         dec £out
#         ⮐ £out
#         ⮐
#         ƒ.error:
#         li £negativeOne -1
#         ⮐ £negativeOne
#         ⮐
#
#     ▶ replace1st £string £toReplace £replaceWith
#         #region Input Assertions:
#             blt £toReplace 0x00 ƒ.error
#             blt £replaceWith 0x00 ƒ.error
#             bgt £toReplace 0x7F ƒ.error
#             bgt £replaceWith 0x7F ƒ.error
#         ∘ £length = string_length £string
#         ⓕ lz £i ; blt £i £length ; inc £i
#             ∘ £char = read_byte_array £string £i
#             ⓘ beq £char £toReplace
#                 ∘ write_byte_array £string £i £replaceWith
#                 add £out £i £string
#                 ⮐ £out
#                 ⮐
#             ⓧ
#         ⓧ
#         lz $0
#         ⮐ $0
#         ⮐
#         ƒ.error:
#         li £negativeOne -1
#         ⮐ £negativeOne
#
# ⮤ #ARRAY FUNCTIONS:
#
#     ⮤ word2half = lambda x:[x,x.replace('4','2').replace('word','half').replace('lw','lhu')]
#     ⮤ byte2wordhalf = lambda x:[x,x.replace('byte','half'),x.replace('byte','word')]
#
#     ▶ force_print £string £length
#         #Will print all characters, not stopping at '\\0' characters. It will print 'length' number of bytes.
#         li $v0 11
#         ⓕ lz £i ; blt £i £length ; inc £i
#             $v0 § ∘ $a0 = read_byte_array £string £i
#             syscall
#         ⓧ
#
#     ▶ reverse_string £address ~ £address
#         ∘ reverse_byte_array £address [∘ ◊ = string_length £address]
#
#     ▶ print_word_array £array £length £spacer_string
#         # Prints the words like "5, 7, 3, 7, 8," where spacer_string is ', '
#         ⓕ lz £i ; blt £i £length ; nop
#             ∘ £t = read_word_array £array £i
#             pint £t
#             inc £i
#             ⓘ blt £i £length
#                 pstr £spacer_string
#             ⓧ
#         ⓧ
#
#     ▶ simple_print_word_array £array £length
#         Δ ƒ.spacer_string: .asciiz ", "
#         ∘ print_word_array £array £length [la ◊ ƒ.spacer_string]
#
#     ▶ string_length £address ~ $ra
#         lb £char (£address)
#         ⓕ lz £length ; bnez £char ; inc £length ¶ inc £address
#             lb £char (£address)
#         ⓧ
#         ⮐ £length
#
#     ▶ read_byte_array £address £index ~ £address £index $ra
#         ⮐ [lb ◊ ([add ◊ £address £index])]
#
#     ▶ read_word_array £address £index ~ £address £index $ra ⮤ word2half #read_half_array
#         ⮐ [lw ◊ ([add ◊ £address [muli ◊ £index 4]])]
#
#     ▶ write_byte_array £address £index £value ~ £address £index £value $ra
#         sb £value ([add ◊ £address £index])
#
#     ▶ write_word_array £address £index £value ~ £address £value £index $ra ⮤ word2half
#         sw £value ([add ◊ £address [muli ◊ £index 4]])
#
#     ▶ little_to_big_endian_address £x ~ $ra £x
#         #x ≣ big_endian_address
#         #This function exists to save my sanity by converting a little-endian address into a big-endian one.
#         #https://www.desmos.com/calculator/ydexwmp6wf
#         # y﹦x﹢3﹣2·(x % 4)
#         ⮐ [sub ◊ [addi ◊ £x 3] [sll ◊ [div £x [li ◊ 4] ¶ mfhi ◊] 1]]
#
#     ▶ big_to_little_endian_address £x ~ £x
#         #This is the inverse function of little_to_big_endian_address
#         #https://www.desmos.com/calculator/7quxauw0ac
#         # f⁻¹(x)﹦f(x﹢1)﹢1
#         ⮐ [addi ◊ [∘ ◊ = little_to_big_endian_address [addi ◊ £x 1]] 1]
#
#     ▶ word_from_four_bytes £AB £CD £EF £GH ~ $ra £AB £CD £EF £GH
#         #Outputs word 0xABCDEFGH
#         lz $v0
#         pe $v0 £AB ¶ sll $v0 $v0 8
#         pe $v0 £CD ¶ sll $v0 $v0 8
#         pe $v0 £EF ¶ sll $v0 $v0 8
#         pe $v0 £GH
#         ⮐ $v0
#
#     ▶ swap_byte_array £address £indexA £indexB ~ £address £indexA £indexB ⮤ byte2wordhalf
#         ∘ £valueA = read_byte_array £address £indexA
#         ∘ £valueB = read_byte_array £address £indexB
#         ∘ write_byte_array £address £indexA £valueB
#         ∘ write_byte_array £address £indexB £valueA
#
#     ▶ reverse_byte_array £address £length ~ £address £length ⮤ byte2wordhalf
#         li £left 0
#         addi £right £length -1
#         ⓦ blt £left £right
#             ∘ swap_byte_array £address £left £right
#             dec £right
#             inc £left
#         ⓧ
#
#     ▶ bubble_sort_byte_array £address £length ~ £address £length ⮤ byte2wordhalf
#         ⓕ lz £iteration ; blt £iteration £length ; inc £iteration
#             ⓕ lz £index ; blt £index £length ; inc £index
#                 addi £jindex £index 1
#                 ∘ £left = read_byte_array £address £index
#                 ∘ £right = read_byte_array £address £jindex
#                 ⓘ bgt £left £right
#                     ∘ swap_byte_array £address £index £jindex
#                 ⓧ
#             ⓧ
#         ⓧ
#
# ⮤ #MATH FUNCTIONS:
#
#     ▶ ternary £bool £if_true £if_false ~ $ra £if_true £if_false £bool
#         ⓘ bnez £bool
#             ⮐ £if_true
#         ⓔ
#             ⮐ £if_false
#         ⓧ
#
#     ▶ min £a £b ~ $ra £a £b ⮤ lambda x:[x,x.replace('ble','bge').replace('min','max')]
#         ⓘ ble £a £b
#             ⮐ £a
#         ⓔ
#             ⮐ £b
#         ⓧ
#
#     ▶ pow £base £exponent ~ $ra £base £exponent
#         # Tested :) ✔
#         # Only works for integer base and positive integer exponent
#         li $v0 1
#         ⓕ lz £i ; blt £i £exponent ; inc £i
#             te $v0 £base
#         ⓧ
#         ⮐ $v0
#
#     ▶ mod £a £b ~ $ra £a £b ⮤ lambda x:[x,x.replace('hi','lo').replace('mod','quotient')]
#         # Tested ✔
#         ⮐ [div £a £b ¶ mfhi ◊]
#
#     ▶ is_prime £n ~ £n $ra
#         # Tested ✔
#         ⓕ l2 £i ; blt £i £n ; inc £i
#         # [∘ ◊ = mod £n £i]
#             ⓘ beqz [div £n £i ¶ mfhi ◊]
#                 ⮐ [l0 ◊]
#                 ⮐
#             ⓧ
#         ⓧ
#         ⮐ [l1 ◊]
#
#     ▶ fibonacci_recursive £i
#         # ƒ(0)=1, ƒ(1)=1, ƒ(2)=2 … etc # Tested ✔
#         ⓘ ble £i 1
#             ⮐ [li ◊ 1]
#         ⓔ
#             ⮐ [add ◊ [∘ ◊ = ƒ [addi ◊ £i -1]] [∘ ◊ = ƒ [addi ◊ £i -2]]]
#         ⓧ
#
#     ▶ factorial_recursive £i
#         # Tested ✔
#         ⓘ blez £i
#             ⮐ [li ◊ 1]
#         ⓔ
#             ⮐ [mul ◊ £i [∘ ◊ = ƒ [addi ◊ £i -1]]]
#         ⓧ
#
#     ▶ bit_flip £i ~ £i $ra
#         # Tested ✔
#         ⮐ [xori ◊ £i 0xFFFFFFFF]
#
# ⮤ #TEST METHODS:
#
#     ▶ test_verifyIPv4Checksum
#         pstrl "Checksum valid_header_ex1:"
#         pl pint [∘ ◊  = verifyIPv4Checksum [la ◊ valid_header_ex1]]
#         pstrl "Checksum valid_header_ex2:"
#         pl pint [∘ ◊  = verifyIPv4Checksum [la ◊ valid_header_ex2]]
#         pstrl "Checksum invalid_header_ex1:"
#         pl pint [∘ ◊  = verifyIPv4Checksum [la ◊ invalid_header_ex1]]
#         pstrl "Checksum invalid_header_ex2:"
#         pl pint [∘ ◊  = verifyIPv4Checksum [la ◊ invalid_header_ex2]]
#
#     ▶ test_get_header_and_total_length
#         pstrl "get_total_length(pktArray_ex1) = "
#         pl pint [∘ ◊ = get_total_length [la ◊ pktArray_ex1]]
#         pstrl "get_total_length(pktArray_ex2) = "
#         pl pint [∘ ◊ = get_total_length [la ◊ pktArray_ex2]]
#         pstrl "get_total_length(pktArray_ex3) = "
#         pl pint [∘ ◊ = get_total_length [la ◊ pktArray_ex3]]
#         pstrl "get_total_length(pktArray_ex4) = "
#         pl pint [∘ ◊ = get_total_length [la ◊ pktArray_ex4]]
#         pstrl "get_header_length(pktArray_ex1) = "
#         pl pint [∘ ◊ = get_header_length [la ◊ pktArray_ex1]]
#         pstrl "get_header_length(pktArray_ex2) = "
#         pl pint [∘ ◊ = get_header_length [la ◊ pktArray_ex2]]
#         pstrl "get_header_length(pktArray_ex3) = "
#         pl pint [∘ ◊ = get_header_length [la ◊ pktArray_ex3]]
#         pstrl "get_header_length(pktArray_ex4) = "
#         pl pint [∘ ◊ = get_header_length [la ◊ pktArray_ex4]]
#
#     ▶ test_replace1st
#         .macro test_replace1st_macro %string_literal %char_literal_old %char_literal_new
#             .data
#                 .asciiz
#                     string:
#                         %string_literal
#             .text
#             la £string string
#             pl pstr £string
#             li £toReplace  %char_literal_old
#             li £replaceWith %char_literal_new
#             ∘ £result = replace1st £string £toReplace £replaceWith
#             pl pstr £string
#             pl phex £result
#             pl
#         .end_macro
#         test_replace1st_macro "Hello" 'l' 'p'
#         test_replace1st_macro "Lalish" 'l' 'p'
#
#     ▶ test_printStringArray
#         Δ sarray0: .asciiz "Stony Brook"
#         Δ sarray1: .asciiz "Computer Science"
#         Δ sarray2: .asciiz "MIPS is amazing!!"
#         Δ sarray3: .asciiz "I\\nlove\\nprogramming"
#         Δ sarray4: .asciiz "FarBeyond"
#         Δ sarray: .word sarray0 sarray1 sarray2 sarray3 sarray4
#         .macro test_printStringArray_macro %arr_ay %start %end %length
#             pl pstrl "TEST CASE:"
#             la £sarray %arr_ay
#             li £startIndex %start
#             li £endIndex %end
#             li £length %length
#             ∘ £result = printStringArray £sarray £startIndex £endIndex £length
#             pstrl "RESULT: "
#             pl pint £result
#         .end_macro
#
#         test_printStringArray_macro sarray 0 2 4
#         test_printStringArray_macro sarray 3 4 5
#         test_printStringArray_macro sarray 1 1 5
#         #test_printStringArray_macro sarray 0 4 -2
#         #test_printStringArray_macro sarray -1 2 5
#         test_printStringArray_macro sarray 0 5 5
#         test_printStringArray_macro sarray 3 2 5
#
# ⮤ #MAIN METHOD:
#
#     ▶ zmain
#         # ⓕ li £i 0 ; blt £i 10 ; inc £i
#         #     pstrl "factorial("
#         #     pint £i
#         #     pstrl ") = "
#         #     pl pint [∘ ◊ = factorial £i]
#         # ⓧ
#
#
#
#         ⓕ li £i 0 ; blt £i 200 ; inc £i
#             # pstrl "Prime("
#             # pint £i
#             # pstrl ") = "
#             pint [∘ ◊ = is_prime £i]
#             # pl
#         ⓧ
#         #
#         ∘ test_get_header_and_total_length
#         ∘ test_verifyIPv4Checksum
#         ∘ test_replace1st
#         ∘ test_printStringArray
#
#         ∘ force_print [addi ◊ [la ◊ msg_buffer] 2] [li ◊ 200]
#
#         ∘ £outA £outB = extractData [la ◊ pktArray_ex3] [l4 ◊] [la ◊ msg_buffer]
#         # pstrl "OutA = "
#         # pint £outA
#         # pstrl "; OutB = "
#         # pl pint £outB
#         # pstr [la ◊ msg_buffer]
#
        # ∘ £m = processDatagram [la ◊ msg] [li ◊ 26] [la ◊ abcArray]
        # pl pint £m
        # ∘ simple_print_word_array  [la ◊ abcArray] £m
        # pl
        # ∘ printStringArray [la ◊ abcArray] [li ◊ 0] [addi ◊ £m -1] £m
#
#
#         # ∘ printDatagram [la ◊ pktArray_ex3] [l4 ◊] [la ◊ msg_buffer] [la ◊ abcArray]
#     ▶ factorial £n ~ £n $t0
#         li $v0 1
#         ⓕ li $t0 2 ; ble $t0 £n ; inc $t0
#             te $v0 $t0
#         ⓧ
#         ⮐ $v0
#
#
#
#
# """
# """
# ##############################################################
# # Homework #2
# # name: Ryan Burgert
# # sbuid: 110176886
# ##############################################################
#
# .eqv pl println
# .eqv pint print_int_register
# .eqv pinti print_int_literal
# .eqv phex print_int_register_as_hex
# .eqv pbin print_int_register_as_bin
# .eqv pchar print_char_register
# .eqv pstr print_str_from_address_via_register
# .eqv pstrl print_str_literal
# .eqv inc increment_register
# .eqv dec decrement_register
# .eqv pe register_plus_equals_register
# .eqv me register_minus_equals_register
# .eqv te register_times_equals_register
# .eqv tei register_times_equals_int_literal
# .eqv pei register_plus_equals_int_literal
# .eqv muli register_equals_register_times_int_literal
# .eqv rbei register_right_bitshift_equals_int_literal
# .eqv lz register_equals_zero #This one might be so sugary it might be a bit toxic...doesn't save any redundancy...
#
# # pl = printline
# # pint = print int
# # pinti = print int immediate
# # phex = print hex
# # pbin = print binary
# # pchar = print char
# # pstr = print string
# # pstrl = print string literal
# # inc = increment = '++'
# # dec = decrement = '--'
# # pe = plus equals = '+='
# # me = minus equals = '-='
# # te = times equals = '*='
# # tei = times equals immediate = '*='
# # pei = plus equals immediate = '+='
# # muli = multiply immediate
# # rbei = right bitshift equals immediate = '>>='
# # lz = load zero
# # l0 = load 0, l1 = load 1, l2 = load 2, ... l9 = load 9
#
#
# # .include "HW2/hw2_examples.asm"
#
# #region HOMEWORK FUNCTIONS:
#
#     ▶ get_header_length £header_address ~ $ra £header_address
#         #Second 4 bits of the 3rd byte of the first word of the header contains the header length # assert ∃ .macro crop_word_to_register_riir %register_word_in %crop_bits_from_left_int_literal %crop_bits_from_right_int_literal %register_word_out#Used for selecting certain bits out of a word
#         ⮐ [crop_word_to_register_riir [lw ◊ (£header_address)] 4 24 ◊]
#
#     ▶ ℳget_total_length £header_address ~ $ra £header_address
#         ⮐ [crop_word_to_register_riir [lw ◊ (£header_address)] 16 0 ◊]
#
#     ▶ replace1st $a0 $a1 $a2 ~ $v0 $a0 $a1 $a2 $s0 $ra
#         #int replace1st(str, a, b): Replaces first occurrence of 'a' in 'str' with 'b'
#         #   If bad inputs, returns -1
#         #   If no matches, returns 0
#         #   Else, returns 1 + (address of first occurrence of 'a')
#         .macro replace1st.macro %out %str %a %b %char
#             blt %a 0x00 error        # assert a ≥ 0
#             blt %b 0x00 error        # assert b ≥ 0
#             bgt %a 0x7F error        # assert a ≤ 127
#             bgt %b 0x7F error        # assert b ≤ 127
#             lz  %out                 # out = 0
#             while:
#                 lb   %char (%str)    # char = *string
#                 beqz %char return    # while char ≠ 0
#                 bne %a %char else    # if char == a
#                     sb %b (%str)     # *string = b
#                     addi %out %str 1 # out = str + 1
#                     j return
#                 else:
#                 inc %str             # string++
#                 j while
#             error:
#                 li %out -1           # out = -1
#             return:
#         .end_macro
#         push_registers_silently  $a0 $s0
#         replace1st.macro $v0 $a0 $a1 $a2 $s0
#         pop_registers_silently   $s0 $a0
#         jr $ra
#
#     ▶  verifyIPv4Checksum $a0 ~ $v0 $a0 $s0 $s1 $s2 $ra
#         #Verified ✔
#         # I'm proud to say this: The older, compiled version of this function (that even called other functions) executed in 760 instructions among all four test cases (including printing and loading test cases etc).
#         # The hand-optimized version runs in 622, among all four tests. The average difference is 34.5 out of 190 steps: an insignificant difference!
#         # In other words, my compiler seems to be really good. (And that, mind you, was when I didn't even attempt to optimize the meta-mips code very far)
#         #int verifyIPv4Checksum(header)
#         .macro verifyIPv4Checksum.macro %v0 %header %i %temp %temp2
#             lz %v0 #Set sum to 0
#             # temp = header + header length in bytes
#                 lw %temp (%header)
#                 crop_word_to_register_riir %temp 4 24 %temp
#                 sll %temp %temp 2
#                 add %temp %temp %header
#             # for(i = header ; i < temp ; i += 2)
#                 move %i %header
#                 bge %i %temp for.end
#                 for:
#                     lhu %temp2 (%i)
#                     pe %v0 %temp2 # v0 += temp2
#                     pei %i 2
#                 blt %i %temp for
#                 for.end:
#             #Now to do the carrying stuff for the sum as seen on Wikipedia...
#             li %temp 0x00010000 # temp = 65536 ∉ immediate
#             # while(v0 ≥ 2¹⁶)
#                 blt %v0 %temp while.end
#                 while:# v0 = (v0 + (v0 & 0xFFFF0000) >> 16) & 0x0000FFFF
#                     andi %temp2 %v0 0xFFFF0000
#                     andi %v0 %v0 0x0000FFFF
#                     srl %temp2 %temp2 8
#                     srl %temp2 %temp2 8
#                     pe %v0 %temp2
#                 bge %v0 %temp while
#                 while.end:
#             #Flip the bits of the sum then return only the second half-word of the result
#             xori %v0 %v0 0xFFFFFFFF #Flip all bits
#             andi %v0 %v0 0x0000FFFF #Mask first half
#         .end_macro
#         push_registers $s0 $s1 $s2
#         verifyIPv4Checksum.macro $v0 $a0 $s0 $s1 $s2
#         pop_registers  $s2 $s1 $s0
#         jr $ra
#
#     ▶ print_packet_array_test £address
#         # This is just a test to see if I understand how the packet arrays work in this homework. It just takes a packet array, such as pktArray_ex3 from hw2_examples.asm, and prints the string contents of the whole thing.
#         ∘ £total_length_in_bytes = get_total_length £address
#         ∘ £header_length_in_words = get_header_length £address
#         pl pstr [add ◊ £address [muli ◊ £header_length_in_words 4]]
#         pl phex [lw ◊ (£address)]
#         add £next_packet_address £address £total_length_in_bytes
#         ∘ ƒ £next_packet_address
#
#     ▶ processDatagram £msg £M £sarray
#         #Returns 1 value (sarray.ℓ for success and -1 for failure)
#         #Started writing this method at 9:01pm, Oct8
#         #Finished writing (about to test) writing this method at 9:26pm, Oct8
#         #M≣Desired ↈbytes in string
#
#         #Step 0: Assert M>0
#         ⓘ blez £M
#             ⮐ [li ◊ -1]
#             ⮐
#         ⓧ
#
#         #Step 1: Set msg[M] = '\\0'
#         sb [li ◊ '\\0'] ([add ◊ £msg £M])
#
#         #Step 2: Replace all '\\n' characters in string to '\\0', and add each index to £sarray
#         # move £i £msg # Used as a char pointer
#         # add £end £msg £M
#
#         ∘ write_word_array £sarray [li ◊ 0] £msg
#         l1 £j
#
#
#         ⓕ l1 £i ; blt £i £M ; inc £i
#             lb £char ([add ◊ £msg £i])
#             ⓘ beq £char '\\n'
#                 ∘ write_word_array £sarray £j [addi ◊ [add ◊ £msg £i] 1]
#                 sb [li ◊ 0] ([add ◊ £msg £i])
#                 inc £j
#             ⓧ
#         ⓧ
#         ⮐ £j
#
#     ▶ printDatagram £parray £n £msg £sarray
#         # Started writing at 9:30pm Oct 8, finished 9:56
#         #Returns 1 value (0 for success and -1 for failure)
#
#         # Step 1: Call extractData, and return -1 if its first output < 0
#         # Also, set £M to extractData's second output for later use
#         ⓘ bltz [∘ ◊ £M = extractData £parray £n £msg]
#             ⮐ [li ◊ -1]
#             ⮐
#         ⓧ
#
#         # Step 2: Call processDatagram, and return -1 if its first output < 0
#         ∘ £sarray_length = processDatagram £sarray £M £msg
#         pstrl "sarray_length ="¶ pl pint £sarray_length
#         ⓘ bltz £sarray_length
#             ⮐ [li ◊ -1]
#             ⮐
#         ⓧ
#
#         # Step 3: Call print, and return -1 if its first output < 0
#         ⓘ bltz [∘ ◊ = printStringArray £sarray [lz ◊] [addi ◊ £sarray_length -1] £sarray_length]
#             ⮐ [li ◊ -1]
#             ⮐
#         ⓧ
#
#         ⮐ [lz ◊]
#
#
#     ▶ extractData £parray £n £msg
#         move £header_address £parray
#         ⓕ lz £k ; blt £k £n ; inc £k
#             ⓘ bnez [∘ ◊ = verifyIPv4Checksum £header_address]
#                 ⮐ [li ◊ -1] £k
#                 ⮐
#             ⓧ
#             pei £header_address 60
#             pl pstrl "ASSERT IS 60"
#             pl pint [crop_word_to_register_riir [lw ◊ (£header_address)] 4 24 ◊]
#         ⓧ
#         move £header_address £parray
#         lz £M
#         ⓕ lz £k ; blt £k £n ; inc £k ¶ pei £header_address 60
#             addi £payload_length [∘ ◊ = get_total_length £header_address] -20
#             addi £payload_address £header_address 20
#             pe £M £payload_length
#             ⓕ lz £j ; blt £j £payload_length ; inc £j ¶ inc £payload_address ¶ inc £msg
#                 sb [lb ◊ (£payload_address)] (£msg)
#             ⓧ
#         ⓧ
#         ⮐ [lz ◊] £M
#
#     ▶ printStringArray £sarray £startIndex £endIndex £length
#         #region Input Assertions:
#             blt £length 1 ƒ.error
#             bltz £startIndex ƒ.error
#             bltz £endIndex ƒ.error
#             bge £startIndex £length ƒ.error
#             bge £endIndex £length ƒ.error
#             blt £endIndex £startIndex ƒ.error
#         #endregion
#         lz £out
#         ⓕ move £i £startIndex ; ble £i £endIndex ; inc £i ¶ inc £out
#             ∘ £string = read_word_array £sarray £i
#             pl pstr £string
#             pl
#         ⓧ
#         dec £out
#         ⮐ £out
#         ⮐
#         ƒ.error:
#         li £negativeOne -1
#         ⮐ £negativeOne
#         ⮐
#
#     ⮤ # ▶ replace1st £string £toReplace £replaceWith
#     ⮤ #     #region Input Assertions:
#     ⮤ #         blt £toReplace 0x00 ƒ.error
#     ⮤ #         blt £replaceWith 0x00 ƒ.error
#     ⮤ #         bgt £toReplace 0x7F ƒ.error
#     ⮤ #         bgt £replaceWith 0x7F ƒ.error
#     ⮤ #     #endregion
#     ⮤ #     ∘ £length = string_length £string
#     ⮤ #     ⓕ lz £i ; blt £i £length ; inc £i
#     ⮤ #         ∘ £char = read_byte_array £string £i
#     ⮤ #         ⓘ beq £char £toReplace
#     ⮤ #             ∘ write_byte_array £string £i £replaceWith
#     ⮤ #             add £out £i £string
#     ⮤ #             ⮐ £out
#     ⮤ #             ⮐
#     ⮤ #         ⓧ
#     ⮤ #     ⓧ
#     ⮤ #     ⮐ [lz 0]
#     ⮤ #     ⮐
#     ⮤ #     ƒ.error:
#     ⮤ #     ⮐ [li ◊ -1]
#
# ⮤ #ARRAY FUNCTIONS:
#
#     ⮤ word2half = lambda x:[x,x.replace('4','2').replace('word','half').replace('lw','lhu')]
#     ⮤ byte2wordhalf = lambda x:[x,x.replace('byte','half'),x.replace('byte','word')]
#
#     ▶ force_print £string £length
#         #Will print all characters, not stopping at '\\0' characters. It will print 'length' number of bytes.
#         li $v0 11
#         ⓕ lz £i ; blt £i £length ; inc £i
#             $v0 § ∘ $a0 = read_byte_array £string £i
#             syscall
#         ⓧ
#
#     ▶ reverse_string £address ~ £address
#         ∘ £length = string_length £address
#         ∘ reverse_byte_array £address £length
#
#     ▶ print_word_array £array £length £spacer_string
#         # Prints the words like "5, 7, 3, 7, 8," where spacer_string is ', '
#         ⓕ lz £i ; blt £i £length ; nop
#             ∘ £t = read_word_array £array £i
#             pint £t
#             inc £i
#             ⓘ blt £i £length
#                 pstr £spacer_string
#             ⓧ
#         ⓧ
#
#     ▶ simple_print_word_array £array £length
#         Δ ƒ.spacer_string: .asciiz ", "
#         ∘ print_word_array £array £length [la ◊ ƒ.spacer_string]
#
#     ▶ string_length £address ~ $ra
#         lb £char (£address)
#         ⓕ lz £length ; bnez £char ; inc £length ¶ inc £address
#             lb £char (£address)
#         ⓧ
#         ⮐ £length
#
#     ▶ read_byte_array £address £index ~ £address £index $ra
#         ⮐ [lb ◊ ([add ◊ £address £index])]
#
#     ▶ read_word_array £address £index ~ £address £index $ra ⮤ word2half #read_half_array
#         ⮐ [lw ◊ ([add ◊ £address [muli ◊ £index 4]])]
#
#     ▶ write_byte_array £address £index £value ~ £address £index £value $ra
#         sb £value ([add ◊ £address £index])
#
#     ▶ write_word_array £address £index £value ~ £address £value £index $ra ⮤ word2half
#         sw £value ([add ◊ £address [muli ◊ £index 4]])
#
#     ▶ little_to_big_endian_address £x ~ $ra £x
#         #x ≣ big_endian_address
#         #This function exists to save my sanity by converting a little-endian address into a big-endian one.
#         #https://www.desmos.com/calculator/ydexwmp6wf
#         # y﹦x﹢3﹣2·(x % 4)
#         ⮐ [sub ◊ [addi ◊ £x 3] [sll ◊ [div £x [li ◊ 4] ¶ mfhi ◊] 1]]
#
#     ▶ big_to_little_endian_address £x ~ £x
#         #This is the inverse function of little_to_big_endian_address
#         #https://www.desmos.com/calculator/7quxauw0ac
#         # f⁻¹(x)﹦f(x﹢1)﹢1
#         ⮐ [addi ◊ [∘ ◊ = little_to_big_endian_address [addi ◊ £x 1]] 1]
#
#     ▶ word_from_four_bytes £AB £CD £EF £GH ~ $ra £AB £CD £EF £GH
#         #Outputs word 0xABCDEFGH
#         lz $v0
#         pe $v0 £AB ¶ sll $v0 $v0 8
#         pe $v0 £CD ¶ sll $v0 $v0 8
#         pe $v0 £EF ¶ sll $v0 $v0 8
#         pe $v0 £GH
#         ⮐ $v0
#
#     ▶ swap_byte_array £address £indexA £indexB ~ £address £indexA £indexB ⮤ byte2wordhalf
#         ∘ £valueA = read_byte_array £address £indexA
#         ∘ £valueB = read_byte_array £address £indexB
#         ∘ write_byte_array £address £indexA £valueB
#         ∘ write_byte_array £address £indexB £valueA
#
#     ▶ reverse_byte_array £address £length ~ £address £length ⮤ byte2wordhalf
#         li £left 0
#         addi £right £length -1
#         ⓦ blt £left £right
#             ∘ swap_byte_array £address £left £right
#             dec £right
#             inc £left
#         ⓧ
#
#     ▶ bubble_sort_byte_array £address £length ~ £address £length ⮤ byte2wordhalf
#         ⓕ lz £iteration ; blt £iteration £length ; inc £iteration
#             ⓕ lz £index ; blt £index £length ; inc £index
#                 addi £jindex £index 1
#                 ∘ £left = read_byte_array £address £index
#                 ∘ £right = read_byte_array £address £jindex
#                 ⓘ bgt £left £right
#                     ∘ swap_byte_array £address £index £jindex
#                 ⓧ
#             ⓧ
#         ⓧ
#
# ⮤ #MATH FUNCTIONS:
#
#     ▶ ternary £bool £if_true £if_false
#         ⓘ bnez £bool
#             ⮐ £if_true
#         ⓔ
#             ⮐ £if_false
#         ⓧ
#
#     ▶ min £a £b ⮤ lambda x:[x,x.replace('ble','bge').replace('min','max')]
#         ⓘ ble £a £b
#             ⮐ £a
#         ⓔ
#             ⮐ £b
#         ⓧ
#
#     ▶ pow £base £exponent
#         # Tested :) ✔
#         # Only works for integer base and positive integer exponent
#         li $v0 1
#         ⓕ lz £i ; blt £i £exponent ; inc £i
#             te $v0 £base
#         ⓧ
#         ⮐ $v0
#
#     ▶ mod £a £b ~ $ra £a £b ⮤ lambda x:[x,x.replace('hi','lo').replace('mod','quotient')]
#         div £a £b
#         ⮐ [mfhi ◊]
#
#     ▶ is_prime £n ~ £n
#         ⓕ l2 £i ; blt £i £n ; inc £i
#             ∘ £remainder = mod £n £i
#             ⓘ beqz £remainder
#                 lz $v0
#                 ⮐ $v0
#                 ⮐
#             ⓧ
#         ⓧ
#         l1 $v0
#         ⮐ $v0
#
#     ▶ fibonacci_recursive £i
#         # ƒ(0)=1, ƒ(1)=1, ƒ(2)=2 … etc
#         ⓘ ble £i 1
#             ⮐ [li ◊ 1]
#             ⮐
#         ⓧ
#         ⮐ [add ◊ [∘ ◊ = ƒ [addi ◊ £i -1]] [∘ ◊ = ƒ [addi ◊ £i -2]]]
#
#     ▶ factorial_recursive £i
#         ⓘ blez £i
#             ⮐ [li ◊ 1]
#         ⓔ
#             ⮐ [mul ◊ £i [∘ ◊ = ƒ [addi ◊ £i -1]]]
#         ⓧ
#
#
#
#     ▶ bit_flip £i ~ £i $ra
#         ⮐ [xori ◊ £i 0xFFFFFFFF]
#
# ⮤ #TEST METHODS:
#
#     ▶ test_verifyIPv4Checksum
#         pstrl "Checksum valid_header_ex1:"
#         pl pint [∘ ◊  = verifyIPv4Checksum [la ◊ valid_header_ex1]]
#         pstrl "Checksum valid_header_ex2:"
#         pl pint [∘ ◊  = verifyIPv4Checksum [la ◊ valid_header_ex2]]
#         pstrl "Checksum invalid_header_ex1:"
#         pl pint [∘ ◊  = verifyIPv4Checksum [la ◊ invalid_header_ex1]]
#         pstrl "Checksum invalid_header_ex2:"
#         pl pint [∘ ◊  = verifyIPv4Checksum [la ◊ invalid_header_ex2]]
#         pl pinti 888
#         pl pint $ra
#         pl pint $sp
#
#     ▶ test_get_header_and_total_length
#         pstrl "get_total_length(pktArray_ex1) = "
#         pl pint [∘ ◊ = get_total_length [la ◊ pktArray_ex1]]
#         pstrl "get_total_length(pktArray_ex2) = "
#         pl pint [∘ ◊ = get_total_length [la ◊ pktArray_ex2]]
#         pstrl "get_total_length(pktArray_ex3) = "
#         pl pint [∘ ◊ = get_total_length [la ◊ pktArray_ex3]]
#         pstrl "get_total_length(pktArray_ex4) = "
#         pl pint [∘ ◊ = get_total_length [la ◊ pktArray_ex4]]
#         pstrl "get_header_length(pktArray_ex1) = "
#         pl pint [∘ ◊ = get_header_length [la ◊ pktArray_ex1]]
#         pstrl "get_header_length(pktArray_ex2) = "
#         pl pint [∘ ◊ = get_header_length [la ◊ pktArray_ex2]]
#         pstrl "get_header_length(pktArray_ex3) = "
#         pl pint [∘ ◊ = get_header_length [la ◊ pktArray_ex3]]
#         pstrl "get_header_length(pktArray_ex4) = "
#         pl pint [∘ ◊ = get_header_length [la ◊ pktArray_ex4]]
#
#     ▶ test_replace1st
#         .macro test_replace1st_macro %string_literal %char_literal_old %char_literal_new
#             .data
#                 .asciiz
#                     string:
#                         %string_literal
#             .text
#             la £string string
#             pl pstr £string
#             li £toReplace  %char_literal_old
#             li £replaceWith %char_literal_new
#             ∘ £result = replace1st £string £toReplace £replaceWith
#             pl pstr £string
#             pl phex £result
#             pl
#         .end_macro
#         test_replace1st_macro "Hello" 'l' 'p'
#         test_replace1st_macro "Lalish" 'l' 'p'
#
#     ▶ test_printStringArray
#         #region Creation of the string array
#             .data
#                 sarray0: .asciiz "Stony Brook"
#                 sarray1: .asciiz "Computer Science"
#                 sarray2: .asciiz "MIPS is amazing!!"
#                 sarray3: .asciiz "I\\nlove\\nprogramming"
#                 sarray4: .asciiz "FarBeyond"
#                 sarray: .word sarray0 sarray1 sarray2 sarray3 sarray4
#             .text
#         #endregion
#
#         .macro test_printStringArray_macro %arr_ay %start %end %length
#             pl pstrl "TEST CASE:"
#                 la £sarray %arr_ay
#                 li £startIndex %start
#                 li £endIndex %end
#                 li £length %length
#                 ∘ £result = printStringArray £sarray £startIndex £endIndex £length
#                 pstrl "RESULT: "
#                 pl pint £result
#         .end_macro
#
#         test_printStringArray_macro sarray 0 2 4
#         test_printStringArray_macro sarray 3 4 5
#         test_printStringArray_macro sarray 1 1 5
#         #test_printStringArray_macro sarray 0 4 -2
#         #test_printStringArray_macro sarray -1 2 5
#         test_printStringArray_macro sarray 0 5 5
#         test_printStringArray_macro sarray 3 2 5
#
# ⮤ #MAIN METHOD:
#
#
#
#
#     ▶ zmain
#         ∘ test_replace1st
#         ⓕ li £i 1 ; ble £i 10 ; inc £i
#             pstrl "fibbonacci("
#             pint £i
#             pstrl ") = "
#             pl pint [∘ ◊ = fibonacci_recursive £i]
#         ⓧ
#
#
#         pl pinti 77
#         ∘ test_verifyIPv4Checksum
#         pl pinti 77
#         # ⮐
#
#
#         #
#         # # ∘ test_get_header_and_total_length
#         # # ∘ test_verifyIPv4Checksum
#         # # ∘ test_replace1st
#         # # ∘ test_printStringArray
#         #
#         # # ∘ force_print [addi ◊ [la ◊ msg_buffer] 2] [li ◊ 200]
#         #
#         # # ∘ £outA £outB = extractData [la ◊ pktArray_ex3] [l4 ◊] [la ◊ msg_buffer]
#         # # pstrl "OutA = "
#         # # pint £outA
#         # # pstrl "; OutB = "
#         # # pl pint £outB
#         # # pstr [la ◊ msg_buffer]
#
#         # ∘ £m = processDatagram [la ◊ msg] [li ◊ 26] [la ◊ abcArray]
#         # pl pint £m
#         # ∘ simple_print_word_array  [la ◊ abcArray] £m
#         # pl
#         # ∘ printStringArray [la ◊ abcArray] [li ◊ 0] [addi ◊ £m -1] £m
#
#
#         # ∘ printDatagram [la ◊ pktArray_ex3] [l4 ◊] [la ◊ msg_buffer] [la ◊ abcArray]
#
#     ▶ factorial £n ~ £n $t0 $ra
#         #Possibly the most efficient possible implementation of factorial as a function...note how it doesn't save $t0...but why not just use a macro anyway? That would be even more efficient!
#         li $v0 1
#         ⓕ li $t0 2 ; ble $t0 £n ; inc $t0
#             te $v0 $t0
#         ⓧ
#         ⮐ $v0
#
#     ▶ replaceFirst £string £a £b ~ £a £b $ra
#         #Local variables:
#         .eqv ƒ.string £string
#         .eqv ƒ.a £a
#         .eqv ƒ.b £b
#         #Local variables:
#         .eqv ƒ.char £char
#
#         # while *string != 0
#         ⓦ bnez [lb ◊ (ƒ.string)]
#             # if *string == a
#             ⓘ beq ƒ.a [#◊]
#                 sb ƒ.b (ƒ.string) # *string = b
#                 ⮐
#             ⓧ
#             inc ƒ.string # string++
#         ⓧ
#
#
#
#
#
# """
# code="""
# ▶ f £x
#     ⓘ beqz £x
#         li $v0 0
#         ⮐
#     ⓧ
#     ⮐ [add ◊ £x [∘ ◊ = f [addi ◊ £x -1]]]
#
# """
# -――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
# -――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
# -――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
    # not_the_code='''
    # ▶ replace1st £a £b £c
    #
    # ▶ pd £s £l £a
    #     ⓘ blez £l
    #         ⮐ [li ◊ -1]
    #         ⮐
    #     ⓧ
    #
    #     add £end £l £s
    #     move £arr £a
    #     move £arr0 £a# Won't be used till later
    #
    #     li £l '\\n'# l = a1
    #     li £a '\\0'# a = a2
    #     #INSERTION START
    #
    #     sw £s (£arr)
    #     addi £arr £arr 4
    #
    #     #INSERTION END
    #
    #     ⓦ blt £s £end
    #         sw £s (£arr)
    #         lb £char (£s)#lb char s
    #         ⓘ beq £char £l
    #             jal replace1st
    #             j blah
    #         ⓧ
    #         ⓘ beqz £char
    #             blah:
    #             sw [addi ◊ £s 1] (£arr)
    #             addi £arr £arr 4#arr+=4
    #         ⓧ
    #         addi £s £s 1#s++
    #     ⓧ
    #     ⮐ [sra ◊ [sub ◊ £arr £arr0] 2]
    #
    #
    #
    #
    #
    # '''
    #
    #
    # extras='''
    #     ⮤ #▶ processDatagram £msg £M £sarray
    #     ⮤ #    #Returns 1 value (sarray.ℓ for success and -1 for failure)
    #     ⮤ #    #Started writing this method at 9:01pm, Oct8
    #     ⮤ #    #Finished writing (about to test) writing this method at 9:26pm, Oct8
    #     ⮤ #    #M≣Desired ↈbytes in string
    # ⮤ #
    #     ⮤ #    #Step 0: Assert M>0
    #     ⮤ #    ⓘ blez £M
    #     ⮤ #        ⮐ [li ◊ -1]
    #     ⮤ #        ⮐
    #     ⮤ #    ⓧ
    # ⮤ #
    #     ⮤ #    #Step 1: Set msg[M] = '\\0'
    #     ⮤ #    sb [li ◊ '\\0'] ([add ◊ £msg £M])
    # ⮤ #
    #     ⮤ #    #Step 2: Replace all '\\n' characters in string to '\\0', and add each index to £sarray
    #     ⮤ #    # move £i £msg # Used as a char pointer
    #     ⮤ #    # add £end £msg £M
    # ⮤ #
    #     ⮤ #    ⮤ # ∘ write_word_array £sarray [li ◊ 0] £msg   # address index value
    #     ⮤ #    sw £msg (£sarray)
    #     ⮤ #    l1 £j
    # ⮤ #
    # ⮤ #
    #     ⮤ #    ⓕ l1 £i ; blt £i £M ; inc £i
    #     ⮤ #        lb £char ([add ◊ £msg £i])
    #     ⮤ #        ⓘ beq £char '\\n'
    #     ⮤ #            ⮤ # ∘ write_word_array £sarray £j [addi ◊ [add ◊ £msg £i] 1]
    #     ⮤ #            sb [li ◊ 0] ([add ◊ £msg £i])
    #     ⮤ #            inc £j
    #     ⮤ #        ⓧ
    #     ⮤ #    ⓧ
    #     ⮤ #    ⮐ £j
    #     ▶ verifyIPv4Chdecksum £header ~ £header
    #         #Tested :) ✔ (after refactoring)
    #         #Optimized :)
    #         #Returns 1 value
    #
    #         #Get the sum of all half-words in the header
    #         lz £sum
    #         ∘ £header_length_in_words = get_header_length £header
    #         add £header_length_in_halves £header_length_in_words £header_length_in_words
    #         add £header_length_in_bytes £header_length_in_halves £header_length_in_halves
    #         add £end £header_length_in_bytes £header # ⟵ For optimization
    #         ⓕ move £i £header ; blt £i £end ; pei £i 2
    #             # pe £sum [∘ ◊ = read_half_array £header £i] ⟵ Was since optimized because this was a bottleneck
    #             pe £sum [lhu ◊ (£i)]
    #         ⓧ
    #
    #         #Now to do the carrying stuff for the sum as seen on Wikipedia...
    #         #2¹⁶ = 65536 (I'm not sure why bge didn't work when I used an int literal; but this seems to work too)
    #         ⓦ bge £sum [li ◊ 65536]
    #             andi £overflow £sum 0xFFFF0000
    #             rbei £overflow 8
    #             rbei £overflow 8
    #             andi £sum £sum 0x0000FFFF
    #             pe £sum £overflow
    #         ⓧ
    #
    #         #Flip the bits of the sum then return only the second half-word of the result
    #         ⮐ [andi ◊ [∘ ◊ = bit_flip £sum] 0x0000FFFF]
    #
    #     ▶ replace1st £string £toReplace £replaceWith
    #         #region Input Assertions:
    #             blt £toReplace 0x00 ƒ.error
    #             blt £replaceWith 0x00 ƒ.error
    #             bgt £toReplace 0x7F ƒ.error
    #             bgt £replaceWith 0x7F ƒ.error
    #         #endregion
    #         ∘ £length = string_length £string
    #         ⓕ lz £i ; blt £i £length ; inc £i
    #             rba £char £string £i
    #             ⓘ beq £char £toReplace
    #                 ∘ write_byte_array £string £i £replaceWith
    #                 add £out £i £string
    #                 inc £out #―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
    #                 ⮐ £out
    #                 ⮐
    #             ⓧ
    #         ⓧ
    #         lz $0
    #         ⮐ $0
    #         ⮐
    #         ƒ.error:
    #         li £negativeOne -1
    #         ⮐ £negativeOne
    #
    #     ▶ reverse_string £address ~ £address
    #         ∘ £length = string_length £address
    #         ∘ reverse_byte_array £address £length
    #
    #     ▶ print_word_array £array £length £spacer_string
    #         # Prints the words like "5, 7, 3, 7, 8," where spacer_string is ', '
    #         ⓕ lz £i ; blt £i £length ; nop
    #             ∘ £t = read_word_array £array £i
    #             pint £t
    #             inc £i
    #             ⓘ blt £i £length
    #                 pstr £spacer_string
    #             ⓧ
    #         ⓧ
    #
    #     ▶ simple_print_word_array £array £length
    #         .data
    #             ƒ.spacer_string: .asciiz ", "
    #         .text
    #         ∘ print_word_array £array £length [la ◊ ƒ.spacer_string]
    #
    #     ▶ print_packet_array_test £address
    #         # This is just a test to see if I understand how the packet arrays work in this homework. It just takes a packet array, such as pktArray_ex3 from hw2_examples.asm, and prints the string contents of the whole thing.
    #         ∘ £total_length_in_bytes = get_total_length £address
    #         ∘ £header_length_in_words = get_header_length £address
    #         pl pstr [add ◊ £address [muli ◊ £header_length_in_words 4]]
    #         pl phex [lw ◊ (£address)]
    #         add £next_packet_address £address £total_length_in_bytes
    #         ∘ ƒ £next_packet_address
    #
    #     ▶ read_byte_array £address £index ~ £address £index $ra
    #         ⮐ [lb ◊ ([add ◊ £address £index])]
    #
    #     ▶ read_word_array £address £index ~ £address £index $ra ⮤ word2half #read_half_array
    #         ⮐ [lw ◊ ([add ◊ £address [muli ◊ £index 4]])]
    #
    #     ▶ write_byte_array £address £index £value ~ £address £index £value $ra
    #         sb £value ([add ◊ £address £index])
    #
    #     ▶ write_word_array £address £index £value ~ £address £value £index $ra ⮤ word2half
    #         sw £value ([add ◊ £address [muli ◊ £index 4]])
    #
    #     ▶ little_to_big_endian_address £x ~ $ra £x
    #         #x ≣ big_endian_address
    #         #This function exists to save my sanity by converting a little-endian address into a big-endian one.
    #         #https://www.desmos.com/calculator/ydexwmp6wf
    #         # y﹦x﹢3﹣2·(x % 4)
    #         ⮐ [sub ◊ [addi ◊ £x 3] [sll ◊ [div £x [li ◊ 4] ¶ mfhi ◊] 1]]
    #
    #     ▶ big_to_little_endian_address £x ~ £x
    #         #This is the inverse function of little_to_big_endian_address
    #         #https://www.desmos.com/calculator/7quxauw0ac
    #         # f⁻¹(x)﹦f(x﹢1)﹢1
    #         ⮐ [addi ◊ [∘ ◊ = little_to_big_endian_address [addi ◊ £x 1]] 1]
    #
    #     ▶ word_from_four_bytes £AB £CD £EF £GH ~ $ra £AB £CD £EF £GH
    #         #Outputs word 0xABCDEFGH
    #         lz $v0
    #         pe $v0 £AB ¶ sll $v0 $v0 8
    #         pe $v0 £CD ¶ sll $v0 $v0 8
    #         pe $v0 £EF ¶ sll $v0 $v0 8
    #         pe $v0 £GH
    #         ⮐ $v0
    #
    #     ▶ swap_byte_array £address £indexA £indexB ~ £address £indexA £indexB ⮤ byte2wordhalf
    #         ∘ £valueA = read_byte_array £address £indexA
    #         ∘ £valueB = read_byte_array £address £indexB
    #         ∘ write_byte_array £address £indexA £valueB
    #         ∘ write_byte_array £address £indexB £valueA
    #
    #     ▶ reverse_byte_array £address £length ~ £address £length ⮤ byte2wordhalf
    #         li £left 0
    #         addi £right £length -1
    #         ⓦ blt £left £right
    #             ∘ swap_byte_array £address £left £right
    #             dec £right
    #             inc £left
    #         ⓧ
    #
    #     ▶ bubble_sort_byte_array £address £length ~ £address £length ⮤ byte2wordhalf
    #         ⓕ lz £iteration ; blt £iteration £length ; inc £iteration
    #             ⓕ lz £index ; blt £index £length ; inc £index
    #                 addi £jindex £index 1
    #                 ∘ £left = read_byte_array £address £index
    #                 ∘ £right = read_byte_array £address £jindex
    #                 ⓘ bgt £left £right
    #                     ∘ swap_byte_array £address £index £jindex
    #                 ⓧ
    #             ⓧ
    #         ⓧ
    #
    # ⮤ #MATH FUNCTIONS:
    #
    #     ▶ ternary £bool £if_true £if_false
    #         ⓘ bnez £bool
    #             ⮐ £if_true
    #         ⓔ
    #             ⮐ £if_false
    #         ⓧ
    #
    #     ▶ min £a £b ⮤ lambda x:[x,x.replace('ble','bge').replace('min','max')]
    #         ⓘ ble £a £b
    #             ⮐ £a
    #         ⓔ
    #             ⮐ £b
    #         ⓧ
    #
    #     ▶ pow £base £exponent
    #         # Tested :) ✔
    #         # Only works for integer base and positive integer exponent
    #         li $v0 1
    #         ⓕ lz £i ; blt £i £exponent ; inc £i
    #             te $v0 £base
    #         ⓧ
    #         ⮐ $v0
    #
    #     ▶ mod £a £b ~ $ra £a £b ⮤ lambda x:[x,x.replace('hi','lo').replace('mod','quotient')]
    #         div £a £b
    #         ⮐ [mfhi ◊]
    #
    #     ▶ is_prime £n ~ £n
    #         ⓕ l2 £i ; blt £i £n ; inc £i
    #             ∘ £remainder = mod £n £i
    #             ⓘ beqz £remainder
    #                 lz $v0
    #                 ⮐ $v0
    #                 ⮐
    #             ⓧ
    #         ⓧ
    #         l1 $v0
    #         ⮐ $v0
    #
    #     ▶ fibonacci_recursive £i
    #         # ƒ(0)=1, ƒ(1)=1, ƒ(2)=2 … etc
    #         ⓘ ble £i 1
    #             ⮐ [li ◊ 1]
    #         ⓔ
    #             ⮐ [add ◊ [∘ ◊ = ƒ [addi ◊ £i -1]] [∘ ◊ = ƒ [addi ◊ £i -2]]]
    #         ⓧ
    #
    #     ▶ factorial_recursive £i
    #         ⓘ blez £i
    #             ⮐ [li ◊ 1]
    #         ⓔ
    #             ⮐ [mul ◊ £i [∘ ◊ = ƒ [addi ◊ £i -1]]]
    #         ⓧ
    #
    #
    # '''

    #endregion
    '''    ⮤ #▶ printStringArray £sarray £startIndex £endIndex £length
    ⮤ #    #region Input Assertions:
    ⮤ #        blt £length 1 ƒ.error
    ⮤ #        bltz £startIndex ƒ.error
    ⮤ #        bltz £endIndex ƒ.error
    ⮤ #        bge £startIndex £length ƒ.error
    ⮤ #        bge £endIndex £length ƒ.error
    ⮤ #        blt £endIndex £startIndex ƒ.error
    ⮤ #    #endregion
    ⮤ #    lz £out
    ⮤ #    ⓕ move £i £startIndex ; ble £i £endIndex ; inc £i ¶ inc £out
    ⮤ #        rwa £string £sarray £i
    ⮤ #        pl pstr £string
    ⮤ #        pl
    ⮤ #    ⓧ
    ⮤ #    # dec £out ⟵ I believe this line caused the errors in the test cases!
    ⮤ #    ⮐ £out
    ⮤ #    ⮐
    ⮤ #    ƒ.error:
    ⮤ #    li £negativeOne -1
    ⮤ #    ⮐ £negativeOne
    ⮤ #    ⮐
'''