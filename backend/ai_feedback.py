import random

positive_feedback = [

    "Excellent technical depth.",
    "Strong backend engineering mindset.",
    "Clear understanding of API architecture.",
    "Very solid communication skills.",
    "Good problem solving approach.",
    "Strong understanding of scalability.",
]

improvement_feedback = [
    "Try giving more real-world examples.",
    "Expand more on performance optimization.",
    "Add more technical detail.",
    "Explain tradeoffs more clearly.",
    "Focus more on scalability concerns.",
    "Discuss security implications deeper.",
]

def generate_feedback(score):

    if score >= 80:
        return {
            "level": "excellent",
            "feedback": random.choice(positive_feedback)
        }
    
    elif score >= 50:
        return {
            "level": "good",
            "feedback": "Solid answer but could use more depth."
        }
    
    return {
        "level": "improve",
        "feedback": random.choice(improvement_feedback)
    }