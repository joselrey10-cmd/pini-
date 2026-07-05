from .profile import BALANCED

def default_profile_report():
    p=BALANCED
    return {
        "profile":p.name,
        "weights":{
            "constraints":p.weights.constraints,
            "teacher":p.weights.teacher,
            "student":p.weights.student,
            "rooms":p.weights.rooms,
        }
    }
