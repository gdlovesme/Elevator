import random

from typing import List


class Building:
    """При инициализации класса создаются случайное количество этажей 'floors'"""

    def __init__(self):
        self.floors: List['Floor'] = []

        count_floors = list(range(1, random.randint(5, 20)))
        for i in count_floors:
            if i == count_floors[0]:
                self.floors.append(Floor(i, first=True))
            elif i == count_floors[-1]:
                self.floors.append(Floor(i, last=True))
            else:
                self.floors.append(Floor(i))


class Floor:

    def __init__(self, number_floor: int, first=False, last=False):
        """Если first=True значит этаж первый и кнопка вызова лифта может быть только 'Вверх' т.е up
           и аналогично если last=True, если же first и last = True обе кнопки будут доступными """
        if first:
            self.up = False
        elif last:
            self.down = False
        else:
            self.up = False
            self.down = False

        self.number_floor: int = number_floor
        self.passengers: List['Passenger'] = self._set_passengers()

    def _set_passengers(self) -> List['Passenger']:
        """Генерируем случайное количество пассажиров"""
        passengers = []
        for i in range(0, random.randint(0, 10)):
            passengers.append(Passenger(self))
        return passengers


class Passenger:
    def __init__(self, current_floor: Floor):
        self.current_floor: Floor = current_floor
        self.desired_floor: int = 1
        self.direction: bool = False  # Направление кнопки, если True то вверх если False - вниз

    def set_desired_floor(self, count_of_floors: int) -> None:
        """Генерируем желаемый этаж для пассажира и кнопки"""
        random.randint(1, count_of_floors)
        while True:
            desired_floor = random.randint(1, count_of_floors)
            if desired_floor != self.current_floor.number_floor:
                break
        self.desired_floor = desired_floor
        # Направление кнопки, если True то вверх если False - вниз
        self.direction = True if self.current_floor.number_floor < self.desired_floor else False


class Elevator(Building):
    passenger_capacity = 5

    def __init__(self):
        self.passenger_count: List[Passenger] = []
        self.current_floor: int = 1
        self.endpoint: int = 2

        # Направление кнопки, если True то вверх если False - вниз
        self.direction = True if self.current_floor < self.endpoint else False
        super().__init__()

    def _append_passengers(self, floor: Floor) -> None:
        for passenger in floor.passengers:
            if len(self.passenger_count) < self.passenger_capacity\
                    and passenger.direction == self.direction:
                self.passenger_count.append(passenger)
                floor.passengers.remove(passenger)

    def _drop_passengers(self, floor: Floor) -> None:
        for passenger in self.passenger_count:
            if passenger.desired_floor == self.current_floor:
                floor.passengers.append(passenger)
                passenger.current_floor = floor
                passenger.set_desired_floor(len(self.floors))

                self.passenger_count.remove(passenger)

    def _get_current_floor_data(self) -> Floor:
        try:
            floor = list(filter(lambda x: self.current_floor == x.number_floor, self.floors))
            return floor[0]
        except IndexError:
            raise IndexError

    def change_direction(self):
        # self.direction = True if self.direction else False
        if self.direction:
            self.direction = False
        else:
            self.direction = True

    def move_elevator(self):
        step_count = 0
        while True:
            step_count += 1
            if step_count > 100:
                break

            print(f'Step {step_count}')
            step_dict = {'Текущий этаж': self.current_floor,
                         'Количество пассажиров': len(self.passenger_count),
                         'Конечная точка': self.endpoint,
                         'Остановки на этажах': sorted([i.desired_floor for i in self.passenger_count]),
                         'Направление лифта': {'вверх' if self.direction else 'вниз'}}
            print(step_dict)

            self._append_passengers(self._get_current_floor_data())
            elevator_path = sorted(list(i.desired_floor for i in self.passenger_count))

            if self.direction:
                try:
                    self.endpoint = elevator_path[-1]

                    if self.current_floor == len(self.floors):
                        self.change_direction()

                    if self.current_floor != self.endpoint:
                        self.current_floor += 1 if self.current_floor != len(self.floors) else 0

                    elif self.current_floor == self.endpoint:
                        self.change_direction()
                except IndexError:
                    if self.current_floor != 1:
                        self.current_floor -= 1
                    else:
                        self.change_direction()

            elif not self.direction:
                try:
                    self.endpoint = elevator_path[0]

                    if self.current_floor == 1:
                        self.change_direction()

                    if self.current_floor != self.endpoint:
                        self.current_floor -= 1 if self.current_floor != 1 else 0

                    elif self.current_floor == self.endpoint:
                        self.change_direction()

                except IndexError:
                    if self.current_floor != len(self.floors):
                        self.current_floor += 1
                    else:
                        self.change_direction()

            self._drop_passengers(self._get_current_floor_data())


def main():
    elevator = Elevator()
    for floor in elevator.floors:
        for passenger in floor.passengers:
            passenger.set_desired_floor(len(elevator.floors))

    elevator.move_elevator()


if __name__ == '__main__':
    main()