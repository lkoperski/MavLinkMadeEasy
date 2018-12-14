from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from ..views import *
from ..models import *


class YourTestClass(TestCase):

    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(cself):
        # Clean up run after every test method.
        pass
		
		
		
    '''
    @getUserByEmail searches the User table to find the User object with a corresponding email
    @param e: the email being searched for
    '''
    def test_getUserByEmail(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
        testCase = getUserByEmail("cdog@test")
        self.assertTrue(testCase == testUser)
		
		
		
    '''
    @getSemesterByMonthYear determines semester (Spring, Summer, Fall) according to current month
    @param m: current month
    '''
    def test_get_semester_by_month(self):
        Spring = getSemesterByMonth(4)
        Summer = getSemesterByMonth(7)
        Fall = getSemesterByMonth(9)
        self.assertTrue(Spring == "Spring")
        self.assertTrue(Summer == "Summer")
        self.assertTrue(Fall == "Fall")
		
		
		
    '''
    @getDegree searches the Degree table to find the Degree object with corresponding degree and major
    @param d: degree attribute of Degree being searched for
    @param m: major attribute of Degree being searched for
    '''
    def test_getDegree(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type='Major', degree_track='Computer Science')
        newDegree.save()
        testDegree = getDegree('Master of Science', 'Major', 'Computer Science')
        self.assertTrue(newDegree == testDegree)

    

# 	'''
# 	@getCompletedByUser provides a list of Course (objects) the user has taken
# 	@param uID: the primary key corresponding to the active user
# 	'''
#   def getCompletedByUser(uID):
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

	
	
# 	'''
# 	@getCoursesForUser provides a list of Course (objects) the user must complete for their respective Degree
# 	@param uID: the primary key corresponding to the active user
# 	'''
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
	
	
		
#def translateCourseInfoToCourse(reqClasses):
#    '''
#    @translateCourseInfoToCourse translate the list of course information (from getCoursesForUser) into a list of Course objects
#    @param reqClasses: a list of course information pieces
#    '''
#    courses = []
#    for rc in reqClasses:
#        courses.append(Course.objects.get(pk=rc[4]))
#    return courses
	
	
	
    '''
    @removeCoursesTaken provides a list of Course (objects) the user must still take (required, but not completed classes)
    @param requiredClasses: a list of Course (objects) required for the User's Degree
    @param classesTaken: a list of Course (objects) that the User has already completed
    '''
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

		
		
# 	'''
# 	@checkPrereqsMet determines if the User has met all Prereqs for a particular Course
# 	@param prereqs: a list of Course (objects) corresponding to Prereqs for a given Course
# 	@param classesTaken: a list of Course (objects) that the User has already completed
# 	@parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
# 	'''
#   def checkPrereqsMet(preqreqs, classesTaken, currentSemester):
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

	
	
    '''
    @checkOfferedSemester determines if a given Course if offered during the current semester
    @param course: the Course under test
    @param ssf: the Spring, Summer, Fall, offering attribute of the Course
    '''
    def test_checkOfferedSemester(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testDegree = Degree(degree_diploma='Bachelor of Science', degree_type = "MAJ", degree_track = 'Computer Science')
        testDegree.save()
        testDegree.degree_users.add(testUser)
        testDegree.save()
		
        testReq = Requirement(req_name='Java', req_credits=3)
        testReq.save()
        testReq.req_degrees.add(testDegree)
        testReq.save()
		
        java2 = Course(course_name='Java2',course_subject='CSCI', course_num='1200', course_semester='F', course_credits=3, course_special='None', course_comment='',)
        javaEE = Course(course_name='JavaEE',course_subject='CSCI', course_num='1550', course_semester='F', course_credits=3, course_special='None', course_comment='',)

        java2.save()
        javaEE.save()
		
        java2.course_enforced_for.add(testReq)
        java2.save()
		
        testCaseKnown = True
        testCaseToProve = checkOfferedSemester(java2, 'Fall')
        print(testCaseToProve)
        print(java2.course_semester)
        self.assertTrue(testCaseKnown == testCaseToProve)
		

	

#def courseValid(course, classesTaken, semesterCourses, ssf):
#    '''
#    @checkCourseValid determines if a given Course can be taken during a given semester
#    @param course: the Course under test
#    @param classesTaken: a list of Course (objects) that the User has already completed
#    @parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
#    @param ssf: the Spring, Summer, Fall, offering attribute of the Course
#    '''
#    valid = False
#    prereqs = getCoursePrereqs(course)
#    prereqsMet = checkPrereqsMet(prereqs, classesTaken, semesterCourses)
#    offered = checkOfferedSemester(course, ssf)
#    if prereqsMet and offered:
#        valid = True
#    return valid

	
	
    '''
    @test_getNextSemseterTitle determines if the expected next semester (Spring, Summer, Fall) is correct
    @param ssf: the title of the current semester
    '''
    def test_getNextSemesterTitle(self):
        knownSemester = 'Fall'
        knownNextSemester = 'Spring'
        testCaseNextSemester = getNextSemesterTitle('Fall')
        self.assertTrue(knownNextSemester == testCaseNextSemester)


		
    '''
    @test_generateNewSemester creates a new logical semester and test it against the expected results of generateNewSemester
    @param semester: previous semester list
    '''
    def test_generate_new_semester(self):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        testSemester = ["Spring", 2019, []]
        ssfSemester = getSemesterByMonth(currentMonth)
        semester = [ssfSemester, currentYear, []]
        currentSemester = generateNewSemester(semester)
        # print("current semester is %s" % currentSemester)
        self.assertTrue(currentSemester == testSemester)

		
		
    '''
    @test_setupReqTracker creates a correct list and test that list against the results of setupReqTracker
    @param user pk: the private key of a user
    '''	
    def test_setupReqTracker(self):
        expectedList = []
        expectedList.append([1, 'Java', 3, 0])		
		
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testDegree = Degree(degree_diploma='Bachelor of Science', degree_type = "MAJ", degree_track = 'Computer Science')
        testDegree.save()
        testDegree.degree_users.add(testUser)
        testDegree.save()
		
        testReq = Requirement(req_name='Java', req_credits=3)
        testReq.save()
        testReq.req_degrees.add(testDegree)
        testReq.save()

        results = setupReqTracker(testUser.id)
        self.assertTrue(expectedList == results)
        
		
	
    '''
    @getEnforcedCourses gets a list of courses that are enforced by requirements for the user's degree
    @param uID: user ID of the user requesting the enforced courses
    @param reqTracker: a list of requirements the user must complete to receive their degree
    '''
    def test_getEnforcedCourses(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testDegree = Degree(degree_diploma='Bachelor of Science', degree_type = "MAJ", degree_track = 'Computer Science')
        testDegree.save()
        testDegree.degree_users.add(testUser)
        testDegree.save()
		
        testReq = Requirement(req_name='Java', req_credits=3)
        testReq.save()
        testReq.req_degrees.add(testDegree)
        testReq.save()
		
        java2 = Course(course_name='Java2',course_subject='CSCI', course_num='1200', course_semester='F', course_credits=3, course_special='None', course_comment='',)
        java2.save()
		
        java2.course_enforced_for.add(testReq)
        java2.save()
		
        results = setupReqTracker(testUser.id)
        testCase = getEnforcedCourses(results)
        #print(testCase[0].course_name)
        self.assertTrue(testCase[0].course_name == java2.course_name)

		
		
    '''
    @getElectiveCourses gets a list of courses that are elective for the user's degree
    @param reqTracker: a list of requirements the user must complete to receive their degree
    '''
    def test_getElectiveCourses(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testDegree = Degree(degree_diploma='Bachelor of Science', degree_type = "MAJ", degree_track = 'Computer Science')
        testDegree.save()
        testDegree.degree_users.add(testUser)
        testDegree.save()
		
        testReq = Requirement(req_name='Java', req_credits=3)
        testReq.save()
        testReq.req_degrees.add(testDegree)
        testReq.save()
		
        java2 = Course(course_name='Java2',course_subject='CSCI', course_num='1200', course_semester='F', course_credits=3, course_special='None', course_comment='',)
        java2.save()
		
        java2.course_counts_toward.add(testReq)
        java2.save()
		
        results = setupReqTracker(testUser.id)
        testCase = getElectiveCourses(results)
        #print(testCase[0].course_name)
        self.assertTrue(testCase[0].course_name == java2.course_name)

		
		
    '''
    @setupSchedule creates a template for generating an schedule
    @param uID: user ID of the user requesting the schedule
    '''
    def test_setupSchedule(self):
        expectedList = []
        expectedList.append(['Spring', 2019, []])
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testUserPref = UserPreferences( pref_minCredits = 3, pref_maxCredits = 15, pref_summer = True, pref_summerMinCredits = 3, pref_summerMaxCredits = 9, pref_nextSSF = 'Spring', pref_nextYear = 2019, pref_nextSemMinCredit = 6, pref_nextSemMaxCredit = 12, pref_user = testUser)
        testUserPref.save()
        testSchedule = setupSchedule(testUser.id)
        self.assertTrue(expectedList == testSchedule)



    '''
    @countCourseTowardReqs credits the user for courses fulfilling their necessary requirements
    @param course: the course to be counted for credit
    @param reqTracker: the array of requirements needed for the user's desired degree
    '''
    def test_countCourseTowardReqs(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testDegree = Degree(degree_diploma='Bachelor of Science', degree_type = "MAJ", degree_track = 'Computer Science')
        testDegree.save()
        testDegree.degree_users.add(testUser)
        testDegree.save()
		
        testReq = Requirement(req_name='Java', req_credits=3)
        testReq.save()
        testReq.req_degrees.add(testDegree)
        testReq.save()
		
        java2 = Course(course_name='Java2',course_subject='CSCI', course_num='1200', course_semester='F', course_credits=3, course_special='None', course_comment='',)
        java2.save()
		
        java2.course_counts_toward.add(testReq)
        java2.save()

        reqTracker = setupReqTracker(testUser.id)
		
        countCourseTowardReqs(java2, reqTracker)
        result = reqTracker[0]
        self.assertTrue(result[3] == 3)
		


#def updateReqTrackerForCompletedCourses(coursesCompleted, reqTracker):
#    '''
#    @updateReqTrackerForCompletedCourses provides credit to a user for completing a number of courses
#    @param course: the courses to be counted for credit toward their requirements
#    @param reqTracker: the array of requirements needed for the user's desired degree
#    '''
#    for c in coursesCompleted:
#        countCourseTowardReqs(c, reqTracker)


#def updateReqTrackerForCompletedCourses(coursesCompleted, reqTracker):
#    '''
#    @updateReqTrackerForCompletedCourses provides credit to a user for completing a number of courses
#    @param course: the courses to be counted for credit toward their requirements
#    @param reqTracker: the array of requirements needed for the user's desired degree
#    '''
#    for c in coursesCompleted:
#        countCourseTowardReqs(c, reqTracker)




#def checkReqsMet(reqTracker):
#    '''
#    @checkReqsMet returns True if all requirements for the user's desired degree have been met
#    @param reqTracker: the list of requirements needed for the user's desired degree
#    '''
#    reqsMet = True
#    for r in reqTracker:
#        if r[2] > r[3]:
#            reqsMet = False
#            break
#    return reqsMet
		
		
#def tallyNumberCreditsTaken(courses):
#    '''
#    @tallyNumberCreditsTaken returns the total number of credits scheduled for a semester
#    @param courses: the list of Course objects scheduled for the semester
#    '''
#    totalCredits = 0
#    for c in courses:
#        totalCredits+=c.course_credits
#    return totalCredits

#def prefNumCreditsMet(uID, ssf, numberCreditsTaken):
#    '''
#    @prefNumCreditsMet returns True if the number of credits scheduled for a semester is within the user's desired constraints
#    @param uID: the id of the user whose schedule is being processed
#    @param ssf: denotes the spring, summer, or fall semester
#    @numberCreditsTaken: the number of credits taken during the semester
#    '''
#    u = User.objects.get(pk=uID)
#    up = UserPreferences.objects.get(pref_user=u)
#    met = False
#    if ssf == "Summer":
#        prefMax = up.pref_summerMaxCredits
#        prefMin = up.pref_summerMinCredits
#    else:
#        prefMax = up.pref_maxCredits
#        prefMin = up.pref_minCredits
#    if numberCreditsTaken <= prefMax and numberCreditsTaken >= prefMin:
#        met = True
#    return met

#def combineEnforcedAndElectiveCourses(enforcedCourses, electiveCourses):
#    '''
#    @combineEnforcedAndElectiveCourses ensures there are no duplicates listed between the enforced and elective courses
#    @param enforcedCourses: a list of the course objects that are enforced
#    @param electiveCourses: a list of the courses objects that can be taken as electives
#    '''
#    potential = [enforcedCourses,[]]
#    for el in electiveCourses:
#        if el not in enforcedCourses:
#            potential[1].append(el)
#    # print("potential courses in combine....", potential)
#    return potential		
	
#def mandatePrereqsForEnforcedCourses(enfCourses):
#    '''
#    @mandatePrereqsForEnforcedCourses determine if there are classes needed as Prereqs for beginning enforced courses and if not accounted for, schedules them
#    @param enfCourses: a list of Course objects that a user is required to take according to their desired Degree Requirements
#    '''
#    for en in enfCourses:
#        prereqs = getCoursePrereqs(en)
#        if prereqs != []:
#            for pr in prereqs:
#                if pr[0][0] not in enfCourses: #TODO - note that this only tests for the first course in an OR and might not be super time-efficient for the student
#                    enfCourses.append(pr[0][0])
#    return enfCourses
	

	
    '''
    @getDegreeRegs returns a list of requirements for all degrees a user has selected
    @param degrees: a list of degrees associated with the user
    '''
    def test_getDegreeReqs(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testDegree = Degree(degree_diploma='Bachelor of Science', degree_type = "MAJ", degree_track = 'Computer Science')
        testDegree.save()
        testDegree.degree_users.add(testUser)
        testDegree.save()
		
        testReq = Requirement(req_name='Java', req_credits=3)
        testReq.save()
        testReq.req_degrees.add(testDegree)
        testReq.save()

        degrees = Degree.objects.filter(degree_users=testUser.id)
        testList = []
        testList.append(testReq)
		
        testCaseList = getDegreeReqs(degrees)
        self.assertTrue(testList == testCaseList)
		
		
	
#def sortCoursesBySubNum(courses):
#    '''
#    @sortCoursesBySubNum takes a list of course information and sorts them course information according to subject and number
#    @param courses: list of courses information pieces that need to be stored for the checkbox page
#    '''
#    numCourses = len(courses)
#    for c in range(numCourses):
#        for j in range(0,numCourses-c-1):
#            oneCourse = courses[j][5] + " " + courses[j][1] + " " + courses[j][2]
#            twoCourse = courses[j+1][5] + " " +courses[j+1][1] + " " + courses[j+1][2]
#            if oneCourse > twoCourse:
#                courses[j], courses[j+1] = courses[j+1], courses[j]
		
		
	
    '''
    @getReqCourses returns a list of courses for all requirements related to a degree a user has selected
    @param reqs: a list of requirements associated with the user's desired degree
    '''
    def test_getReqCourses(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testDegree = Degree(degree_diploma='Bachelor of Science', degree_type = "MAJ", degree_track = 'Computer Science')
        testDegree.save()
        testDegree.degree_users.add(testUser)
        testDegree.save()
		
        testReq = Requirement(req_name='Java', req_credits=3)
        testReq.save()
        testReq.req_degrees.add(testDegree)
        testReq.save()
		
        java2 = Course(course_name='Java2',course_subject='CSCI', course_num='1200', course_semester='F', course_credits=3, course_special='None', course_comment='',)
        javaEE = Course(course_name='JavaEE',course_subject='CSCI', course_num='1550', course_semester='F', course_credits=3, course_special='None', course_comment='',)

        java2.save()
        javaEE.save()
		
        java2.course_requirements.add(testReq)
        javaEE.course_requirements.add(testReq)
		
        java2.save()
        javaEE.save()
		
        degrees = Degree.objects.filter(degree_users=testUser.id)
		
        expectedCase = []
        expectedCase.append(java2)
        expectedCase.append(javaEE)
		
        #print(expectedCase)
		
        testReqList = []
        testReqList.append(testReq)
        
        testCase = getReqCourses( testReqList[0] )
        #print(testCase)
		
        self.assertTrue( expectedCase == testCase)
		
		
		
#def getCoursePrereqs(course):
#    '''
#    @getCoursePrereqs returns a list of prereqs required for a course in the logical form:
#        ex: [[courseA, courseB], [courseC, CourseD], [courseE]]
#        where subset lists represent logical ORs and the larger list joined by logical ANDs.
#        The above list would have prereqs: (courseA OR courseB) AND (courseC OR courseD) AND courseE
#    @param course: the Course under test
#    '''
#    prereqs = []
#    for p in course.prereq_set.all():
#        options = []
#        for pc in p.prereqcourse_set.all():
#            options.append(list(pc.prereqcourse_course.all()))
#        prereqs.append(options)
#    return prereqs



    '''
    @generateCheckBoxEntities creates a list of tuples of requirements, course names and numbers for the selectcourses page
    @param uID: primary key corresponding to the active user
    '''
    def test_generateCheckBoxEntities(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
		
        testDegree = Degree(degree_diploma='Bachelor of Science', degree_type = "MAJ", degree_track = 'Computer Science')
        testDegree.save()
        testDegree.degree_users.add(testUser)
        testDegree.save()
		
        testReq = Requirement(req_name='Java', req_credits=3)
        testReq.save()
        testReq.req_degrees.add(testDegree)
        testReq.save()
		
        java2 = Course(course_name='Java2',course_subject='CSCI', course_num='1200', course_semester='F', course_credits=3, course_special='None', course_comment='',)
        javaEE = Course(course_name='JavaEE',course_subject='CSCI', course_num='1550', course_semester='F', course_credits=3, course_special='None', course_comment='',)

        java2.save()
        javaEE.save()
		
        java2.course_requirements.add(testReq)
        javaEE.course_requirements.add(testReq)
		
        java2.save()
        javaEE.save()
		
        degrees = Degree.objects.filter(degree_users=testUser.id)
		
        expectedReq = getDegreeReqs(degrees)                # this is holding java
        expectedCheckBoxEnitites = []
        expectedReqID = expectedReq[0].id                   #1
        expectedReqName = expectedReq[0].req_name           #java
        expectedReqCredits = expectedReq[0].req_credits     #3
        expectedCatalog = getReqCourses(expectedReq[0])     #java2, javaEE
        expectedCourseList = []
        expectedCourseList.append([expectedCatalog[0].course_subject, expectedCatalog[0].course_num, expectedCatalog[0].course_name, expectedCatalog[0]. course_credits])
        expectedCourseList.append([expectedCatalog[1].course_subject, expectedCatalog[1].course_num, expectedCatalog[1].course_name, expectedCatalog[1]. course_credits])
        expectedCheckBoxEnitites.append([expectedReq[0].id, expectedReq[0].req_name, expectedReq[0].req_credits, expectedCourseList])
        #print(expectedCheckBoxEnitites)
		
        testCheckBoxEntities = generateCheckBoxEntities(testUser.id)
        #print(testCheckBoxEntities)
        self.assertTrue( expectedCheckBoxEnitites == testCheckBoxEntities )
		
		
	
    '''
    @generateMajorDD creates a list of possible majors for use on the createuser page
    '''
    def test_generateMajorDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="MAJ", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateMajorDD()
        self.assertTrue(testList == testCase)

		
		
    '''
    @generateMinorDD creates a list of possible minors for use on the createuser page
    '''
    def test_generateMinorDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="MIN", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateMinorDD()
        self.assertTrue(testList == testCase)

		
		
    '''
    @generateConcentrationsDD creates a list of possible concentrations for use on the createuser page
    '''
    def test_generateConcentrationsDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="CON", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateConcentrationsDD()
        self.assertTrue(testList == testCase)

		
		
    '''
    @generateDiplomaDD creates a list of possible diplomas for use on the createuser page
    '''
    def test_generateDiplomaDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="CON", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_diploma)
        testCase = generateDiplomaDD()
        self.assertTrue(testList == testCase)
	
	
	
	
#def generateNumCreditsDD(lo, hi, default):
#    '''
#    @generateNumCreditsDD generates a dropdown for the number of credits the user can take
#    @param lo: the lowest number of credits possible
#    @param hi: the highest number of credits possible
#    @param default: the value of the number credits dropdown that ahould be selected automatically as a default
#    '''
#    credits = []
#    for credit in range(lo, hi+1):
#        if credit is default:
#            credits.append(['S', credit])
#        else:
#            credits.append(['X', credit])
#    return credits


#def generateYearDD(default):
#    '''
#    @generateYearDD creates a list of upcoming years for use on the createuser page
#    @parm default: the year value to be selected by default
#    '''
#    years = []
#    currentYear = datetime.now().year
#    for year in range(currentYear, currentYear+4):
#        if year == default:
#            years.append(['S', year])
#        else:
#            years.append(['X', year])
#    return years

#def generateSemesterDD(default):
#    '''
#    @generateSemesterDD creates a list of upcoming semester for use on the createuser page
#    @parm default: the year value to be selected by default
#    '''
#    sems = []
#    for s in ['Fall', 'Spring', 'Summer']:
#        if s is default:
#            sems.append(['S', s])
#        else:
#            sems.append(['X', s])
#    return sems
		
	
			
    '''
    @emailFound provides feedback if the email is already in the User database table
    @param email: email under test
    '''
    def test_emailFound(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
        flag = True
        testCase = emailFound("cdog@test")
        self.assertTrue(flag == testCase)

	
	
#	def saveClassesToUser(classesChecked, uID):
#	'''		
# 	@saveClassesToUser ...description...
# 	@param classesChecked:	...description...
# 	@param uID:	...description...
# 	'''
	

	#def saveClassesToUser(classesChecked, uID):
	#    '''
	#    @saveClassesToUser updates database with a list of the user has taken
	#    @param classesChecked: list of courses the user specified as having taken
	#    @param uID: pk of the associated active user
	#    '''
	#    u = User.objects.get(pk=uID)
	#    if u in Complete.objects.all(): #TODO - this probably needs to be updated to get the actual user object instead of Complete
	#        completed = Complete.objects.get(complete_user=u)
	#    else:
	#        completed = Complete(complete_user=u)
	#        completed.save()
	#    for cc in classesChecked:
	#        course = cc.split()
	#        print( course )
	#        subject = course[0]
	#        print( subject )
	#        number = course[1]
	#        print( number )
	#        c = Course.objects.get(course_subject=subject, course_num=number)
	#        completed.complete_courses.add(c)
	
	
	
    '''
    @removeUserCompletedEnteries updates database to remove courses completed from a particular user
    @param uID: pk of the associated active user
    '''
    def test_removeUserCompletedEnteries(self):
	    flag = True
	    caseFlag = False
	    email = "cdog@test"
	    p = "secure"
	    testUser = User(username=email, password=p)
	    testUser.save()
		
		# next ... lines create data to be called upon by Complete.objects.all()
	    completed = Complete(complete_user = testUser)
	    completed.save()
		
		# create three courses
	    java = Course(course_name='Java',course_subject='CSCI', course_num='1000', course_semester='F', course_credits=3, course_special='None', course_comment='',)
	    java2 = Course(course_name='Java2',course_subject='CSCI', course_num='1200', course_semester='F', course_credits=3, course_special='None', course_comment='',)
	    javaEE = Course(course_name='JavaEE',course_subject='CSCI', course_num='1550', course_semester='F', course_credits=3, course_special='None', course_comment='',)
	    java.save()
	    java2.save()
	    javaEE.save()
		
	    completed.complete_courses.add(java)
	    completed.complete_courses.add(java2)
	    completed.complete_courses.add(javaEE)
	    completed.save()
	
		# run function in question
	    removeUserCompletedEnteries(testUser.id)
	
		# if expected results are found set caseFlag to true
	    try:
	        Complete.objects.get(complete_user=testUser)
	    except ObjectDoesNotExist:
	        caseFlag = True
	    #print(caseFlag)
	    #print(flag)
	    self.assertTrue(flag == caseFlag)
		
		
		
		
		
#def getDefaultPreferences(uID):
#    u = User.objects.get(pk=uID)
#    up = UserPreferences.objects.get(pref_user=u)
#    summerClass = up.pref_summer
#    month = datetime.now().month
#    year = datetime.now().year
#    semester = getSemesterByMonth(month)
#    nextYear = ""
#    nextSem = ""
#    minCredit = ""
#    maxCredit = ""
#    if getNextSemesterTitle(semester) == "Summer" and not summerClass:
#        nextSem = "Fall"
#        nextYear = year
#        minCredit = up.pref_minCredits
#        maxCredit = up.pref_maxCredits
#    elif getNextSemesterTitle(semester) == "Summer":
#        nexSem = "Summer"
#        nextYear = year
#        minCredit = up.pref_summerMinCredits
#        maxCredit = up.pref_summerMaxCredits
#    elif getNextSemesterTitle(semester) == "Spring":
#        nextSem = "Spring"
#        nextYear = year + 1
#        minCredit = up.pref_minCredits
#        maxCredit = up.pref_maxCredits
#    else:
#        nextSem = getNextSemesterTitle(semester)
#        nextYear = year
#        minCredit = up.pref_minCredits
#        maxCredit = up.pref_maxCredits
#    return [nextSem, nextYear, minCredit, maxCredit]

	
	
