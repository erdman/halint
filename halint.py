#!/usr/bin/env python3

import argparse, json, gzip
from itertools import chain
from collections import namedtuple, Counter, defaultdict
from tabulate import tabulate

NORTH, EAST, SOUTH, WEST, STILL = range(5)
Square = namedtuple('Square', 'x y owner strength production')
Move = namedtuple('Move', 'square direction')
Placement = namedtuple('Placement','square owner strength')

def opposite_cardinal(direction):
    "Returns the opposing cardinal direction."
    return (direction + 2) % 4 if direction != STILL else STILL

class Replay:
    def __init__(self, replay_filename):
        try:
            with gzip.open(replay_filename,'rt') as f:
                self.data = json.load(f)
        except:
            with open(replay_filename) as f:
                self.data = json.load(f)
        self.game_map = GameMap(self.data)
        self.names = ['PLAYER_ZERO'] + self.data['player_names']  #1-indexed list   #{index: name for index, name in enumerate(self.data['player_names'], 1)}

    def __iter__(self):
        "Allows direct iteration over all maps and moves in the replay."
        return (self[frame_num] for frame_num, _ in enumerate(self.data['moves']))

    def __getitem__(self, frame_num):
        self.game_map._update_frame(self.data['frames'][frame_num])
        moves = {square : (move - 1) % 5 for square, move in zip(self.game_map, chain.from_iterable(self.data['moves'][frame_num]))}   #translate to Python move constants
        return self.game_map, moves


class GameMap:
    def __init__(self, data):
        self.width, self.height = data['width'], data['height']
        self.production = data['productions']
        self.contents = None
        self._update_frame(data['frames'][0])
        self.starting_player_count = len(set(square.owner for square in self)) - 1


    def _update_frame(self, frame):
        "Updates the map information with frame from replay file."
        self.contents = [[Square(x, y, owner, strength, production)
                          for x, ((owner, strength), production)
                          in enumerate(zip(frame_row, production_row))]
                         for y, (frame_row, production_row)
                         in enumerate(zip(frame, self.production))]

    def __iter__(self):
        "Allows direct iteration over all squares in the GameMap instance."
        return chain.from_iterable(self.contents)

    def neighbors(self, square, n=1, include_self=False):
        "Iterable over the n-distance neighbors of a given square.  For single-step neighbors, the enumeration index provides the direction associated with the neighbor."
        assert isinstance(include_self, bool)
        assert isinstance(n, int) and n > 0
        if n == 1:
            combos = ((0, -1), (1, 0), (0, 1), (-1, 0), (0, 0))   # NORTH, EAST, SOUTH, WEST, STILL ... matches indices provided by enumerate(game_map.neighbors(square))
        else:
            combos = ((dx, dy) for dy in range(-n, n+1) for dx in range(-n, n+1) if abs(dx) + abs(dy) <= n)
        return (self.contents[(square.y + dy) % self.height][(square.x + dx) % self.width] for dx, dy in combos if include_self or dx or dy)

    def get_target(self, square, direction):
        "Returns a single, one-step neighbor in a given direction."
        dx, dy = ((0, -1), (1, 0), (0, 1), (-1, 0), (0, 0))[direction]
        return self.contents[(square.y + dy) % self.height][(square.x + dx) % self.width]

    def get_distance(self, sq1, sq2):
        "Returns Manhattan distance between two squares."
        dx = min(abs(sq1.x - sq2.x), sq1.x + self.width - sq2.x, sq2.x + self.width - sq1.x)
        dy = min(abs(sq1.y - sq2.y), sq1.y + self.height - sq2.y, sq2.y + self.height - sq1.y)
        return dx + dy

def lint_msg(msg, frame_num, bot_name, locx, locy, value=None):
    if not args.names or any(name in bot_name for name in args.names):
        if value is not None:
            msg = 'Frame {:>3}: {:>16}: {:>25} ({:>2},{:>2}): {:>3}'.format(frame_num, bot_name, msg, locx, locy, value)
        else:
            msg = 'Frame {:>3}: {:>16}: {:>25} ({:>2},{:>2})'.format(frame_num, bot_name, msg, locx, locy)
        print(msg)

