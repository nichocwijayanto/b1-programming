#collect test scores for 6 students
student_records = []    #list of tuples
unique_scores = set()   #empty set in python. = {} is always an empty dictionary.
stats = {}              #dictionary

for i in range(6):
    name = input("\nEnter name: ")
    score = int(input("Enter score: ")) #casting needed bcs input stores as string in default. 
    student_tuple = (name, score)
    student_records.append(student_tuple)   #add to a list
    unique_scores.add(score)                #add to a set
    stats[score] = stats.get(score, 0) + 1  #add to a dictionary

print("\n=== STUDENT RECORDS ===")
for j in range(0,6,1):
    print(f"{j+1}. {student_records[j][0].title()}: {student_records[j][1]}")

#Statistics
highest_score = max(student_records, key=lambda t: t[1]) #returns a tuple with max value | this can also use for loops if a single value is to be returned.
lowest_score = min(student_records, key=lambda t: t[1]) #returns a tuple with min value  | same for this. 
total_score = sum(t[1] for t in student_records) #sum has to return a single value, so no tuples like min() & max()
total_student = len(student_records)
average_score = total_score/total_student

print("\n=== CLASS STATISTICS ===")
print(f"Highest Score: {highest_score[1]}")
print(f"Lowest Score: {lowest_score[1]}")
print(f"Average Score: {average_score:.2f}")

print("\n=== UNIQUE SCORES ===")
print(sorted(unique_scores))    # sorted(set) sorts the set from lowest to highest
print(f"Total unique scores: {len(unique_scores)}")

print("\n=== GRADE DISTRIBUTION ===")
for grade, count in stats.items():
    print(f"Score {grade}: {count} students")