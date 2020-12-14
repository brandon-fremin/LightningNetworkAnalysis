import random
import matplotlib.pyplot as plt
from src.helper import load


def box_plot(filename="1.pkl", fieldname="final_dist", metric_label="Path Length"):
    json_data = load(filename)
    if not json_data:
        return

    def retriever(raw_data):
        cleaned_data = []
        for d in raw_data:
            if d["final_dist"] == float("inf"):
                continue
            else:
                cleaned_data.append(d[fieldname])
        return cleaned_data

    data_1 = retriever(json_data["answers_short"])
    data_2 = retriever(json_data["answers_loop"])
    data_3 = retriever(json_data["answers_rand"])
    data = [data_1, data_2, data_3]

    x = []
    y = []
    c = []
    col = ["red", "blue", "green"]
    for i in range(len(data)):
        for j in range(len(data[i])):
            x.append(i + 1 + random.normalvariate(0, 0.05))
            y.append(data[i][j])
            c.append(col[i])

    plt.scatter(x, y, s=10, c=c)
    plt.boxplot(data)
    plt.title(f'{metric_label} for {len(data_1)} Samples of 3 Routing Algorithms [10k sat]')
    plt.xticks([1, 2, 3], ["short", "loop", "rand"])
    plt.ylabel(f"{metric_label}")
    plt.xlabel("Algorithm Type")
    plt.show()
