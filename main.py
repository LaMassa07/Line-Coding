from PIL import Image #type: ignore
import matplotlib.pyplot as plt #type:ignore
miny = -0.1
maxy = 1.2
altezza_clock = 2 #incrementa per diminuire l'altezza
bit_time = 1
using_4b5b = False

def cls():
    print("\033c", end="")

dict4b5b = {
    '0000': '11110',
    '0001': '01001',
    '0010': '10100',
    '0011': '10101',
    '0100': '01010',
    '0101': '01011',
    '0110': '01110',
    '0111': '01111',
    '1000': '10010',
    '1001': '10011',
    '1010': '10110',
    '1011': '10111',
    '1100': '11010',
    '1101': '11011',
    '1110': '11100',
    '1111': '11101',
}

def conv_4b5b(b):    
    c = ""
    for bits in b:
        try:
            c += dict4b5b[bits]
        except:
            c += bits
    return c


def conversion():
    cls()
    print("\033[38;2;143;163;191mTYPE THE BITS: ", end="")
    b = input()
    b = [b[i:i+4] for i in range(0, len(b), 4)]

    c = conv_4b5b(b)
    print("\033[38;2;143;163;191mCONVERTED: ", end="")
    print(f"\033[38;2;191;201;217m{c}\033[0m\n\n")

    input()



def clock(n):
    t = []
    y = []
    t.append(0)
    y.append(0)
    for i in range(1, n+1):
        t.append((i-1)*bit_time/2)
        y.append((i%2)/altezza_clock)
    y.append(0)
    t.append(((i-1)*bit_time/2)+bit_time/2)
    return t, y
        
def nrz(bits):
    t = []
    y = []
    for i, b in enumerate(bits):
        t.append(i*bit_time)
        y.append(b)
    t.append(len(bits)*bit_time)
    y.append(bits[-1])

    return t, y

def nrzi(bits):
    t = []
    y = []
    v = 0
    for i, b in enumerate(bits):
        t.append(i*bit_time)
        if b == 1:
            v = v^1
        y.append(v)
    t.append(len(bits)*bit_time)
    y.append(v)

    return t, y

def rz(bits):
    t = []
    y = []
    for i, b in enumerate(bits):
        t.append(i*bit_time)
        t.append((i*bit_time)+bit_time/2)
        y.append(b)
        y.append(0)
    t.append(len(bits)*bit_time)
    y.append(0)

    return t, y

def manchester(bits):
    t = []
    y = []
    for i, b in enumerate(bits):
        t.append(i*bit_time)
        t.append((i*bit_time)+bit_time/2)
        if b == 0:
            y.append(1)
            y.append(0)
        else:
            y.append(0)
            y.append(1)
    t.append(len(bits)*bit_time)
    y.append(bits[-1])

    return t, y

def diff_base(bits):
    t = []
    y = []
    phase = True
    for i, b in enumerate(bits):
        t.append(i*bit_time)
        t.append((i*bit_time)+bit_time/2)
        if b == 1:
            phase = not phase
        if phase:
            y.append(1)
            y.append(0)
        else:
            y.append(0)
            y.append(1)
    t.append(len(bits)*bit_time)
    y.append(0 if phase else 1)

    return t, y


def ami100(bits):
    t = []
    y = []
    pos = False
    v = 0
    for i, b in enumerate(bits):
        t.append(i*bit_time)
        if b == 0:
            v = 0
        else:
            pos = not pos
            if pos:
                v = 1
            else:
                v = -1
        y.append(v)
    t.append(len(bits)*bit_time)
    y.append(v)

    return t, y

def ami50(bits):
    t = []
    y = []
    pos = False
    for i, b in enumerate(bits):
        t.append(i*bit_time)
        t.append((i*bit_time)+bit_time/2)
        if b == 0:
            y.append(0)
            y.append(0)
        else:
            pos = not pos
            if pos:
                y.append(1)
                y.append(0)
            else:
                y.append(-1)
                y.append(0)
    t.append(len(bits)*bit_time)
    y.append(0)

    return t, y


