CREATE OR REPLACE VIEW view_set_match_player_performance AS
SELECT 
	leag.league_name, ma.year, ma.season, ma.date, sm.set_number,
	h_tm.team_name AS team_1, a_tm.team_name AS team_2, cor_tm.team_name AS corresponding_team,
	ma.tiebreaker, ma.match_round,
	ply.player_name, chp.champion_name, smibt.wdl, smibt.side, smibt.team_first_blood, smibt.team_baron_kills,
	smibt.team_dragon_kills, smibt.team_rift_kills, 
	sm.game_length, smpp.kills, smpp.deaths, smpp.assists, smpp.double, smpp.triple, smpp.quadra,
	smpp.penta, smpp.first_blood, smpp.total_gold, smpp.earned_gold, smpp.total_cs,
	smpp.minion_kills, smpp.monster_kills, smpp.cspm, smpp.goldat10, smpp.golddiffat10, 
	smpp.goldat15, smpp.golddiffat15, smpp.csat10, smpp.csdiffat10, smpp.csat15, smpp.csdiffat15,
	smpp.largest_killing_spree, smpp.largest_multi_kill, smpp.total_damage_dealt_to_champions,
	smpp.total_damage_taken, smpp.vision_wards_bought_in_game
FROM set_match_player_performance smpp
	LEFT JOIN set_match_info_by_team smibt
		USING (set_match_info_by_team_id)
	LEFT JOIN player ply
		USING (player_id)
	LEFT JOIN set_match sm
		USING (set_match_id)
	LEFT JOIN match ma
		ON sm.match_id = ma.match_id
	LEFT JOIN team cor_tm
		ON smibt.team_id = cor_tm.team_id
	LEFT JOIN league leag
		ON ma.league_id = leag.league_id
	LEFT JOIN team h_tm
		ON ma.home_team_id = h_tm.team_id
	LEFT JOIN team a_tm
		ON ma.away_team_id = a_tm.team_id
	LEFT JOIN champion chp
		USING (champion_id)
ORDER BY league_name, year, season, date, set_number
;



SELECT 
	leag.league_name, ma.year, ma.season, ma.date, sm.set_number,
	h_tm.team_name AS team_1, a_tm.team_name AS team_2,
	ma.tiebreaker, ma.match_round
FROM set_match sm
	LEFT JOIN match ma
		ON sm.match_id = ma.match_id
	LEFT JOIN league leag
		ON ma.league_id = leag.league_id
	LEFT JOIN team h_tm
		ON ma.home_team_id = h_tm.team_id
	LEFT JOIN team a_tm
		ON ma.away_team_id = a_tm.team_id
	LEFT JOIN set_match_info_by_team smibt
		ON sm.set_match_id = smibt.set_match_id
		AND ma.home_team_id = smibt.team_id







-- view_set_match_player_perf_home --top, jg, mid, bot, sup
CREATE OR REPLACE VIEW view_set_match_player_perf_sup_home AS
SELECT 
	ma.*, sm.set_number, sm.ckpm, sm.game_length, smibt.team_id as "corresponding_team_id", perf1.*
FROM set_match sm
	LEFT JOIN match ma
		ON sm.match_id = ma.match_id
	LEFT JOIN set_match_info_by_team smibt
		ON sm.set_match_id = smibt.set_match_id
		AND ma.home_team_id = smibt.team_id
	INNER JOIN set_match_player_performance perf1
		ON smibt.set_match_info_by_team_id = perf1.set_match_info_by_team_id
		AND smibt.sup_player_id = perf1.player_id
;


-- view_set_match_player_perf_away --top, jg, mid, bot, sup
CREATE OR REPLACE VIEW view_set_match_player_perf_sup_away AS
SELECT 
	ma.*, sm.set_number, sm.ckpm, sm.game_length, smibt.team_id as "corresponding_team_id", perf1.*
FROM set_match sm
	LEFT JOIN match ma
		ON sm.match_id = ma.match_id
	LEFT JOIN set_match_info_by_team smibt
		ON sm.set_match_id = smibt.set_match_id
		AND ma.away_team_id = smibt.team_id
	INNER JOIN set_match_player_performance perf1
		ON smibt.set_match_info_by_team_id = perf1.set_match_info_by_team_id
		AND smibt.sup_player_id = perf1.player_id
;













