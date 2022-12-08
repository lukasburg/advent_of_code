from itertools import chain


class Node:
    def __init__(self, name: str, parent: 'Directory', size: int):
        self.name = name
        self.parent = parent
        self._add_self_to_parent()
        self._size = size

    @property
    def size(self):
        return self._size

    def _add_self_to_parent(self):
        self.parent.children.add(self)

    def __bool__(self):
        return True

    def format(self, deepness=0, symbol='-'):
        return ' '*(deepness*2 - 1) + f'{symbol} {self.name} {self.size if self._size else ""}\n'


class Directory(Node):
    def __init__(self, name: str, parent: 'Directory', children: set[Node] = None):
        super().__init__(name, parent, None)
        if children is None:
            children = set()
        self.children = children
        self._size = None

    @property
    def size(self):
        # if not self._size:
        #     raise AttributeError("Size has not jet been calculated.")
        return self._size

    def add_child(self, child: Node):
        self.children.add(child)

    def try_calculate_size(self):
        if self._can_calculate_size():
            self._calculate_size()
            self.parent.try_calculate_size()

    def find_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        raise KeyError(f"Directory {self.name} contains no directory named {name}")

    def _calculate_size(self):
        self._size = sum([child.size for child in self.children])

    def _can_calculate_size(self) -> bool:
        return all(self.children)

    def __bool__(self):
        return bool(self._size)

    def __str__(self):
        return super().format(0, '').removesuffix("\n")

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(chain([self], *[iter(child) for child in self.children if isinstance(child, Directory)]))

    def format(self, deepness=0, symbol='\\'):
        file_strings = []
        dir_strings = []
        for child in self.children:
            if isinstance(child, Directory):
                dir_strings.append(child.format(deepness+1))
            else:
                file_strings.append(child.format(deepness+1))
        return super().format(deepness, symbol=symbol) + ''.join(file_strings + dir_strings)


class RootDirectory(Directory):
    def __init__(self, name: str, children: set[Node] = None):
        super().__init__(name, None, children)

    def _add_self_to_parent(self):
        return

    def try_calculate_size(self):
        """Dont try to calculate parent"""
        if self._can_calculate_size():
            self._calculate_size()


root = RootDirectory('')
current_dir = root
small_dirs = set()
TOTAL_SAVE_SPACE = 70000000
REQUIRED_SPACE = 30000000


with open("input") as file:
    while line := file.readline():
        # print(line)
        if line.startswith('$'):
            if line.startswith('$ ls'):
                continue
            elif line.startswith('$ cd'):
                current_dir.try_calculate_size()
                if current_dir and current_dir.size <= 100000:
                    small_dirs.add(current_dir)
                if line.startswith('$ cd /'):
                    current_dir = root
                elif line.startswith('$ cd ..'):
                    current_dir = current_dir.parent
                elif line.startswith('$ cd'):
                    child_dir_name = line.removeprefix('$ cd ')
                    current_dir = current_dir.find_child(child_dir_name.strip())
            else:
                raise AttributeError(f'Unknown command "{line}"')
        else:
            # ls output
            if line.startswith('dir'):
                dir_name = line.removeprefix('dir ')
                Directory(dir_name.strip(), current_dir)
            else:
                size, file_name = line.split(" ")
                Node(file_name.strip(), current_dir, int(size))
    current_dir.try_calculate_size()
    if current_dir.size and current_dir.size < 100000:
        small_dirs.add(current_dir)

small_dirs_sum = sum([directory.size for directory in small_dirs])
space_missing = REQUIRED_SPACE - (TOTAL_SAVE_SPACE - root.size)
print(root.format())
print(f'small dirs sum: {small_dirs_sum}')
print(f'used space: {root.size}, free_space: {(TOTAL_SAVE_SPACE - root.size)}, amount to delete for update: {space_missing}')

current_deletion_candidate = root
for directory in root:
    if directory.size < space_missing:
        continue
    elif directory.size < current_deletion_candidate.size:
        current_deletion_candidate = directory

print('Deletion candidate: ', current_deletion_candidate)