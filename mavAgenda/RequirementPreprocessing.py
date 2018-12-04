import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mavAgenda.settings")
django.setup()

from landing.models import *

####################
# General Education
####################

gen_ed_requirements = {
    'English Composition': {
        'credit': 9
    },
    'Mathematics': {
        'credit': 3
    },
    'Public Speaking': {
        'credit': 3
    },
    'Humanities': {
        'credit': 9
    },
    'Social Science': {
        'credit': 9
    },
    'Natural/Physical Science': {
        'credit': 7
    },
    'Global Diversity': {
        'credit': 3
    },
    'US Diversity': {
        'credit': 3
    }
}
#####################
# Gen Ed Requirements
#####################
d = Degree.objects.all()
for gen_ed in gen_ed_requirements.items():
    r = Requirement(req_name=gen_ed[0], req_credits=gen_ed[1]['credit'])
    r.save()
    r.req_degrees.set(d)
    r.save()

####################
# Computer Science
####################

compsci_maj_requirements = {
    'Humanities': {
        'credit': 3
    },
    'Social Science': {
        'credit': 3
    },
    'IS&T Core': {
        'credit': 18
    },
    'Mathematics': {
        'credit': 16
    },
    'Major Core': {
        'credit': 27
    },
    'Elective': {
        'credit': 7
    },
    'Core Extension': {
        'credit': 21
    },
}

compsci_min_requirements = {
    'Minor Core': {
        'credit': 12
    },
    'Elective (2000 level)': {
        'credit': 6
    },
    'Elective (3000 level)': {
        'credit': 6
    },
}

compsci_con_requirements = {
    'Game Programming Core': {
        'credit': 9
    },
    'Game Programming Elective': {
        'credit': 9
    },
    'Cyber Security Core': {
        'credit': 9
    },
    'Cyber Security Elective': {
        'credit': 9
    },
    'Internet Technologies Core': {
        'credit': 9
    },
    'Internet Technologies Elective': {
        'credit': 9
    },
}

###################
# CSCI Requirements
###################

