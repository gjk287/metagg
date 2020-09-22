-- odds_by_match -- only over_under
CREATE OR REPLACE VIEW view_odds_by_match AS
	SELECT 
		odds_match.match_id, ((((ou.bet_name)::text || ':'::text) || (ou.threshold)::text) || ':'::text) || (ou.over_under)::text AS bet_column,
		odds_match.odds, odds_match.betting_site_id, odds_match.bet_type, odds_match.saved_time
	FROM odds_by_match odds_match
		INNER JOIN bet_type_ou ou
			USING (bet_id)
	WHERE odds_match.bet_type = 'over_under'
;



-- odds_by_match_info -- handicap, special
CREATE OR REPLACE VIEW view_odds_by_match_info AS
	SELECT 
		odds_mi.match_info_by_team_id, ((hdc.bet_name::text || ':'::text) || hdc.handicap_amount::text) AS bet_column,
		odds_mi.odds, odds_mi.betting_site_id, odds_mi.bet_type, odds_mi.saved_time
	FROM odds_by_match_info odds_mi
		INNER JOIN bet_type_handicap hdc
			USING (bet_id)
	WHERE odds_mi.bet_type = 'handicap'
UNION
	SELECT 
		odds_mi.match_info_by_team_id, bt.bet_name AS bet_column,
		odds_mi.odds, odds_mi.betting_site_id, odds_mi.bet_type, odds_mi.saved_time
	FROM odds_by_match_info odds_mi
		INNER JOIN bet_type_special bt
			USING (bet_id)
	WHERE odds_mi.bet_type = 'special'
ORDER BY match_info_by_team_id
;




-- odds_by_set_match -- over_under, both
CREATE OR REPLACE VIEW view_odds_by_set_match AS
	SELECT 
		ob.set_match_id,  ((((bt1.bet_name)::text || ':'::text) || (bt1.threshold)::text) || ':'::text) || (bt1.over_under)::text AS bet_column,
		ob.odds, ob.betting_site_id, ob.bet_type, ob.saved_time
	FROM odds_by_set_match ob
		INNER JOIN bet_type_ou bt1
			USING (bet_id)
	WHERE ob.bet_type = 'over_under'
UNION
	SELECT 
		ob2.set_match_id, ((bt2.bet_name::text || ':'::text) || bt2.yes_no::text) AS bet_column,
		ob2.odds, ob2.betting_site_id, ob2.bet_type, ob2.saved_time
	FROM odds_by_set_match ob2
		INNER JOIN bet_type_both bt2
			USING (bet_id)
	WHERE ob2.bet_type = 'both'
ORDER BY set_match_id
;




-- odds_by_set_match_info -- handicap, special
CREATE OR REPLACE VIEW view_odds_by_set_match_info AS
	SELECT 
		ob.set_match_info_by_team_id,  ((bt1.bet_name::text || ':'::text) || bt1.handicap_amount::text) AS bet_column,
		ob.odds, ob.betting_site_id, ob.bet_type, ob.saved_time
	FROM odds_by_set_match_info ob
		INNER JOIN bet_type_handicap bt1
			USING (bet_id)
	WHERE ob.bet_type = 'handicap'
UNION
	SELECT 
		ob2.set_match_info_by_team_id, bt2.bet_name AS bet_column,
		ob2.odds, ob2.betting_site_id, ob2.bet_type, ob2.saved_time
	FROM odds_by_set_match_info ob2
		INNER JOIN bet_type_special bt2
			USING (bet_id)
	WHERE ob2.bet_type = 'special'
ORDER BY set_match_info_by_team_id
;





SELECT DISTINCT bet_type FROM odds_by_set_match_info;



















