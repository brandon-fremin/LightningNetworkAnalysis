def insider_verify(node, channel, channel_balances, amount):
    # Make sure channel can actually supply the amount required
    if channel_balances[channel["short_channel_id"]][node["id"]] < amount:
        return False
    else:
        return True


def outsider_verify(node, channel, channel_balances, amount):
    if channel["satoshis"] < amount:
        return False
    else:
        return True

