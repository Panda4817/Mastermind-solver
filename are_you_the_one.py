from itertools import combinations
from copy import deepcopy

# Number of pairs
num_of_pairs = 10

# Retrive name data from txt file
f = open("/home/kanta/are_you_the_one/are_you_the_one.txt", "r")
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

# Set up knowledge base
male_set = set(male.keys())
female_set = set(female.keys())
all_combinations  = [(x, y) for x in male_set for y in female_set]

# Filter knowledge base
# From truth booth of the show
not_matched = [("D", "8"), ("F","5"), ("H","9"), ("E","5"), ("B","1"), ("I", "6"), ("H", "4")]
matches = [("E","3"), ("D","7"), ("J", "6")]
for pair in not_matched:
    all_combinations.remove(pair)
for pair in matches:
    for i in range(num_of_pairs):
        if str(i) != pair[1] and (pair[0], str(i)) in all_combinations:
            all_combinations.remove((pair[0], str(i)))
    for m in male_set:
        if m != pair[0] and (m, pair[1]) in all_combinations:
            all_combinations.remove((m, pair[1]))

# Store possible combos
possible_combos = []

# Function to calculate number of known matches in the total matches found
def confirmed_match_per_ep(ep):
    number_confirmed = 0
    for m in matches:
        if m in ep:
            number_confirmed += 1
    return number_confirmed

# Use what is known to update the knowledge base
def eliminate_matches(ep, num):
    global all_combinations, possible_combos, matches, not_matched
    number_confirmed = confirmed_match_per_ep(ep)
    if number_confirmed == num:
        for pair in ep:
            if pair not in matches:
                try:
                    all_combinations.remove(pair)
                    not_matched.append(pair)
                except ValueError:
                    continue

# Evaluate an episode to gain likely combos of people                    
def evaluate_episode(ep, num, most_likely=[]):
    global all_combinations, possible_combos, matches, not_matched
    number_confirmed = confirmed_match_per_ep(ep)

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
                if pair[0] == m[0] or pair[1] == m[1]:
                    cont = True
                    break
        
        if cont or found_confirmed != number_confirmed:
            continue

        # Find other matches (ignoring letters and numbers in the keys)
        combos = []
        for pair in v:
            if pair in k and pair not in combos:
                combos.append(pair)
            else:
                for p in all_combinations:
                    if p != pair and p not in combos:
                        for g in k:
                            if p[0] == g[0] or p[1] == g[1]:
                                break
                        else:
                            for m in most_likely:
                                if p != m and p[0] == m[0]:
                                    break
                                elif p != m and p[1] == m[1]:
                                    break
                            else:
                                combos.append(p)
        
        if len(combos) >= num_of_pairs and len(combos) <= 11:
            # Reduce the combos to 10 if possible
            combos.sort(key=lambda x: x[0])
            counts = {}
            for c in combos:
                if c[0] in counts:
                    counts[c[0]].append(c[1])
                else:
                    counts[c[0]] = [c[1]]
            for m in male_set:
                if m not in counts:
                    break
            else:
                new_combo = []
                for k, v in counts.items():
                    if len(v) > 1:
                        for ke, ve in counts.items():
                            if ke != k and len(ve) == 1 and ve[0] in v:
                                v.remove(ve[0])
                    for val in v:
                        new_combo.append((k, val))
                # Check a combo is not already in the list of combos                
                for p in possible_combos:
                    p.sort(key=lambda x: x[0])
                    if "".join(f"{x}" for x in new_combo) == "".join(f"{x}" for x in p):
                        break
                else:
                    possible_combos.append(new_combo)

# Find most likely pairs based on how many match ups there have been
# Ignore known matches and remove any matches that cannot be
def most_likely(episodes, matches_per_ep):
    global matches, not_matched
    common_matches = {}
    for ep, i in zip(episodes, range(8)):
        confirmed_matches = confirmed_match_per_ep(ep)
        if confirmed_matches == matches_per_ep[i]:
            continue
        for pair in ep:
            if pair in not_matched:
                continue
            contradict = [m for m in matches if m[0] == pair[0] or m[1] == pair[1]]
            if contradict:
                continue
            if pair not in common_matches:
                common_matches[pair] = 1
            else:
                common_matches[pair] += 1
               
    sorted_lst = sorted(common_matches.items(), key=lambda x: x[1], reverse=True)
    # Return only the top 4
    return [m[0] for m in sorted_lst][0:4]


# Data from show
ep1 = [("J", "6"), ("F", "8"), ("A", "2"), ("B", "4"), ("H", "9"), ("D", "5"), ("G", "7"), ("I", "0"), ("E", "3"), ("C", "1")]
# 2 matches
eliminate_matches(ep1, 2)

ep2 = [("F", "0"), ("B", "1"), ("G", "2"), ("J", "3"), ("H", "4"), ("E", "5"), ("I", "6"), ("D", "7"), ("A", "8"), ("C", "9")]
# 4 matches
eliminate_matches(ep2, 4)

ep3 = [("A", "2"), ("B", "1"), ("C", "7"), ("D", "9"), ("E", "3"), ("F", "0"), ("G", "8"), ("H", "5"), ("I", "6"), ("J", "4")]
# 2 matches
eliminate_matches(ep3, 2)

ep4 = [("E", "3"), ("C", "7"), ("J", "5"), ("B", "9"), ("I", "2"), ("F", "6"), ("A", "0"), ("D", "1"), ("H", "8"), ("G", "4")]
# 2 matches
eliminate_matches(ep4, 2)

ep5 = [("E", "3"), ("F", "0"), ("G", "5"), ("J", "6"), ("H", "4"), ("C", "9"), ("A", "8"), ("D", "7"), ("B", "2"), ("I", "1")]
# 5 matches
eliminate_matches(ep5, 5)

ep7 = [("E", "3"), ("D", "7"), ("H", "4"), ("J", "6"), ("G", "9"), ("C", "2"), ("A", "1"), ("B", "8"), ("I", "5"), ("F", "0")]
# 5 matches
eliminate_matches(ep7, 5)

ep8 = [("E", "3"), ("D", "7"), ("C", "4"), ("J", "6"), ("B", "9"), ("H", "2"), ("I", "1"), ("A", "8"), ("G", "5"), ("F", "0")]
# 7 matches
eliminate_matches(ep8, 7)

ep9 = [("E", "3"), ("D", "7"), ("J", "6"), ("H", "4"), ("I", "5"), ("A", "8"), ("B", "9"), ("G", "2"), ("C", "1"), ("F", "0")]
# 8 matches
eliminate_matches(ep9, 8)


# Rank from most likely to least (not including known matches)
episodes = [ep1, ep2, ep3, ep4, ep5, ep7, ep8, ep9]
matches_per_ep = [2, 4, 2, 2, 5, 5, 7, 8]
most_likely_lst = most_likely(episodes, matches_per_ep)

# evaluate likely combos from episode with the max matches
index = matches_per_ep.index(max(matches_per_ep))
evaluate_episode(episodes[index], matches_per_ep[index]) # Could add a third argument - most likely list

# Print out likely combos
if possible_combos:
    for p in possible_combos:
        p.sort(key=lambda x:x[0])
        for pair in p:
            print(pair[0], male[pair[0]], pair[1], female[pair[1]])
        print()
else:
    print("No conclusive result. Add most likely list to the evaluation function.")
