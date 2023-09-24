#A geography quiz based on countries and their capital
#quiz variable (initialized as a dictionary) containing the question and answers

quiz={"question1":{"question":"What is the capital of India?","answer":"New Delhi"},
"question2":{"question":"What is the capital of Afghanistan?","answer":"Kabul"},
"question3":{"question":"What is the capital of Argentina?","answer":"Buenos Aires"},
"question4":{"question":"What is the capital of Azerbaijan?","answer":"Baku"},
"question5":{"question":"What is the capital of Belgium?","answer":"Brussels"},
"question6":{"question":"What is the capital of Denmark?","answer":"Copenhagen"},
"question7":{"question":"What is the capital of Egypt?","answer":"Cairo"},
"question8":{"question":"What is the capital of Finland?","answer":"Helsinki"},
"question9":{"question":"What is the capital of Japan?","answer":"Tokyo"},
"question10":{"question":"What is the capital of Germany?","answer":"Berlin"}
}

#score variable to keep track of the score
score=0

#looping through the quiz dictionary
for key,value in quiz.items():
    print(value['question'])
    answer=input("Answer: ")

    #Checking the user given answers to the correct answers
    if answer.lower()==value['answer'].lower():
        print("Correct!")
        score+=1
        print("Your score is: ",str(score))
    else:
        print("Incorrect Answer!!!")
        print("Correct Answer: ",value['answer'])
        print("Your score is: ",str(score))

#Printing the final score and percentage
print("Your final score is: ",str(score))
print("Percentage Achieved: ",int((score/10)*100),"%")



