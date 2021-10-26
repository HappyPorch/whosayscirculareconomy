

def filter_by_location(mainLocation):
    ignore = ["Outwith Scotland"]
    for i in ignore:
        if i in mainLocation:
            return 0
    return 1

def filter_by_name(name):
    ignore = ["BBC", "Ellen MacArthur Foundation"]
    for i in ignore:
        if i in name:
            return 0
    return 1

def filter_by_purposes(purposes):
    if "'The advancement of religion'" in purposes:
        return 0
    return 1

def filter_by_activities(activities):
    if "'It carries out activities or services itself'" in activities:
        return 1
    return 0

def filter_by_income(income):
    if income and int(income) > 30000:
        return 1
    return 0

