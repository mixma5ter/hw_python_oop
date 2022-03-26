class InfoMessage:
    """Информационное сообщение о тренировке."""
    
    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float) -> None:
        self.training_type = training_type
        self.duration = format(duration, '.3f')
        self.distance = format(distance, '.3f')
        self.speed = format(speed, '.3f')
        self.calories = format(calories, '.3f')
    
    def get_message(self):
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration} ч.; '
            f'Дистанция: {self.distance} км; '
            f'Ср. скорость: {self.speed} км/ч; '
            f'Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_H = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Логика подсчета калорий для каждого вида тренировки своя."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_info = InfoMessage(
            str(self),
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return ((coeff_calorie_1 * self.get_mean_speed() -
                coeff_calorie_2) * self.weight / self.M_IN_KM *
                self.duration * self.M_IN_H)

    def __str__(self):
        return 'Running'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((0.035 * self.weight + (self.get_mean_speed()**2 //
                self.height) * 0.029 * self.weight) * self.duration *
                self.M_IN_H)

    def __str__(self):
        return 'SportsWalking'


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    
    def __init__(
            self, action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool /
                self.M_IN_KM / self.duration)

    def __str__(self):
        return 'Swimming'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
        return Running(*data)
    else:
        return SportsWalking(*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