def seq(v, prev):
    if abs(v) == 1:
        return 0
    else:
        if prev == 1:
            return -1
        else:
            return 1
    
def mlt3(bits):
    t = []
    y = []
    v = 0
    prev = -1
    mem = prev
    for i, b in enumerate(bits):
        t.append(i*bit_time)
        mem = v
        if b == 1:
            v = seq(v, prev)
            prev = mem
        y.append(v)
    t.append(len(bits)*bit_time)
    y.append(v)
    
    return t, y


def hdb3(bits):
    t = []
    y = []
    rule = True
    pos = True
    v = 1
    i = 0

    while i < len(bits):
        t.append(i*bit_time)
        t.append((i*bit_time)+bit_time/2)

        if bits[i] == 0:
            next3 = bits[i+1:i+4]
            if len(next3) == 3 and all(x == 0 for x in next3):
                for k in range(3):
                    t.append((i+k+1)*bit_time)
                    t.append(((i+k+1)*bit_time)+bit_time/2)
                if rule:
                    y.append(1 if v == -1 else -1)
                    y.append(0)
                    y.append(0)
                    y.append(0)
                    y.append(0)
                    y.append(0)
                    y.append(1 if v == -1 else -1)
                    y.append(0)
                    pos = not pos
                else:
                    y.append(0)
                    y.append(0)
                    y.append(0)
                    y.append(0)
                    y.append(0)
                    y.append(0)
                    y.append(v)
                    y.append(0)
                    pos = not pos
                i += 4
                rule = True
            else:
                y.append(0)
                y.append(0)
                i += 1

        else:
            rule = not rule
            pos = not pos
            if pos:
                v = 1
            else:
                v = -1
            y.append(v)
            y.append(0)
            i += 1
    t.append(len(bits)*bit_time)
    y.append(0)
    
    return t, y




