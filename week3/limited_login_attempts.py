correct_pin = "1234"
max_attempt = 3
login_successful = False

while max_attempt > 0 :
    pin = input("Please enter the correct pin: ")
    
    if pin == correct_pin :
        login_successful = True
        break  #exits the LOOP entirely. doesn't care about conditional statements.
    else :
        max_attempt -= 1
        print(f"Failed attempt. Remaining attempt: {max_attempt}")

if login_successful == True :
    print("Pin is correct. You're in!") 
else:
    print("Oops! Max attempt reached. Your account is locked!")