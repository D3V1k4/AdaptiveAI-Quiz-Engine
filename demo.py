import numpy as np
from colorama import Fore, init
import matplotlib.pyplot as plt
from agent import QLearningAgent
from question_generator import generate_question

init(autoreset=True)

print(Fore.CYAN + "=" * 60)
print(Fore.CYAN + "           AdaptiveAI Quiz Engine")
print(Fore.CYAN + "           Powered by RL + Gemini")
print(Fore.CYAN + "=" * 60)

subjects = [
    "Python",
    "DAA",
    "Operating Systems",
    "DBMS",
    "Computer Networks"
]

print("\nAvailable Subjects:\n")

for i, subject in enumerate(subjects):
    print(f"{i+1}. {subject}")

while True:

    try:
        choice = int(input("\nEnter Choice (1-5): "))

        if 1 <= choice <= len(subjects):
            break

        print("Invalid Choice.")

    except ValueError:
        print("Please enter a number.")

subject = subjects[choice - 1]

agent = QLearningAgent()

try:
    agent.q_table = np.load("q_table.npy")
except:
    print("q_table.npy not found. Run train.py first.")
    exit()

difficulty_map = {
    0: "Easy",
    1: "Medium",
    2: "Hard"
}

score = 0
total_questions = 5

# Starting state
current_state = 4
difficulty_history = []
difficulty_numeric = []
performance_history = []
for question_no in range(1, total_questions + 1):

    action = np.argmax(
        agent.q_table[current_state]
    )

    difficulty = difficulty_map[action]
    difficulty_history.append(difficulty)
    difficulty_numeric.append(action)
    print(
        Fore.BLUE +
        f"\nAdaptive State: {current_state}"
    )

    question = generate_question(
        subject,
        difficulty
    )

    print("\n")
    print(Fore.YELLOW + "=" * 60)
    print(Fore.YELLOW + f"Question {question_no}/{total_questions}")
    print(Fore.YELLOW + f"Subject: {subject}")
    print(Fore.YELLOW + f"Difficulty: {difficulty}")
    print(Fore.YELLOW + "=" * 60)

    print("\n" + question["question"])

    print("\nOptions:")

    for i, option in enumerate(question["options"]):
        print(f"{chr(65+i)}) {option}")

    answer = input("\nYour Answer: ").strip().upper()

    correct_answer = question["answer"]

    correct_option = None

    for i, option in enumerate(question["options"]):

        if option.lower().strip() == correct_answer.lower().strip():

            correct_option = chr(65 + i)
            break

    # Gemini sometimes returns only A/B/C/D
    if correct_option is None:

        if len(correct_answer.strip()) == 1:
            correct_option = correct_answer.strip().upper()

    is_correct = (
        answer == correct_option
        or answer.lower() == correct_answer.lower()
    )

    if is_correct:

        score += 1

        print(
            Fore.GREEN +
            "\n✅ Correct!"
        )
        performance_history.append(1)

        # Move to higher state
        if current_state < 5:
            current_state += 1

    else:

        print(
            Fore.RED +
            "\n❌ Incorrect!"
        )
        performance_history.append(0)

        if correct_option:

            print(
                Fore.GREEN +
                f"Correct Answer: {correct_option}) {correct_answer}"
            )

        else:

            print(
                Fore.GREEN +
                f"Correct Answer: {correct_answer}"
            )

        # Move to lower state
        if current_state > 0:
            current_state -= 1

    print(
        Fore.CYAN +
        f"Current Score: {score}/{question_no}"
    )

print("\n")
print(Fore.MAGENTA + "=" * 60)
print(Fore.MAGENTA + "                 QUIZ REPORT")
print(Fore.MAGENTA + "=" * 60)

accuracy = (score / total_questions) * 100

print(f"\nSubject             : {subject}")
print(f"Questions Attempted : {total_questions}")
print(f"Correct Answers     : {score}")
print(f"Wrong Answers       : {total_questions - score}")
print(f"Accuracy            : {accuracy:.2f}%")
print(f"Final Learning State: {current_state}")

print()

if accuracy >= 80:

    print(
        Fore.GREEN +
        "Recommended Level: Hard"
    )

elif accuracy >= 50:

    print(
        Fore.YELLOW +
        "Recommended Level: Medium"
    )

else:

    print(
        Fore.RED +
        "Recommended Level: Easy"
    )
print("\nDifficulty Path:")
print(" → ".join(difficulty_history))
print(Fore.MAGENTA + "\n" + "=" * 60)
plt.figure(figsize=(8, 4))

plt.plot(
    range(1, len(performance_history) + 1),
    performance_history,
    marker="o"
)

plt.yticks([0, 1], ["Wrong", "Correct"])

plt.title("Student Performance During Quiz")
plt.xlabel("Question Number")
plt.ylabel("Result")

plt.grid(True)

plt.show()