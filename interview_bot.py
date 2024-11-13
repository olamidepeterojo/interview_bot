"""""
This script serves as an interactive interview preparation bot designed to help users practice technical coding 
interview questions. The bot asks users a set of 40 common coding interview questions randomly, collects the user's 
responses, and provides feedback or guidance where applicable.

"""
import random
import difflib
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# List of 40 interview questions and expected answers (for similarity comparison only, not shown to the user)
questions_and_answers = [
    {"question": "What is the difference between a stack and a queue?", "answer": "A stack is LIFO, while a queue is FIFO."},
    {"question": "Explain the concept of a binary tree.", "answer": "A binary tree is a data structure in which each node has at most two children."},
    {"question": "What is a linked list?", "answer": "A linked list is a linear data structure where elements are stored in nodes linked together with pointers."},
    {"question": "What is a Data Structure?", "answer": "A data structure is a storage format that defines the way data is stored, organized, and manipulated."},
    {"question": "What is an Array?", "answer": "An array is commonly referred to as a collection of items stored at contiguous memory locations."},
    {"question": "What is FIFO?", "answer": "FIFO stands for First In First Out."},
    {"question": "What is Recursion?", "answer": "Recursion refers to a function calling itself based on a terminating condition."},
    {"question": "What is the OOPs concept?", "answer": "OOPs stands for Object-Oriented Programming System, a paradigm that provides concepts such as objects, classes, and inheritance."},
    {"question": "What is a Graph?", "answer": "A graph is a particular type of data structure that contains a set of ordered pairs"},
    {"question": "What is a Deque?", "answer": "A deque is a double-ended queue."},
    {"question": "How does variable declaration affect memory?", "answer": "The amount of memory to be reserved or allocated depends on the data type stored in that variable."},
    {"question": "How do you determine if a string is a palindrome?", "answer": "A string is a palindrome when it stays the same on reversing the order of characters in that string."},
    {"question": "How would you implement the insertion sort algorithm?", "answer": "We assume the first element in the array to be sorted. The second element is stored separately in the key. This sorts the first two elements. You can then compare the third element with the ones on its left. This process will continue until we sort the array."},
    {"question": "What is a factorial", "answer": "A factorial is a function that multiplies a number by every number below it."},
    {"question": "How do you sum all the elements in an array?", "answer": "Use for loop to iterate through the array and keep adding the elements in that array"},
    {"question": "What is LIFO?", "answer": "LIFO is an abbreviation for Last In First Out"},
    {"question": "What is a Stack?", "answer": "A stack refers to a linear data structure performing operations in a LIFO (Last In First Out) order."},
    {"question": "What is a Queue?", "answer": "A queue refers to a linear data structure that performs operations in a FIFO order."},
    {"question": "Explain what a Binary Search Tree is.", "answer": "A binary search tree stores data and retrieves it very efficiently."},
    {"question": "Explain Doubly Linked Lists?", "answer": "Doubly linked lists are categorized as a particular type of linked list in which traversal across the data elements can be done in both directions."},
    {"question": "What is a linear data structure?", "answer": "It is a structure in which data elements are adjacent to each other"},
    {"question": "What is a non-linear data structure?", "answer": "It is a structure in which each data element can connect to two adjacent data elements"},
    {"question": "List examples of a linear data structure", "answer": "linked lists, arrays, queues, and stacks"},
    {"question": "List examples of a non-linear data structure", "answer": "graphs and trees"},
    {"question": "Which sorting algorithm is the best?", "answer": "No algorithm can be considered the best or fastest because they have been designed for a specific type of data structure where it performs the best."},
    {"question": "What are dynamic data structures?", "answer": "Dynamic data structures have the feature where they expand and contract as a program runs. It provides a very flexible data manipulation method because it adjusts based on the data size to be manipulated."},
    {"question": "How to find the number of occurrences of a character in a String?", "answer": "To find the number of occurrences, loop through the string and search for that character at every iteration; whenever it is found, it will update the count."},
    {"question": "What is a class", "answer": "A blueprint or prototype for creating objects. It defines the attributes and behaviors that objects created from the class will have"},
    {"question": "What is an object", "answer": "An instance of a class. It is the actual realization of the class, containing real data and states."},
    {"question": "What is Big O Notation?", "answer": "Big O Notation is a mathematical notation used to describe the upper bound of an algorithm's running time in terms of input size. It helps to analyze the efficiency of algorithms."},
    {"question": "What is a Hash Table?", "answer": "A Hash Table is a data structure that stores key-value pairs. It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found"},
    {"question": "What is SQL and how is it used?", "answer": "SQL (Structured Query Language) is a standard language used to manage and manipulate relational databases. It is used to perform operations like querying data, inserting, updating, and deleting records, as well as managing database structure (e.g., creating tables)."},
    {"question": "What are Web APIs?", "answer": "Web APIs (Application Programming Interfaces) are sets of rules and protocols that allow different software applications to communicate with each other over the web."},
    {"question": "What is TCP", "answer": "TCP (Transmission Control Protocol): A connection-oriented protocol that ensures reliable data transmission by establishing a connection and confirming receipt of data."},
    {"question": "What is UDP", "answer": "UDP (User Datagram Protocol): A connectionless protocol that sends data without ensuring that it is received. It is faster but less reliable than TCP."},
    {"question": "What is static binding", "answer": "Also known as early binding, it occurs at compile-time, where the method to be called is determined by the compiler."},
    {"question": "What is dynamic binding", "answer": "Also known as late binding, it occurs at runtime, where the method to be called is determined based on the object's actual class."},
    {"question": "What is Polymorphism in OOP?", "answer": "Polymorphism allows objects of different classes to be treated as instances of a common superclass, enabling method overriding and dynamic method calls."},
    {"question": "What is the 'final' keyword in Java?", "answer": "The final keyword in Java makes variables constants, prevents method overriding, and prevents class inheritance."},
    {"question": "What is the purpose of an index in a database?", "answer": "An index improves the speed of data retrieval operations on a database table, allowing for faster searches by creating pointers to rows."},
]

