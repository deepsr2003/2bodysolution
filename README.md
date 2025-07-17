This project works in three main steps:
1. Teach the AI
First, I act like a "physicist" and use real physics equations to generate thousands of examples of perfect planetary orbits. Then, I show all this data to a "student" AI model (scikit-learn). The AI's only job is to learn the pattern of how planets move, without ever seeing the actual physics formulas.
2. Build the App
I create a simple website with a backend server. The server holds the AI's "brain" (the trained model). A user can go to the website and input starting conditions for a new, unseen planet.
3. Compare the Results
When the user clicks "Simulate," the backend does two things simultaneously:
It calculates the perfect orbit using the original physics formulas.
It asks the AI to predict the orbit, one step at a time.
Finally, the website draws both paths on the screen—a blue line for perfect physics and an orange line for the AI's prediction. The goal is to visually see how well the AI learned physics just by observing data.
# 2bodysolution



├── backend
│   ├── app.py
│   ├── data
│   ├── generate_data.py
│   ├── models
│   └── train_model.py
├── frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
├── README.md
└── requirements.txt

5 directories, 8 files

folder structure
