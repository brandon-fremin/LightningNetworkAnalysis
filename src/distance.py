def cost_d(channel, amount):
    return channel["outpol"]["base"] * 1000 + amount * channel["outpol"]["rate"]


def dist_d(channel, amount):
    return 1
