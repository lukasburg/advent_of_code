import math
from collections import Counter
import itertools
import re
from typing import Iterable

import networkx
import matplotlib.pyplot as plt


VERBOSE = True
with open('example_input') as file:
    inp = file.readlines()


valve_parser = re.compile('[A-Z]{2}')
flow_rate_parser = re.compile('\d+')


class OutOfTimeException(Exception):
    pass


class NoMoreOptions(Exception):
    pass


class Room:
    def __init__(self, name: str, flow_rate: int):
        self.name = name
        self.flow_rate = flow_rate
        self.leads_to: set[Room] = set()
        self.distances: dict[Room, int] = dict()
        self.current_best_score_if_reached_after_time_i = [0 for i in range(30)]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Room) and self.name == other.name

    def __str__(self):
        return f'{self.name}, flow rate {self.flow_rate}, leads to {self.leads_to}'

    def __repr__(self):
        return f'{self.name}'

    def calculate_time_to_move_to_room(self, destination: 'Room', current_time: int):
        time_after_opening_valve = current_time - self.distances[destination]
        if time_after_opening_valve < 0:
            raise OutOfTimeException
        else:
            return time_after_opening_valve

    def does_update_score(self, time, score) -> bool:
        """
        Look if reaching this room at time i with the given score is the best possible score for reaching it this early.
        If yes, update this rooms score and return True
        If no, return False
        """
        if self.current_best_score_if_reached_after_time_i[time] <= score:
            for i in reversed(range(0, time)):
                if self.current_best_score_if_reached_after_time_i[i] > score:
                    break
                else:
                    self.current_best_score_if_reached_after_time_i[i] = score
            return True
        else:
            return False


class PossiblePath:
    def __init__(self, current_score: int, current_room: Room, remaining_time: int, remaining_rooms: set[Room],
                 path_to_here=None, score_added_by_current_room=0):
        if path_to_here is None:
            path_to_here = []
        self.remaining_rooms = remaining_rooms
        self.remaining_time = remaining_time
        self.current_score = current_score
        self.current_room = current_room
        self.path_to_here = path_to_here
        # helper for double path
        self.score_added_by_current_room = score_added_by_current_room

    def _calc_new_path_values(self, next_room):
        remaining_time_after_move = self.current_room.calculate_time_to_move_to_room(next_room, self.remaining_time)
        pressure_released_by_next_room = remaining_time_after_move * next_room.flow_rate
        new_score = self.current_score + pressure_released_by_next_room
        path_to_next = self.path_to_here + [self.current_room.name]
        next_remaining_rooms = self.remaining_rooms.difference({next_room})
        new_path = PossiblePath(new_score, next_room, remaining_time_after_move, next_remaining_rooms,
                                path_to_here=path_to_next, score_added_by_current_room=pressure_released_by_next_room)
        return new_path

    def _calc_new_possibles(self, verbose, do_not_optimize):
        next_possibles = []
        for next_room in self.remaining_rooms:
            try:
                new_path = self._calc_new_path_values(next_room)
                if next_room.does_update_score(new_path.remaining_time, new_path.current_score) or do_not_optimize:
                    next_possibles.append(new_path)
                elif verbose:
                    print(f'Path {new_path} was discarded, because going this way reached a score of {new_path.current_score}. '
                          f'But {next_room.name} was already reached by the time {new_path.remaining_time} with a higher possible score of'
                          f' {next_room.current_best_score_if_reached_after_time_i[new_path.remaining_time]}')
            except OutOfTimeException:
                if verbose:
                    print(f'On path {self.path_to_here} tried to move to {next_room.name} with a remaining time of {self.remaining_time}. '
                          f'But this would have taken {self.current_room.distances[next_room]} minutes, so going that way will not be considered.')
        return next_possibles

    def next_possibles(self, verbose=False, do_not_optimize=False):
        next_possibles = self._calc_new_possibles(verbose, do_not_optimize)
        if not next_possibles:
            if verbose:
                print(f"Path {self} has no more options.")
            raise NoMoreOptions
        return next_possibles

    def __str__(self):
        return f'{" -> ".join(self.path_to_here + [self.current_room.name])}: {self.current_score}'

    def __repr__(self):
        return f"{{{str(self)}}}"


