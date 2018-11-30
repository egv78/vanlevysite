import random


class Die:
    def __init__(self, name, meanings, initial):
        self.name = name
        self.meanings = meanings
        self.initial = initial
        self.faces = []
        self.results = []

    def roll(self, times=1):
        self.faces = []
        self.results = []
        all_faces = []
        self.times = times
        i = 0
        while i < self.times:
            number = random.randint(1, len(self.meanings))
            this_face = self.initial
            this_face += (str(number).zfill(2))
            this_face += ","
            all_faces.append(this_face)
            this_result = self.meanings[(number-1)]
            self.results.append(this_result)
            i += 1
        self.faces = ''.join(all_faces)
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

    faces_strings = boost_sides + ability_sides + proficiency_sides + setback_sides + difficulty_sides + \
                    challenge_sides + force_sides + additional_sides

    good_results = boost_results + ability_results + proficiency_results
    bad_results = setback_results + difficulty_results + challenge_results

    net_results = summarize(good_results, bad_results, force_results,
                            additional_triumph, additional_despair, additional_success, additional_failure,
                            additional_advantage, additional_threat, additional_light_pips, additional_dark_pips
                            )

    return faces_strings, net_results


boost_meanings = ["-", "-", "S", "SA", "AA", "A"]
ability_meanings = ["-", "S", "S", "SS", "A", "A", "SA", "AA"]
proficiency_meanings = ["-", "S", "S", "SS", "SS", "A", "SA", "SA", "SA", "AA", "AA", "P"]
setback_meanings = ["-", "-", "F", "F", "T", "T"]
difficulty_meanings = ["-", "F", "FF", "T", "T", "T", "TT", "FT"]
challenge_meanings = ["-", "F", "F", "FF", "FF", "T", "T", "FT", "FT", "TT", "TT", "R"]
force_meanings = ["D", "D", "D", "D", "D", "D", "DD", "L", "L", "LL", "LL", "LL"]

BOOST = Die("Boost", boost_meanings, "B")
SETBACK = Die("Setback", setback_meanings, "S")
ABILITY = Die("Ability", ability_meanings, "A")
DIFFICULTY = Die("Difficulty", difficulty_meanings, "D")
PROFICIENCY = Die("Proficiency", proficiency_meanings, "P")
CHALLENGE = Die("Challenge", challenge_meanings, "C")
FORCE = Die("Force", force_meanings, "F")


