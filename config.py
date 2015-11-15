#!/usr/bin/python
#coding=utf-8

import re

cinema_filter = [re.compile(u'2015|2014'), re.compile(u'1080|720')]
humor_filter = [re.compile(u'КВН|Уральские\sпельмени'), re.compile(u'1080|720')]
serial_filter = [re.compile(u'Теория\sБольшого\sВзрыва'), re.compile(u'1080|720'), re.compile(u'Кураж-Бамбей')]

config = [
            ('http://alt.rutor.org/rss.php?category=1', cinema_filter, 'зарубежные'),
            ('http://alt.rutor.org/rss.php?category=5', cinema_filter, 'наши'),
            ('http://alt.rutor.org/rss.php?category=7', cinema_filter, 'мультики'),
            ('http://alt.rutor.org/rss.php?category=15', humor_filter, 'юмор'),
            ('http://alt.rutor.org/rss.php?category=4', serial_filter, 'сериалы')
        ]
