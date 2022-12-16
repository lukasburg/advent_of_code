import re
import networkx
import matplotlib.pyplot as plt


with open('input') as file:
    inp = file.readlines()


valve_parser = re.compile('[A-Z]{2}')
flow_rate_parser = re.compile('\d+')


class Room:
    def __init__(self, name: str, flow_rate: int):
        self.name = name
        self.flow_rate = flow_rate
        self.leads_to: set[Room] = set()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Room) and self.name == other.name

    def __str__(self):
        return f'{self.name}, flow rate {self.flow_rate}, leads to {self.leads_to}'

    def __repr__(self):
        return f'{self.name}'


def parse_valve(string):
    groups = valve_parser.findall(string)
    flow_rate = int(flow_rate_parser.search(string).group())
    valve_name = groups[0]
    dests = groups[1:]
    return valve_name, dests, flow_rate


def set_up_graph():
    rooms: dict[str, Room] = dict()
    rooms_name_dests_dict: dict[str, list[str]] = dict()
    first_room = None
    for line in inp:
        name, dest, flow = parse_valve(line)
        room = Room(name, flow)
        rooms[room.name] = room
        rooms_name_dests_dict[room.name] = dest
        if not first_room:
            first_room = room

    for room in rooms.values():
        for dest_str in rooms_name_dests_dict[room.name]:
            room.leads_to.add(rooms[dest_str])
    return rooms.values(), first_room


def main():
    graph = networkx.Graph()
    rooms, start = set_up_graph()
    for room in rooms:
        print(room)
        graph.add_node(room.name)
    for room in rooms:
        for dest in room.leads_to:
            graph.add_edge(room.name, dest.name)
    networkx.draw_kamada_kawai(graph, with_labels=True)
    plt.show()


main()
