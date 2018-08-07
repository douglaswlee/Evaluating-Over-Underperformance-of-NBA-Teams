# Evaluating-Over-Underperformance-of-NBA-Teams

This repo contains files for Project Luther, the first individual project I completed for Metis. For this project, I built a linear regression model to predict the difference between the actual winning perecentage of teams and their expected winning percentage by [Pythagorean expectation](https://en.wikipedia.org/wiki/Pythagorean_expectation). The response variable `diffWP` is the difference between actual and expected winning percentage (from Pythagorean expectation). If this difference is positive (negative), a team can be said to have overperformed (underperformed).

For all teams from the 2001-02 through the 2017-18 seasons, I focused on the [Four Factors](https://www.nbastuffer.com/analytics101/four-factors/), which some have found to correlate well with offensive/defensive success in basketball:
* **Effective Field Goal Pct.**: The percentage of shots made (adjusting for 3 point shots being worth more than 2 point shots
* **Offensive Rebounding Pct.**: The percentage of available offensive rebounds collected
* **Turnover Pct.**: The percentage of plays ending in a turnover
* **Free Throw Attempt Rate**: The free throw attempts per field goal attempts

I collected these numbers for each team for each season via the following:
* "Season Summary" pages from [Basketball Reference](https://www.basketball-reference.com). Here's an [example](https://www.basketball-reference.com/leagues/NBA_2018.html), which provided these numbers over all game situations in a given season.
* The collection of "clutch" situation statistics from [NBA.com](https://http://stats.nba.com/teams/clutch-four-factors/?sort=W_PCT&dir=-1). These situations are defined as occurring within the last five minutes of regulation or overtime with neither team leading by more than five points.
My purpose in including the latter is based on a belief that performance in "close and late" game situations separate overperforming and underperforming teams (the latter performing especially well in these situations, the former poorly relative to overall game performance).

The files I created to carry out this project are as follows:
* **bbref_scrape.py**, defining functions to scrape "Season Summary" pages from [Basketball Reference](https://www.basketball-reference.com).
* **nba_dot_com_scrape.py**, defining functions to scrape "clutch" situation statistics from [NBA.com](https://http://stats.nba.com/teams/clutch-four-factors/?sort=W_PCT&dir=-1).
* **Team_Game_Stats_Only_Analysis.ipynb**, notebook containing code that scrapes and prepares data from [Basketball Reference](https://www.basketball-reference.com) only, and then performs the full linear regression workflow on this data.
* **Team_Game+Clutch_Analysis.ipynb**, notebook containing code that scrapes and prepares data from [NBA.com](https://http://stats.nba.com/teams/clutch-four-factors/?sort=W_PCT&dir=-1) and combines it with the [Basketball Reference](https://www.basketball-reference.com) data put together in 'Team_Game_Stats_Only_Analysis.ipynb', before building a linear regression model on the combined data.
