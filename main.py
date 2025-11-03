from dataclasses import dataclass, field
from typing import List, Set, Optional


@dataclass
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]
    assigned_subjects: Set[str] = field(default_factory=set, init=False, repr=False)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.age})"


def create_schedule(subjects: Set[str], teachers: List[Teacher]) -> Optional[List[Teacher]]:
    uncovered_subjects = set(subjects)
    schedule: List[Teacher] = []
    available_teachers = list(teachers)

    while uncovered_subjects:
        candidates = []
        for teacher in available_teachers:
            coverable_subjects = teacher.can_teach_subjects.intersection(uncovered_subjects)
            if coverable_subjects:
                candidates.append((teacher, coverable_subjects))

        if not candidates:
            return None

        candidates.sort(key=lambda x: (-len(x[1]), x[0].age))

        most_suitable_teacher, subjects_to_assign = candidates[0]

        most_suitable_teacher.assigned_subjects = subjects_to_assign
        schedule.append(most_suitable_teacher)

        uncovered_subjects -= subjects_to_assign
        available_teachers.remove(most_suitable_teacher)

    return schedule


if __name__ == '__main__':
    subjects: Set[str] = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}

    teachers: List[Teacher] = [
        Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com', {'Математика', 'Фізика'}),
        Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com', {'Хімія'}),
        Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com', {'Інформатика', 'Математика'}),
        Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}),
        Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}),
        Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com', {'Біологія'}),
    ]

    final_schedule: Optional[List[Teacher]] = create_schedule(subjects, teachers)

    if final_schedule:
        print("Розклад занять:")
        for teacher in final_schedule:
            assigned = ', '.join(sorted(list(teacher.assigned_subjects)))
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {assigned}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")