# Keep track of asked questions
asked_questions = set()

def get_openai_response(user_question):
    """Use OpenAI API to get an answer to any non-interview-related question."""
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo",
            prompt=f"Answer this question comprehensively: {user_question}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error accessing OpenAI API:", e)
        return "I'm sorry, but I'm currently unable to fetch information."

def ask_interview_question():
    """Randomly select an interview question that hasn't been asked yet."""
    remaining_questions = [qa for qa in questions_and_answers if qa["question"] not in asked_questions]
    if not remaining_questions:
        return None
    qa = random.choice(remaining_questions)
    asked_questions.add(qa["question"])
    return qa["question"], qa["answer"]

def main():
    """Function that contains the main operations of the code."""
    print("Welcome to the Interview Bot!")
    print("I’ll ask you interview questions, but you can also ask me anything else for clarity.")
    print("Type 'quit' at any time to exit.")
    
    while True:
        # Ask a new interview question if available
        question, expected_answer = ask_interview_question()
        if question:
            print(f"\nInterview Bot: {question}")
            user_answer = input("Your Answer: ")

            # Check if user wants to quit
            if user_answer.lower() == "quit":
                print("Exiting the chatbot. Good luck with your preparation!")
                break

            # Check similarity (optional)
            similarity = difflib.SequenceMatcher(None, user_answer.lower(), expected_answer.lower()).ratio()
            if similarity > 0.6:
                print("Interview Bot: That’s a good answer!")
            else:
                print("Interview Bot: Consider revising your answer. A strong response could include something like:")
                print(f"Suggested Answer: {expected_answer}")

        else:
            print("\nInterview Bot: You've completed all interview questions.")
            break

        # Allow user to ask any question
        user_question = input("\nDo you have a question for me, or type 'next' for another interview question: ")

        # If user asks a new question
        if user_question.lower() != "next":
            if user_question.lower() == "quit":
                print("Exiting the chatbot. Good luck with your preparation!")
                break
            response = get_openai_response(user_question)
            print("Interview Bot:", response)

if __name__ == "__main__":
    main()