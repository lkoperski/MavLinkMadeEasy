from .models import *
import csv
import re

course_path = "C:\\Users\\ekbuc\\Desktop\\Class List for Capstone v2.csv"
credits_path = "C:\\Users\\ekbuc\\Desktop\\Course Credits.csv"
reqs_path = "C:\\Users\\ekbuc\\Desktop\\Course Requirements.csv"


def buildingToCampus(b):
    mapping = {
        'HPER': 'N',
        'ALLWINE': 'N',
        'CPACS': 'N',
        'ARTSCI': 'N',
        'ROSKNS': 'N',
        'DURHAM': 'N',
        'KAYSER': 'N',
        'FINEART': 'N',
        'SCLPTRE': 'N',
        'CERAMCS': 'N',
        'STRAUSS': 'N',
        'LIBRARY': 'N',
        'HK': 'N',
        'MAMMEL': 'S',
        'PKIEWIT': 'S',
        'OCEXAM': 'S',
        'OCMTG': 'S',
        'MAVVIL': 'S',
        'CENTER': 'B',
        'STC': 'B',
        'OFFCAMPUS': 'R',
        'TOTLONLINE': 'R',
        'PARTONLINE': 'R',
        'TBA': 'R',
        'UNMCTBA': 'R',
        'OFFUTTTBA': 'R',
        'HOLLANDICE': 'R',
        'MILSTHTBA': 'R',
        'JOSLYNTBA': 'R',
        'BELWESTTBA': 'R',
    }


'''
@readCSV reads in csv data into model objects
'''


def readCSVs():
    with open(course_path) as f:
        reader = csv.reader(f)
        semester = 'A'

        placeholder_instructor = Instructor(instructor_firstName='John', instructor_lastName='Smith')
        placeholder_instructor.save()

        # days of the week objects
        monday = Weekday(weekday_name='M')
        monday.save()
        tuesday = Weekday(weekday_name='T')
        tuesday.save()
        wednesday = Weekday(weekday_name='W')
        wednesday.save()
        thursday = Weekday(weekday_name='R')
        thursday.save()
        friday = Weekday(weekday_name='F')
        friday.save()
        saturday = Weekday(weekday_name='S')
        saturday.save()
        sunday = Weekday(weekday_name='U')
        sunday.save()

        # campus objects
        north = Campus(campus_name='N')
        north.save()
        south = Campus(campus_name='S')
        south.save()
        centerStreet = Campus(campus_name='B')
        centerStreet.save()

        building = ''
        roomNumber = ''

        next(f)
        for row in reader:
            # parse semester code (i.e. 1181 -> 1 at end indicates spring)
            if row[1][3] == '1':
                semester = 'S'
            elif row[1][3] == '5':
                semester = 'M'
            elif row[1][3] == '8':
                semester = 'F'

            # parse Facility ID for building, room #, and campus data
            if row[7] == 'TOTLONLINE' or row[7] == 'PARTONLINE':
                building = row[7]
                roomNumber = 'None'

            else:
                building = re.split('(\d+)', row[7])[0]
                roomNumber = re.split('(\d+)', row[7])[1]

                campus = Campus.objects.filter(campus_name=buildingToCampus(building))
                print(building)
                print(roomNumber)
                print(campus)

            # check if course already exists
            course = Course.objects.filter(course_subject=row[4], course_num=row[5])
            # if course does not exist, generate it
            if not course:
                course, created = Course.objects.get_or_create(
                    course_name=row[6],
                    course_subject=row[4],
                    course_num=row[5],
                    course_semester=semester,
                    course_credits=3,
                    course_special='None',
                    course_comment='',
                )
                # print(course)
            # else, get Course object from QueryList course and change the semester info if needed
            else:
                for c in course:
                    # change semester information if there is more than one semester offered
                    print(semester)
                    print(c.course_semester)
                    if semester != c.course_semester:
                        # determine semester status
                        c.course_semester = semester
                        # print(c.course_semester)

            # then, generate an offering object for each row

            # first, check if there exists an instructor object
            # (to be implemented later when we have that data)
            # instructor = Instructor.objects.filter(first_name='placeholder', last_name='placeholder')
            # instructor = Instructor.objects.filter(instructor_firstName='John', instructor_lastName='Smith')

            # secondly we check if there exists a building object that matches this row
            campus = Campus.objects.filter()
            location = Building.objects.filter(building_name=building, building_roomNumber=roomNumber,
                                               building_campus='')

            # for i in instructor:
            offering, created = Offering.objects.get_or_create(
                offering_course=c.pk,
                offering_time=row[8],
                offering_location=row[7],
                offering_days=monday,
                offering_sectionNum=row[3],
                offering_instructor=placeholder_instructor,
            )
        f.close()

