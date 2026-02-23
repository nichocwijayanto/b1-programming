num_score = int(input("Enter your score (0-100): "))

if num_score >= 90 : 
    grade = "A"
    encourg = "Excellent work!"
elif num_score >= 80 : 
    grade = "B"
    encourg = "Well done!"
elif num_score >= 70 :
    grade = "C"
    encourg = "Good job!"
elif num_score >= 60 : 
    grade = "D"
    encourg = "You've passed!"
else : 
    grade = "F"
    encourg = "FAILED! Please do better next time."

print(f"Your grade is: {grade}\n{encourg}")