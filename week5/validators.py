import random

def check_min_length(password, min_len=8):  #min_len=8 is a default value. In case the caller doesn't insert a value for it.
    return len(password) >= min_len

def has_uppercase(password):
    return any(c.isupper() for c in password)

def has_lowercase(password):
    return any(c.islower() for c in password)

def has_digit(password):
    return any(c.isnumeric() for c in password)

def has_special_char(password):
    return any(not c.isalnum() for c in password) # not any() --> only True if all is non-alnum.
                                                  # any(not c.isalnum()) --> True if one non-alnum character exist.
def validate_password(password):
    checklist = {} 
    out_checklist = []
    hints = [
        "Add more characters!", 
        "Try a capital letter!",
        "Try a lowercase letter!",
        "Try adding a number!",
        "Try adding special character!"
    ]
    cheers = [
        "Great job!",
        "Strong choice!",
        "Well done!",
        "Congrats!"
    ]

    is_valid_len = check_min_length(password)
    is_valid_upper = has_uppercase(password)
    is_valid_lower = has_lowercase(password)
    is_valid_digit = has_digit(password)
    is_valid_s_char = has_special_char(password)

    if is_valid_len:
        checklist['min_len'] = True
        out_checklist.append("\n8 Minimum Length: Met (V)")
    else:
        checklist['min_len'] = False
        out_checklist.append("\n8 Minimum Length: Not Met (X)")
    if is_valid_upper:
        checklist['uppercase'] = True
        out_checklist.append("Has Uppercase: Met (V)")
    else:
        checklist['uppercase'] = False
        out_checklist.append("Has Uppercase: Not Met (X)")
    if is_valid_lower:
        checklist['lowercase'] = True
        out_checklist.append("Has Lowercase: Met (V)")
    else:
        checklist['lowercase'] = False
        out_checklist.append("Has Lowercase: Not Met (X)")
    if is_valid_digit:
        checklist['digit'] = True
        out_checklist.append("Has Digit: Met (V)")
    else:
        checklist['digit'] = False
        out_checklist.append("Has Digit: Not Met (X)")
    if is_valid_s_char:
        checklist['s_char'] = True
        out_checklist.append("Has Special Character: Met (V)")
    else:
        checklist['s_char'] = False
        out_checklist.append("Has Special Character: Not Met (X)")
    
    is_strong = all(checklist.values())              #all is True
    is_totally_invalid = not any(checklist.values()) #all is False

    if is_strong:                                 
        checklist['is_valid'] = True
        out_checklist.append("\nPassword is strong and valid.")
    elif is_totally_invalid:
        checklist['is_valid'] = False
        out_checklist.append("\nPassword is weak and invalid!")
    else:
        checklist['is_valid'] = False
        out_checklist.append("\nPassword is weak.")   #at least one False (not all())
    
    if checklist['is_valid'] == False:
        out_hint = random.choice(hints)
        out_checklist.append(f"\nHint: {out_hint}")
    else:
        out_hint = random.choice(cheers)
        out_checklist.append(f"\nFeedback: {out_hint}")

    return out_checklist

password = input("Enter your password: ")
result = validate_password(password)
print(f"\n== Password validation ==\n{'\n'.join(result)}\n")