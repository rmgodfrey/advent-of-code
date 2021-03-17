RANGE_MIN = 145852
RANGE_MAX = 616942

def contains_same_adjacent_digits(num):
    for i in range(len(num) - 1):
        if num[i] == num[i+1]:
            return True
    return False
    
def contains_exactly_two_adjacent_digits(num):
    digit_stretches = []
    last_digit = None
    for digit in num:
        if digit == last_digit:
            digit_stretches[-1] += 1
        else:
            digit_stretches.append(1)
        last_digit = digit
    if 2 in digit_stretches:
        return True
    return False        
    
def contains_decreasing_digits(num):
    for i in range(len(num) - 1):
        if int(num[i]) > int(num[i+1]):
            return True
    return False
    
def meets_criteria(num, early_version=False):
    num = str(num)
    if early_version:
        if (contains_same_adjacent_digits(num) and
            not contains_decreasing_digits(num)):
                return True
        return False
    if (contains_exactly_two_adjacent_digits(num) and
        not contains_decreasing_digits(num)):
            return True
    return False

def passwords_meeting_criteria(range_min, range_max, early_version=False):
    result = []
    for password in range(range_min, range_max + 1):
        if meets_criteria(password, early_version):
            result.append(password)
    return result

passwords_within_range = len(passwords_meeting_criteria(RANGE_MIN, RANGE_MAX, early_version=True))
print('Part 1 answer:', passwords_within_range)

passwords_within_range = len(passwords_meeting_criteria(RANGE_MIN, RANGE_MAX))
print('Part 2 answer:', passwords_within_range)