class DoublePaths:
    def __init__(self, player_path: PossiblePath, elefant_path: PossiblePath):
        self.player_path = player_path
        self.elefant_path = elefant_path

    def next_possibles(self, verbose=False):
        player_next_possibles = self.player_path.next_possibles(verbose, do_not_optimize=True)
        player_next_possibles.append(self.player_path)  # player did not move is a possibility
        elefant_next_possibles = self.elefant_path.next_possibles(verbose, do_not_optimize=True)
        elefant_next_possibles.append(self.elefant_path)  # elefant did not move is a possibility
        next_possibles = []
        for player_path, elefant_path in list(itertools.product(player_next_possibles, elefant_next_possibles)):
            if player_path.current_room == elefant_path.current_room:
                # player and elefant chose the same next destination
                continue
            else:
                # remove option to move to room opened by the other protagonist
                player_path.remaining_rooms.remove(elefant_path.current_room)
                elefant_path.remaining_rooms.remove(player_path.current_room)
                player_path.current_score += elefant_path.score_added_by_current_room
                elefant_path.current_score += player_path.score_added_by_current_room
                is_player_path_better = player_path.current_room.does_update_score(player_path.remaining_time, player_path.current_score)
                is_elefant_path_better = elefant_path.current_room.does_update_score(elefant_path.remaining_time, elefant_path.current_score)
                if is_player_path_better or is_elefant_path_better:
                    next_possibles.append(DoublePaths(player_path, elefant_path))
                elif verbose:
                    print(f'Paths {self} were discarded, because going this way reached a lower score.'
                          f'{player_path.current_room.name} was already reached by the time {player_path.remaining_time} with a higher possible score '
                          f'and {elefant_path.current_room.name} was already reached by the time {elefant_path.remaining_time} with a higher possible score.')
        if not next_possibles:
            if verbose:
                print(f"Path {self} has no more options.")
            raise NoMoreOptions
        return next_possibles

    def __str__(self):
        return f'[{self.player_path}  |  {self.elefant_path}]'


def parse_valve(string):
    groups = valve_parser.findall(string)
    flow_rate = int(flow_rate_parser.search(string).group())
    valve_name = groups[0]
    dests = groups[1:]
    return valve_name, dests, flow_rate


def set_up_graph():
    rooms: dict[str, Room] = dict()
    rooms_name_dests_dict: dict[str, list[str]] = dict()
    for line in inp:
        name, dest, flow = parse_valve(line)
        room = Room(name, flow)
        rooms[room.name] = room
        rooms_name_dests_dict[room.name] = dest
        if room.name == 'AA':
            first_room = room
    for room in rooms.values():
        for dest_str in rooms_name_dests_dict[room.name]:
            room.leads_to.add(rooms[dest_str])
    return rooms, first_room


def print_stats(graph: list[Room]):
    number_of_nodes = len(graph)
    useless_valves = len(list(filter(lambda r: r.flow_rate == 0, graph)))
    max_flow_rate = sorted(graph, key=lambda r: r.flow_rate, reverse=True)[0]
    print(f'Number of nodes: {number_of_nodes}.')
    print(f'Number of nodes with flow_rate of 0: {useless_valves}')
    print(f'Node with highest flow rate: ({max_flow_rate})')


def plot_graph(graph: networkx.Graph):
    labels = {room: room.name for room in graph}
    edge_labels = {key: graph.edges[key]['weight'] for key in graph.edges()}
    positions = networkx.kamada_kawai_layout(graph)
    networkx.draw(graph, pos=positions, labels=labels)
    networkx.draw_networkx_edge_labels(graph, pos=positions, edge_labels=edge_labels)
    plt.show()


