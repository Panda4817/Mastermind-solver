from logic import *
from itertools import combinations
from copy import deepcopy

# Number of pairs
num_of_pairs = 5

# Retrive data from txt file
f = open("/home/kanta/are_you_the_one/ayto_smaller_data.txt", "r")
data = f.read()
lst = data.split("\n\n")
male = {}
female = {}
for l in lst[0].split("\n"):
    sub_lst = l.split()
    male[sub_lst[0]] = sub_lst[1]
for l in lst[1].split("\n"):
    sub_lst = l.split()
    female[sub_lst[0]] = sub_lst[1]


# Separate letters and numbers from names
male_set = set(male.keys())
female_set = set(female.keys())

# From truth booth
not_matched = {"A-0", "E-3"}
matches = {"B-1", "D-2", "A-3"}

# Setup of model checking algorithm but too slow with num_of_pairs pairs
symbols = []
for i in range(num_of_pairs):
    for m in male_set:
        if f"{m}-{i}" in not_matched:
            continue
        symbols.append(Symbol(f"{m}-{i}"))

# Knowledge base
knowledge = And()

# Information from truth booth
for m in not_matched:
    knowledge.add(Not(Symbol(m)))
# Confirmed matches
for m in matches:
    knowledge.add(Symbol(m))

# Each male has one female
for m in male_set:
    in_matches = [pair for pair in matches if m in pair.split("-")]
    if in_matches:
        continue
    else:
        or_state = Or()
        for i in range(num_of_pairs):
            if f"{m}-{i}" in not_matched:
                continue
            or_state.add(Symbol(f"{m}-{i}"))
        knowledge.add(or_state)

# Only one female per male
for m in male_set:
    in_matches = [pair for pair in matches if m in pair.split("-")]
    if in_matches:
        continue
    else:
        for i in range(num_of_pairs):
            for j in range(num_of_pairs):
                if i != j and f"{m}-{i}" not in not_matched and f"{m}-{j}" not in not_matched:
                    knowledge.add(Implication(
                        Symbol(f"{m}-{i}"), Not(Symbol(f"{m}-{j}"))
                    ))

# Only one male per female
for i in range(num_of_pairs):
    in_matches = [pair for pair in matches if str(i) in pair.split("-")]
    if in_matches:
        continue
    else:
        for m1 in male_set:
            for m2 in male_set:
                if m1 != m2 and f"{m1}-{i}" not in not_matched and f"{m2}-{i}" not in not_matched:
                    knowledge.add(Implication(
                        Symbol(f"{m1}-{i}"), Not(Symbol(f"{m2}-{i}"))
                    ))


# Function to calculate number of known matches in the total matches found
def confirmed_match_per_ep(ep):
    global matches
    number_confirmed = 0
    for m in matches:
        if m in ep:
            number_confirmed += 1
    return number_confirmed

# Use what is known to update the knowledge base
def eliminate_matches(ep, num):
    global matches, not_matched
    number_confirmed = confirmed_match_per_ep(ep)
    if number_confirmed == num:
        for pair in ep:
            if pair not in matches and pair not in not_matched:
                not_matched.add(pair)
    return number_confirmed


def evaluate_episode(ep, num):
    global matches, not_matched
    or_statement = Or()
    
    # Eliminate matches based on new data
    number_confirmed = eliminate_matches(ep, num)

    # Combinations
    combi = {c: deepcopy(ep) for c in combinations(ep, num)}

    for k, v in combi.items():
        # Filter the keys - known matches and/or potential matches
        cont = False
        found_confirmed = 0
        for pair in k:
            if pair in not_matched:
                cont = True
                break
            if pair in matches:
                found_confirmed += 1
                continue
            for m in matches:
                p = pair.split("-")
                mf = m.split("-")
                if p[0] == mf[0] or p[1] == mf[1]:
                    cont = True
                    break
        
        if cont or found_confirmed != number_confirmed:
            continue

        # Add to knowledge base
        match = And()
        for pair in k:
            v.remove(pair)
            match.add(Symbol(pair))
        not_match = And()
        for pair in v:
            not_match.add(Not(Symbol(pair)))
        
        or_statement.add(And(match, not_match))
    
    return or_statement


# Data from episodes
ep1 = {"A-3", "C-0", "B-2", "D-4", "E-1"}
# 2 matches
knowledge.add(evaluate_episode(ep1, 2))

ep2 = {"A-3", "C-0", "B-1", "D-4", "E-2"}
# 3 matches
knowledge.add(evaluate_episode(ep2, 3))

for symbol in symbols:
    if model_check(knowledge, symbol):
        m_f = symbol.name.split("-")
        print(symbol, male[m_f[0]], female[m_f[1]])