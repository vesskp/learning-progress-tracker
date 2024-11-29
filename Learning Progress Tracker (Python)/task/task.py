import re
from traceback import print_tb

students = {}
next_id = 10000
course_points = {
    'Python': 600,
    'DSA': 400,
    'Databases': 480,
    'Flask': 550
}


def is_valid_name(name):
    for n in name.split(" "):
        if not re.match(r"^[A-Za-z][A-Za-z'-]*[A-Za-z]$", n):
            return False
        if "--" in n or "''" in n or "-'" in n or "'-" in n:
            return False
    return True


def is_valid_email(email):
    return re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]+$", email) is not None


def add_students():
    global next_id
    print("Enter student credentials or 'back' to return.")
    while True:
        credentials = input().strip()
        if credentials.lower() == 'back':
            print(f"Total {len(students)} students have been added.")
            break

        parts = credentials.split()
        if len(parts) < 3:
            print("Incorrect credentials")
            continue

        first_name = parts[0]
        last_name = " ".join(parts[1:-1])
        email = parts[-1]

        if not is_valid_name(first_name):
            print("Incorrect first name")
        elif not is_valid_name(last_name):
            print("Incorrect last name")
        elif not is_valid_email(email):
            print("Incorrect email")
        elif email in [student['email'] for student in students.values()]:
            print("This email is already taken.")
        else:
            students[next_id] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'points': {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0},
                'notified': False,
            }
            print("The student has been added.")
            next_id += 1


def list_students():
    if students:
        print("Students:")
        for student_id in students:
            print(student_id)
    else:
        print("No students found.")


def add_points():
    print("Enter an id and points or 'back' to return.")
    while True:
        data = input().strip()
        if data.lower() == 'back':
            break

        parts = data.split()
        if len(parts) != 5:
            print("Incorrect points format.")
            continue

        if not parts[0].isnumeric():
            print(f"No student is found for id={parts[0]}.")
            continue

        student_id = int(parts[0])
        if student_id not in students:
            print(f"No student is found for id={student_id}.")
            continue

        try:
            points = list(map(int, parts[1:]))
            if any(p < 0 for p in points):
                raise ValueError
        except ValueError:
            print("Incorrect points format.")
            continue

        students[student_id]['points']['Python'] += points[0]
        students[student_id]['points']['DSA'] += points[1]
        students[student_id]['points']['Databases'] += points[2]
        students[student_id]['points']['Flask'] += points[3]
        print("Points updated.")


def find_student():
    print("Enter an id or 'back' to return.")
    while True:
        data = input().strip()
        if data.lower() == 'back':
            break

        if not data.isnumeric():
            print(f"No student is found for id={data}.")
            continue

        student_id = int(data)
        if student_id not in students:
            print(f"No student is found for id={data}.")
        else:
            student = students[student_id]
            points = student['points']
            print(
                f"id={student_id} points: Python={points['Python']}; DSA={points['DSA']}; Databases={points['Databases']}; Flask={points['Flask']}")


def calculate_statistics():
    course_stats = {}

    for student in students.values():
        for course, points in student['points'].items():

            if points > 0:
                if course not in course_stats:
                    course_stats[course] = {
                        'enrolled': 0,
                        'submissions': 0,
                        'total_points': 0,
                        'total_assignments': 0
                    }
                course_stats[course]['enrolled'] += 1
                course_stats[course]['submissions'] += 1
                course_stats[course]['total_points'] += points
                course_stats[course]['total_assignments'] += 1

    most_popular = max(course_stats, key=lambda x: course_stats[x]['enrolled'], default='n/a')
    if most_popular != 'n/a':
        v = course_stats[most_popular]['enrolled']
        most_popular = ", ".join([x for x in course_points if course_stats[x]['enrolled'] == v])

    least_popular = min(course_stats, key=lambda x: course_stats[x]['enrolled'], default='n/a')
    if least_popular != 'n/a':
        v = course_stats[least_popular]['enrolled']
        a = [x for x in course_points if course_stats[x]['enrolled'] == v]
        if len(a) < len(course_points):
            least_popular = ", ".join(a)
        else:
            least_popular = 'n/a'

    highest_activity = max(course_stats, key=lambda x: course_stats[x]['submissions'], default='n/a')
    if highest_activity != 'n/a':
        v = course_stats[highest_activity]['submissions']
        highest_activity = ", ".join([x for x in course_points if course_stats[x]['submissions'] == v])


    lowest_activity = min(course_stats, key=lambda x: course_stats[x]['submissions'], default='n/a')
    if lowest_activity != 'n/a':
        v = course_stats[lowest_activity]['submissions']
        a = [x for x in course_points if course_stats[x]['submissions'] == v]
        if len(a) < len(course_points):
            lowest_activity = ", ".join(a)
        else:
            lowest_activity = 'n/a'

    easiest_course = max(course_stats,
                         key=lambda x: course_stats[x]['total_points'] / course_stats[x]['total_assignments'] if
                         course_stats[x]['total_assignments'] > 0 else 0, default='n/a')
    hardest_course = min(course_stats,
                         key=lambda x: course_stats[x]['total_points'] / course_stats[x]['total_assignments'] if
                         course_stats[x]['total_assignments'] > 0 else 0, default='n/a')

    print("Type the name of a course to see details or 'back' to quit:")
    print(f"Most popular: {most_popular}")
    print(f"Least popular: {least_popular}")
    print(f"Highest activity: {highest_activity}")
    print(f"Lowest activity: {lowest_activity}")
    print(f"Easiest course: {easiest_course}")
    print(f"Hardest course: {hardest_course}")


def notify_students():
    notified = 0
    for student in students:
        if not students[student]['notified']:
            student_notified = False
            for course in course_points:
                if students[student]['points'][course] >= course_points[course]:
                    print(f"To: {students[student]['email']}")
                    print("Re: Your Learning Progress")
                    print(f"Hello, {students[student]['first_name']} {students[student]['last_name']}! You have accomplished our {course} course!")
                    students[student]['notified'] = True
                    student_notified = True
            if student_notified:
                notified += 1
    print(f"Total {notified} students have been notified.")


def course_details(course_name):
    course_name_tolerant = ""
    for c in course_points:
        if course_name.lower() == c.lower():
            course_name_tolerant = c
            break

    if course_name_tolerant == "":
        print("Unknown course.")
        return

    print(f"{course_name}")
    print("id     points completed")
    students_in_course = [(student_id, student['points'][course_name_tolerant]) for student_id, student in students.items() if
                          student['points'][course_name_tolerant] > 0]
    students_in_course.sort(key=lambda x: (-x[1], x[0]))

    for student_id, points in students_in_course:
        completion = (points / course_points[course_name_tolerant]) * 100
        print(f"{student_id} {points} {round(completion, 1)}%")


def main():
    print("Learning Progress Tracker")
    while True:
        command = input().strip().lower()
        if command == "":
            print("No input")
            continue
        elif command == 'add students':
            add_students()
        elif command == 'list':
            list_students()
        elif command == 'add points':
            add_points()
        elif command == 'find':
            find_student()
        elif command == 'notify':
            notify_students()
        elif command == 'statistics':
            calculate_statistics()
            while True:
                course_name = input().strip()
                if course_name == 'back':
                    break
                course_details(course_name)
        elif command == 'back':
            print("Enter 'exit' to exit the program")
        elif command == 'exit':
            print("Bye!")
            break
        else:
            print("Unknown command!")


if __name__ == "__main__":
    main()
