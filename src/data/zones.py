from enum import Enum


class Zones(Enum):
    CLAPIER = 'clapier'
    CACHETTE = 'cachette'
    FOIN = 'foin'
    CENTER = 'center'
    TUNNEL = 'tunnel'
    FONTAINE = 'fontaine'
    BAS = 'bas'


data_zones = [
    {
        'name': Zones.CLAPIER,
        'points': [0.44114380899500283, 0.10858165216854834, 0.1349250416435313, 0.20729224504904684]
    },
    {
        'name': Zones.CACHETTE,
        'points': [0.5710716268739591, 0.10315256956012092, 0.11715713492504154, 0.19643407983219202]
    },
    {
        'name': Zones.FOIN,
        'points': [0.7245974458634092, 0.12783021778024556, 0.18212104386451955, 0.24578937627244127]
    },
    {
        'name': Zones.TUNNEL,
        'points': [0.30433656367545264, 0.3069899438583503, 0.1231425306168904, 0.2290085754827565]
    },
    {
        'name': Zones.FONTAINE,
        'points': [0.17036919189950347, 0.723704110315175, 0.33888404818322526, 0.539270766129764]
    },
    {
        'name': Zones.BAS,
        'points': [0.7676878564903726, 0.7904982781643124, 0.4554859058182106, 0.39581137114343945]
    }
]
