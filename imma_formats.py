# -*- coding: utf-8 -*-

from imma_conversions import float1, float2

TABLE_C0 = [
    (1, int, 4, 'YR', 'year UTC', 1600, 2024, '(AAAA)'),
    (2, int, 2, 'MO', 'month UTC1', 1, 12, '(MM)'),
    (3, int, 2, 'DY', 'day UTC1', 1, 31, '(YY)'),
    (4, int, 4, 'HR', 'hour UTC1', 0, 23.99, '0.01 hour (Δ GG)'),
    (5, float2, 5, 'LAT', 'latitude', -90.00, 90.00, '0.01°N (Δ LaLaLa)'),
    (6, float2, 6, 'LON', 'longitude1', -179.99, 359.99, '0.01°E (Δ LoLoLoLo)'),
#    (0, float2, 0, '', '', 0.00, 359.99, '(ICOADS convention)'),
#    (0, float2, 0, '', '', -179.99, 180.00, '(NCDC-variant  convention)'),
    (7, int, 2, 'IM', 'IMMA version', 0, 99, '(Δ •65)'),
    (8, int, 1, 'ATTC', 'attm count', 0, 9, ''),
    (9, int, 1, 'TI', 'time indicator', 0, 3, ''),
    (10, int, 1, 'LI', 'latitude/long. indic.', 0, 6, ''),
    (11, int, 1, 'DS', 'ship course', 0, 9, '(Ds)'),
    (12, int, 1, 'VS', 'ship speed', 0, 9, '(Δ vs)'),
    (13, int, 2, 'NID', 'national source indic.1', 0, 99, ''),
    (14, int, 2, 'II', 'ID indicator', 0, 10, ''),
    (15, str, 9, 'ID', 'identification/call  sign', 'c', 'c', '(Δ •42)'),
    (16, str, 2, 'C1', 'country code', 'b', 'b', '(Δ •43)'),
    (17, int, 1, 'DI', 'wind direction indic.', 0, 6, ''),
    (18, int, 3, 'D', 'wind direction (true)', 1, 362, '°, 361-2 (Δ dd)'),
    (19, int, 1, 'WI', 'wind speed indicator', 0, 8, '(Δ iW)'),
    (20, float1, 3, 'W', 'wind speed', 0, 99.9, '0.1 m/s (Δ ff)'),
    (21, int, 1, 'VI', 'VV indic.', 0, 2, '(Δ •9)'),
    (22, int, 2, 'VV', 'visibility', 90, 99, '(VV)'),
    (23, int, 2, 'WW', 'present weather', 0, 99, '(ww)'),
    (24, int, 1, 'W1', 'past weather', 0, 9, '(W1)'),
    (25, float1, 5, 'SLP', 'sea level pressure', 870.0, 1074.6, '0.1 hPa (Δ PPPP)'),
    (26, int, 1, 'A', 'characteristic of PPP', 0, 8, '(a)'),
    (27, float1, 3, 'PPP', 'amt. pressure tend.', 0, 51.0, '0.1 hPa (ppp)'),
    (28, int, 1, 'IT', 'indic. for temperatures', 0, 9, '(Δ iT)'),
    (29, float1, 4, 'AT', 'air temperature', -99.9, 99.9, '0.1°C (Δ sn, TTT)'),
    (30, int, 1, 'WBTI', 'WBT indic.', 0, 3, '(Δ sw)'),
    (31, float1, 4, 'WBT', 'wet-bulb temperature', -99.9, 99.9, '0.1°C (Δ sw, TbTbTb)'),
    (32, int, 1, 'DPTI', 'DPT indic.', 0, 3, '(Δ st)'),
    (33, float1, 4, 'DPT', 'dew-point temperature', -99.9, 99.9, '0.1°C (Δ st, TdTdTd)'),
    (34, int, 2, 'SI', 'SST meas. method', 0, 12, '(Δ •30)'),
    (35, float1, 4, 'SST', 'sea surface temp.', -99.9, 99.9, '0.1°C (Δ sn, TwTwTw)'),
    (36, int, 1, 'N', 'total cloud amount', 0, 9, '(N)'),
    (37, int, 1, 'NH', 'lower cloud amount', 0, 9, '(Nh)'),
    (38, str, 1, 'CL', 'low cloud type', 0, '9, A', '(Δ CL)'),
    (39, int, 1, 'HI', 'H indic.', 0, 1, '(Δ •9)'),
    (40, str, 1, 'H', 'cloud height', 0, '9, A', '(Δ h)'),
    (41, str, 1, 'CM', 'middle cloud type', 0, '9, A', '(Δ CM)'),
    (42, str, 1, 'CH', 'high cloud type', 0, '9, A', '(Δ CH)'),
    (43, int, 2, 'WD', 'wave direction', 0, 38, ''),
    (44, int, 2, 'WP', 'wave period', 0, '30, 99', 'seconds (PWPW)'),
    (45, int, 2, 'WH', 'wave height', 0, 99, '(HWHW)'),
    (46, int, 2, 'SD', 'swell direction', 0, 38, '(dW1dW1)'),
    (47, int, 2, 'SP', 'swell period', 0, '30, 99', 'seconds (PW1PW1)'),
    (48, int, 2, 'SH', 'swell height', 0, 99, '(HW1HW1)'), ]

TABLE_C1 = [ ]
TABLE_C2 = [ ]
TABLE_C3 = [ ]
TABLE_C4 = [ ]
TABLE_C5 = [ ]
TABLE_C6 = [ ]

TABLES = {
    'c0': TABLE_C0,
    'c1': TABLE_C1,
    'c2': TABLE_C2,
    'c3': TABLE_C3,
    'c4': TABLE_C4,
    'c5': TABLE_C5,
    'c6': TABLE_C6, }