def line_coding():
    cls()
    print("\033[38;2;143;163;191mTYPE THE BITS: ", end="")
    b = input()
    input_bits_4b5b = [b[i:i+4] for i in range(0, len(b), 4)]
    input_bits = [int(bit) for bit in b]
    print("\033[38;2;143;163;191mUSING 4B-5B? Y/n: ", end="")
    a = input()
    if a.lower() == 'y' or a == '':
        using_4b5b = True
    elif a.lower() == 'n':
        using_4b5b = False
    else: 
        print("using default settings")
        using_4b5b = True

    if using_4b5b:
        bits = [int(b) for b in conv_4b5b(input_bits_4b5b)]
    else: 
        bits = [int(b) for b in input_bits]

    
    t1, y1 = clock(len(bits)*2)
    t2, y2 = nrz(bits)
    t3, y3 = nrzi(bits)
    t4, y4 = rz(bits)
    t5, y5 = manchester(bits)
    t6, y6 = diff_base(bits)
    t7, y7 = ami100(bits)
    t8, y8 = ami50(bits)
    t9, y9 = mlt3(bits)
    t10, y10 = hdb3(bits)

    #FINESTRA 1#
    fig, ax = plt.subplots(4, 1, sharex=True)
    fig.suptitle(f"Codifiche binarie (1)")
    #CLOCK#
    ax[0].step(t1, y1, where="post")
    ax[0].set_title("CLOCK")
    ax[0].set_ylim(miny,maxy)
    ax[0].grid(True)
    #NRZ#
    ax[1].step(t2, y2, where="post")
    ax[1].set_title("Segnale NRZ")
    ax[1].set_ylim(miny,maxy)
    ax[1].grid(True)
    #NRZI#
    ax[2].step(t3, y3, where="post")
    ax[2].set_title("Segnale NRZI")
    ax[2].set_ylim(miny,maxy)
    ax[2].grid(True)
    #RZ#
    ax[3].step(t4, y4, where="post")
    ax[3].set_title("Segnale RZ")
    ax[3].set_ylim(miny,maxy)
    ax[3].grid(True)
    #layout#
    plt.tight_layout()


    #FINESTRA 2#
    fig, ax = plt.subplots(3, 1, sharex=True)
    fig.suptitle(f"Codifiche binarie (2)")
    #CLOCK#
    ax[0].step(t1, y1, where="post")
    ax[0].set_title("CLOCK")
    ax[0].set_ylim(miny,maxy)
    ax[0].grid(True)
    #MANCHESTER#
    ax[1].step(t5, y5, where="post")
    ax[1].set_title("MANCHESTER")
    ax[1].set_ylim(miny,maxy)
    ax[1].grid(True)
    #BASE DIFFERENZIALE#
    ax[2].step(t6, y6, where="post")
    ax[2].set_title("DIFFERENTIAL BASE")
    ax[2].set_ylim(miny,maxy)
    ax[2].grid(True)
    #layout#
    plt.tight_layout()


    #FINESTRA 3#
    fig, ax = plt.subplots(4, 1, sharex=True)
    fig.suptitle(f"Codifiche pseudoternarie (1)")
    #CLOCK#
    ax[0].step(t1, y1, where="post")
    ax[0].set_title("CLOCK")
    ax[0].set_ylim(miny,maxy)
    ax[0].grid(True)
    #AMI 100%#
    ax[1].step(t7, y7, where="post")
    ax[1].set_title("AMI 100%")
    ax[1].set_ylim(-maxy,maxy)
    ax[1].grid(True)
    #AMI 50%#
    ax[2].step(t8, y8, where="post")
    ax[2].set_title("AMI 50%")
    ax[2].set_ylim(-maxy,maxy)
    ax[2].grid(True)
    #MLT-3#
    ax[3].step(t9, y9, where="post")
    ax[3].set_title("MLT-3")
    ax[3].set_ylim(-maxy,maxy)
    ax[3].grid(True)
    #layout#
    plt.tight_layout()



    #FINESTRA 4#
    fig, ax = plt.subplots(2, 1, sharex=True)
    fig.suptitle(f"Codifiche pseudoternarie (2)")
    #CLOCK#
    ax[0].step(t1, y1, where="post")
    ax[0].set_title("CLOCK")
    ax[0].set_ylim(miny,maxy)
    ax[0].grid(True)
    #HDB-3#
    ax[1].step(t10, y10, where="post")
    ax[1].set_title("HDB-3")
    ax[1].set_ylim(-maxy,maxy)
    ax[1].grid(True)
    #layout#
    plt.tight_layout()



    plt.show()
    return
    





title = """\033[38;2;58;95;138m
██╗     ██╗███╗   ██╗███████╗               ██████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
██║     ██║████╗  ██║██╔════╝              ██╔════╝██╔═══██╗██╔══██╗██║████╗  ██║██╔════╝ 
██║     ██║██╔██╗ ██║█████╗      █████╗    ██║     ██║   ██║██║  ██║██║██╔██╗ ██║██║  ███╗      \033[38;2;143;163;191mBY Maso\033[38;2;58;95;138m
██║     ██║██║╚██╗██║██╔══╝      ╚════╝    ██║     ██║   ██║██║  ██║██║██║╚██╗██║██║   ██║      \033[38;2;191;201;217mV 1.0\033[38;2;58;95;138m
███████╗██║██║ ╚████║███████╗              ╚██████╗╚██████╔╝██████╔╝██║██║ ╚████║╚██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝               ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
\033[38;2;143;163;191mOPTIONS:
    \033[38;2;191;201;217m1. line coding
    \033[38;2;191;201;217m2. 4b-5b conversion\033[0m
"""

def main():
    while True:
        cls()
        print(title)
        n = 0
        while n not in ["1", "2"]:
            n = input()
            if n == "1":
                line_coding()
            elif n == "2":
                conversion()
            else:
                print("\033[F\033[K", end="")


main()