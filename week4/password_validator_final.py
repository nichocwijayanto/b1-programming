passwords = [
    "Pass123",
    "SecurePassword1",
    "weak",
    "MyP@ssw0rd",
    "NOLOWER123"
]

print("\nValidating passwords...\n" )

comp_count = {
        'comp': 0,
        'non_comp': 0
    }

for x in passwords:
    checklist = {
        'min_length': False,
        'has_upper': False,
        'has_lower': False,
        'has_digit': False
    }

    length = len(x)
    if length >= 8:
        checklist['min_length'] = True
        
    if any(c.isupper() for c in x):                
        checklist['has_upper'] = True
        
    if any(c.islower() for c in x):  
        checklist['has_lower'] = True  
        
    if any(c.isnumeric() for c in x):  
        checklist['has_digit'] = True
        

    fail_list = []
        
    if checklist['min_length'] == False:
        fail_list.append("Too short")
        
    if checklist['has_upper'] == False:
        fail_list.append("No uppercase letter")
        
    if checklist['has_lower'] == False:
        fail_list.append("No lowercase letter")
        
    if checklist['has_digit'] == False:
        fail_list.append("No digits")
        

    if not fail_list: 
        print(f"PASS: \'{x}\' - Meets all requirements.")
        comp_count['comp'] += 1
    else:
       print(f"FAIL: \'{x}\' - {', '.join(fail_list)}.")
       comp_count['non_comp'] += 1
            
print(f"\nSummary: {comp_count['comp']} compliant, {comp_count['non_comp']} non-compliant.\n")