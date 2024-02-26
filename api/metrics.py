# Performance metric

# Objective Achievement Rate (OAR)
 	
# OAR=[Completed Objectives/Assigned Objectives] * 100

def oar(list_1, list_2):
    return (len(list_2) / len(list_1))*100


# Calculate the overall progress at day x using the weighted average formula

def calculate_overall_progress(weights, progress, x):
    total_weighted_progress = 0
    for i in range(len(weights)):
        if i <= x:
            total_weighted_progress += progress[i] * weights[i]
    return total_weighted_progress

weights = [0.2, 0.5, 0.3]
progress = [1.5, 0.4, 0.3]
x = 2  # Calculate progress at day 2
overall_progress = calculate_overall_progress(weights, progress, x)
print(f"Overall progress at day {x}: {overall_progress * 100}%")


#n = 5 and we are on day 1

daily_progress = 0.59
total_days = 5
overall_progress_first_day = daily_progress / total_days

# day 2, daily_progress = 0.40 ie 40%
daily_progress_day1 = 0.59
daily_progress_day2 = 0.40

overall_progress_day1 = daily_progress_day1
overall_progress_day2 = overall_progress_day1 + daily_progress_day2
print(f"Overall progress after two day: {overall_progress_day2  * 100}%")

remaining_days = 3
overall_progress_remaining_days = overall_progress_day2 / 2  # Average progress per day for the remaining days
overall_progress_remaining = overall_progress_remaining_days * remaining_days
