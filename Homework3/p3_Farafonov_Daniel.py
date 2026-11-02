"""Homework 3, Problem 3: predator-prey simulation with humans.

Daniel Farafonov

Based on program13-14.py (Punch & Enbody). Five classes are defined:
Island, Animal, Prey, Predator and Human. The island is an n x n grid
where the animals live. Prey breed; predators eat prey, breed and
starve; humans eat predators, breed and starve. All animals move.
"""

import random
from typing import Optional, Tuple, Type, Union

import matplotlib.pyplot as plt

# number of ticks with unchanged populations that counts as convergence
STABLE_TICKS = 50


class Island:
    """An n x n grid where a value of 0 means the cell is not occupied."""

    def __init__(self, n: int, prey_count: int = 0, predator_count: int = 0,
                 count_humans: int = 0) -> None:
        """Creates an empty n x n grid, then fills it with animals."""
        self.grid_size = n
        self.grid = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, count_humans)

    def init_animals(self, prey_count: int, predator_count: int,
                     count_humans: int) -> None:
        """Puts the given numbers of animals at random unoccupied cells."""
        for animal_class, total in ((Prey, prey_count),
                                    (Predator, predator_count),
                                    (Human, count_humans)):
            count = 0
            # keep trying until total unoccupied positions are found
            while count < total:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if not self.animal(x, y):
                    self.register(animal_class(island=self, x=x, y=y))
                    count += 1

    def clear_all_moved_flags(self) -> None:
        """Clears every animal's moved flag so the next turn can start."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        """Returns the size of one dimension of the island."""
        return self.grid_size

    def register(self, animal: 'Animal') -> None:
        """Puts animal on the grid at its own coordinates."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: 'Animal') -> None:
        """Removes animal from the grid."""
        self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> Union['Animal', int]:
        """Returns the animal at (x, y), 0 if empty, -1 if off the island."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def __str__(self) -> str:
        """Returns the grid as text, with (0, 0) in the lower left corner."""
        s = ''
        for j in range(self.grid_size - 1, -1, -1):  # print row size-1 first
            for i in range(self.grid_size):  # each row starts at 0
                if not self.grid[i][j]:
                    s += '{:<2s}'.format('.' + '  ')
                else:
                    s += '{:<2s}'.format(str(self.grid[i][j]) + '  ')
            s += '\n'
        return s

    def count(self, animal_class: Type['Animal']) -> int:
        """Returns the number of animals of type animal_class on the grid."""
        total = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if isinstance(self.grid[x][y], animal_class):
                    total += 1
        return total

    def count_prey(self) -> int:
        """Returns the number of Prey objects on the grid."""
        return self.count(Prey)

    def count_predators(self) -> int:
        """Returns the number of Predator objects on the grid."""
        return self.count(Predator)

    def count_humans(self) -> int:
        """Returns the number of Human objects on the grid."""
        return self.count(Human)


class Animal:
    """An animal on the island that can move and breed."""

    starve_time: Optional[int] = None  # None: the animal never starves

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = 'A') -> None:
        """Creates an animal at (x, y) on island, printed as s."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False
        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time

    def position(self) -> Tuple[int, int]:
        """Returns the coordinates of the current position."""
        return self.x, self.y

    def __str__(self) -> str:
        """Returns the character used to print the animal on the grid."""
        return self.name

    def check_grid(self, type_looking_for: type = int
                   ) -> Optional[Tuple[int, int]]:
        """Returns a neighboring cell holding type_looking_for, or None."""
        # neighbor offsets
        offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1),
                   (0, -1), (1, -1)]
        for dx, dy in offsets:
            x = self.x + dx  # neighboring coordinates
            y = self.y + dy
            if not 0 <= x < self.island.size() or \
               not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x, y)) == type_looking_for:
                return x, y
        return None

    def move_to(self, location: Tuple[int, int]) -> None:
        """Moves the animal to location and marks it as moved."""
        self.island.remove(self)  # remove from current spot
        self.x, self.y = location  # new coordinates
        self.island.register(self)  # register new coordinates
        self.moved = True

    def move(self) -> None:
        """Moves to an open neighboring cell, if not moved this turn."""
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.move_to(location)

    def eat(self) -> None:
        """Does nothing: a plain animal does not eat other animals."""

    def eat_neighbor(self, food_type: Type['Animal']) -> bool:
        """Moves onto a neighboring animal of type food_type and removes it."""
        if self.moved:
            return False
        location = self.check_grid(food_type)
        if not location:
            return False
        self.island.remove(self.island.animal(*location))
        self.move_to(location)
        return True

    def breed(self) -> None:
        """Places a new animal in an open neighboring cell when ready."""
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                new_animal = self.__class__(self.island, x=location[0],
                                            y=location[1])
                self.island.register(new_animal)

    def fed(self) -> None:
        """Resets the starve clock after eating."""
        self.starve_clock = self.starve_time

    def clock_tick(self) -> None:
        """Updates the clocks and removes the animal if it starves."""
        self.breed_clock -= 1
        if self.starve_clock is not None:
            self.starve_clock -= 1
            if self.starve_clock <= 0:
                self.island.remove(self)

    def clear_moved_flag(self) -> None:
        """Clears the moved flag for the next turn."""
        self.moved = False


