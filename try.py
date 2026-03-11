import matplotlib.pyplot as plt #type:ignore
miny = -0.1
maxy = 1.2
altezza_clock = 2 #incrementa per diminuire l'altezza

b = input()
bits = [int(bit) for bit in b]

bit_time = 1
def clock(n):
    t = []
    y = []
    t.append(0)
    y.append(0)
    for i in range(1, n+1):
        t.append((i-1)*bit_time/2)
        y.append((i%2)/altezza_clock)
    t.append(len(bits)*bit_time)
    y.append(0)
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