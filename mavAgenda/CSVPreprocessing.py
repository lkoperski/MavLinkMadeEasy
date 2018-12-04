import os
from mavAgenda.settings import BASE_DIR
import csv
import re
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mavAgenda.settings")
django.setup()

from landing.models import *

# hard-coded file paths
course_path = '\\landing\\degreeData\\Class List.csv'
credits_path = '\\landing\\degreeData\\Course Credits.csv'
reqs_path = '\\landing\\degreeData\\Course Requirements.csv'

'''
dictionary of buildings to campuses
'''

buildings_to_campuses = {
    'HPER': 'N',
    'HPERTBA': 'N',
    'ALLWINE': 'N',
    'CPACS': 'N',
    'ARTSCI': 'N',
    'ROSKNS': 'N',
    'ROSKNSTBA': 'N',
    'DURHAM': 'N',
    'KAYSER': 'N',
    'FINEART': 'N',
    'SCLPTRE': 'N',
    'CERAMCS': 'N',
    'STRAUSS': 'N',
    'FLDHOUS': 'N',
    'STRAUSSRH': 'N',
    'STRAUSSTBA': 'N',
    'LIBRARY': 'N',
    'HK': 'N',
    'MAMMEL': 'S',
    'PKIEWIT': 'S',
    'PKIEWITTBA': 'S',
    'MAMMELTBA': 'S',
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
    'None': 'R'
}

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
remote = Campus(campus_name='R')
remote.save()

# dictionary of semester data to cumulative semester data
semesters = {
    'A': {
        'F': 'A',
        'S': 'A',
        'M': 'A',
    },
    'S': {
        'F': 'Y',
        'S': 'S',
        'M': 'P',
    },
    'F': {
        'F': 'F',
        'S': 'Y',
        'M': 'H',
    },
    'M': {
        'F': 'H',
        'S': 'P',
        'M': 'M',
    },
    'Y': {
        'F': 'Y',
        'S': 'Y',
        'M': 'A',
    },
    'P': {
        'F': 'A',
        'S': 'P',
        'M': 'P',
    },
    'H': {
        'F': 'H',
        'S': 'A',
        'M': 'H',
    },
}

# dictionary to map courses to their unique CourseID listed in the Class List CSV doc
# to be generated at runtime in read_course_csv()
course_id_to_course = {}

'''
@read_csv calls each CSV reader method to read in CSVs in this order:
    Class List for Capstone v2.csv
    Course Credits.csv
    Course Requirements.csv
'''


def read_csvs():
    read_course_csv()
    read_credit_csv()
    read_reqs_csv()


'''
@read_course_csv reads the course data from the Class List CSV, 
        generates Building, Course, and Offering objects 
'''


