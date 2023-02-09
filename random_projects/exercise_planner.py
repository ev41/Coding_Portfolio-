#READ ME:
"""
This is an exercise schedule generator, and is also a work in progress. So far, each week in the schedule is the same, in other words, 
    it isn't rotating the way I want it to.
Additionally, I need to find a way to show the output as a multi-dimensional (insert more appropriate description) dataframe that 
displays both the muscle groups being worked in any given week, as well as the corresponding exercises & rep ranges. 

Tips to self: Do more digging into dataframes, as well as how iterate dictionary lists / shift the order of elements for each iteration.
"""

import pandas as pd
import random
import pickle


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


val = input(
    "Are you creating a new workout plan, or do you have an existing plan?")

if "new" in val:
    wo_interval = int(input('How many days in a row do you want to exercise?'))
    rest_day = 1

    # Step 1: Create a nested dictionary with muscle groups and corresponding exercises and reps
    exercise_dict = {
        "Legs": {"Bulgarian Split Squats": '3 x 8', "RDLs": '3 x 12', "KoT Lunges": '3 x 8-12 each', 'Hamstring Curls': '3 x 8', 'Calf Raises': '4 x 6+', 'Hip flexor/abductor machines': '3 x 8 each'},
        "Back": {"Pull-ups": '4 x 6-8', "Cable Rows": 'RPT', "Lat Pulldowns": 'RPT'},
        "Chest": {"Incline DB Press": 'RPT', "Flat Bench Machine": 'RPT', "Fly Machine": '3x10', 'Pushups': '50'},
        "Shoulders": {"DB Shoulder Press": 'RPT', "Lateral Raises": '5 x 12-15', "Rear Delt Flies": '4 x 8-12', 'DB External Rotation': '3 x 6-10'},
        "Arms": {"Incline Bicep Curls": '4x8', "DB Skullcrushers": '4 x 8 each', 'Rope Pushdowns': '4 x 6-10', 'Kickbacks': '3 x 8-12'}  
       
    }

    # Convert dictionary to pandas dataframe
    df = pd.DataFrame(exercise_dict)

    # Step 2: Assign muscle groups to days of the week, following the specified order
    days_of_week = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]
    muscle_groups = list(df.columns)
    schedule = {}
    remaining_muscle_groups = []
    week = 1
    while week <= 12:
        print(f"Week {week}:")
        # if remaining_muscle_groups:
        #     muscle_groups = remaining_muscle_groups + muscle_groups
        #     remaining_muscle_groups = []
        for i, day in enumerate(days_of_week):
            if i % wo_interval == 0 and i != 0:
                schedule[day] = "Rest Day"
            else:
                if muscle_groups:
                    schedule[day] = muscle_groups.pop(0)
                else:
                    remaining_muscle_groups.append(day)
                    break
        print(schedule)
        week += 1
    save_obj(schedule, "workout_plan")

inp = input('Which week do you want to see the workout schedule for?')
week = int(inp)
schedule = load_obj("workout_plan")

for day, workout in schedule.items():
    if "Week" in day:
        if week in int(day.split()[1]):
            print(day)
            for muscle_group, exercises in exercise_dict.items():
                if muscle_group == workout:
                    print(muscle_group)
                    for exercise, reps in exercises.items():
                        print(f"{exercise}: {reps}")
