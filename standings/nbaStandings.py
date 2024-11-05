from espn_api.basketball import League
import json

with open('keys.json', 'r') as file:
	keys = json.load(file)


# For the 2024-2025 season, the current year should be:
# 	Basketball --> 2025
# 	Football --> 2024
league = League(keys["basketball"]["leagueID"], 2025, keys["espnS2"], keys["swid"])

# create shell for standings
allTeams = []
for team in league.teams:
	allTeams.append({
		"name": team.team_name,
		"wins": 0,
		"losses": 0,
		"points": 0,
		"games_behind": 0
	})

# set variables for iterating through the weeks
# FORFEIT TIMINGS:
# thanksgiving --> 1 - 5
# christmas --> 6 - 10
# spring break --> 11 - 20
current = league.current_week
if (current > 20):
	current = 20
start = 1
end = current
# iterate through each week to find wins and losses and points
if (start < end):
	for week in range(start, end + 1):

		# iterate through all matchups in the week through we are iterating through
		matchups = league.box_scores(week)
		for m in matchups:
			home = m.home_team.team_name
			# NOTE: if the week was a bye, points do not count
			if m.away_team == 0:
				continue
			away = m.away_team.team_name
			if m.winner == "HOME":
				winner = home
			else:
				winner = away

			# iterate through list(dict) of all teams
			# add points to correct team, add wins/losses to the winning/losing team
			for team in allTeams:
				if team["name"] == home:
					team["points"] += m.home_score
					if winner == home:
						team["wins"] += 1
					else:
						team["losses"] += 1
				elif team["name"] == away:
					team["points"] += m.away_score
					if winner == away:
						team["wins"] += 1
					else:
						team["losses"] += 1

# sort list of teams by standings without considering conference.
allTeams.sort(key=lambda x: (x["wins"], -x["losses"], x["points"]), reverse=True)

# find how many games behind a team is
for i, team in enumerate(allTeams):
		team["games_behind"] = ((allTeams[0]["wins"] - allTeams[0]["losses"]) - (team["wins"] - team["losses"])) / 2
		# print team
		print(str(i + 1) + ".", team)