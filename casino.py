import random
def bet(bet):
    a = ['🎰', '💣', '🍒',]
    sum = 0
    c = random.choice(a) + random.choice(a) + random.choice(a)
    if c[0] == c[1] == c[2]:
        sum = bet*10
    else:
        sum -= bet
    a = [sum,c]
    return a
