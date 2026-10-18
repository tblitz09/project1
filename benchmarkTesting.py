from itertools import combinations
import random
import matplotlib.pyplot as plt
import time

def baseline_solution(tasks):
    max_revenue = 0
    best_schedule = []

    for i in range(1, len(tasks) + 1):
        for subset in combinations(tasks, i):
        # Takes all combinations of the tasks from the input list and makes each a subset

            current_schedule = list(subset)
            # convert the subsets of combinations to lists
            current_schedule.sort()
            # sort them to check for deadlines easier
            is_valid = True
            current_revenue = 0

            for day, (deadline, pay) in enumerate(current_schedule, start=1):
                if day > deadline:
                    is_valid = False
                    break
                    # because the deadline was missed
                current_revenue = current_revenue + pay

            if is_valid and current_revenue > max_revenue:
                max_revenue = current_revenue
                best_schedule = current_schedule

    return max_revenue, best_schedule

def freelanceTasksGreedy(tasks):
    tasks = sorted(tasks, key=lambda x: x[1], reverse = True)
    max_deadline = max((deadline for deadline, _ in tasks))
    schedule = [None] * (max_deadline)
    revenue = 0
    for deadline, pay in tasks:
        for day in range(min(deadline - 1, max_deadline), -1, -1):
            if schedule[day] is None:
                schedule[day] = (deadline, pay)
                revenue += pay
                break
    return revenue, schedule

size = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

def benchmarkTesting():
     # Creates input sizes that will be used to test speed at different sizes
    slow_list = []
    fast_list = [] # Creates lists to take all the average times

    for n in size:
        slow_times = []
        fast_times = []
        tasks = []
        for i in range(n + 1):
            deadline = random.randint(1, 10)
            pay = random.randint(10, 100)
            tasks.append([deadline, pay])
        
         # Creates data that is a list of numbers from 1 to n

        for j in range (0, 10): # Tests each algorithm 10 times per size
            start_time = time.perf_counter()
            baseline_solution(tasks)
            end_time = time.perf_counter()
            slow_times.append(end_time - start_time)
    
            start_time_2 = time.perf_counter()
            freelanceTasksGreedy(tasks)
            end_time_2 = time.perf_counter()
            fast_times.append(end_time_2 - start_time_2)
        fast_average = sum(fast_times) / 10
        slow_average = sum(slow_times) / 10 # Creates an average of the 10 times to see the average of the algorithms per size
        slow_list.append(slow_average)
        fast_list.append(fast_average) # Puts these average times into a list to be graphed
        print(f"for n = {n} (n = size)")
        print(f"Fast alg average time = {fast_average} seconds")
        print(f"Slow alg average time = {slow_average} seconds")
        print()

    # Plot Code
    plt.figure()
    plt.plot(size, fast_list, label="Greedy Algorithm Time", color="red", marker="o")
    plt.plot(size, slow_list, label="Baseline Algorithm Time", color="blue", marker="s")
    plt.title("Comparing Baseline vs Greedy Algorithms with Varied Amounts of Tasks to Sort")
    plt.xlabel("amount of tasks")
    plt.ylabel("average time (seconds)")
    plt.legend()
    plt.grid((True))
    plt.savefig('results.png', dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure()
    plt.plot(size, fast_list, label="Greedy Algorithm Time", color="red", marker="o")
    plt.plot(size, slow_list, label="Baseline Algorithm Time", color="blue", marker="s")
    plt.yscale('log')
    plt.title("Comparing Baseline vs Greedy Algorithms with Varied Amounts of Tasks to Sort (log scale)")
    plt.xlabel("amount of tasks")
    plt.ylabel("average time (log scale seconds)")
    plt.legend()
    plt.grid((True))
    plt.savefig('resultslog.png', dpi=300, bbox_inches='tight')

benchmarkTesting()