class Prey(Animal):
    """An animal that only moves and breeds."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = 'O') -> None:
        """Creates a prey at (x, y) on island, printed as s."""
        super().__init__(island, x, y, s)


class Predator(Animal):
    """An animal that eats prey and starves if it does not eat."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = 'X') -> None:
        """Creates a predator at (x, y) on island, printed as s."""
        super().__init__(island, x, y, s)

    def eat(self) -> None:
        """Eats a neighboring prey, if there is one."""
        if self.eat_neighbor(Prey):
            self.fed()


class Human(Animal):
    """An animal that hunts predators every hunt_time ticks."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = 'H') -> None:
        """Creates a human at (x, y) on island, printed as s."""
        super().__init__(island, x, y, s)
        self.hunt_clock = self.hunt_time

    def eat(self) -> None:
        """Every hunt_time ticks, eats a neighboring predator if any."""
        if self.hunt_clock <= 0:
            self.hunt_clock = self.hunt_time
            if self.eat_neighbor(Predator):
                self.fed()

    def clock_tick(self) -> None:
        """Updates the hunt clock, then the breed and starve clocks."""
        self.hunt_clock -= 1
        super().clock_tick()


def main(predator_breed_time: int = 6, predator_starve_time: int = 4,
         initial_predators: int = 90, prey_breed_time: int = 3,
         initial_prey: int = 225, human_breed_time: int = 15,
         human_starve_time: int = 15, human_hunt_time: int = 6,
         initial_humans: int = 8, size: int = 30, ticks: int = 1000) -> None:
    """Runs the simulation and plots the populations at the end."""
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    # for graphing
    prey_list = []
    predator_list = []
    human_list = []

    isle = Island(size, initial_prey, initial_predators, initial_humans)
    print('Island at the start:')
    print(isle)

    # event loop: every tick, every animal tries to eat, move, breed
    # and update its clocks
    for tick in range(ticks):
        # important to clear all the moved flags!
        isle.clear_all_moved_flags()
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)
                if animal:
                    animal.eat()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()

        # record info for display, plotting
        prey_list.append(isle.count_prey())
        predator_list.append(isle.count_predators())
        human_list.append(isle.count_humans())
        # print every 10th tick to see what's going on
        if not tick % 10:
            print(f'tick {tick:4d}: prey {prey_list[-1]:3d}, '
                  f'predators {predator_list[-1]:3d}, '
                  f'humans {human_list[-1]:3d}')

        # converged if no population changed in the last STABLE_TICKS ticks
        if len(prey_list) > STABLE_TICKS and all(
                len(set(counts[-STABLE_TICKS:])) == 1
                for counts in (prey_list, predator_list, human_list)):
            print(f'Populations converged at tick {tick}.')
            break

    print(f'Island at the end (tick {len(prey_list) - 1}):')
    print(isle)
    print(f'Final populations: prey {prey_list[-1]}, '
          f'predators {predator_list[-1]}, humans {human_list[-1]}')
    print(f'Maximum populations: prey {max(prey_list)}, '
          f'predators {max(predator_list)}, humans {max(human_list)}')

    plt.plot(prey_list, label='Prey')
    plt.plot(predator_list, label='Predators')
    plt.plot(human_list, label='Humans')
    plt.xlabel('Time (ticks)')
    plt.ylabel('Population')
    plt.title('Prey, predator and human populations')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
