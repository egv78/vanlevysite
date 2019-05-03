import random


class Die:
    def __init__(self, name, meanings, initial, sum_faces):
        # Leave initial as "" for numerical; this changes the results output to numerical total
        self.name = name
        self.meanings = meanings
        self.initial = initial
        self.sum_faces = sum_faces
        self.faces = []
        self.results = []

    def roll(self, times=1):
        self.faces = []
        results = []
        all_faces = []
        roll_times = times
        i = 0
        total = 0
        while i < roll_times:
            number = random.randint(1, len(self.meanings))
            this_face = self.initial
            if self.initial == "":
                this_face += (str(number))  # .zfill(2)
            else:
                this_face += (str(number)).zfill(2)
            this_face += ","
            all_faces.append(this_face)
            this_result = self.meanings[(number-1)]
            results.append(this_result)
            if self.sum_faces:
                total += number
            i += 1
        self.faces = ''.join(all_faces)
        if self.sum_faces:
            self.results = total
        else:
            init_results = ''.join(str(results))
            results = init_results.replace("[", "").replace("]", "")
            self.results = results
        return self.faces, self.results


def summarize(good, bad, force,
              additional_triumph, additional_despair, additional_success, additional_failure,
              additional_advantage, additional_threat, additional_light_pips, additional_dark_pips
              ):
    good_results = ''.join(good)
    bad_results = ''.join(bad)
    force_results = ''.join(force)

    success = additional_success + additional_triumph
    advantage = additional_advantage
    triumph = additional_triumph

    failure = additional_failure + additional_despair
    threat = additional_threat
    despair = additional_despair

    dark_pips = additional_dark_pips
    light_pips = additional_light_pips

    for letter in good_results:
        if letter == 'S':
            success += 1
        elif letter == 'A':
            advantage += 1
        elif letter == 'P':
            success += 1
            triumph += 1

    for letter in bad_results:
        if letter == 'F':
            failure += 1
        elif letter == 'T':
            threat += 1
        elif letter == 'R':
            failure += 1
            despair += 1

    for letter in force_results:
        if letter == 'L':
            light_pips += 1
        elif letter == 'D':
            dark_pips += 1

    net_success = max(0, (success - failure))
    net_failure = max(0, (failure - success))
    net_advantage = max(0, (advantage - threat))
    net_threat = max(0, (threat - advantage))

    results = [triumph, despair, net_success, net_failure, net_advantage, net_threat, dark_pips, light_pips]
    return results


def roll_sw_dice(boost=0, ability=0, proficiency=0, setback=0, difficulty=0, challenge=0, force=0,
                 additional_triumph=0, additional_despair=0, additional_success=0, additional_failure=0,
                 additional_advantage=0, additional_threat=0, additional_light_pips=0, additional_dark_pips=0
                 ):
    boost_sides, boost_results = BOOST.roll(boost)
    ability_sides, ability_results = ABILITY.roll(ability)
    proficiency_sides, proficiency_results = PROFICIENCY.roll(proficiency)
    setback_sides, setback_results = SETBACK.roll(setback)
    difficulty_sides, difficulty_results = DIFFICULTY.roll(difficulty)
    challenge_sides, challenge_results = CHALLENGE.roll(challenge)
    force_sides, force_results = FORCE.roll(force)
    additional_sides = ''
    if additional_triumph > 0:
        for i in range(additional_triumph):
            additional_sides += "Add01,"
    if additional_despair > 0:
        for i in range(additional_despair):
            additional_sides += "Add02,"
    if additional_success > 0:
        for i in range(additional_success):
            additional_sides += "Add03,"
    if additional_failure > 0:
        for i in range(additional_failure):
            additional_sides += "Add04,"
    if additional_advantage > 0:
        for i in range(additional_advantage):
            additional_sides += "Add05,"
    if additional_threat > 0:
        for i in range(additional_threat):
            additional_sides += "Add06,"
    if additional_light_pips > 0:
        for i in range(additional_light_pips):
            additional_sides += "Add07,"
    if additional_dark_pips > 0:
        for i in range(additional_dark_pips):
            additional_sides += "Add08,"

    faces_strings = (boost_sides + ability_sides + proficiency_sides + setback_sides + difficulty_sides +
                     challenge_sides + force_sides + additional_sides)

    good_results = boost_results + ability_results + proficiency_results
    bad_results = setback_results + difficulty_results + challenge_results

    net_results = summarize(good_results, bad_results, force_results,
                            additional_triumph, additional_despair, additional_success, additional_failure,
                            additional_advantage, additional_threat, additional_light_pips, additional_dark_pips
                            )

    return faces_strings, net_results


