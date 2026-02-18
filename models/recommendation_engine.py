def analyze_performance(marks):
    weak = []
    average = []
    strong = []

    for m in marks:
        if m.score < 40:
            weak.append(m.subject)
        elif m.score <= 70:
            average.append(m.subject)
        else:
            strong.append(m.subject)

    return weak, average, strong


def generate_study_plan(weak, average, strong):
    plan = {}

    for subject in weak:
        plan[subject] = "Revise basics + watch YouTube lectures + practice 5 questions daily"

    for subject in average:
        plan[subject] = "Practice PYQs + revise notes 30 mins daily"

    for subject in strong:
        plan[subject] = "Just weekly revision"

    return plan
