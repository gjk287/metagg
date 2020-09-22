-- view_match_info 뷰 테이블
CREATE OR REPLACE VIEW view_match_info AS
SELECT
	leag.league_name, ma.year, ma.season, ma.date,
	h_tm.team_name AS team_1, a_tm.team_name AS team_2,
	ma.tiebreaker, ma.match_round, ma.patch,
	mibt.result AS result_1, mibt2.result AS result_2,
	mibt.wdl AS wdl_1, mibt2.wdl AS wdl_2
FROM match ma
	LEFT JOIN match_info_by_team mibt
		ON ma.match_id = mibt.match_id
		AND ma.home_team_id = mibt.team_id
	LEFT JOIN match_info_by_team mibt2
		ON ma.match_id = mibt2.match_id
		AND ma.away_team_id = mibt2.team_id
	LEFT JOIN league leag
		ON ma.league_id = leag.league_id
	LEFT JOIN team h_tm
		ON ma.home_team_id = h_tm.team_id
	LEFT JOIN team a_tm
		ON ma.away_team_id = a_tm.team_id
ORDER BY league_name, year, season, date
;

-- set_match 뷰 테이블
CREATE OR REPLACE VIEW view_set_match AS
SELECT
	leag.league_name, ma.year, ma.season, ma.date, sm.set_number,
	h_tm.team_name AS team_1, a_tm.team_name AS team_2,
	ma.tiebreaker, ma.match_round, 
	sm.ckpm, sm.game_length, ply.player_name AS mvp
FROM set_match sm
	LEFT JOIN match ma
		ON sm.match_id = ma.match_id
	LEFT JOIN league leag
		ON ma.league_id = leag.league_id
	LEFT JOIN team h_tm
		ON ma.home_team_id = h_tm.team_id
	LEFT JOIN team a_tm
		ON ma.away_team_id = a_tm.team_id
	LEFT JOIN player ply
		ON sm.mvp = ply.player_id
ORDER BY league_name, year, season, date, set_number
;


-- set_match_info_home
CREATE OR REPLACE VIEW view_set_match_info_home AS
SELECT
	leag.league_name, ma.year, ma.season, ma.date, sm.set_number,
	h_tm.team_name AS team_1, a_tm.team_name AS team_2, 
	ma.tiebreaker, ma.match_round,
	smibt.wdl AS wdl_1, smibt.side AS side_1, 
	t_ply.player_name AS top_player_1, j_ply.player_name AS jg_player_1, m_ply.player_name AS mid_player_1, b_ply.player_name AS bot_player_1, s_ply.player_name AS sup_player_1, 
	c1.champion_name AS ban1_1, c2.champion_name AS ban2_1, c3.champion_name AS ban3_1, c4.champion_name AS ban4_1, c5.champion_name AS ban5_1, 
	smibt.team_kills AS team_kills_1, smibt.team_deaths AS team_deaths_1, smibt.team_double AS team_double_1, smibt.team_triple AS team_triple_1,
	smibt.team_quadra AS team_quadra_1, smibt.team_penta AS team_penta_1, smibt.team_kpm AS team_kpm_1,
	smibt.team_first_blood AS team_first_blood_1, smibt.team_first_baron AS team_first_baron_1,
	smibt.team_first_dragon AS team_first_dragon_1, smibt.team_first_elder AS team_first_elder_1, smibt.team_first_rift AS team_first_rift_1, smibt.team_first_tower AS team_first_tower_1, 
	smibt.team_first_inhib AS team_first_inhib_1, smibt.team_first_midtower AS team_first_midtower_1, smibt.team_first_three_towers AS team_first_three_towers_1, smibt.team_baron_kills AS team_baron_kills_1, 
	smibt.team_dragon_kills AS team_dragon_kills_1, smibt.team_elder_kills AS team_elder_kills_1, smibt.team_rift_kills AS team_rift_kills_1, smibt.team_tower_kills AS team_tower_kills_1, 
	smibt.team_inhib_kills AS team_inhib_kills_1, smibt.team_total_gold AS team_total_gold_1, smibt.team_earned_gold AS team_earned_gold_1, smibt.team_minion_kills AS team_minion_kills_1, 
	smibt.team_monster_kills AS team_monster_kills_1, smibt.team_goldat10 AS team_goldat10_1, smibt.team_goldat15 AS team_goldat15_1, smibt.team_golddiffat10 AS team_golddiffat10_1, 
	smibt.team_golddiffat15 AS team_golddiffat15_1, smibt.team_csat10 AS team_csat10_1, smibt.team_csat15 AS team_csat15_1, smibt.team_csdiffat10 AS team_csdiffat10_1, 
	smibt.team_csdiffat15 AS team_csdiffat15_1 
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
	LEFT JOIN player t_ply
		ON smibt.top_player_id = t_ply.player_id
	LEFT JOIN player j_ply
		ON smibt.jg_player_id = j_ply.player_id
	LEFT JOIN player m_ply
		ON smibt.mid_player_id = m_ply.player_id
	LEFT JOIN player b_ply
		ON smibt.bot_player_id = b_ply.player_id
	LEFT JOIN player s_ply
		ON smibt.sup_player_id = s_ply.player_id
	LEFT JOIN champion c1
		ON smibt.ban1_id = c1.champion_id
	LEFT JOIN champion c2
		ON smibt.ban2_id = c2.champion_id
	LEFT JOIN champion c3
		ON smibt.ban3_id = c3.champion_id
	LEFT JOIN champion c4
		ON smibt.ban4_id = c4.champion_id
	LEFT JOIN champion c5
		ON smibt.ban5_id = c5.champion_id
