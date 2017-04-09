es needs to know if publisher is dead
pub and sub and others es need to know if es is dead

*can create two znodes if necessary. one under es on separate? 
*it takes 10 second for ephimeral nodes to disapear!
*should es stop maintaining a publishers list?

/ess data: addr,
	/ess/esx/pubs
/pubs data: topic, os, current_master
/subs data: topic, current_master


es joins: 
	es watches /ess so they update their own view
	joiner es gets info about others from children of /ess

es fails:
	pubs and subs watch the master es znode when dead > wait and query /ess get a new master and restart.. 
	ess view will stay updated with the already existing watch

pubs fails:
	es watches it's own pubs. how? pubs create znodes under their master es at /ess/esx ( if es znode goes away children will too)


