from typing import List, Set
from team import Team
from meeting import Meeting

# Dummy meetings
meeting1 = Meeting("1", ["B", "C"], 1, ["2"])
meeting2 = Meeting("2", ["A", "B", "C"], 3, ["4"])
meeting3 = Meeting("3", ["B", "C"], 2, ["2", "1"])
meeting4 = Meeting("4", ["A"], 2, [])
meetings = [meeting1, meeting2, meeting3, meeting4]


# Dummy teams
team1 = Team("A")
team2 = Team("B")
team3 = Team("C")
teams = [team1, team2, team3]

# Map names to meeting/team objects for convenience
team_map = dict([(t._name, t) for t in teams])
meeting_map = dict([(m._name, m) for m in meetings])


def prioritize_meetings_via_counts(meetings: Set[Meeting]) -> dict:
    """
    Creating an map of highest priorty meetings based on how 
    many times each meeting occurs in the dependencies of other meetings.

    Then, create meeting ranks based of the largest depth depedencies of 
    the highest dependency meetings.
    """
    counts = dict([(m._name, 0) for m in meetings])
    for meeting in meetings:
        for dependency in meeting._dependencies:
            counts[dependency] += 1

    # Rank meetings, according to meetings with the most dependencies
    ranks = dict([(m._name, -1) for m in meetings])
    cur_rank = 0
    while counts:
        max_dependency_meeting = max(counts, key=counts.get)
        dependencies = meeting_map[max_dependency_meeting]._dependencies

        # Perform bfs on dependencies, adding the loweset dependencies to next rank
        stack = []  # Stack
        queue = [max_dependency_meeting] + list(dependencies)
        while queue:
            next_dep = queue.pop(0)
            if next_dep in counts.keys():
                stack.append(next_dep)
                del counts[next_dep]
                for d in meeting_map[next_dep]._dependencies:
                    queue.append(d)

        while stack:
            ranks[stack.pop()] = cur_rank
            cur_rank += 1

    return ranks



def are_teams_available(meeting: Meeting) -> bool:
    """
    Check if all teams required for meeting are available
    """
    print("CHECKING AVAILABILITY FOR MEETING: {}".format(meeting))
    for team_name in meeting._required_teams:
        team = team_map[team_name]
        print("checking team: {}".format(team))
        if team._timesteps_busy != 0:
            print("not available")
            return False

    return True


def are_prereqs_done(meeting: Meeting, meetings_todo: Set[Meeting]):
    """
    Check if all prerequisite meetings are completed
    """
    print("CHECKING PREREQS FOR MEETING: {}".format(meeting))
    for dep in meeting._dependencies:
        print("checking dep: {}".format(dep))
        if dep in meetings_todo:
            print("not done")
            return False
    
    return True


def schedule_meeting(schedule: list, meeting: Meeting, timeslot: int) -> bool:
    """
    Schedule a new meeting
    """
    # Add to schedule 
    schedule[-1].append("Meeting {} starting with teams {}".format(meeting._name, meeting._required_teams))

    # Adjust availability
    for team_name in meeting._required_teams:
        team = team_map[team_name]
        team._timesteps_busy = meeting._duration


def print_schedule(schedule: List[List[str]]) -> None:
    """
    Final printing of schedule
    """
    time = 0
    print("\n\nGENERATED SCHEDULE:")
    for slot in schedule:
        print("Current time: {}".format(time))
        time += 1
        for meeting_start in slot:
            print(meeting_start)


def main():
    # Get meeting priority/rank mapping
    meeting_priorities = prioritize_meetings_via_counts(meetings)

    # Sort meetings according to priority
    meetings.sort(key=lambda x: meeting_priorities[x._name])
    # [print(m, m._dependencies) for m in meetings]

    schedule = []
    timeslot = 0
    meetings_todo = set([m._name for m in meetings])
    # Iterate over all timeslots
    while meetings_todo:
        schedule.append([])
        
        # Step forward team availability
        for team in teams:
            team.timestep()
        
        # Iterate over all sorted meetings, schedule remaining ones
        for meeting in meetings:
            if meeting._name in meetings_todo \
            and are_teams_available(meeting) \
            and are_prereqs_done(meeting, meetings_todo):
                schedule_meeting(schedule, meeting, timeslot)
                meetings_todo.remove(meeting._name)

        timeslot += 1

    print_schedule(schedule)
    
    
if __name__ == '__main__':
    main()

# Bad code
# schedule = []
#     for slot in range(days * timeslots_per_day):
#         schedule.append([])
#         teams_w_meetings_left = 0
#         for team in teams:
#             team._timesteps_busy -= 1
#             team._timesteps_busy = max(0, team._timesteps_busy)
            
#             # Done with meetings
#             if not team._required_meetings:
#                 continue

#             teams_w_meetings_left += 1
#             # Schedule new meeting
#             if team._timesteps_busy == 0:
                
#                 meeting = team._required_meetings.pop(0)
#                 team._timesteps_busy = meeting_map[meeting]._duration
#                 schedule[-1].append("Team {} is now attending meeting {}".format(team._name, meeting))
                
#             # Still busy
#             else:
#                 schedule[-1].append("Team {} is still busy".format(team._name))

#         if teams_w_meetings_left == 0:
#             break

#     print_schedule(schedule)