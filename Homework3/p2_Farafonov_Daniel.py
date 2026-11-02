"""Homework 3, Problem 2: university parking permits.

Daniel Farafonov
"""

from typing import Dict, List


class ParkingPermit:
    """A parking permit with an owner, a duration and a fee schedule."""

    def __init__(self, owner: str, months: int,
                 fees: Dict[str, float]) -> None:
        """Creates a permit.

        Precondition: owner is a non-empty string, months is an int >= 1,
            fees maps fee names to amounts.
        Raises ValueError if months < 1.
        """
        if months < 1:
            raise ValueError('months must be at least 1')
        self.owner = owner
        self.months = months
        self.fees = dict(fees)

    def cost(self) -> float:
        """Returns the permit cost: the monthly fee times the months."""
        return self.fees['monthly'] * self.months

    def __str__(self) -> str:
        """Returns a readable description of the permit."""
        return f'{self.owner}: {self.months} month(s)'

    def __repr__(self) -> str:
        """Returns a string that recreates the permit when evaluated."""
        return f'ParkingPermit({self.owner!r}, {self.months}, {self.fees!r})'


class StudentPermit(ParkingPermit):
    """A student permit that also records the number of vehicles."""

    def __init__(self, owner: str, months: int, fees: Dict[str, float],
                 vehicles: int = 1) -> None:
        """Creates a student permit.

        Precondition: fees has keys 'monthly' and 'extra_vehicle',
            vehicles is an int >= 1.
        Raises ValueError if vehicles < 1.
        """
        super().__init__(owner, months, fees)
        if vehicles < 1:
            raise ValueError('vehicles must be at least 1')
        self.vehicles = vehicles

    def cost(self) -> float:
        """Returns the monthly cost plus a one-time fee per extra vehicle."""
        return (super().cost()
                + self.fees['extra_vehicle'] * (self.vehicles - 1))

    def __str__(self) -> str:
        """Returns a readable description of the student permit."""
        return (f'Student permit, {super().__str__()}, '
                f'{self.vehicles} vehicle(s)')

    def __repr__(self) -> str:
        """Returns a string that recreates the permit when evaluated."""
        return (f'StudentPermit({self.owner!r}, {self.months}, '
                f'{self.fees!r}, {self.vehicles})')


class FacultyPermit(ParkingPermit):
    """A faculty permit that also records whether garage access is included."""

    def __init__(self, owner: str, months: int, fees: Dict[str, float],
                 garage: bool = False) -> None:
        """Creates a faculty permit.

        Precondition: fees has keys 'monthly' and 'garage'.
        """
        super().__init__(owner, months, fees)
        self.garage = garage

    def cost(self) -> float:
        """Returns the monthly cost plus the monthly garage fee, if any."""
        garage_cost = self.fees['garage'] * self.months if self.garage else 0
        return super().cost() + garage_cost

    def __str__(self) -> str:
        """Returns a readable description of the faculty permit."""
        access = 'with' if self.garage else 'without'
        return f'Faculty permit, {super().__str__()}, {access} garage'

    def __repr__(self) -> str:
        """Returns a string that recreates the permit when evaluated."""
        return (f'FacultyPermit({self.owner!r}, {self.months}, '
                f'{self.fees!r}, {self.garage})')


def summarize_list(permits: List[ParkingPermit]) -> float:
    """Prints each permit (its __str__, which starts with the owner's
    name) with its cost, and returns the total revenue.

    Precondition: permits is a list of ParkingPermit objects.
    """
    total = 0
    for permit in permits:
        cost = permit.cost()
        print(f'{permit} -> cost ${cost:.2f}')
        total += cost
    return total


def main() -> None:
    """Creates a mixed list of permits and summarizes it."""
    student_fees = {'monthly': 25, 'extra_vehicle': 10}
    faculty_fees = {'monthly': 40, 'garage': 15}
    permits = [
        StudentPermit('Alice', 4, student_fees),
        StudentPermit('Bob', 9, student_fees, vehicles=3),
        FacultyPermit('Dr. Cardei', 12, faculty_fees, garage=True),
        FacultyPermit('Dr. Smith', 6, faculty_fees),
    ]

    print('Permits (str):')
    for permit in permits:
        print(' ', permit)
    print('Permits (repr):')
    print(' ', permits)

    print('Summary:')
    total = summarize_list(permits)
    print(f'Total revenue: ${total:.2f}')


if __name__ == '__main__':
    main()
