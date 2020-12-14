import random
import matplotlib.pyplot as plt


class ChannelSplit:
    def __init__(self, num_splits):
        self.pdf_samples = [0.5]
        self.calibrate_pdf(num_splits)
        self.num_splits = num_splits

    def log_pdf(self, x):
        return 24 * x ** 2 - 13 * x + 2

    def calibrate_pdf(self, num_splits):
        pdf = [0] * num_splits
        interval_length = 0.5
        width = interval_length / num_splits
        for i in range(num_splits):
            lower_ratio = i / num_splits
            upper_ratio = (i + 1) / num_splits
            lower = lower_ratio * interval_length
            upper = upper_ratio * interval_length
            height = (10 ** self.log_pdf(lower) + 10 ** self.log_pdf(upper)) / 2
            area = height * width
            pdf[i] = area
        minn = min(pdf)
        pdf = [round(p / minn) for p in pdf]
        pdf_samples = []
        for i in range(num_splits):
            lower = i / num_splits / 2
            width = 1 / num_splits / 2
            value = lower + width / 2
            assert value <= 0.5
            for j in range(pdf[i]):
                pdf_samples.append(value)
        self.pdf_samples = pdf_samples

    def plot(self):
        x = []
        y = []
        for value in self.pdf_samples:
            counter = 0
            for s in self.pdf_samples:
                if s == value:
                    counter = counter + 1
            x.append(value)
            y.append(counter)
        plt.plot(x, y)
        plt.show()

    def sample(self):
        return random.choice(self.pdf_samples)


def define_channel_balances(all_nodes, all_channels):
    valid_active_channel_ids = frozenset(all_channels.keys())
    channel_balances = {}
    funds_distributor = ChannelSplit(100)
    for key, node in all_nodes.items():
        node["channels"] = {}
        for edge in node["edges"]:
            channel_id = edge["short_channel_id"]
            if channel_id not in valid_active_channel_ids:
                continue
            try:
                channel = channel_balances[channel_id]
                assert node["id"] in channel.keys()
                assert edge["peer_id"] in channel.keys()
            except KeyError:
                total_balance = edge["satoshis"]
                r = funds_distributor.sample()
                my_balance = int(total_balance * r)
                peer_balance = total_balance - my_balance
                channel_balances[channel_id] = {}
                channel_balances[channel_id][node["id"]] = my_balance
                channel_balances[channel_id][edge["peer_id"]] = peer_balance

            node["channels"][channel_id] = edge

    print()
    print(f"Total Nodes   : {len(all_nodes)}")
    print(f"Total Channels: {len(valid_active_channel_ids)}")
    print()

    return channel_balances
