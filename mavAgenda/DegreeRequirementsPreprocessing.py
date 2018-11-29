import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mavAgenda.settings")
django.setup()

from landing.models import *

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

compsci_maj_requirements = {
    'IS&T Core': {
        'credit': 18
    },
    'Mathematics': {
        'credit': 16
    },
    'Computer Science Core': {
        'credit': 27
    },
    'Elective': {
        'credit': 7
    },
    'Core Extension': {
        'credit': 21
    },
}

compsci_con_requirements = {
    'Game Programming': {
        'Core': {
            'credit': 9
        },
        'Elective': {
            'credit': 9
        }
    },
    'Information Assurance': {
        'Core': {
            'credit': 9
        },
        'Elective': {
            'credit': 9
        }
    },
    'Internet Technologies': {
        'Core': {
            'credit': 9
        },
        'Elective': {
            'credit': 9
        }
    },
}

mis_maj_requirements = {
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
    'MIS Core': {
        'credit': 21
    }
}

mis_con_requirements = {
    'Game Programming': {
        'Core': {
            'credit': 9
        },
        'Elective': {
            'credit': 9
        }
    },
    'Information Assurance': {
        'Core': {
            'credit': 9
        },
        'Elective': {
            'credit': 9
        }
    },
    'Internet Technologies': {
        'Core': {
            'credit': 9
        },
        'Elective': {
            'credit': 9
        }
    },
}

#####################################################

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
    '14': {
        'diploma': 'BS',
        'track': 'CYBR',
    },
}

concentration_tracks = {
    'CS':
        {'Game Programming',
         'Information Assurance',
         'Internet Technologies'},
    'MIS':
        {'i-Business Application/Development/Management',
         'Information Assurance',
         'Internet Technologies',
         'IT Audit & Control',
         'Global IT Leadership/Management'}
}

minor_tracks = {
    'CS', 'MIS', 'IA'
}

# generate degree objects
for key, val in degrees.items():
    d = Degree(degree_diploma=val['diploma'],
               degree_type='MAJ',
               degree_track=val['track'])
    d.save()
    d = Degree(degree_diploma=val['diploma'],
               degree_type='MIN',
               degree_track=val['track'])
    d.save()
    d = Degree(degree_diploma=val['diploma'],
               degree_type='CON',
               degree_track=val['track'])
    d.save()

d = Degree(degree_diploma='BS',
           degree_type='CERT',
           degree_track='MIS')
d.save()
