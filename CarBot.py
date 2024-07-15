import random

# Define the facts about cars
facts = [
    "The world’s first automobile was built in 1885 by Karl Benz.",
    "The average car has about 30,000 parts.",
    "The Volkswagen Beetle was in production for 65 years, making it one of the longest-running car models.",
    "The fastest car in the world is the SSC Tuatara, reaching speeds over 300 mph.",
    "The most expensive car ever sold at auction is a 1962 Ferrari 250 GTO, sold for $48.4 million.",
    "The world’s longest traffic jam took place in China, stretching over 62 miles.",
    "The first car radio was invented in 1929.",
    "The Lamborghini company started as a tractor manufacturer.",
    "The average car spends about 95% of its time parked.",
    "The record for the longest car jump was set at 332 feet.",
    "Formula 1 cars can accelerate from 0 to 100 mph and decelerate back to 0 in just four seconds.",
    "The Mercedes-Benz 300SL Gullwing introduced the iconic gullwing doors in 1954.",
    "The Ford Model T, introduced in 1908, was the first car to be mass-produced on assembly lines.",
    "The Bugatti Veyron's tires need to be replaced every 2,500 miles and cost about $42,000 per set.",
    "A Formula 1 car generates so much downforce that it can drive upside down in a tunnel at high speeds.",
    "The Cadillac was the first car to feature modern automotive controls, including a foot pedal accelerator, gearshift, and steering wheel.",
    "In 1941, Henry Ford made a car out of soybeans.",
    "The Rolls-Royce Phantom II from 1930 featured a hood ornament called the 'Spirit of Ecstasy,' which remains iconic to this day.",
    "The Chevrolet Corvette was the first mass-produced car with a fiberglass body, introduced in 1953.",
    "The Porsche 911 has remained in continuous production since 1963, making it one of the oldest sports car nameplates still in production.",
    "The Ford GT40, designed to beat Ferrari at Le Mans, won the race four times in a row from 1966 to 1969.",
    "The McLaren F1, launched in 1992, held the title of the world's fastest production car for over a decade, with a top speed of 240 mph.",
    "The Jeep Wrangler is one of the few vehicles that retains its resale value exceptionally well, often selling for close to its original price even after several years.",
    "The Toyota Prius, introduced in 1997, was the world's first mass-produced hybrid car.",
    "The Tesla Model S, an electric sedan, has a 'Ludicrous Mode' that accelerates from 0 to 60 mph in just 2.4 seconds.",
    "The Bugatti Chiron's engine can consume 15,850 liters of air per minute at full throttle, equivalent to the volume of about eight average human adults.",
    "The McLaren Speedtail, a hypercar, has a top speed of 250 mph and can accelerate from 0 to 186 mph in just 12.8 seconds.",
    "The Koenigsegg Jesko, a high-performance hypercar, has a top speed of over 300 mph and is designed for exceptional handling.",
    "The Ford Mustang Mach-E is an all-electric SUV that pays homage to the classic Mustang while embracing modern technology and sustainability.",
    "The Mercedes-Benz EQS, an all-electric luxury sedan, features a futuristic interior with the MBUX Hyperscreen, spanning over 56 inches."
]

# Randomly shuffle the facts for variety
random.shuffle(facts)

# Define the responses for chatbot interaction
responses = {
    "facts": facts,
    "exit": [
        "Thank you for visiting. Have a great day!",
        "Goodbye! Have a great day!"
    ],
    "default": [
        "I'm sorry, I don't have that information.",
        "Could you please ask something else?"
    ]
}

# Function to respond to user queries
def respond(query):
    query = query.lower()
    if 'fact' in query:
        return random.choice(responses["facts"])
    elif query == 'exit':
        return random.choice(responses["exit"])
    else:
        return random.choice(responses["default"])

# Function to handle the chat session
def chat():
    print("Welcome to CarBot. How can I assist you today?")
    while True:
        user_input = input("User: ")
        response = respond(user_input)
        print("CarBot:", response)
        if user_input.lower() == 'exit':
            break

# Main function
if __name__ == "__main__":
    chat()