def lint(filename):
    replay = Replay(filename)
    accum_caploss = defaultdict(int)
    accum_caploss_incl_prod = defaultdict(int)
    caploss = {key: [0] * len(replay.names) for key in ('merge_standard', 'merge_production', 'still_big_production', 'movement')}
    move_counts = defaultdict(list)
    territory_counts = defaultdict(list)
    previous_moves = previous_moves_2 = None
    accum_overkill = defaultdict(lambda: defaultdict(int))
    for frame_num, (game_map, moves) in enumerate(replay):
        move_count = defaultdict(int)
        territory_count = defaultdict(int)
        placements = defaultdict(lambda: defaultdict(int))
        for square in game_map:
            if square.owner != 0 :
                target = game_map.get_target(square, moves[square])
                placements[target][square.owner] += square.strength
                if moves[square] != STILL:
                    caploss['movement'][square.owner] += square.production
                territory_count[square.owner] += 1
                move_count[square.owner] += moves[square] != STILL
                if square.strength == 0 and moves[square] != STILL:
                    lint_msg('Zero strength move at',frame_num, replay.names[square.owner], square.x, square.y)
                if args.show_flip_flops and previous_moves and previous_moves_2 \
                    and previous_moves.get((target.x, target.y, square.owner), None) == opposite_cardinal(moves[square]) != STILL \
                    and previous_moves_2.get((square.x, square.y, square.owner), None) == moves[square] != STILL:
                        lint_msg('Flip-flop move at', frame_num, replay.names[square.owner], square.x, square.y)
        for owner, count in territory_count.items():
            territory_counts[owner].append(count)
        for owner, count in move_count.items():
            move_counts[owner].append(count)

        for target, sub_d in placements.items():
            for owner, total in sub_d.items():
                if total > 255:   # immediate caploss
                    caploss['merge_standard'][owner] += total - 255
                    lint_msg('Cap loss at', frame_num, replay.names[owner], target.x, target.y, total - 255)
                    total = min(total, 255)   #remove effect of standard caploss, to accumulate production caploss separately
                if target.owner == owner and moves[target] == STILL:
                    total += target.production
                    if total > 255:
                        if total > target.strength + target.production:
                            caploss['merge_production'][owner] += total - 255
                            if args.show_caploss_from_production:
                                lint_msg('Cap loss ex production at', frame_num, replay.names[owner], target.x, target.y, total - 255)
                        else:
                            caploss['still_big_production'][owner] += total - 255
                placements[target][owner] = min(total, 255)

        interactions = dict()
        for target, sub_d in placements.items():
            for owner, total in sub_d.items():
                interactions[Placement(target,owner,total)] = [Placement(neighbor,key,value) for neighbor in game_map.neighbors(target, include_self=True) for key,value in placements.get(neighbor,dict()).items() if key != owner]

        for target, sub_d in placements.items():
            for owner, total in sub_d.items():
                # check for failed mining attempt
                if target.owner == 0 and total <= min(254, target.strength):
                    lint_msg('Failed mining attempt at',frame_num, replay.names[owner], target.x, target.y)

                # check overkill
                attacker = Placement(target, owner, total)
                overkill = defaultdict(int)
                for defender in interactions[attacker]:
                    other_damage = sum(min(defender.strength, placement.strength) for placement in interactions[defender] if placement != attacker)
                    overkill[defender.owner] += min(max(0, defender.strength - other_damage), attacker.strength)
                for defender_owner, damage in overkill.items():
                    if damage > attacker.strength:
                        if args.show_overkill:
                            lint_msg('Overkill received from', frame_num, replay.names[defender_owner], target.x, target.y, damage - attacker.strength)
                        accum_overkill[attacker.owner][defender_owner] += damage - attacker.strength

        previous_moves, previous_moves_2 = {(square.x,square.y,square.owner) : direction for square, direction in moves.items()}, previous_moves

    print()
    headers = ['Caploss'] + replay.names[1:] + ['TOTAL']
    table = [['Standard'] + caploss['merge_standard'][1:] + [sum(caploss['merge_standard'])]]
    table.append(['Merge ex Production'] + caploss['merge_production'][1:] + [sum(caploss['merge_production'])])
    table.append(['StillBig ex Production'] + caploss['still_big_production'][1:] + [sum(caploss['still_big_production'])])
    table.append(['TOTAL'] + [sum(values) for values in zip(*[values for key, values in caploss.items() if key != 'movement'])][1:] + [sum(sum(values) for key, values in caploss.items() if key != 'movement')])  #exclude caploss from movement here
    print(tabulate(table,headers,tablefmt='grid'))

    print()
    headers = [''] + ['Prod cost from moves', 'Total moves', 'Prod cost per move']
    table=list()
    for bot_index, name in enumerate(replay.names[1:],1):
        table.append([name, caploss['movement'][bot_index], sum(move_counts[bot_index]), caploss['movement'][bot_index] / sum(move_counts[bot_index])])
    print(tabulate(table,headers,tablefmt='grid',floatfmt='5.3f'))

    print()
    segment_length = max(len(count) for count in territory_counts.values()) // 5   # 1/5 of the whole game
    headers = ['Move %','1 / 5','2 / 5','3 / 5','4 / 5','5 / 5']
    table = list()
    for bot_index, name in enumerate(replay.names[1:],1):
        table.append([name] +  [sum(move_counts[bot_index][n*segment_length:(n+1)*segment_length]) / (0.01 + sum(territory_counts[bot_index][n*segment_length:(n+1)*segment_length])) for n in range(5)])
    print(tabulate(table,headers,tablefmt='grid',floatfmt='5.3f'))

    print()
    print('Cumulative overkill')
    headers = ['from / to'] + replay.names[1:] + ['TOTAL']
    table = [[name] + [accum_overkill[src][target] for target, _ in enumerate(replay.names[1:],1)]  + [sum(accum_overkill[src].values())] for src, name in enumerate(replay.names[1:],1)]
    table.append(['TOTAL'] + [sum(accum_overkill[src][target] for src, _ in enumerate(replay.names[1:],1)) for target, _ in enumerate(replay.names[1:],1)] + [sum(sum(d.values()) for d in accum_overkill.values())])
    print(tabulate(table, headers, tablefmt='grid'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', type=str, nargs='+')
    parser.add_argument('--names',type=str, nargs='?', default=None, help='Restrict lint output to these named bots.')
    parser.add_argument('--show_caploss_from_production',dest="show_caploss_from_production", action = "store_true", default = False, help='Shows caploss which occured solely due to production.')
    parser.add_argument('--show_overkill',dest='show_overkill', action='store_true', default=False, help='Show detailed overkill frame-by-frame.')
    parser.add_argument('--show_flip_flops',dest='show_flip_flops', action='store_true', default=False, help='Show pieces that flip-flop between adjacent squares.')
    args = parser.parse_args()

    if args.names:
        args.names = args.names.split()

    for filename in args.filenames:
        print('Starting halint for {}'.format(filename))
        lint(filename)
        print('Replay may be available at https://halite.io/game.php?replay={}'.format(filename))
        print('Completed halint for {}'.format(filename))
        print()
