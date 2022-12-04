class Map:
    def __init__(self, filename) -> None:
        self.reverse_index = {}
        with open(filename, "r") as f:
            for line in f.readlines():
                a, b = line.strip().split(")")
                if b in self.reverse_index:
                    raise Exception("multiple unexpected")
                self.reverse_index[b] = a

    def count_orbits(self, object_name):
        if object_name == "COM":
            return 0
        return 1 + self.count_orbits(self.reverse_index[object_name])

    def count_all_orbits(self):
        total_orbits = 0
        for k in self.reverse_index.keys():
            total_orbits += self.count_orbits(k)
        return total_orbits

    def get_transfers_from(self, object_name):
        transfers_from_object = []
        count = 1
        orbited_object = self.reverse_index[object_name]
        transfers_from_object.append((orbited_object, count))
        while orbited_object != "COM":
            orbited_object = self.reverse_index[orbited_object]
            count += 1
            transfers_from_object.append((orbited_object, count))
        return transfers_from_object

    def min_orbital_transfers(self):
        transfers_from_me = self.get_transfers_from("YOU")
        transfers_from_me_dict = dict(transfers_from_me)
        transfers_from_santa = self.get_transfers_from("SAN")
        for obj, count in transfers_from_santa:
            if obj in transfers_from_me_dict:
                transfers_to_me = transfers_from_me_dict[obj]
                return transfers_to_me + count - 2


orbit_maps = Map("input.txt")
# print(orbit_maps.count_all_orbits())
print(orbit_maps.min_orbital_transfers())
