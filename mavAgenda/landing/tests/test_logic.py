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

	
	
# 	'''
# 	@removeCoursesTaken provides a list of Course (objects) the user must still take (required, but not completed classes)
# 	@param requiredClasses: a list of Course (objects) required for the User's Degree
# 	@param classesTaken: a list of Course (objects) that the User has already completed
# 	'''
#   def removeCoursesTaken( requiredClasses, classesTaken ):
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

	
	
# 	'''
# 	@checkOfferedSemester determines if a given Course if offered during the current semester
# 	@param course: the Course under test
# 	@param ssf: the Spring, Summer, Fall, offering attribute of the Course
# 	'''
#   def checkOfferedSemester(course, ssf):
    # offered = False
    # if course.semester == ssf or course.semester == 'All':
    # offered = True
    # return offered
    # def test_checkOfferedSemester(self):
    # create a course object

	
	
# 	'''
# 	@checkCourseValid determines if a given Course can be taken during a given semester
# 	@param course: the Course under test
# 	@param classesTaken: a list of Course (objects) that the User has already completed
# 	@parm scheduledClasses: a list of Course (objects) the scheduling algorithm has accounted for already
# 	@param ssf: the Spring, Summer, Fall, offering attribute of the Course
# 	'''
#   def checkCourseValid(course, classesTaken, semesterCourses, ssf): #checkCourseValid( nc, classesTaken, semesterCourses, ssfSemester )

	
	
# 	'''
# 	@getSemesterByMonthYear determines semester (Spring, Summer, Fall) according to current month
# 	@param m: current month
# 	'''
# 	def get_semester_by_month_year(m)
    def test_get_semester_by_month_year(self):
        Spring = getSemesterByMonthYear(4)
        Summer = getSemesterByMonthYear(7)
        Fall = getSemesterByMonthYear(9)
        self.assertTrue(Spring == "Spring")
        self.assertTrue(Summer == "Summer")
        self.assertTrue(Fall == "Fall")

		
		
# 	'''
# 	@generateNewSemester creates a new logical semester
# 	@param semester: previous semester list
# 	'''
#   def generateNewSemester(semester):
    def test_generate_new_semester(self):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        testSemester = ["Spring", 2019, []]
        ssfSemester = getSemesterByMonthYear(currentMonth)
        semester = [ssfSemester, currentYear, []]
        currentSemester = generateNewSemester(semester)
        # print("current semester is %s" % currentSemester)
        self.assertTrue(currentSemester == testSemester)

		
		
# 	'''
#	@isFull determines if a semester has hit the maximum number of credits allowable
# 	@param courseList: list of Course (objects) the user is scheduled to take during current semester
# 	'''
#   def isFull(courseList):
    def test_is_full(self):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        ssfSemester = getSemesterByMonthYear(currentMonth)
        semester = [ssfSemester, currentYear, []]
        currentSemester = generateNewSemester(semester)
        false = isFull(currentSemester[2])
        # still need to do the true case
	
	
	
# 	'''
# 	@createSchedule generates semester-by-semester schedule for User's needed Courses according to Degree
# 	@param uID: primary key associated with active user
# 	'''
#   def createSchedule(uID):



########################################################################################################################
########################################################################################################################



#   def removeUserCompletedEnteries(uID):
# 	'''
# 	@removeUserCompletedEnteries updates database to remove courses completed from a particular user
# 	@param uID: pk of the associated active user
# 	'''
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
		
		
		
#    def generateCheckBoxEntities(uID):
#    '''
#    @generateCheckBoxEntities creates a list of tuples of requirements, course names and numbers for the selectcourses page
#    @param uID: primary key corresponding to the active user
#    '''
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
		
	
	
#	def getDegreeReqs(degrees):
#   '''
#   @getDegreeRegs returns a list of requirements for all degrees a user has selected
#   @param degrees: a list of degrees associated with the user
#   '''
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
		

		
#	def getReqCourses(req):
#   '''
#   @getReqCourses returns a list of courses for all requirements related to a degree a user has selected
#   @param reqs: a list of requirements associated with the user's desired degree
#   '''
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
		
		
		
#	def getUserByEmail(e):
#	 '''
# 	@getUserByEmail searches the User table to find the User object with a corresponding email
# 	@param e: the email being searched for
# 	'''
    def test_getUserByEmail(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
        testCase = getUserByEmail("cdog@test")
        self.assertTrue(testCase == testUser)
		
	
	
#    def emailFound(email):		
# 	'''
# 	@emailFound provides feedback if the email is already in the User database table
# 	@param email: email under test
# 	'''
    def test_emailFound(self):
        email = "cdog@test"
        p = "secure"
        testUser = User(username=email, password=p)
        testUser.save()
        flag = True
        testCase = emailFound("cdog@test")
        self.assertTrue(flag == testCase)

		

#   def getDegree(diploma, type, track):	
# 	'''
# 	@getDegree searches the Degree table to find the Degree object with corresponding degree and major
# 	@param d: degree attribute of Degree being searched for
# 	@param m: major attribute of Degree being searched for
#	 '''
    def test_getDegree(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type='Major', degree_track='Computer Science')
        newDegree.save()
        testDegree = getDegree('Master of Science', 'Major', 'Computer Science')
        self.assertTrue(newDegree == testDegree)

	
	
#	def generateMajorDD():
#	'''
#	@generateMajorDD creates a list of possible majors for use on the createuser page
#	'''
    def test_generateMajorDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="MAJ", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateMajorDD()
        self.assertTrue(testList == testCase)

		
		
#	def generateMinorDD():
#   '''
#   @generateMinorDD creates a list of possible minors for use on the createuser page
#   '''
    def test_generateMinorDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="MIN", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateMinorDD()
        self.assertTrue(testList == testCase)

		
		
#	def generateConcentrationsDD():
#   '''
#   @generateConcentrationsDD creates a list of possible concentrations for use on the createuser page
#   '''
    def test_generateConcentrationsDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="CON", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_track)
        testCase = generateConcentrationsDD()
        self.assertTrue(testList == testCase)

		
		
#	def generateDiplomaDD():
#   '''
#   @generateDiplomaDD creates a list of possible diplomas for use on the createuser page
#   '''
    def test_generateDiplomaDD(self):
        newDegree = Degree(degree_diploma='Master of Science', degree_type="CON", degree_track='Computer Science')
        newDegree.save()
        testList = []
        testList.append(newDegree.degree_diploma)
        testCase = generateDiplomaDD()
        self.assertTrue(testList == testCase)
	
	
	
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



#																		Selenium
#   def login(request):
# 	'''
# 	@login send a request to render the login.html page
# 	@param request: generates the response
# 	'''



#																		Selenium
#   def selectcourses(request, pk):
#	'''
# 	@selectcourses send a request to render the selectcourses.html page
# 	@param request: generates the response
# 	@param pk: primary key corresponding to active user
# 	'''



#																		Selenium
#   def createuser(request):
# 	'''
# 	@createuser send a request to render the createuser.html page
# 	@param request: generates the response
# 	'''