# faces for SW and Genesys Dice
# (S)uccess, (A)dvantage, Trium(P)h
# (F)ailure, (T)hreat, Despai(R)
# (L)ight, (D)ark
boost_meanings = ["-", "-", "S", "SA", "AA", "A"]
ability_meanings = ["-", "S", "S", "SS", "A", "A", "SA", "AA"]
proficiency_meanings = ["-", "S", "S", "SS", "SS", "A", "SA", "SA", "SA", "AA", "AA", "P"]
setback_meanings = ["-", "-", "F", "F", "T", "T"]
difficulty_meanings = ["-", "F", "FF", "T", "T", "T", "TT", "FT"]
challenge_meanings = ["-", "F", "F", "FF", "FF", "T", "T", "FT", "FT", "TT", "TT", "R"]
force_meanings = ["D", "D", "D", "D", "D", "D", "DD", "L", "L", "LL", "LL", "LL"]

# SW and Genesys Dice
BOOST = Die("Boost", boost_meanings, "B", False)
SETBACK = Die("Setback", setback_meanings, "S", False)
ABILITY = Die("Ability", ability_meanings, "A", False)
DIFFICULTY = Die("Difficulty", difficulty_meanings, "D", False)
PROFICIENCY = Die("Proficiency", proficiency_meanings, "P", False)
CHALLENGE = Die("Challenge", challenge_meanings, "C", False)
FORCE = Die("Force", force_meanings, "F", False)


# Polyhedral Dice
# Initial left as "" to prevent leading zeroes
D4 = Die("D4", range(1, 5), "", True)
D6 = Die("D6", range(1, 7), "", True)
D8 = Die("D8", range(1, 9), "", True)
D10 = Die("D10", range(1, 11), "", True)
D12 = Die("D12", range(1, 13), "", True)
D20 = Die("D20", range(1, 21), "", True)
D100 = Die("D4", range(1, 101), "", True)


def roll_myz_dice(base=0, skill=0, gear=0, is_pushed=False,
                  add_trauma=0, add_damage=0, add_failure=0,
                  add_success_base=0, add_success_gear=0, add_success_skill=0):
    if not is_pushed:
        base_sides, base_results = BASE.roll(base)
        gear_sides, gear_results = GEAR.roll(gear)
    else:
        base_sides, base_results = PUSHED_BASE.roll(base)
        gear_sides, gear_results = PUSHED_GEAR.roll(gear)
    if skill < 0:
        skill_sides, skill_results = NEGATIVE.roll(abs(skill))
    else:
        skill_sides, skill_results = SKILL.roll(skill)

    additional_sides = ''
    if add_trauma > 0:
        for i in range(add_trauma):
            additional_sides += "PU_BA01,"
    if add_success_base > 0:
        for i in range(add_success_base):
            additional_sides += "PU_BA06,"
    if add_failure > 0:
        for i in range(add_failure):
            additional_sides += "NE06,"
    if add_success_skill > 0:
        for i in range(add_success_skill):
            additional_sides += "SK06,"
    if add_damage > 0:
        for i in range(add_damage):
            additional_sides += "PU_GE01,"
    if add_success_gear > 0:
        for i in range(add_success_gear):
            additional_sides += "PU_GE06,"

    faces_string = base_sides + skill_sides + gear_sides

    successes = add_success_base + add_success_gear + add_success_skill - add_failure
    trauma = add_trauma
    damage = add_damage

    available_base = base
    available_skill = skill
    available_gear = gear

    base_success = 0
    skill_success = 0
    gear_success = 0
    push_trauma = 0
    push_failure = 0
    push_damage = 0

    base_string = "".join(base_results)
    for letter in base_string:
        if letter == 'S':
            successes += 1
            base_success += 1
            available_base -= 1
        elif letter == 'A':
            push_trauma += 1
            available_base -= 1
        elif letter == 'T':
            trauma += 1
            available_base -= 1

    gear_string = "".join(gear_results)
    for letter in gear_string:
        if letter == 'S':
            successes += 1
            gear_success += 1
            available_gear -= 1
        elif letter == 'E':
            push_damage += 1
            available_gear -= 1
        elif letter == 'D':
            damage += 1
            available_gear -= 1

    skill_string = "".join(skill_results)
    for letter in skill_string:
        if letter == 'S':
            successes += 1
            skill_success += 1
            available_skill -= 1
        elif letter == 'F':
            successes -= 1
            push_failure += 1
            available_skill += 1

    if successes > 0:
        success = successes
        failure = 0
    elif successes < 0:
        success = 0
        failure = abs(successes)
    else:
        success = 0
        failure = 0

    net_results = [success, failure, trauma, damage, available_base, available_skill, available_gear,
                   base_success, skill_success, gear_success, push_trauma, push_failure, push_damage]
    can_be_pushed = (available_base + available_gear) > 0 or available_skill > 0

    return faces_string, net_results, can_be_pushed, additional_sides