ORDER BY league_name, year, season, date, set_number
;


-- set_match_info_away
CREATE OR REPLACE VIEW view_set_match_info_away AS
SELECT
	leag.league_name, ma.year, ma.season, ma.date, sm.set_number,
	h_tm.team_name AS team_1, a_tm.team_name AS team_2,
	ma.tiebreaker, ma.match_round,
	smibt.wdl AS wdl_2, smibt.side AS side_2, 
	t_ply.player_name AS top_player_2, j_ply.player_name AS jg_player_2, m_ply.player_name AS mid_player_2, b_ply.player_name AS bot_player_2, s_ply.player_name AS sup_player_2, 
	c1.champion_name AS ban1_2, c2.champion_name AS ban2_2, c3.champion_name AS ban3_2, c4.champion_name AS ban4_2, c5.champion_name AS ban5_2, 
	smibt.team_kills AS team_kills_2, smibt.team_deaths AS team_deaths_2, smibt.team_double AS team_double_2, smibt.team_triple AS team_triple_2,
	smibt.team_quadra AS team_quadra_2, smibt.team_penta AS team_penta_2, smibt.team_kpm AS team_kpm_2,
	smibt.team_first_blood AS team_first_blood_2, smibt.team_first_baron AS team_first_baron_2,
	smibt.team_first_dragon AS team_first_dragon_2, smibt.team_first_elder AS team_first_elder_2, smibt.team_first_rift AS team_first_rift_2, smibt.team_first_tower AS team_first_tower_2, 
	smibt.team_first_inhib AS team_first_inhib_2, smibt.team_first_midtower AS team_first_midtower_2, smibt.team_first_three_towers AS team_first_three_towers_2, smibt.team_baron_kills AS team_baron_kills_2, 
	smibt.team_dragon_kills AS team_dragon_kills_2, smibt.team_elder_kills AS team_elder_kills_2, smibt.team_rift_kills AS team_rift_kills_2, smibt.team_tower_kills AS team_tower_kills_2, 
	smibt.team_inhib_kills AS team_inhib_kills_2, smibt.team_total_gold AS team_total_gold_2, smibt.team_earned_gold AS team_earned_gold_2, smibt.team_minion_kills AS team_minion_kills_2, 
	smibt.team_monster_kills AS team_monster_kills_2, smibt.team_goldat10 AS team_goldat10_2, smibt.team_goldat15 AS team_goldat15_2, smibt.team_golddiffat10 AS team_golddiffat10_2, 
	smibt.team_golddiffat15 AS team_golddiffat15_2, smibt.team_csat10 AS team_csat10_2, smibt.team_csat15 AS team_csat15_2, smibt.team_csdiffat10 AS team_csdiffat10_2, 
	smibt.team_csdiffat15 AS team_csdiffat15_2 
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
	LEFT JOIN player t_ply
		ON smibt.top_player_id = t_ply.player_id
	LEFT JOIN player j_ply
		ON smibt.jg_player_id = j_ply.player_id
	LEFT JOIN player m_ply
		ON smibt.mid_player_id = m_ply.player_id
	LEFT JOIN player b_ply
		ON smibt.bot_player_id = b_ply.player_id
	LEFT JOIN player s_ply
		ON smibt.sup_player_id = s_ply.player_id
	LEFT JOIN champion c1
		ON smibt.ban1_id = c1.champion_id
	LEFT JOIN champion c2
		ON smibt.ban2_id = c2.champion_id
	LEFT JOIN champion c3
		ON smibt.ban3_id = c3.champion_id
	LEFT JOIN champion c4
		ON smibt.ban4_id = c4.champion_id
	LEFT JOIN champion c5
		ON smibt.ban5_id = c5.champion_id
ORDER BY league_name, year, season, date, set_number
;


-- view_set_match_info
CREATE OR REPLACE VIEW view_set_match_info AS
SELECT * 
FROM view_set_match_info_home home
	LEFT JOIN view_set_match_info_away away
		USING (league_name, year, season, date, set_number, team_1, team_2, tiebreaker, match_round)
ORDER BY league_name, year, season, date, set_number
;
	




SELECT * FROM view_match_info;
SELECT * FROM view_set_match_info_away;
SELECT * FROM view_set_match_info_home;
SELECT * FROM view_set_match_info;