def reduce_graph(graph: networkx.Graph, start_room: Room):
    """
    Remove all nodes that have a flow rate of 0 and plot
    Only for understanding the graph better
    """
    reduced_graph = networkx.Graph()
    reduced_graph.add_node(start_room)
    for room in graph.nodes():  # add rooms
        if room.flow_rate > 0:
            reduced_graph.add_node(room)
    for room_a, room_b in itertools.permutations(reduced_graph.nodes, 2):
        shortest_path = networkx.shortest_path(graph, room_a, room_b)
        # if shortest path consists only of removed nodes
        if not list(filter(lambda r: r in reduced_graph.nodes or r == start_room, shortest_path[1:-1])):
            reduced_graph.add_edge(room_a, room_b, weight=len(shortest_path)-1)
    return reduced_graph


def calculate_distance_matrix(graph: networkx.Graph, start_room: Room):
    """
    Add the shortest distance from any node with flow to every other node with flow.
    IMPORTANT! This adds one extra minute for opening the valve at the destination.
    So to move to room x means moving there and opening the valve which takes distance + 1 min. time
    """
    for start, paths in networkx.shortest_path_length(graph, weight='weight'):
        for dest in graph.nodes:
            if start != dest and dest != start_room:
                shortest_path = paths[dest]
                start.distances[dest] = shortest_path + 1


def calculate_best_path(start_room: Room, all_other_rooms: set[Room], verbose=False):
    starting_path = PossiblePath(0, start_room, 30, all_other_rooms)
    next_paths = [starting_path]
    final_scores = dict()
    total_paths_considered = 0
    while next_paths:
        next_path = next_paths.pop(0)
        total_paths_considered += 1
        if verbose:
            print(f'Looking at path {next_path} with {next_path.remaining_time} minutes remaining')
        try:
            new_possibilities = next_path.next_possibles(verbose=verbose, do_not_optimize=True)
            next_paths += new_possibilities
        except NoMoreOptions:
            final_scores[next_path.current_score] = next_path
    top_scores = sorted(final_scores.keys(), reverse=True)[0:5]
    top_scores_str = '\n  '.join([str(final_scores[score]) for score in top_scores])
    print(f'Top scores: {top_scores_str}')
    print(f'Considered {total_paths_considered} paths in total.')
    return top_scores[0], final_scores[top_scores[0]]


def print_formatted_path(path: list[Room], original_graph: networkx.Graph, start: Room):
    open_valves = []
    real_path = []
    currently_opening = None
    total_released_pressure = 0
    for a, b in zip([start] + path[:-1], path):
        real_path += networkx.shortest_path(original_graph, a, b)
    real_path.append(path[-1])
    real_path.pop(0)
    print(len(real_path))
    for minute, room in enumerate(real_path + [None for i in range(30 - len(real_path))]):
        print(f"== Minute {minute+1} ==")
        if open_valves:
            released_pressure = sum([valve.flow_rate for valve in open_valves])
            total_released_pressure += released_pressure
            print(f"Valves {', '.join([room.name for room in open_valves])} are open, releasing {released_pressure} pressure.")
        else:
            print("No valves are open.")
        if room in path and room != currently_opening:
            print(f'You move to valve {room.name}.')
            currently_opening = room
        elif room in path:
            print(f'You open valve {room.name}.')
            open_valves.append(room)
        elif room:
            print(f'You move to valve {room.name}.')
        print()
    print(f'Total pressure released: {total_released_pressure}')


def main():
    graph = networkx.Graph()
    room_dict, start = set_up_graph()
    rooms = list(room_dict.values())
    for room in rooms:
        graph.add_node(room)
    for room in rooms:
        for dest in room.leads_to:
            graph.add_edge(room, dest)
    print_stats(rooms)
    reduced = reduce_graph(graph, start)
    plot_graph(reduced)
    calculate_distance_matrix(reduced, start)
    all_relevant_rooms = set(reduced.nodes)
    all_relevant_rooms.remove(start)
    score, path = calculate_best_path(start, all_relevant_rooms, verbose=VERBOSE)
    print(f'Best score: {score}')
    if VERBOSE:
        path_to_end_skipping_start = [room_dict[name] for name in path.path_to_here[1:]] + [path.current_room]
        print_formatted_path(path_to_end_skipping_start, graph, start)


main()