# Mutant Year Zero
# Meanings
base_meanings = ['A', '-', '-', '-', '-', 'S']
skill_meanings = ['-', '-', '-', '-', '-', 'S']
gear_meanings = ['E', '-', '-', '-', '-', 'S']
pushed_base_meanings = ['T', '-', '-', '-', '-', 'S']
pushed_gear_meanings = ['D', '-', '-', '-', '-', 'S']
negative_skill_meanings = ['-', '-', '-', '-', '-', 'F']
d66_meanings = [11, 12, 13, 14, 15, 16, 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35, 36,
                41, 42, 43, 44, 45, 46, 51, 52, 53, 54, 55, 56, 61, 62, 63, 64, 65, 66]
d666_meanings = [111, 112, 113, 114, 115, 116, 121, 122, 123, 124, 125, 126, 131, 132, 133, 134, 135, 136,
                 141, 142, 143, 144, 145, 146, 151, 152, 153, 154, 155, 156, 161, 162, 163, 164, 165, 166,
                 211, 212, 213, 214, 215, 216, 221, 222, 223, 224, 225, 226, 231, 232, 233, 234, 235, 236,
                 241, 242, 243, 244, 245, 246, 251, 252, 253, 254, 255, 256, 261, 262, 263, 264, 265, 266,
                 311, 312, 313, 314, 315, 316, 321, 322, 323, 324, 325, 326, 331, 332, 333, 334, 335, 336,
                 341, 342, 343, 344, 345, 346, 351, 352, 353, 354, 355, 356, 361, 362, 363, 364, 365, 366,
                 411, 412, 413, 414, 415, 416, 421, 422, 423, 424, 425, 426, 431, 432, 433, 434, 435, 436,
                 441, 442, 443, 444, 445, 446, 451, 452, 453, 454, 455, 456, 461, 462, 463, 464, 465, 466,
                 511, 512, 513, 514, 515, 516, 521, 522, 523, 524, 525, 526, 531, 532, 533, 534, 535, 536,
                 541, 542, 543, 544, 545, 546, 551, 552, 553, 554, 555, 556, 561, 562, 563, 564, 565, 566,
                 611, 612, 613, 614, 615, 616, 621, 622, 623, 624, 625, 626, 631, 632, 633, 634, 635, 636,
                 641, 642, 643, 644, 645, 646, 651, 652, 653, 654, 655, 656, 661, 662, 663, 664, 665, 666
                 ]

# MYZ Dice
BASE = Die("Base", base_meanings, "BA", False)
GEAR = Die("Gear", gear_meanings, "GE", False)
SKILL = Die("Skill", skill_meanings, "SK", False)
NEGATIVE = Die("Negative", negative_skill_meanings, "NE", False)
PUSHED_BASE = Die("Base", pushed_base_meanings, "PU_BA", False)
PUSHED_GEAR = Die("Gear", pushed_gear_meanings, "PU_GE", False)

# Initial left as "" to prevent leading zeroes
D6_MYZ = Die("MYZ_D6", range(1, 7), "", False)
D66_MYZ = Die("MYZ_D66", d66_meanings, "", False)
D666_MYZ = Die("MYZ_D666", d666_meanings, "", False)

