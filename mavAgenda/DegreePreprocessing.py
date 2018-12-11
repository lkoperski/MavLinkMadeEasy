import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mavAgenda.settings")
django.setup()

from landing.models import *

#####################################################

####################
# Degree data
####################

degrees = {
    '1': {
        'diploma': 'BS',
        'track': 'CSCI',
    },
    '2': {
        'diploma': 'BS',
        'track': 'MIS',
    },
    '3': {
        'diploma': 'BS',
        'track': 'BIOI',
    },
    '4': {
        'diploma': 'BS',
        'track': 'ITIN',
    },
    '5': {
        'diploma': 'BS',
        'track': 'CYBR',
    }
}

minor_tracks = {
    'CSCI', 'MIS', 'CYBR', 'ITIN'
}

concentration_tracks = {
    'CSCI':
        {'Game Programming',
         'Cyber Security',
         'Internet Technologies'},
    'MIS':
        {'i-Business Application/Development/Management',
         'Cyber Security',
         'Internet Technologies',
         'IT Audit & Control',
         'Global IT Leadership/Management'}
}

mis_cert_requirements = {
    'Data Management',
    'Systems Development',
    'IT Administration'
}

# generate major degree objects
for key, val in degrees.items():
    d = Degree(degree_diploma=val['diploma'],
               degree_type='MAJ',
               degree_track=val['track'])
    d.save()

# generate minor degree objects
for minor in minor_tracks:
    d = Degree(degree_diploma='BS',
               degree_type='MIN',
               degree_track=minor)
    d.save()

# generate minor degree objects
for major in concentration_tracks.items():
    for concentration in major[1]:
        d = Degree(degree_diploma='BS',
                   degree_type='CON',
                   degree_track=major[0],
                   degree_additional_track=concentration)
        d.save()

for certification in mis_cert_requirements:
    d = Degree(degree_diploma='BS',
               degree_type='CERT',
               degree_track='MIS',
               degree_additional_track=certification)
    d.save()
