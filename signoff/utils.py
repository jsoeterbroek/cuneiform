from datetime import datetime, date


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:  # Over midnight
        return nowTime >= startTime or nowTime <= endTime


def calculate_period():

    today = date.today()
    dtime = datetime.now()
    hour = dtime.hour
    period = 'unknown'
    # periods
    if isNowInTimePeriod(6, 7, hour):
        period = 'p00100'
    elif isNowInTimePeriod(8, 11, hour):
        period = 'p00200'
    elif isNowInTimePeriod(12, 16, hour):
        period = 'p00300'
    elif isNowInTimePeriod(17, 20, hour):
        period = 'p00400'
    elif isNowInTimePeriod(21, 5, hour):
        period = 'p00500'

    valid = {'p00100', 'p00200', 'p00300', 'p00400', 'p00500'}
    if period not in valid:
        raise ValueError("results: period must be one of %r." % valid)
    return period


def get_matrix_lookupkey():
    """
    get lookupkey to check matrix for med at this specific day and
    period
    eg.:
    At on monday, 12:50 should return 'm_d00100_p00300'
    """

    period = calculate_period()

    (weekday_int, weekday_hr) = get_today()
    matrix_lookupkey = "m_d00" + str(weekday_int) + "00_" + period

    return matrix_lookupkey


def get_period():
    """get the correct period from argument period
    return an int for period and hr string in dutch
    eg.
    period: 'p_00100' returns
    (100, "Ronde 1 vanaf 07:00")
    """

    today = date.today()
    today_weekday_int = today.weekday()

    period_hr = ''
    period_int = 0
    period = calculate_period()

    if period == 'p00100':
        period_hr = "Ronde 1 vanaf 07:00"
        period_int = 1
    elif period == 'p00200':
        period_hr = "Ronde 2 vanaf 08:00"
        period_int = 2
    elif period == 'p00300':
        period_hr = "Ronde 3 vanaf 12:00"
        period_int = 3
    elif period == 'p00400':
        period_hr = "Ronde 4 vanaf 17:00"
        period_int = 4
    elif period == 'p00500':
        period_hr = "Ronde 5 vanaf 21:00"
        period_int = 5

    #period_matrixfield = get_matrix_lookupkey()
    return period_hr


def get_today():
    """get the day of the week
    return an int for weekday and hr string in dutch
    """

    today = date.today()
    today_weekday_int = today.weekday()

    if today_weekday_int == 0:
        today_weekday_hr = "Maandag"
    elif today_weekday_int == 1:
        today_weekday_hr = "Dinsdag"
    elif today_weekday_int == 2:
        today_weekday_hr = "Woensdag"
    elif today_weekday_int == 3:
        today_weekday_hr = "Donderdag"
    elif today_weekday_int == 4:
        today_weekday_hr = "Vrijdag"
    elif today_weekday_int == 5:
        today_weekday_hr = "Zaterdag"
    elif today_weekday_int == 6:
        today_weekday_hr = "Zondag"

    today_weekday_iso_int = today_weekday_int + 1
    return today_weekday_hr


def is_prescription_signedoff_today_period(prescription_id, weekday_int, period_int):
    # is_prescription_signedoff_today_period(26,4,4)
    try:
        signoff_current = Signoff.objects.filter(prescription=prescription_id).filter(
            signoff_period=period_int, signoff_weekday=weekday_int
        )
        if signoff_current:
            return True
        else:
            return False

    except Exception:
        pass
        return False
