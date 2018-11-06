from django.test import TestCase

from ..views import *
from ..models import *


class YourTestClass(TestCase):

    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(cself):
        # Clean up run after every test method.
        pass

    # def test_get_user_by_email(self):
    # d = Degree(degree="Bachelor's of Science", major="CS")
    # d.save()
    # u = User(email="sample@test.com", degree=d)
    # u.save()
    # foundUser = getUserByEmail(u.email)
    # self.assertTrue(u == foundUser)

    # def test_get_degree(self):
    # deg = Degree(degree="Bachelor's of Science", major="CS")
    # deg.save()
    # foundDegree = getDegree("Bachelor's of Science", "CS")
    # self.assertTrue(deg == foundDegree)

    # def test_get_completed_by_user(self):
    # d = Degree(degree="Bachelor's of Science", major="CS")
    # d.save()
    # u = User(email="completedbyuser@test.com", degree=d)
    # u.save()
    # uID = u.pk
    # completed = Complete(user=u)
    # completed.save()
    # cc = Course(name="Java1", num="CIST1400", semester="A", credits=3, special="N")
    # cc.save()
    # completed.complete.add(cc)
    # completed.save()
    # self.assertTrue([cc] == getCompletedByUser(uID))

    # def test_check_prereqs_met(self):
    # classesTaken = []
    # prereqs = []
    # collegeAl = Course(id=1, name="College Algebra", num="MATH 1220", semester='All', credits=3)
    # collegeAl.save()
    # coAl = Prereq(id=3, prereq=collegeAl, req_type="Prerequisite")
    # coAl.save()
    # precalcAlgebra = Course(id=2, name="Pre-Calculus Algebra", num="MATH 1320", semester='All', credits=3)
    # precalcAlgebra.save()
    # precalcAlgebra.prereqs.add(coAl)
    # precalcAlgebra.save()
    # pr = Course.objects.get(name="Pre-Calculus Algebra").prereqs.all()
    # for p in pr:
    # prereqs.append(p)
    # c1 = Course.objects.get(name="College Algebra")
    # classesTaken.append(c1)
    # self.assertTrue(checkPrereqsMet(pr, classesTaken, []))

    # def test_check_prereqs_met_with_thisor(self):
    # classesTaken = []
    # prereqs = []
    # collegeAl = Course(id=1, name="College Algebra", num="MATH 1220", semester='All', credits=3)
    # collegeAl.save()
    # test = Course(id=2, name="Testing", num="TEST 1234", semester='All', credits=3)
    # test.save()
    # pr = Prereq(id=3, prereq=collegeAl, this_or=test, req_type="Prerequisite")
    # pr.save()
    # precalcAlgebra = Course(id=2, name="Pre-Calculus Algebra", num="MATH 1320", semester='All', credits=3)
    # precalcAlgebra.save()
    # precalcAlgebra.prereqs.add(pr)
    # precalcAlgebra.save()
    # pr = Course.objects.get(name="Pre-Calculus Algebra").prereqs.all()
    # for p in pr:
    # prereqs.append(p)
    # classesTaken.append(test)
    # self.assertTrue(checkPrereqsMet(pr, classesTaken, []))

    # def test_check_offered_semester(self):
    # collegeAl = Course(id=1, name="College Algebra", num="MATH 1220", semester='Fall', credits=3)
    # collegeAl.save()
    # print("CollegeAl semester is %s" % collegeAl.semester)
    # currentMonth = datetime.now().month
    # ssfSemester = getSemesterByMonthYear(currentMonth)
    # print("ssfSemester is %s" % ssfSemester)
    # self.assertTrue(collegeAl.semester == ssfSemester)

    # def test_email_found(self):
    # d = Degree(degree="Bachelor's of Science", major="CS")
    # d.save()
    # u = User(email="email@test.com", degree=d)
    # u.save()
    # foundEmail = emailFound(u.email)
    # self.assertTrue(foundEmail)

    # def test_generate_major_dd(self):
    # degreeOne = Degree(degree="Bachelor of Science", major="Computer Science")
    # degreeOne.save()
    # degrees = generateMajorDD()
    # self.assertTrue([degreeOne.major] == degrees)

    # def test_save_classes_to_user(self):
    # d = Degree(degree="Bachelor's of Science", major="CS")
    # d.save()
    # u = User(email="sample@test.com", degree=d)
    # u.save()
    # collegeAl = Course(id=1, name="College Algebra", num="MATH 1220", semester='Fall', credits=3)
    # collegeAl.save()
    # classesChecked = [collegeAl.num]
    # saveClassesToUser(classesChecked, u.pk)
    # self.assertTrue(collegeAl.num == Complete.objects.get(user=u).complete.get(name="College Algebra").num)

    # def test_remove_courses_taken(self):
    # d = Degree(degree="Bachelor's of Science", major="CS")
    # d.save()
    # u = User(email="sample@test.com", degree=d)
    # u.save()
    # collegeAl = Course(id=1, name="College Algebra", num="MATH 1220", semester='Fall', credits=3)
    # collegeAl.save()
    # collegeAl2 = Course(id=2, name="College Algebra 2", num="MATH 1620", semester='Fall', credits=3)
    # collegeAl2.save()
    # classesReq = ["College Algebra", "College Algebra 2"]
    # classesTaken = [collegeAl.name]
    # result = removeCoursesTaken(classesReq, classesTaken)
    # self.assertTrue(result == [collegeAl2.name])

    # def test_remove_user_completed_entries(self):
    # d = Degree(degree="Bachelor's of Science", major="CS")
    # d.save()
    # u = User(email="sample@test.com", degree=d)
    # u.save()
    # collegeAl = Course(id=1, name="College Algebra", num="MATH 1220", semester='Fall', credits=3)
    # collegeAl.save()
    # collegeAl2 = Course(id=2, name="College Algebra 2", num="MATH 1620", semester='Fall', credits=3)
    # collegeAl2.save()
    # uID = u.pk
    # completed = Complete(user=u)
    # completed.save()
    # completed.complete.add(collegeAl)
    # completed.save()
    # removeUserCompletedEnteries(uID)
    # passed = False
    # try:
    # Complete.objects.get(user=u).complete.all()
    # except:
    # passed = True
    # self.assertTrue(passed)

    # def test_generate_checkbox_entities(self):
    # collegeAl = Course(id=1, name="College Algebra", num="MATH 1220", semester='Fall', credits=3)
    # collegeAl.save()
    # reqs = Req(id=1, name="test", credits=3, req_type="Electives")
    # reqs.save()
    # reqs.course.add(collegeAl)
    # reqs.save()
    # d = Degree(degree="Bachelor's of Science", major="CS")
    # d.save()
    # d.req.add(reqs)
    # d.save()
    # u = User(email="sample@test.com", degree=d)
    # u.save()
    # result = generateCheckBoxEntities(u.id)
    # self.assertTrue(len(result) == 1)

    # def test_get_courses_for_user(self):
    # collegeAl = Course(id=1, name="College Algebra", num="MATH 1220", semester='Fall', credits=3)
    # collegeAl.save()
    # reqs = Req(id=1, name="test", credits=3, req_type="Electives")
    # reqs.save()
    # reqs.course.add(collegeAl)
    # reqs.save()
    # d = Degree(degree="Bachelor's of Science", major="CS")
    # d.save()
    # d.req.add(reqs)
    # d.save()
    # u = User(email="sample@test.com", degree=d)
    # u.save()
    # courses = getCoursesForUser(u.id)
    # self.assertTrue(courses[0].name == collegeAl.name)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11starting here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Desktop\MavLinkMadeEasy-lauren-m2\MavLinkMadeEasy-lauren-m2\mavAgenda>python manage.py test landing

    # '''
    # @getUserByEmail searches the User table to find the User object with a corresponding email
    # @param e: the email being searched for
    # '''

    def test_getUserByEmail(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
        testCase = getUserByEmail("cdog@test")
        self.assertTrue(testCase == testUser)

    # '''
    # @getDegree searches the Degree table to find the Degree object with corresponding degree and major
    # @param d: degree attribute of Degree being searched for
    # @param m: major attribute of Degree being searched for
    # '''
    #    def getDegree(diploma, type, track):
    def test_getDegree(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type='Major', degree_track='Computer Science')
        newDegree.save()
        testDegree = getDegree('Master of Science', 'Major', 'Computer Science')
        self.assertTrue(newDegree == testDegree)

    # '''
    # @getCompletedByUser provides a list of Course (objects) the user has taken
    # @param uID: the primary key corresponding to the active user
    # '''
    #    def getCompletedByUser(uID):
    # def test_getCompletedByUser(self):
    # email = "cdog@test"
    # p = "GameOfThrones"
    # testUser = User(username = email, password = p)
    # testUser.save()
    #   recreate            classesChecked = request.POST.getlist('chexmix')
    #   recreate            saveClassesToUser(classesChecked, pk)
    #   call getCompletedByUser
    #   self.assertTrue

    # cu = User.objects.get(pk=uID)
    # completedCourses = []
    # for cc in Complete.objects.get(user=cu).complete.all():
    # completedCourses.append(cc)
    # return completedCourses

    # '''
    # @getCoursesForUser provides a list of Course (objects) the user must complete for their respective Degree
    # @param uID: the primary key corresponding to the active user
    # '''
    #   def getCoursesForUser(uID):
    # requiredCourses = []
    # reqs = Degree.objects.get(user=uID).req.all()
    # for r in reqs:
    # catalog = r.course.all()
    # for g in catalog:
    # requiredCourses.append(g)
    # prereqs = Course.objects.get(id=g.id).prereqs.all()
    # for pr in prereqs:
    # additionalCourse = Course.objects.get(id=pr.prereq.id)
    # if additionalCourse not in requiredCourses:
    # requiredCourses.append(additionalCourse)
    # return requiredCourses

    # '''
    # @removeCoursesTaken provides a list of Course (objects) the user must still take (required, but not completed classes)
    # @param requiredClasses: a list of Course (objects) required for the User's Degree
    # @param classesTaken: a list of Course (objects) that the User has already completed
    # '''
    #    def removeCoursesTaken( requiredClasses, classesTaken ):
    def test_removeCoursesTaken(self):
        needed = []
        taken = []
        difference = []
        testCase = []
        needed.append('Compilers')
        needed.append('Operating Systems')
        needed.append('Capstone')
        taken.append('Operating Systems')
        difference.append('Compilers')
        difference.append('Capstone')
        testCase = removeCoursesTaken(needed, taken)
        self.assertTrue(difference == testCase)

    # '''
    # @checkPrereqsMet determines if the User has met all Prereqs for a particular Course
    # @param prereqs: a list of Course (objects) corresponding to Prereqs for a given Course
    # @param classesTaken: a list of Course (objects) that the User has already completed
    # @parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
    # '''
    #    def checkPrereqsMet(preqreqs, classesTaken, currentSemester):
    # def test_checkPrereqsMet(self):
    # newDegree = Degree(degree_diploma = 'Master of Science', degree_type = 'Major', degree_track = 'Computer Science')
    # newDegree.save()

    # newRequirement = Requirement(req_name = "Operating Systems", req_credits = 3)
    # newRequirement.save()
    # newRequirement.req_degrees.add(newDegree)
    # newRequirement.save()

    # newCourse = Course(course_name = "Compilers", course_num = "4700", course_semester = "All", course_credits = 3, course_special = "No", course_comment = "", course_requirements = newRequirement)
    # newCourse.save()

    # newPrereq = Prereq(prereq_type = "Corequisite")
    # newPrereq.save()
    # newPrereq.prereq_courses.add(newCourse)
    # newPrereq.save()

    # preReqs = newCourse.prereqs.all()
    # print(preReqs)

    # '''
    # @checkOfferedSemester determines if a given Course if offered during the current semester
    # @param course: the Course under test
    # @param ssf: the Spring, Summer, Fall, offering attribute of the Course
    # '''
    #       def checkOfferedSemester(course, ssf):
    # offered = False
    # if course.semester == ssf or course.semester == 'All':
    # offered = True
    # return offered
    # def test_checkOfferedSemester(self):
    # create a course object

    # '''
    # @checkCourseValid determines if a given Course can be taken during a given semester
    # @param course: the Course under test
    # @param classesTaken: a list of Course (objects) that the User has already completed
    # @parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
    # @param ssf: the Spring, Summer, Fall, offering attribute of the Course
    # '''
    #    def checkCourseValid(course, classesTaken, semesterCourses, ssf): #checkCourseValid( nc, classesTaken, semesterCourses, ssfSemester )

    # '''
    # @getSemesterByMonthYear determines semester (Spring, Summer, Fall) according to current month
    # @param m: current month
    # '''

    def test_get_semester_by_month_year(self):
        Spring = getSemesterByMonthYear(4)
        Summer = getSemesterByMonthYear(7)
        Fall = getSemesterByMonthYear(9)
        self.assertTrue(Spring == "Spring")
        self.assertTrue(Summer == "Summer")
        self.assertTrue(Fall == "Fall")

    # '''
    # @generateNewSemester creates a new logical semester
    # @param semester: previous semester list
    # '''
    #    def generateNewSemester(semester):
    def test_generate_new_semester(self):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        testSemester = ["Spring", 2019, []]
        ssfSemester = getSemesterByMonthYear(currentMonth)
        semester = [ssfSemester, currentYear, []]
        currentSemester = generateNewSemester(semester)
        # print("current semester is %s" % currentSemester)
        self.assertTrue(currentSemester == testSemester)

    # '''
    # @isFull determines if a semester has hit the maximum number of credits allowable
    # @param courseList: list of Course (objects) the user is scheduled to take during current semester
    # '''
    #    def isFull(courseList):
    def test_is_full(self):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        ssfSemester = getSemesterByMonthYear(currentMonth)
        semester = [ssfSemester, currentYear, []]
        currentSemester = generateNewSemester(semester)
        false = isFull(currentSemester[2])
        # still need to do the true case

    # '''
    # @createSchedule generates semester-by-semester schedule for User's needed Courses according to Degree
    # @param uID: primary key associated with active user
    # '''
    #    def createSchedule(uID):

    # '''
    # @generateCheckBoxEntities creates a list of tuples of requirements, course names and numbers for the selectcourses page
    # @param uID: primary key corresponding to the active user
    # '''
    #    def generateCheckBoxEntities(uID):

    # '''
    # @generateMajorDD creates a list of possible majors for use on the createuser page
    # '''
    #       def generateMajorDD():
    # allDegrees = Degree.objects.all()
    # majors = []
    # for d in allDegrees:
    # if d.degree_type == "MAJ" and d.degree_track not in majors:
    # majors.append(d.degree_track)
    # return majors

    def test_generateMajorDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="MAJ", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateMajorDD()
        self.assertTrue(testList == testCase)

    #       def generateMinorDD():
    # allDegrees = Degree.objects.all()
    # minors = []
    # for d in allDegrees:
    # if d.degree_type == "MIN" and d.degree_track not in minors:
    # minors.append(d.degree_track)
    # return minors
    def test_generateMinorDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="MIN", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateMinorDD()
        self.assertTrue(testList == testCase)

    #    def generateConcentrationsDD():
    def test_generateConcentrationsDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="CON", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateConcentrationsDD()
        self.assertTrue(testList == testCase)

    #    def generateDiplomaDD():
    def test_generateDiplomaDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="CON", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_diploma)
        testCase = generateDiplomaDD()
        self.assertTrue(testList == testCase)

    # '''
    # @emailFound provides feedback if the email is already in the User database table
    # @param email: email under test
    # '''
    #    def emailFound(email):
    def test_emailFound(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
        flag = True
        testCase = emailFound("cdog@test")
        self.assertTrue(flag == testCase)
# '''
# @saveClassesToUser updates database with a list of the user has taken
# @param classesChecked: list of courses the user specified as having taken
# @param uID: pk of the associated active user
# '''
#   def saveClassesToUser(classesChecked, uID):
# u = User.objects.get(pk=uID)
# if u in Complete.objects.all():
# completed = Complete.objects.get(user_id=u)
# else:
# completed = Complete(user=u)
# completed.save()
# for cc in classesChecked:
# c = Course.objects.get(num=cc)
# completed.complete.add(c)
# completed.save()
# def test_saveClassesToUser(self):
# email = "cdog@test"
# p = "secure"
# testUser = User(username = email, password = p)
# testUser.save()


# '''
# @removeUserCompletedEntries updates database to remove courses completed from a particular user
# @param uID: pk of the associated active user
# '''
#    def removeUserCompletedEnteries(uID):


########################################################################################################################
########################################################################################################################

# '''
# @login send a request to render the login.html page
# @param request: generates the response
# '''
#   def login(request):


# '''
# @createuser send a request to render the createuser.html page
# @param request: generates the response
# '''
#   def createuser(request):

# @selectcourses send a request to render the selectcourses.html page
# @param request: generates the response
# @param pk: primary key corresponding to active user
# '''
#   def selectcourses(request, pk):


# '''
# @schedule send a request to render the schedule.html page
# @param request: generates the response
# @param pk: primary key corresponding to active user
# '''
#   def schedule(request, pk):
