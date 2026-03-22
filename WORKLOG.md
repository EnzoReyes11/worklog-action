# Worklog

### 22/03/26
Removed parser.py, it was dead code.
Several improvements and small fixes.
Updated the README

#### Next Steps:
- Add a way to sync private repos.
- Add /docs directory with Backstage docs.


### 20/03/26
Added a script to sync the PAT into the repos.

### 14/10/25
I haven't done any work with the action today. But discovered that Private repos
are unable to run it. As when it runs, it clones the (private) repo, and that requires
some kind of authentication.

I've added a item on the backlog to investigate how to work with private repos.

### 08/10/25
Work done: 
- Tried having PROJECT and WORKLOG files with different behaviors. WORKLOG would 
be parsed and different date items would create different files. But I'm discarding this
solution. Instead I'm going to create just one file for the WORKLOG and one for PROJECT.
Then, the Astro blog would parse WORKLOG and create the different blog posts programmatically.
- Detect both PROJECT and WORKLOG changes. Overwrite into target destination.
- TEST 3