# Major
csci = Degree.objects.filter(degree_diploma='BS', degree_type='MAJ', degree_track='CSCI')
for req in compsci_maj_requirements.items():
    r = Requirement(req_name="Computer Science " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(csci)
    r.save()

# Minor
csci = Degree.objects.filter(degree_diploma='BS', degree_type='MIN', degree_track='CSCI')
for req in compsci_min_requirements.items():
    r = Requirement(req_name="Computer Science " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(csci)
    r.save()

# Concentration
for req in compsci_con_requirements.items():
    s = req[0].rsplit(' ', 1)[0]
    con = Degree.objects.filter(degree_diploma='BS', degree_type='CON',
                                degree_track='CSCI', degree_additional_track=s)
    r = Requirement(req_name="Computer Science " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(con)
    r.save()

################################
# Management Information Systems
################################

mis_maj_requirements = {
    'Humanities': {
        'credit': 3
    },
    'Social Science': {
        'credit': 3
    },
    'Global Diversity': {
        'credit': 3
    },
    'IS&T Core': {
        'credit': 21
    },
    'Mathematics': {
        'credit': 6
    },
    'Co-Req Topic': {
        'credit': 15
    },
    'Specialization': {
        'credit': 12
    },
    'Elective': {
        'credit': 20
    },
    'Major Core': {
        'credit': 21
    }
}

mis_min_requirements = {
    'Minor Core': {
        'credit': 9
    },
    'Elective': {
        'credit': 3
    },
}

mis_con_requirements = {
    'i-Business Application/Development/Management Prerequisites': {
        'credit': 12
    },
    'i-Business Application/Development/Management Core': {
        'credit': 6
    },
    'i-Business Application/Development/Management Elective': {
        'credit': 9
    },
    'i-Business Application/Development/Management Capstone': {
        'credit': 3
    },
    'Cyber Security Prerequisites': {
        'credit': 21
    },
    'Cyber Security Core': {
        'credit': 18
    },
    'Internet Technologies Core': {
        'credit': 6
    },
    'Internet Technologies Elective': {
        'credit': 9
    },
    'Internet Technologies Capstone': {
        'credit': 3
    },
    'IT Audit & Control Core': {
        'credit': 9
    },
    'IT Audit & Control Elective': {
        'credit': 6
    },
    'IT Audit & Control Capstone': {
        'credit': 3
    },
    'Global IT Leadership Prerequisites': {
        'credit': 24
    },
    'Global IT Leadership Core': {
        'credit': 15
    },
    'Global IT Leadership Capstone': {
        'credit': 3
    }
}

mis_cert_requirements = {
    'Data Management Core': {
        'credit': 12
    },
    'Data Management Elective': {
        'credit': 3
    },
    'Systems Development Core': {
        'credit': 12
    },
    'Systems Development Elective': {
        'credit': 3
    },
    'IT Administration Core': {
        'credit': 14
    }
}

###################
# MIS Requirements
###################

# Major
mis = Degree.objects.filter(degree_diploma='BS', degree_type='MAJ', degree_track='MIS')
for req in mis_maj_requirements.items():
    r = Requirement(req_name="Management Information Systems " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(mis)
    r.save()

# Minor
mis = Degree.objects.filter(degree_diploma='BS', degree_type='MIN', degree_track='MIS')
for req in mis_min_requirements.items():
    r = Requirement(req_name="Management Information Systems " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(mis)
    r.save()

# Concentration
for req in mis_con_requirements.items():
    con = Degree.objects.filter(degree_diploma='BS', degree_type='CON',
                                degree_track='MIS', degree_additional_track=req[0])
    r = Requirement(req_name="Management Information Systems " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(con)
    r.save()

# Certification
for req in mis_cert_requirements.items():
    cert = Degree.objects.filter(degree_diploma='BS', degree_type='CERT',
                                 degree_track='MIS', degree_additional_track=req[0])
    r = Requirement(req_name="Management Information Systems " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(cert)
    r.save()

####################
# Bioinformatics
####################

bioi_maj_requirements = {
    'Humanities': {
        'credit': 3
    },
    'Natural/Physical Science': {
        'credit': 7
    },
    'IS&T Core': {
        'credit': 24
    },
    'Mathematics': {
        'credit': 11
    },
    'Biology': {
        'credit': 16
    },
    'Chemistry': {
        'credit': 17
    },
    'Bioinformatics': {
        'credit': 24
    },
    'Elective': {
        'credit': 1
    },
}

#############################
# Bioinformatics Requirements
#############################

# Major
bioi = Degree.objects.filter(degree_diploma='BS', degree_type='MAJ', degree_track='BIOI')
for req in bioi_maj_requirements.items():
    r = Requirement(req_name="Bioinformatics " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(bioi)
    r.save()

####################
# Cyber Security
####################

cybr_maj_requirements = {
    'Humanities': {
        'credit': 3
    },
    'Social Science': {
        'credit': 6
    },
    'Global Diversity': {
        'credit': 3
    },
    'IS&T Core': {
        'credit': 9
    },
    'Mathematics': {
        'credit': 8
    },
    'Computer Science Core': {
        'credit': 21
    },
    'Cyber Security Core': {
        'credit': 27
    },
    'Elective': {
        'credit': 7
    },
    'Cyber Security Elective': {
        'credit': 8
    },
    'Co-Requisite': {
        'credit': 12
    },
}

cybr_min_requirements = {
    'Prerequisites': {
        'credit': 9
    },
    'Minor Core': {
        'credit': 9
    },
    'Minor Elective': {
        'credit': 9
    },
}

#############################
# Cyber Security Requirements
#############################

# Major
cybr = Degree.objects.filter(degree_diploma='BS', degree_type='MAJ', degree_track='CYBR')
for req in cybr_maj_requirements.items():
    r = Requirement(req_name="Cyber Security " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(cybr)
    r.save()

# Minor
mis = Degree.objects.filter(degree_diploma='BS', degree_type='MIN', degree_track='CYBR')
for req in cybr_min_requirements.items():
    r = Requirement(req_name="Cyber Security " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(cybr)
    r.save()

####################
# IT Innovation
####################

itin_maj_requirements = {
    'Humanities': {
        'credit': 3
    },
    'Social Science': {
        'credit': 3
    },
    'Global Diversity': {
        'credit': 3
    },
    'IS&T Core': {
        'credit': 45
    },
    'Mathematics': {
        'credit': 6
    },
    'Major Elective': {
        'credit': 3
    },
}

itin_min_requirements = {
    'Minor Core': {
        'credit': 12
    },
    'Minor Elective': {
        'credit': 9
    }
}

#############################
# IT Innovation Requirements
#############################

# Major
itin = Degree.objects.filter(degree_diploma='BS', degree_type='MAJ', degree_track='ITIN')
for req in itin_maj_requirements.items():
    r = Requirement(req_name="IT Innovation " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(itin)
    r.save()

# Minor
itin = Degree.objects.filter(degree_diploma='BS', degree_type='MIN', degree_track='ITIN')
for req in itin_min_requirements.items():
    r = Requirement(req_name="IT Innovation " + req[0], req_credits=req[1]['credit'])
    r.save()
    r.req_degrees.set(itin)
    r.save()
