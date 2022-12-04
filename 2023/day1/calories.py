def read_from_file():
    totals = []
    with open("input.txt") as f:
        all_items = []
        items = []
        for line in f.readlines():
            line = line.strip()
            if line == "":
                all_items.append(items)
                items = []
            else:
                items.append(int(line))
                totals.append(sum(items))
    return all_items, totals


all_items, totals = read_from_file()
print(sum(sorted(totals, reverse=True)[:3]))
