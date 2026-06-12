from student import Student

class AdaptiveQuizEnvironment:

    def __init__(self):

        self.student = Student(0.7)

        self.subject = "Python"

        self.difficulty_map = {
            0: 0.3,  # Easy
            1: 0.6,  # Medium
            2: 0.9   # Hard
        }

        self.difficulty_name = {
            0: "Easy",
            1: "Medium",
            2: "Hard"
        }

        self.correct_streak = 0

    def get_state(self):

        if self.student.ability < 0.4:
            ability_level = 0

        elif self.student.ability < 0.7:
            ability_level = 1

        else:
            ability_level = 2

        streak_level = 0

        if self.correct_streak >= 3:
            streak_level = 1

        return ability_level * 2 + streak_level

    def step(self, action):

        difficulty = self.difficulty_map[action]

        correct = self.student.answer(difficulty)

        # Reward calculation
        if action == 0:

            if correct:
                reward = 0.3
            else:
                reward = -1.0

        elif action == 1:

            if correct:
                reward = 1.0
            else:
                reward = -0.5

        else:

            if correct:
                reward = 1.5
            else:
                reward = -0.2

        # Update streak
        if correct:
            self.correct_streak += 1
        else:
            self.correct_streak = 0

        next_state = self.get_state()

        return next_state, reward, correct