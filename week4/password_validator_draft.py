passwords = [
    "Pass123",
    "SecurePassword1",
    "weak",
    "MyP@ssw0rd",
    "NOLOWER123"
]

print("Validating passwords...")

#password length check (min 8. char)
for x in passwords:
    checklist = {
        'min_length': False,
        'has_upper': False,
        'has_lower': False,
        'has_digit': False
    }

    length = len(x)
    if length >= 8:
        #min_length = True
        checklist['min_length'] = True

    if any(x.isupper() for c in x):                    #any() replaces for loop and boolean. 
        checklist['has_upper'] = True
    
    if any(x.islower() for c in x):  
        checklist['has_lower'] = True  

    if any(x.isnumeric() for c in x):  
        checklist['has_digit'] = True

   # has_upper = False
   # for c in x :
    #    if c.isupper() :
    #        has_upper = True

   # has_lower = False
   # for c in x: 
   #     if c.islower():
   #         has_lower = True

    #for criteria in checklist:
        #if all(checklist.values()) == True:
        #    print(f"PASS: \'{x}\' - Meets all requirements.")
        
    fail_list = []
        
    if checklist['min_length'] == False:
        fail_list.append("Too short")
    elif checklist['has_upper'] == False:
        fail_list.append("No uppercase")
    elif checklist['has_lower'] == False:
         fail_list.append("No lowercase")
    elif checklist['has_digit'] == False:
         fail_list.append("No digits")

    if not fail_list:   #empty list is considered False in Python, with items is True. Alternative with len(list)
         print(f"PASS: \'{x}\' - Meets all requirements.")
    else:
       print(f"FAIL: \'{x}\' - {', '.join(fail_list)}")

        #elif checklist['min_length'] == False:
        #    print(f"FAIL: \'{x}\' - Too short")
        #elif checklist['has_upper'] == False:
        #    print(f"FAIL: \'{x}\' - No uppercase")
        #elif checklist['has_lower'] == False:
        #    print(f"FAIL: \'{x}\' - No lowercase")
        #elif checklist['has_digit'] == False:
        #    print(f"FAIL: \'{x}\' - No digits")

            
            

#summary
print()