def read_course_csv():
    with open(BASE_DIR + course_path) as f:
        reader = csv.reader(f)
        semester = 'A'

        next(f)
        for row in reader:
            # parse semester code (i.e. 1181 -> 1 at end indicates spring)
            if row[1][3] == '1':
                semester = 'S'
            elif row[1][3] == '5':
                semester = 'M'
            elif row[1][3] == '8':
                semester = 'F'

            # check if course already exists
            course = Course.objects.filter(course_subject=row[4], course_num=row[5])
            # if course does not exist, generate it
            if not course:
                c, created = Course.objects.get_or_create(
                    course_name=row[6],
                    course_subject=row[4],
                    course_num=row[5],
                    course_semester=semester,
                    course_credits=3,
                    course_special='None',
                    course_comment='',
                )

                course_id_to_course[row[0].lstrip('0')] = {'subject': row[4], 'num': row[5]}

            # else, get Course object from QueryList course and change the semester info if needed
            else:
                # change semester information if there is more than one semester offered

                if semester != course[0].course_semester:
                    # determine semester status
                    # course[0].course_semester = semesters[course[0].course_semester][semester]
                    sem = semesters[course[0].course_semester][semester]
                    Course.objects.filter(course_subject=row[4], course_num=row[5]).update(course_semester=sem)
                    c = course[0]

            # then, generate an offering object for each row
            # secondly we check if there exists a building object that matches this row
            # parse Facility ID for building, room #, and campus data
            building = re.split('(\d+)', row[7])[0]

            if building == '':
                building = 'None'
                roomNumber = 'None'
            elif building != row[7]:
                roomNumber = re.split('(\d+)', row[7])[1]
            else:
                roomNumber = 'None'

            # check for location's existence in table
            campus = Campus.objects.filter(campus_name=buildings_to_campuses[building])

            location = Building.objects.filter(building_name=building, building_roomNumber=roomNumber,
                                               building_campus=campus[0])

            # if not, generate a new row
            if not location:
                l = Building(building_name=building, building_roomNumber=roomNumber)
                l.save()
                l.building_campus.set(campus)
                l.save()
            else:
                l = location[0]

            # check if there exists an instructor object
            # (to be implemented dynamically later when we have that data)

            instructor = Instructor.objects.filter(instructor_firstName='John', instructor_lastName='Smith')
            if not instructor:
                i = Instructor(instructor_firstName='John', instructor_lastName='Smith')
            else:
                i = instructor[0]

            # generate offering for each row
            offering = Offering(
                offering_course=c,  # double-check this logic
                offering_time=row[8],
                offering_location=l,
                offering_sectionNum=row[3],
                offering_instructor=i,
            )
            offering.save()

            # determine set of Weekdays offering if offered for
            if row[10] == 'Y':
                offering.offering_days.add(monday)
            if row[11] == 'Y':
                offering.offering_days.add(tuesday)
            if row[12] == 'Y':
                offering.offering_days.add(wednesday)
            if row[13] == 'Y':
                offering.offering_days.add(thursday)
            if row[14] == 'Y':
                offering.offering_days.add(friday)
            if row[15] == 'Y':
                offering.offering_days.add(saturday)
            if row[16] == 'Y':
                offering.offering_days.add(sunday)

        f.close()


'''
@read_credit_csv reads the course data from the Course Credit CSV,
        updates credit information for each course  
'''


def read_credit_csv():
    with open(BASE_DIR + credits_path) as f:
        reader = csv.reader(f)
        next(f)
        for row in reader:
            Course.objects.filter(course_subject=row[3], course_num=row[4]).update(course_credits=int(float(row[0])))
        f.close()


'''
@read_reqs_csv
'''


def read_reqs_csv():
    with open(BASE_DIR + reqs_path) as f:
        #print(course_id_to_course)
        reader = csv.reader(f)
        next(f)

        for row in reader:
            if row[5] == 'CRSE':
                if row[0].lstrip('0') in course_id_to_course and row[17].lstrip('0') in course_id_to_course:
                    subject = course_id_to_course[row[0].lstrip('0')]['subject']
                    num = course_id_to_course[row[0].lstrip('0')]['num']
                    course = Course.objects.filter(course_subject=subject, course_num=num)

                    if row[26] == 'OR':
                        # check if prereq object already exists for prereq course
                        prec = PrereqCourse.objects.filter(prereqcourse_prereqs=prereq.pk)
                        if not prec:
                            prereq = Prereq(
                                prereq_type=row[8][0],
                            )
                            prereq.save()
                            prereq.prereq_course.set(course)
                            prereq.save()

                        subject = course_id_to_course[row[17].lstrip('0')]['subject']
                        num = course_id_to_course[row[17].lstrip('0')]['num']
                        p = Course.objects.filter(course_subject=subject, course_num=num)

                        # generate the new prereqcourse
                        prereqcourse = PrereqCourse()
                        prereqcourse.save()
                        prereqcourse.prereqcourse_prereqs.add(prereq)
                        prereqcourse.prereqcourse_course.add(p[0])
                        prereqcourse.save()

                    else:
                        if row[17].lstrip('0') in course_id_to_course:
                            prereq = Prereq(
                                prereq_type=row[8][0],
                            )
                            prereq.save()
                            prereq.prereq_course.set(course)
                            prereq.save()

                            subject = course_id_to_course[row[17].lstrip('0')]['subject']
                            num = course_id_to_course[row[17].lstrip('0')]['num']
                            p = Course.objects.filter(course_subject=subject, course_num=num)

                            prereqcourse = PrereqCourse()
                            prereqcourse.save()
                            prereqcourse.prereqcourse_prereqs.add(prereq)
                            prereqcourse.prereqcourse_course.add(p[0])
                            prereqcourse.save()

        f.close()
