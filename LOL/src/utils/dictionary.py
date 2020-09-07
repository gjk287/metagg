class GameDictionary(object):
	def __init__(self):
		self.championName_dict = {
			"Cho'gath": "Cho gath", "Cho'Gath": "Cho gath", "Kha'zix": "Kha zix", "Rek'Sai": "Rek Sai", "Vel'koz": "Vel koz", "Kog'Maw": "Kog Maw", "Kai'sa": "Kai sa", "Kai'Sa": "Kai sa",
			"Kha'Zix": "Kha zix", "Vel'Koz": "Vel koz"
		}

		self.leagueName_dict = {
			**dict.fromkeys(['CBLOL', 'CBLoL'], 'CBLOL'), # 브라질 
			**dict.fromkeys(['Legends Champions Korea', 'LCK'], 'LCK'), # 한국
			**dict.fromkeys(['Continental League', 'LCL'], 'LCL'), # 러시아 
			**dict.fromkeys(['NALCS', 'NA LCS', 'NA_LCS', 'LCS'], 'LCS'), # 미국
			**dict.fromkeys(['EULCS', 'EU LCS', 'EU_LCS', 'LEC'], 'LEC'), # 유럽
			**dict.fromkeys(['LJL'], 'LJL'), # 일본
			**dict.fromkeys(['Latin America League', 'LLA'], 'LLA'), # 라틴 아메리카
			**dict.fromkeys(['LMS'], 'LMS'), # 대만
			**dict.fromkeys(['Legends Pro League', 'LPL'], 'LPL'), # 중국
			**dict.fromkeys(['Oceanic Pro League', 'OPL'], 'OPL'), # 오세아니아
			**dict.fromkeys(['Pacific Championship Series', 'PCS'], 'PCS'), # 대만/홍콩/마카오
			**dict.fromkeys(['Turkish Championship League', 'TCL'], 'TCL'), # 터키
			**dict.fromkeys(['Vietnam Championship Series', 'VCS', 'VCS_A'], 'VCS'), # 베트남

			**dict.fromkeys(['Belgian League', 'Belgian_League', 'BL'], 'BL'), # 벨기에 2부
			**dict.fromkeys(['Brazilian_Challenger_Circuit', 'BRCC'], 'BRCC'), # CBLOL 2부
			**dict.fromkeys(['Challengers Korea', 'CK', 'Challengers_Korea'], 'Challengers Korea'), # LCK 2부
			**dict.fromkeys(['CIS_Challenger_League', 'CIS_CL', 'CIS CL'], 'CIS_CL'), # LCL 2부
			**dict.fromkeys(['LSPL', 'LDL'], 'LDL'), # 중국 2부
			**dict.fromkeys(['Dutch League', 'Dutch_League', 'DL'], 'DL'), # 네덜란드 2부
			**dict.fromkeys(['ECS'], 'ECS'), # LMS 2부
			**dict.fromkeys(['EU CS', 'EU_Challenger_Series', 'European_Masters', 'EM'], 'EM'), # LEC 2부
			**dict.fromkeys(['NA_Academy_League', 'NA_Challenger_Series', 'NA CS', 'LCS_a', 'LCS.A'], 'LCS_a'), # LCS 2부
			**dict.fromkeys(['LJL_Challenger_Series', 'LJL_CS'], 'LJL_CS'), # LJL 2부
			**dict.fromkeys(['LPLOL'], 'LPLOL'), # 포르투갈 2부
			**dict.fromkeys(['OCS'], 'OCS'), # OPL 2부
			**dict.fromkeys(['PG Nationals', 'PG_Nationals', 'PGN'], 'PGN'), # 이탈리아 2부
			**dict.fromkeys(['Premier Tour'], 'Premier Tour'), # 독일 2부
			**dict.fromkeys(['TPL', 'TCS', 'Turkey_Academy_League', 'TPL_a', 'TRA'], 'TPL_a') # TCL 2부
		}

		self.teamName_dict = {
			# Korea (LCK)
			**dict.fromkeys(['Afreeca', 'Afreeca Freecs', 'AF', '1AF'], 'Afreeca'),
			**dict.fromkeys(['APK', 'APK Prince', 'SeolHaeOne Prince', 'SP'], 'SeolHaeOne Prince'),
			**dict.fromkeys(['Damwon', 'DAMWON Gaming', 'DWG', 'Damwon Gaming', 'MiraGe Gaming'], 'Damwon'),
			**dict.fromkeys(['DragonX', 'DRX', 'KZ', 'LZ', 'Longzhu Gaming', 'Kingzone DragonX', 'Longzhu', 'LZ2'], 'DragonX'),
			**dict.fromkeys(['GenG', 'Gen.G', 'GEN', 'KSV', 'KSV Esports', 'KSV eSports'], 'GenG'),
			**dict.fromkeys(['Hanwha', 'Hanwha Life Esports', 'HLE', 'Hanwha Life'], 'Hanwha'),
			**dict.fromkeys(['KT', 'KT 롤스터', 'KT Rolster'], 'KT'),
			**dict.fromkeys(['Sandbox', 'SANDBOX Gaming', 'SB', 'Sandbox Gaming'], 'Sandbox'),
			**dict.fromkeys(['T1', 'SKT', 'SK Telecom T1'], 'T1'),
			**dict.fromkeys(['Dynamics', 'DYN', 'Team Dynamics'], 'Dynamics'),
			**dict.fromkeys(['GRF', 'Griffin'], 'Griffin'),
			**dict.fromkeys(['JAG', 'Jin Air Green Wings', '1JAG', 'Jin Air'], 'Jin Air'),
			**dict.fromkeys(['MVP'], 'MVP'),
			**dict.fromkeys(['bbq', 'BBQ Olivers', 'bbq Olivers'], 'bbq'),
			**dict.fromkeys(['KDM', 'Kongdoo Monster', 'Kongdoo'], 'Kongdoo'),
			**dict.fromkeys(['ROX', 'ROX Tigers'], 'ROX'),
			**dict.fromkeys(['E8W', 'Ever8 Winners', 'EEW', 'Ever8'], 'Ever8'),
			**dict.fromkeys(['SSG', 'Samsung Galaxy', 'SSG1'], 'Samsung Galaxy'),

			# China (LPL)
			**dict.fromkeys(['Bilibili Gaming', 'BLG'], 'Bilibili Gaming'),
			**dict.fromkeys(['Dominus Esports', 'DMO'], 'Dominus Esports'),
			**dict.fromkeys(['Edward Gaming', 'EDG', 'EDward Gaming'], 'EDG'),
			**dict.fromkeys(['eStar', 'ES', '이스타 게이밍', 'eStar Pro'], 'eStar'),
			**dict.fromkeys(['FPX', 'FunPlus Phoenix', 'Funplus Phoenix', 'FunPlus Phoenix'], 'FPX'),
			**dict.fromkeys(['IG', 'iG', '인빅터스 게이밍', 'Invictus Gaming'], 'IG'),
			**dict.fromkeys(['JDG', 'JD Gaming'], 'JDG'),
			**dict.fromkeys(['LGD', 'LGD Gaming', 'LGD 게이밍', 'LGD.International'], 'LGD'),
			**dict.fromkeys(['LNG Esports', 'LNG'], 'LNG'),
			**dict.fromkeys(['Oh My God', 'OMG'], 'OMG'),
			**dict.fromkeys(['Rogue Warriors', 'RW'], 'Rogue Warriors'),
			**dict.fromkeys(['Royal Never Give Up', '로얄 네버 기브 업', 'RNG'], 'RNG'),
			**dict.fromkeys(['Suning', 'SN', 'Suning Gaming'], 'Suning'),
			**dict.fromkeys(['Team WE', 'WE'], 'Team WE'),
			**dict.fromkeys(['Top Esports', 'TES', 'TOP', 'Topsports Gaming'], 'TES'),
			**dict.fromkeys(['Vici Gaming', 'VG'], 'Vici Gaming'),
			**dict.fromkeys(['Victory Five', 'V5'], 'Victory Five'),
			**dict.fromkeys(['SS', 'Snake Esports', 'Snake eSports'], 'Snake Esports'),
			**dict.fromkeys(['SDG', 'SinoDragon Gaming', 'SinoDragon'], 'SinoDragon'),
			**dict.fromkeys(['IM', 'I May', 'I MAY', 'IMay'], 'I May'),
			**dict.fromkeys(['DAN', 'DAN Gaming'], 'DAN Gaming'),
			**dict.fromkeys(['NB', 'Newbee', 'NewBee'], 'Newbee'),
			**dict.fromkeys(['GT', 'Game Talents'], 'Game Talents'),
			**dict.fromkeys(['QGR', 'QG Reapers', 'Qiao Gu Reapers'], 'QG Reapers'),

			# Europe (LEC) //betjoe
			**dict.fromkeys(['Excel Esports', 'exceL', 'XL', 'exceL eSports', 'Excel'], 'Excel Esports'),
			**dict.fromkeys(['FC Schalke', 'FC 살케 04', 'S04', 'FC Schalke 04', 'Schalke 04', 'FC Schalke 04 Esports'], 'FC Schalke'),
			**dict.fromkeys(['Fnatic', '프나틱', 'FNC'], 'Fnatic'),
			**dict.fromkeys(['G2', 'G2 Esports'], 'G2'),
			**dict.fromkeys(['MAD', 'MAD Lions'], 'MAD'),
			**dict.fromkeys(['Misfits', 'MSF', 'Misfits Gaming'], 'Misfits'),
			**dict.fromkeys(['Origen', 'OG'], 'Origen'),
			**dict.fromkeys(['Rogue', 'RGE', 'Team Rogue'], 'Rogue'),
			**dict.fromkeys(['SK Gaming', 'SK', 'SK 게이밍'], 'SK Gaming'),
			**dict.fromkeys(['Team Vitality', 'VIT', 'Vitality'], 'Team Vitality'),
			**dict.fromkeys(['SPY', 'Splyce'], 'Splyce'),
			**dict.fromkeys(['ROC', 'Roccat', 'Team ROCCAT'], 'Team ROCCAT'),
			**dict.fromkeys(['UOL', 'Unicorns of Love', 'Unicorns Of Love'], 'Unicorns Of Love'),
			**dict.fromkeys(['GIA', 'Giants', 'Giants Gaming'], 'Giants Gaming'),
			**dict.fromkeys(['H2K', 'H2k-Gaming', 'H2k Gaming'], 'H2k Gaming'),
			**dict.fromkeys(['NiP', 'Ninjas in Pyjamas'], 'Ninjas in Pyjamas'),
			**dict.fromkeys(['MM', 'Mysterious Monkeys'], 'Mysterious Monkeys'),

			# North America (LCS)
			**dict.fromkeys(['100 Thieves', '100'], '100 Thieves'),
			**dict.fromkeys(['Cloud9', 'C9'], 'Cloud9'),
			**dict.fromkeys(['CLG', 'Counter Logic Gaming'], 'CLG'),
			**dict.fromkeys(['Dignitas', 'DIG', '디니타스', 'Team Dignitas'], 'Dignitas'),
			**dict.fromkeys(['Evil Geniuses', 'EG', '에빌 지니어스'], 'Evil Geniuses'),
			**dict.fromkeys(['FlyQuest', 'FLY', 'Flyquest', 'FlyQuest eSports'], 'FlyQuest'),
			**dict.fromkeys(['Golden Guardians', 'GG'], 'Golden Guardians'),
			**dict.fromkeys(['Immortals', 'IMT', '이모탈'], 'Immortals'),
			**dict.fromkeys(['TL', '팀 리퀴드', 'Team Liquid'], 'TL'),
			**dict.fromkeys(['TSM', 'Team Solo Mid', 'Team SoloMid'], 'TSM'),
			**dict.fromkeys(['OPT', 'Optic Gaming', 'OpTic Gaming'], 'OpTic Gaming'),
			**dict.fromkeys(['FOX', 'Echo Fox'], 'Echo Fox'),
			**dict.fromkeys(['CG', 'Clutch Gaming'], 'Clutch Gaming'),
			**dict.fromkeys(['nV', 'EnVyUs', 'Team EnVyUs'], 'Team EnVyUs'),
			**dict.fromkeys(['P1', 'Phoenix1'], 'Phoenix1'),

			# Brazil (CBLOL)
			**dict.fromkeys(['Flamengo eSports', 'FLA', 'Flamengo', 'Flamengo Esports'], 'Flamengo'),
			**dict.fromkeys(['FURIA Esports', 'FURIA', 'FUR', 'FURIA Uppercut'], 'FURIA'),
			**dict.fromkeys(['INTZ e-Sports', 'INTZ', 'ITZ', 'INTZ e-Sports Club', 'INTZ-eSports'], 'INTZ'),
			**dict.fromkeys(['KaBuM! e-Sports', 'KBM', 'Kabum', 'KaBuM eSports', 'KaBuM e-Sports', 'KaBuM'], 'Kabum'),
			**dict.fromkeys(['paiN Gaming', 'PNG', 'PAIN'], 'PAIN'),
			**dict.fromkeys(['Prodigy Esports', 'PRG', 'Prodigy'], 'Prodigy'),
			**dict.fromkeys(['Santos e-Sports', 'SAN', 'Santos'], 'Santos'),
			**dict.fromkeys(['Vivo Keyd', 'VK', 'kStars', 'Keyd Stars'], 'Vivo Keyd'),

			**dict.fromkeys(['RDP', 'Redemption eSports', 'Redemption', 'Redemption eSports Porto Alegre', 'REPA', 'Redemption POA'], 'Redemption POA'),
			**dict.fromkeys(['UP', 'Uppercut esports', 'Uppercut'], 'Uppercut'),
			**dict.fromkeys(['CNB', 'CNB e-Sports Club', 'CNB e-Sports'], 'CNB'),
			**dict.fromkeys(['ONE', 'Team oNe e-Sports', 'Team One e-Sports', 'Team One', 'Team oNe eSports', 'Team oNe'], 'Team oNe'),
			**dict.fromkeys(['IDM', 'Ilha da Macacada Gaming', 'IDM Gaming'], 'IDM Gaming'),
			**dict.fromkeys(['RED', 'RED Canids', 'Red Canids'], 'RED Canids'),
			**dict.fromkeys(['TShow', 'T Show E-Sports', 'T Show'], 'T Show'),
			**dict.fromkeys(['OPK', 'Operation Kino', 'Operation Kino e-Sports'], 'Operation Kino'),
			**dict.fromkeys(['RBRV', 'Remo Brave eSports', 'Remo Brave', 'Brave e-Sports', 'Brave'], 'Remo Brave'),
			**dict.fromkeys(['ProGaming Esports', 'ProGaming e-Sports'], 'ProGaming Esports'),

			# Turkey (TCL)
			**dict.fromkeys(['FBts', '1907 페네르바체', 'FB', '1907 Fenerbahce', 'Fenerbahce Esports', '1907 Fenerbahçe Esports'], '1907 Fenerbahce'),
			**dict.fromkeys(['5 Ronin', '5R'], '5 Ronin'),
			**dict.fromkeys(['Besiktas', 'Besiktas e-Sports', 'BJK', 'Besiktas Esports', 'Beşiktaş Esports'],
							'Besiktas Esports'),
			**dict.fromkeys(['Dark Passage', 'DP', 'Dark Passage Academy'], 'Dark Passage'),
			**dict.fromkeys(['Galakticos', 'GAL', 'Galakticos Academy'], 'Galakticos'),
			**dict.fromkeys(['Galatasaray Esports', '갈라타사라이', 'GS', 'Galatasaray', 'Galatasaray Academy'], 'Galatasaray'),
			**dict.fromkeys(['Istanbul Wildcats', 'Istanbul Wild Cats', 'İstanbul Wildcats'], 'Istanbul Wildcats'),
			**dict.fromkeys(['Papara SuperMassive', 'SuperMassive eSports', 'SUP', 'SuperMassive'], 'Papara SuperMassive'),
			**dict.fromkeys(['Royal Youth', 'RY', 'Royal Youth Academy', 'RYL'], 'Royal Youth'),
			**dict.fromkeys(['Team AURORA', 'AUR', 'Team Aurora', 'AURORA Academy'], 'Team Aurora'),

			**dict.fromkeys(['BUR', 'Bursaspor Esports', 'Bursaspor'], 'Bursaspor'),
			**dict.fromkeys(['HWA', 'HWA Gaming'], 'HWA Gaming'),
			**dict.fromkeys(['RBE', 'Royal Bandits e-sports', 'Royal Bandits'], 'Royal Bandits'),
			**dict.fromkeys(['YC', 'YouthCREW', 'YouthCrew Esports', 'YouthCrew'], 'YouthCrew'),
			**dict.fromkeys(['CEC', 'Crew e-Sports Club', 'Crew eSports'], 'Crew eSports'),
			**dict.fromkeys(['P3P', 'P3P eSports'], 'P3P eSports'),
			**dict.fromkeys(['CLK', 'Cilekler', 'ÇİLEKLER'], 'Cilekler'),
			**dict.fromkeys(['TT', 'Team Turquality'], 'Team Turquality'),
			**dict.fromkeys(['SUP TNG', 'SuperMassive TNG'], 'SuperMassive TNG'),
			**dict.fromkeys(['Pars', 'Pars eSports'], 'Pars eSports'),
			**dict.fromkeys(['Cappa', 'Team Cappadocia'], 'Team Cappadocia'),
			**dict.fromkeys(['OH', 'Oyun Hizmetleri'], 'Oyun Hizmetleri'),

			# Oceania (OPL)
			**dict.fromkeys(['Avant Gaming', 'AVANT', 'Av', 'AV', 'Avant Garde'], 'Avant Gaming'),
			**dict.fromkeys(['Chiefs eSports Club', '치프스', 'CHF', 'Chiefs Esports', 'Chiefs Esports Club'], 'Chiefs Esports'),
			**dict.fromkeys(['Dire Wolves', 'DW', 'LG Dire Wolves'], 'Dire Wolves'),
			**dict.fromkeys(['Gravitas', 'GRV'], 'Gravitas'),
			**dict.fromkeys(['Legacy eSports', 'Legacy', 'LGC', 'Legacy Esports'], 'Legacy Esports'),
			**dict.fromkeys(['Mammoth', 'MAMMOTH', 'MMM'], 'Mammoth'),
			**dict.fromkeys(['Order', 'ORDER', 'ORD'], 'ORDER'),
			**dict.fromkeys(['Pentanet.GG', 'PGG'], 'Pentanet.GG'),
			**dict.fromkeys(['BMR', 'Bombers'], 'Bombers'),
			**dict.fromkeys(['TTC', 'Tectonic'], 'Tectonic'),
			**dict.fromkeys(['SIN', 'Sin Gaming'], 'Sin Gaming'),
			**dict.fromkeys(['ABY', 'Abyss Esports', 'Abyss'], 'Abyss'),
			**dict.fromkeys(['tM', 'TM Gaming'], 'TM Gaming'),
			**dict.fromkeys(['RGC', 'Team Regicide'], 'Team Regicide'),
			**dict.fromkeys(['TM', 'Tainted Minds'], 'Tainted Minds'),
			**dict.fromkeys(['X5', 'Team Exile5'], 'Team Exile5'),

			# HK, Macau, SEA (PCS)
			**dict.fromkeys(['AHQ', 'ahq', 'AHQ e-Sports Club', 'ahq eSports Club', 'ahq e-Sports Club', 'ahq eSports'], 'AHQ'),
			**dict.fromkeys(['Alpha Esports', 'ALF', '1ALF', '2ALF'], 'Alpha Esports'),
			**dict.fromkeys(['Berjaya Dragons', 'BJD'], 'Berjaya Dragons'),
			**dict.fromkeys(['Hong Kong Attitude', 'HKA'], 'Hong Kong Attitude'),
			**dict.fromkeys(['J Team', 'JT'], 'J Team'),
			**dict.fromkeys(['Liyab Esports', 'LYB', '3LYB', '4LYB', '5LYB', '7LYB', '8LYB', 'LYB6'], 'Liyab Esports'),
			**dict.fromkeys(['Machi Esports', 'MCX', 'Machi 17'], 'Machi Esports'),
			**dict.fromkeys(['Nova Esports', 'NOV', 'Team Nova'], 'Nova Esports'),
			**dict.fromkeys(['Resurgence', 'RSG'], 'Resurgence'),
			**dict.fromkeys(['Talon Esports', 'TLN', 'PSG', 'Talon', 'PSG Talon'], 'Talon Esports'),
			**dict.fromkeys(['MAD Team'], 'MAD Team'),
			**dict.fromkeys(['GRX', 'G-Rex', 'G Rex'], 'G Rex'),
			**dict.fromkeys(['FW', 'Flash Wolves'], 'Flash Wolves'),
			**dict.fromkeys(['DG', 'Dragon Gate Team'], 'Dragon Gate Team'),
			**dict.fromkeys(['Afro', 'Team Afro'], 'Team Afro'),
			**dict.fromkeys(['Raise', 'Raise Gaming'], 'Raise Gaming'),
			**dict.fromkeys(['WS', 'Wayi Spider'], 'Wayi Spider'),
			**dict.fromkeys(['FBL', 'Fire Ball', 'Fireball'], 'Fireball'),
			**dict.fromkeys(['XG', 'eXtreme Gamers'], 'eXtreme Gamers'),
			**dict.fromkeys(['HKES', 'Hong Kong Esports'], 'Hong Kong Esports'),
			**dict.fromkeys(['ahq Fighter'], 'ahq Fighter'),


			# Japan (LJL)
			**dict.fromkeys(['AXIZ', 'AXZ'], 'AXIZ'),
			**dict.fromkeys(['Burning Core', 'BC'], 'Burning Core'),
			**dict.fromkeys(['Crest Gaming Act', 'CGA'], 'Crest Gaming Act'),
			**dict.fromkeys(['Detonation FocusMe', 'DFM', 'DetonatioN FM', 'DetonatioN FocusMe', 'DetonatioN Rising'], 'Detonation FocusMe'),
			**dict.fromkeys(['Fukuoka SoftBank Hawks', 'SHG', 'SoftBank Hawk', 'Fukuoka SoftBank Hawks gaming'], 'Fukuoka SoftBank Hawks'),
			**dict.fromkeys(['Rascal Jester', 'RJ'], 'Rascal Jester'),
			**dict.fromkeys(['Sengoku Gaming', 'SG'], 'Sengoku Gaming'),
			**dict.fromkeys(['V3 Esports', 'V3'], 'V3 Esports'),
			**dict.fromkeys(['USG', 'Unsold Stuff Gaming'], 'Unsold Stuff Gaming'),
			**dict.fromkeys(['PGM', '1PGM', 'PGM1', 'PENTAGRAM'], 'PENTAGRAM'),
			**dict.fromkeys(['7h', '7th heaven'], '7th heaven'),
			**dict.fromkeys(['RPG', 'Rampage'], 'Rampage'),
			**dict.fromkeys(['SCARZ', 'SCARZ Burning Core'], 'SCARZ'),
			**dict.fromkeys(['AE', 'AKIHABARA ENCOUNT', 'AKIBA ENCOUNT'], 'AKIHABARA ENCOUNT'),
			**dict.fromkeys(['BQB', 'BowQen Blackbucks'], 'BowQen Blackbucks'),

			# Latin America (LLA)
			**dict.fromkeys(['All Knights', 'AK'], 'All Knights'),
			**dict.fromkeys(['Azules Esports', 'AZU', 'UCH'], 'Azules Esports'),
			**dict.fromkeys(['Furious Gaming', 'FG', 'Furious'], 'Furious Gaming'),
			**dict.fromkeys(['Infinity Esports', 'INF', 'Gillette INF', 'Infinity'], 'Infinity Esports'),
			**dict.fromkeys(['Isurus', 'ISG', 'Isurus Gaming'], 'Isurus'),
			**dict.fromkeys(['Pixel Esports', 'PIX', 'Pixel Esports Club', 'Pixel Club'], 'Pixel Esports'),
			**dict.fromkeys(['Rainbow7', 'R7'], 'Rainbow7'),
			**dict.fromkeys(['XTEN', 'XTEN Esports', 'XTN'], 'XTEN'),
			**dict.fromkeys(['KLG', 'Kaos Latin Gamers'], 'Kaos Latin Gamers'),
			**dict.fromkeys(['MLC', 'MAD Lions E.C. Colombia'], 'MADL Colombia'),

			# Vietnam (VCS)
			**dict.fromkeys(['Cerberus Esports', 'CERBERUS Esports', 'Cerberus', 'CES'], 'Cerberus Esports'),
			**dict.fromkeys(['EVOS Esports', 'EVOS', 'EVS'], 'EVOS Esports'),
			**dict.fromkeys(['GAM Esports', 'GAM'], 'GAM Esports'),
			**dict.fromkeys(['OverPower Esports', 'OverPower', 'OPG'], 'OverPower Esports'),
			**dict.fromkeys(['Percent Esports'], 'Percent Esports'),
			**dict.fromkeys(['Saigon Buffalo', 'PVB', 'DBL', 'SGB', 'Phong Vũ Buffalo'], 'Saigon Buffalo'),
			**dict.fromkeys(['Team Flash', 'FL'], 'Team Flash'),
			**dict.fromkeys(['Team Secret', '팀 시크릿', 'LK', 'Lowkey Esports.Vietnam'], 'Team Secret'),
			**dict.fromkeys(['CR', 'Cherry Esports'], 'Cherry Esports'),
			**dict.fromkeys(['FFQ', 'Friends Forever Gaming'], 'Friends Forever Gaming'),
			**dict.fromkeys(['YGE', 'Young Generation'], 'Young Generation'),
			**dict.fromkeys(['NGE', 'Next Gen Esports'], 'Next Gen Esports'),
			**dict.fromkeys(['EHU', 'e.Hub United'], 'e.Hub United'),
			**dict.fromkeys(['UTM', 'Ultimate', 'UTM Esports'], 'Ultimate'),
			**dict.fromkeys(['LG Red'], 'LG Red'),
			**dict.fromkeys(['FIG', 'Fighters Gaming'], 'Fighters Gaming'),
			**dict.fromkeys(['FTV', 'FTV Esports'], 'FTV Esports'),
			**dict.fromkeys(['HOF', 'Hall of Fame'], 'Hall of Fame'),
			**dict.fromkeys(['ADN', 'Cube Adonis', 'V Gaming Adonis'], 'Cube Adonis'),
			**dict.fromkeys(['Vikings', 'Vikings Gaming'], 'Vikings Gaming'),
			**dict.fromkeys(['SGD', 'Sky Gaming Daklak', 'Sky Gaming'], 'Sky Gaming Daklak'),
			**dict.fromkeys(['QG', 'QTV Gaming'], 'QTV Gaming'),
			**dict.fromkeys(['VGA', 'V Gaming Adonis'], 'V Gaming Adonis'),
			**dict.fromkeys(['PER', 'Percent Esports'], 'Percent Esports'),
			**dict.fromkeys(['LPG', 'LP Gaming'], 'LP Gaming'),

			# Common Wealth (LCL)
			**dict.fromkeys(['CrowCrowd', 'CC'], 'CrowCrowd'),
			**dict.fromkeys(['Dragon Army', 'DA'], 'Dragon Army'),
			**dict.fromkeys(['Elements Pro Gaming', 'EPG'], 'Elements Pro Gaming'),
			**dict.fromkeys(['Gambit', 'Gambit Esports', 'Gambit.CIS', 'GMB'], 'Gambit'),
			**dict.fromkeys(['RoX'], 'RoX'),
			**dict.fromkeys(['Vega Squadron', 'VEG'], 'Vega Squadron'),
			**dict.fromkeys(['One Breath Gaming', 'OBG'], 'One Breath Gaming'),
			**dict.fromkeys(['M19'], 'M19'),
			**dict.fromkeys(['VS', 'Vaevictis eSports'], 'Vaevictis eSports'),
			**dict.fromkeys(['Just A', 'Team Just Alpha'], 'Team Just Alpha'),
			**dict.fromkeys(['NV.CIS', 'Natus Vincere', 'Natus Vincere.CIS', 'Natus Vincere CIS'], 'Natus Vincere.CIS'),
			**dict.fromkeys(['TJ', 'Team Just'], 'Team Just'),
			**dict.fromkeys(['Virtus.pro'], 'Virtus.pro'),
			**dict.fromkeys(['Unicorns Of Love.CIS'], 'UOL.CIS'),
			

			# Belgian (BL)
			**dict.fromkeys(['ATR', 'Aethra Esports', 'Aethra'], 'Aethra'),
			**dict.fromkeys(['BG', 'Brussels Guardians'], 'Brussels Guardians'),
			**dict.fromkeys(['KVM', 'KV Mechelen'], 'KV Mechelen'),
			**dict.fromkeys(['S1', 'Sector One'], 'Sector One'),
			**dict.fromkeys(['7AM', 'Team 7AM'], 'Team 7AM'),
			**dict.fromkeys(['RSCA', 'RSCA Esports'], 'RSCA'),
			**dict.fromkeys(['TO', 'Timeout Esports'], 'Timeout Esports'),

			# Dutch (DL)
			**dict.fromkeys(['TRL', 'Team THRILL', 'Team THRLL'], 'THRILL'),
			**dict.fromkeys(['PSV', 'PSV Esports'], 'PSV'),
			**dict.fromkeys(['EZ', 'Team Echo Zulu', 'Echo Zulu'], 'Echo Zulu'),
			**dict.fromkeys(['Dynasty'], 'Dynasty'),
			**dict.fromkeys(['LLL', 'LowLandLions'], 'LowLandLions'),
			**dict.fromkeys(['MCN', 'mCon', 'mCon esports', 'mCon Rotterdam'], 'mCon Rotterdam'),
			**dict.fromkeys(['DK', 'Defusekids'], 'Defusekids'),

			# Italy (PGN)
			**dict.fromkeys(['SPK', 'CP Sparks', 'Campus Party Sparks'], 'CP Sparks'),
			**dict.fromkeys(['MKS', 'Mkers'], 'Mkers'),
			**dict.fromkeys(['RCN', 'Racoon'], 'Racoon'),
			**dict.fromkeys(['SMS', 'Morning Stars', 'Samsung Morning Stars'], 'Morning Stars'),
			**dict.fromkeys(['OP', 'Outplayed', 'OutPlayed'], 'Outplayed'),
			**dict.fromkeys(['CGG', 'Cyberground', 'Cyberground Gaming'], 'Cyberground'),
			**dict.fromkeys(['DD', 'DayDreamers', 'Daydreamers'], 'DayDreamers'),
			**dict.fromkeys(['YDN', 'YDN Gamers'], 'YDN'),
			**dict.fromkeys(['Q4G', 'QLASH Forge'], 'QLASH Forge'),
			**dict.fromkeys(['MOR', 'MOBA ROG'], 'MOBA ROG'),

			# Portugal (LPLOL)
			**dict.fromkeys(['BFC', 'Boavista FC', 'Boavista'], 'Boavista'),
			**dict.fromkeys(['EGN', 'Electronik Generation', 'Electronik', 'EGN Esports'], 'Electronik'),
			**dict.fromkeys(['FTW', 'For The Win eSports', 'For The Win', 'For The Win Esports'], 'For The Win'),
			**dict.fromkeys(['GCE', 'GeekCase eSports', 'GeekCase', 'GC'], 'GeekCase'),
			**dict.fromkeys(['GTZ', 'GTZ Bulls'], 'GTZ'),
			**dict.fromkeys(['KLE', 'Karma Clan Esports', 'Karma Clan', 'KRM', 'Karma'], 'Karma'),
			**dict.fromkeys(['OFF', 'OFFSET Esports', 'OFF7'], 'OFFSET'),
			**dict.fromkeys(['SAMC', 'SAMCLAN Esports Club', 'SAM'], 'SAMCLAN'),
			**dict.fromkeys(['EPE', 'Estoril Praia eSports'], 'Estoril Praia eSports'),

			# Germany (Premier Tour)
			**dict.fromkeys(['S04E', 'FC Shalke 04 Evolution', 'Schalke Evolution', 'FC Schalke 04 Evolution'], 'S04E'),
			**dict.fromkeys(['UOLSE', 'Unicorns Of Love Sexy Edition', 'Unicorns Of Love SE'], 'UOLSE'),
			**dict.fromkeys(['OP innogy', 'OP innogy eSport'], 'OP innogy'),
			**dict.fromkeys(['mYinsanity'], 'mYinsanity'),
			**dict.fromkeys(['Team GamerLegion', 'GamerLegion', 'GL'], 'Team GamerLegion'),
			**dict.fromkeys(['EURONICS Gaming', 'EURONICS'], 'EURONICS Gaming'),
			**dict.fromkeys(['Ad Hoc Gaming', 'ad hoc gaming'], 'Ad Hoc Gaming'),
			**dict.fromkeys(['mousesports', 'Mousesports', 'MOUZ'], 'mousesports'),
			**dict.fromkeys(['BIG', 'Berlin International Gaming'], 'BIG'),

			# LCS_a
			**dict.fromkeys(['GCU', 'Gold Coin United'], 'Gold Coin United'),
			**dict.fromkeys(['TS', 'Tempo Storm'], 'Tempo Storm'),
			**dict.fromkeys(['EUN', 'eUnited'], 'eUnited'),
			**dict.fromkeys(['BGJ', 'Big Gods Jackals'], 'Big Gods Jackals'),
			**dict.fromkeys(['TG', 'Team Gates'], 'Team Gates'),
			**dict.fromkeys(['DFX', 'Delta Fox'], 'Delta Fox'),
			**dict.fromkeys(['CLG.A', 'CLG Academy'], 'CLG Academy'),
			**dict.fromkeys(['FOX.A', 'Echo Fox Academy'], 'Echo Fox Academy'),
			**dict.fromkeys(['TL.A', 'TL Academy', 'Team Liquid Academy'], 'TL Academy'),
			**dict.fromkeys(['C9.A', 'Cloud9 Academy'], 'Cloud9 Academy'),
			**dict.fromkeys(['FLY.A', 'FlyQuest Academy'], 'FlyQuest Academy'),
			**dict.fromkeys(['TSM.A', 'TSM Academy'], 'TSM Academy'),
			**dict.fromkeys(['CG.A', 'Clutch Gaming Academy'], 'Clutch Gaming Academy'),
			**dict.fromkeys(['100.A', '100 Thieves Academy'], '100 Thieves Academy'),
			**dict.fromkeys(['OPT.A', 'OpTic Gaming Academy'], 'OpTic Gaming Academy'),
			**dict.fromkeys(['GG.A', 'Golden Guardians Academy'], 'Golden Guardians Academy'),
			**dict.fromkeys(['DIG.A', 'Dignitas Academy'], 'Dignitas Academy'),
			**dict.fromkeys(['EG.A', 'Evil Geniuses Academy'], 'Evil Geniuses Academy'),
			**dict.fromkeys(['IMT.A', 'Immortals Academy'], 'Immortals Academy'),

			# LDL
			**dict.fromkeys(['EDGY', 'EDG Youth Team'], 'EDG Youth Team'),
			**dict.fromkeys(['87', 'V5 87'], 'V5 87'),
			**dict.fromkeys(['JDM', 'Joy Dream'], 'Joy Dream'),
			**dict.fromkeys(['VP', 'VP Game'], 'VP Game'),
			**dict.fromkeys(['SWD', 'Snake WuDu'], 'Snake WuDu'),
			**dict.fromkeys(['WEA', 'Team WE Academy'], 'Team WE Academy'),
			**dict.fromkeys(['LEG', 'Legend Esport Gaming'], 'Legend Esport Gaming'),
			**dict.fromkeys(['RWS', 'Rogue Warriors Shark'], 'Rogue Warriors Shark'),
			**dict.fromkeys(['IGY', 'IG Young', 'Invictus Gaming Young'], 'IG Young'),
			**dict.fromkeys(['FPB', 'FunPlus Phoenix Blaze'], 'FunPlus Phoenix Blaze'),
			**dict.fromkeys(['OMD', 'Oh My Dream'], 'Oh My Dream'),
			**dict.fromkeys(['VTG', 'Victorious Gaming'], 'Victorious Gaming'),
			**dict.fromkeys(['LGE', 'LinGan eSports', 'LinGan e-Sports'], 'LinGan eSports'),
			**dict.fromkeys(['SNS', 'Suning S', 'Suning-S'], 'Suning S'),
			**dict.fromkeys(['KOF', 'King of Future'], 'King of Future'),
			**dict.fromkeys(['TSG', 'Triumphant Song Gaming'], 'Triumphant Song Gaming'),
			**dict.fromkeys(['VGP', 'Vici Gaming Potential'], 'Vici Gaming Potential'),
			**dict.fromkeys(['BLGJ', 'Bilibili Gaming Junior'], 'Bilibili Gaming Junior'),
			**dict.fromkeys(['YM', 'Young Miracles'], 'Young Miracles'),
			**dict.fromkeys(['SDX', 'Shu Dai Xiong Gaming'], 'Shu Dai Xiong Gaming'),
			**dict.fromkeys(['SDP', 'SinoDragon Prince'], 'SinoDragon Prince'),
			**dict.fromkeys(['TESC', 'Top Esports Challenger'], 'Top Esports Challenger'),
			**dict.fromkeys(['D7G', 'D7G Esports Club'], 'D7G Esports Club'),
			**dict.fromkeys(['DMOY', 'Dominus Esports Young'], 'Dominus Esports Young'),
			**dict.fromkeys(['LNGA', 'LNG Academy'], 'LNG Academy'),
			**dict.fromkeys(['LGDY', 'LGD Gaming Young', 'LGD Gaming Young Team'], 'LGD Gaming Young'),
			**dict.fromkeys(['WZ', 'WanZhen Esports Club'], 'WanZhen Esports Club'),
			**dict.fromkeys(['AC', 'All Combo'], 'All Combo'),
			**dict.fromkeys(['ESY', 'eStar Young'], 'eStar Young'),
			**dict.fromkeys(['JNG', 'JingNetGame'], 'JingNetGame'),
			**dict.fromkeys(['OSE', 'Optical Spectrum E-sport', 'optical spectrum E-sports'], 'Optical Spectrum E-sport'),
			**dict.fromkeys(['DS', 'DS Gaming'], 'DS Gaming'),
			**dict.fromkeys(['LD', 'Legend Dragon'], 'Legend Dragon'),
			**dict.fromkeys(['NON', 'Now or Never'], 'Now or Never'),
			**dict.fromkeys(['ING', 'IN Gaming'], 'IN Gaming'),
			**dict.fromkeys(['ME', 'Mighty Eagle'], 'Mighty Eagle'),
			**dict.fromkeys(['SAT', 'Saint Gaming'], 'Saint Gaming'),
			**dict.fromkeys(['GED', 'Gama E-Sport Dream', 'GD', 'Gama Dream', 'Gama E-Sport Dream (伽马电子竞技)'], 'Gama Dream'),
			**dict.fromkeys(['YG', 'Young Glory'], 'Young Glory'),
			**dict.fromkeys(['TH', 'Team Hurricane'], 'Team Hurricane'),
			**dict.fromkeys(['TF', 'Team Fighter'], 'Team Fighter'),
			**dict.fromkeys(['MSC', 'Moss Seven Club'], 'Moss Seven Club'),
			**dict.fromkeys(['Scorpio Game'], 'Scorpio Game'),
			**dict.fromkeys(['Royal Club'], 'Royal Club'),
			**dict.fromkeys(['Unlimited Potential'], 'Unlimited Potential'),
			
			# OCS
			**dict.fromkeys(['NX', 'Team Noxide'], 'Team Noxide'),
			**dict.fromkeys(['OLW', 'Outlaws'], 'Outlaws'),
			**dict.fromkeys(['SNA', 'Sin Academy'], 'Sin Academy'),
			**dict.fromkeys(['CVD', 'Corvidae'], 'Corvidae'),
			**dict.fromkeys(['AS', 'Alpha Sydney'], 'Alpha Sydney'),
			**dict.fromkeys(['LGG', 'Legacy Genesis'], 'Legacy Genesis'),
			**dict.fromkeys(['TM.B', 'Tainted Minds Blue'], 'Tainted Minds Blue'),
			**dict.fromkeys(['ATH', 'Athletico Esports'], 'Athletico Esports'),
			**dict.fromkeys(['LX', 'Lynx'], 'Lynx'),
			**dict.fromkeys(['Abyss Academy'], 'Abyss Academy'),
			**dict.fromkeys(['Chiefs Academy'], 'Chiefs Academy'),

			# Challengers Korea
			**dict.fromkeys(['CJ', 'CJ Entus'], 'CJ Entus'),
			**dict.fromkeys(['BPZ'], 'BPZ'),
			**dict.fromkeys(['IGS', 'I Gaming Star'], 'I Gaming Star'),
			**dict.fromkeys(['BtC', 'Team BattleComics'], 'Team BattleComics'),
			**dict.fromkeys(['RSSG', 'Rising Star Gaming', 'Rising SuperStar Gaming'], 'Rising Star Gaming'),
			**dict.fromkeys(['ESS', 'ES Sharks'], 'ES Sharks'),
			**dict.fromkeys(['RGA', 'REVERSE Gaming'], 'REVERSE Gaming'),
			**dict.fromkeys(['WNS', 'Winners'], 'Winners'),
			**dict.fromkeys(['GCB', 'GC Busan Rising Star'], 'GC Busan Rising Star'),
			**dict.fromkeys(['VSG'], 'VSG'),
			**dict.fromkeys(['BRB', 'hyFresh Blade'], 'hyFresh Blade'),
			**dict.fromkeys(['ASR', 'Asura'], 'Asura'),
			**dict.fromkeys(['SPG', 'ASP', 'Awesome Spear', 'Spear Gaming'], 'Awesome Spear'),
			**dict.fromkeys(['Seorabeol Gaming', 'SRB'], 'Seorabeol Gaming'),
			**dict.fromkeys(['EM', 'Element Mystic'], 'Element Mystic'),
			**dict.fromkeys(['OZ', 'OZ Gaming'], 'OZ Gaming'),
			**dict.fromkeys(['RNW', 'RunAway'], 'RunAway'),
			**dict.fromkeys(['ESC', 'ESC Shane'], 'ESC Shane'),
			**dict.fromkeys(['HOU', 'HOU GAMING'], 'HOU GAMING'),
			**dict.fromkeys(['WhereAreyouFrom'], 'WhereAreyouFrom'),
			
			# TPL_a
			**dict.fromkeys(['FB.A', 'Fenerbahce Academy', '1907 Fenerbahçe Academy'], 'Fenerbahce Academy'),
			**dict.fromkeys(['HWA.A', 'HWA Gaming Academy', 'HWA Academy'], 'HWA Gaming Academy'),
			**dict.fromkeys(['SUP.A', 'SuperMassive Academy'], 'SuperMassive Academy'),
			**dict.fromkeys(['BJK.A', 'Besiktas Academy', 'Beşiktaş Academy'], 'Besiktas Academy'),
			**dict.fromkeys(['RY.A', 'Royal Youth Academy'], 'Royal Youth Academy'),
			**dict.fromkeys(['DP.A', 'Dark Passage Academy'], 'Dark Passage Academy'),
			**dict.fromkeys(['GS.A', 'Galatasaray Academy'], 'Galatasaray Academy'),
			**dict.fromkeys(['AUR.A', 'AURORA Academy', 'Team AURORA Academy'], 'AURORA Academy'),
			**dict.fromkeys(['BS.A', 'Bursaspor Academy'], 'Bursaspor Academy'),
			**dict.fromkeys(['GAL.A', 'Galakticos Academy'], 'Galakticos Academy'),
			**dict.fromkeys(['IWC.A', 'Istanbul Wildcats Academy', 'İstanbul Wildcats Academy'], 'Istanbul Wildcats Academy'),
			**dict.fromkeys(['5R.A', '5 Ronin Academy'], '5 Ronin Academy'),

			# ECS - LMS 2부
			**dict.fromkeys(['Yetti', 'Team Yetti'], 'Team Yetti'),
			**dict.fromkeys(['JII', 'J Team 2'], 'J Team 2'),
			**dict.fromkeys(['Cougar', 'Cougar E-Sport'], 'Cougar E-Sport'),
			**dict.fromkeys(['NonHK'], 'NonHK'),
			**dict.fromkeys(['228', 'TWOTWOEIGHT'], 'TWOTWOEIGHT'),
			**dict.fromkeys(['WOR', 'WingsOflibeRty'], 'WingsOflibeRty'),
			**dict.fromkeys(['17A', '17 Academy'], '17 Academy'),
			**dict.fromkeys(['HKA.M', 'HK Attitude Mage'], 'HK Attitude Mage'),
			**dict.fromkeys(['KE', 'Kowloon Esports', 'Kowloon Esports (九龍電競)'], 'Kowloon Esports'),
			**dict.fromkeys(['AOC', 'AOC Gaming'], 'AOC Gaming'),
			**dict.fromkeys(['AFB', 'Afro Beast'], 'Afro Beast'),
			**dict.fromkeys(['KSF', 'K Special Forces'], 'K Special Forces'),
			**dict.fromkeys(['AG', 'Ares Gaming'], 'Ares Gaming'),
			**dict.fromkeys(['178', 'ONE SEVEN EIGHT'], 'ONE SEVEN EIGHT'),
			**dict.fromkeys(['BUFF'], 'BUFF'),
			**dict.fromkeys(['SE', 'SuperEsports'], 'SuperEsports'),
			**dict.fromkeys(['NFC', 'NoFancy'], 'NoFancy'),
			**dict.fromkeys(['AQ', 'Alice Queen'], 'Alice Queen'),
			**dict.fromkeys(['Forger', 'Forger Esports'], 'Forger Esports'),
			**dict.fromkeys(['FS', 'F-Soul Esports'], 'F-Soul Esports'),
			**dict.fromkeys(['GRI', 'G Rex Infinite'], 'G Rex Infinite'),
			**dict.fromkeys(['FD', 'Fish Dive Team'], 'Fish Dive Team'),
			**dict.fromkeys(['FH', 'Flash Husky'], 'Flash Husky'),
			**dict.fromkeys(['SGH', 'Suns Gos Hawk'], 'Suns Gos Hawk'),

			# EM
			**dict.fromkeys(['FNC.A', 'Fnatic Academy'], 'Fnatic Academy'),
			**dict.fromkeys(['MSF.A', 'Misfits Academy'], 'Misfits Academy'),
			**dict.fromkeys(['MIL', 'Millenium'], 'Millenium'),
			**dict.fromkeys(['TK', 'Team Kinguin'], 'Team Kinguin'),
			**dict.fromkeys(['RB', 'Red Bulls'], 'Red Bulls'),
			**dict.fromkeys(['WAR', 'Wind and Rain'], 'Wind and Rain'),
			**dict.fromkeys(['ESB', 'eSuba'], 'eSuba'),
			**dict.fromkeys(['ENC', 'Enclave Gaming'], 'Enclave Gaming'),
			**dict.fromkeys(['4G', 'Team Forge'], 'Team Forge'),
			**dict.fromkeys(['MRS', 'Movistar Riders'], 'Movistar Riders'),
			**dict.fromkeys(['CBB', 'Could Be Better'], 'Could Be Better'),
			**dict.fromkeys(['Klik', 'KlikTech'], 'KlikTech'),
			**dict.fromkeys(['ACT', 'Team Ascent'], 'Team Ascent'),
			**dict.fromkeys(['K1CK', 'K1CK eSports', 'K1', 'K1CK Neosurf', 'K1ck Neosurf'], 'K1CK Neosurf'),
			**dict.fromkeys(['SP5', 'Spain5'], 'Spain5'),
			**dict.fromkeys(['PPK', 'Packa Pappas Kappsack', 'Packa Pappas Kappsäck'], 'Packa Pappas Kappsack'),
			**dict.fromkeys(['SM', 'Szata Maga'], 'Szata Maga'),
			**dict.fromkeys(['Gent', 'Gentside'], 'Gentside'),
			**dict.fromkeys(['VGIA', 'Vodafone Giants', 'Vodafone Giants.Spain'], 'Vodafone Giants'),
			**dict.fromkeys(['CZV', 'Crvena zvezda', 'Crvena zvezda Esports'], 'Crvena zvezda'),
			**dict.fromkeys(['SKP', 'SK Gaming Prime'], 'SK Gaming Prime'),
			**dict.fromkeys(['DV1', 'devils.one'], 'devils.one'),
			**dict.fromkeys(['MSFP', 'Misfits Premier'], 'Misfits Premier'),
			**dict.fromkeys(['Diabolus Esports'], 'Diabolus Esports'),
			**dict.fromkeys(['NKI', 'NYYRIKKI White'], 'NYYRIKKI White'),
			**dict.fromkeys(['OGB', 'Origen BCN'], 'Origen BCN'),
			**dict.fromkeys(['VITB', 'Vitality.Bee'], 'Vitality.Bee'),
			**dict.fromkeys(['REC', 'Rogue Esports Club'], 'Rogue Esports Club'),
			**dict.fromkeys(['FLK', 'FALKN'], 'FALKN'),
			**dict.fromkeys(['ASUS', 'ASUS ROG ELITE'], 'ASUS ROG ELITE'),
			**dict.fromkeys(['VIP', 'Vipers Inc'], 'Vipers Inc'),
			**dict.fromkeys(['IF', 'Intrepid Fox Gaming'], 'Intrepid Fox Gaming'),
			**dict.fromkeys(['MADM', 'MAD Lions Madrid'], 'MAD Lions Madrid'),
			**dict.fromkeys(['KEN', 'Kenty'], 'Kenty'),
			**dict.fromkeys(['WLG', 'WLGaming Esports'], 'WLGaming Esports'),
			**dict.fromkeys(['PIG', 'PIGSPORTS'], 'PIGSPORTS'),
			**dict.fromkeys(['Team-LDLC', 'LDLC', 'LDLC OL'], 'LDLC OL'),
			**dict.fromkeys(['G2AR', 'G2 Arctic'], 'G2 Arctic'),
			**dict.fromkeys(['CR4', 'CR4ZY'], 'CR4ZY'),
			**dict.fromkeys(['RDL', 'Riddle Esports'], 'Riddle Esports'),
			**dict.fromkeys(['IW', 'Iron Wolves'], 'Iron Wolves'),
			**dict.fromkeys(['PT7', '7more7 Pompa', '7more7 Pompa Team'], '7more7 Pompa'),
			**dict.fromkeys(['5K', 'Five Kings'], 'Five Kings'),
			**dict.fromkeys(['MAD Lions E.C.'], 'MAD Lions E.C.'),
			**dict.fromkeys(['PAO', 'Panathinaikos AC eSports'], 'Panathinaikos'),
			**dict.fromkeys(['ATL', 'Team Atlantis'], 'Team Atlantis'),
			**dict.fromkeys(['IHG', 'Illuminar Gaming'], 'Illuminar Gaming'),
			**dict.fromkeys(['Turing eSports'], 'Turing eSports'),
			**dict.fromkeys(['PGM', 'Penguins', 'UCAM Penguins'], 'Penguins'),
			**dict.fromkeys(['SPGeSports'], 'SPGeSports'),
			**dict.fromkeys(['VT', 'Ventus Esports'], 'Ventus Esports'),
			**dict.fromkeys(['FP.WLG', 'Future Perfect WLGaming'], 'Future Perfect WLGaming'),
			**dict.fromkeys(['R5', 'Random 5'], 'Random 5'),
			**dict.fromkeys(['eN', 'eNsure'], 'eNsure'),
			**dict.fromkeys(['FNC.R', 'Fnatic Rising'], 'Fnatic Rising'),
			**dict.fromkeys(['AST', 'AS Trencin esports', 'AS Trenčín esports'], 'AS Trencin esports'),
			**dict.fromkeys(['SVP', 'Splyce Vipers'], 'Splyce Vipers'),
			**dict.fromkeys(['GOD', 'Godsent'], 'Godsent'),
			**dict.fromkeys(['GO', 'GamersOrigin'], 'GamersOrigin'),
			**dict.fromkeys(['BTXL', 'BT Excel', 'XL.UK', 'Excel UK'], 'BT Excel'),
			**dict.fromkeys(['RGO', 'AGO ROGUE'], 'AGO ROGUE'),
			**dict.fromkeys(['SNG', 'Team Singularity'], 'Team Singularity'),
			**dict.fromkeys(['WIZ', 'Energypot Wizards'], 'Energypot Wizards'),
			**dict.fromkeys(['SUPP', 'SuppUp eSports'], 'SuppUp eSports'),
			**dict.fromkeys(['SINNERS Esports'], 'SINNERS Esports'),
			**dict.fromkeys(['Cyber Gaming'], 'Cyber Gaming'),
			**dict.fromkeys(['Paris Saint-Germain eSports'], 'Paris Saint-Germain'),

			# CIS_CL
			**dict.fromkeys(['DOL', 'Dolphins'], 'Dolphins'),
			**dict.fromkeys(['Salary', 'The Largest Salary'], 'The Largest Salary'),
			**dict.fromkeys(['CMCE', 'Comanche'], 'Comanche'),
			**dict.fromkeys(['J.ICE', 'Team Just.ICE', 'Team Just Ice'], 'Team Just.ICE'),
			**dict.fromkeys(['DA.A', 'Dragon Army Academy'], 'Dragon Army Academy'),
			**dict.fromkeys(['Aston', 'Aston eSports'], 'Aston eSports'),
			**dict.fromkeys(['PPC58', 'PlaPro.c58'], 'PlaPro.c58'),
			**dict.fromkeys(['AVN', 'AVANGAR'], 'AVANGAR'),
			**dict.fromkeys(['MNL', 'Monolith Gaming'], 'Monolith Gaming'),
			**dict.fromkeys(['SEAD', 'SeaDoggos'], 'SeaDoggos'),
			
			# BRCC
			**dict.fromkeys(['INTZ G', 'INTZ.Genesis'], 'INTZ.Genesis'),
			**dict.fromkeys(['HKS', 'Iron Hawks e-Sports', 'Iron Hawks'], 'Iron Hawks'),
			**dict.fromkeys(['IDMP', 'IDM Pirata'], 'IDM Pirata'),
			**dict.fromkeys(['KEEP', 'Keep Gaming'], 'Keep Gaming'),
			**dict.fromkeys(['MGG', 'Merciless Gaming'], 'Merciless Gaming'),
			**dict.fromkeys(['IDM', 'IDM Gaming'], 'IDM Gaming'),
			**dict.fromkeys(['5Fox', '5Fox E-Sports Club'], '5Fox'),
			**dict.fromkeys(['SUB', 'Submarino Stars'], 'Submarino Stars'),
			**dict.fromkeys(['WP', 'WP Gaming'], 'WP Gaming'),
			**dict.fromkeys(['FKL', 'Falkol'], 'Falkol'),
			**dict.fromkeys(['HL', 'Havan Liberty Gaming', 'Havan Liberty Academy'], 'Havan Liberty Gaming'),
			**dict.fromkeys(['RNS', 'Rensga eSports'], 'Rensga eSports'),
			**dict.fromkeys(['ITX', 'Intergalaxy Tigers', 'Intergalaxy Tigers Gaming'], 'Intergalaxy Tigers')		
		}

		self.playerName_dict = {
			**dict.fromkeys(['reje'], 'Reje')
		}

		self.betType_dict = {
			**dict.fromkeys(['2-0', '2-1', '0-2', '1-2', '3-0', '3-1', '3-2', '0-3', '1-3', '2-3',
			'penta_team_1', 'penta_team_2', 'quadra_team_1', 'quadra_team_2', 'first_baron_team_1',
			'first_baron_team_2', 'first_blood_team_1', 'first_blood_team_2', 'first_dragon_team_1',
			'first_dragon_team_2', 'first_inhib_team_1', 'first_inhib_team_2', 'first_tower_team_1',
			'first_tower_team_2', 'game_win_team_1', 'game_win_team_2', 'match_handicap+1.50_team_away',
			'match_handicap+1.50_team_home', 'match_handicap-1.50_team_away', 'match_handicap-1.50_team_home',
			'second_dragon_team_1', 'second_dragon_team_2', 'set_win_team_1', 'set_win_team_2',
			'third_dragon_team_1', 'third_dragon_team_2', 'first_10kill_team_1', 'first_10kill_team_2',
			'first_5kill_team_1', 'first_5kill_team_2', 'first_rift_team_1', 'first_rift_team_2'], 'special'),

			**dict.fromkeys(['match_handicap+1.50_team_away', 'match_handicap+1.50_team_home', 
			'match_handicap+2.50_team_away', 'match_handicap+2.50_team_home',
			'match_handicap-1.50_team_away', 'match_handicap-1.50_team_home', 
			'match_handicap-2.50_team_away', 'match_handicap-2.50_team_home',
			'total_kill_handicap +0.5_1', 'total_kill_handicap +0.5_2', 'total_kill_handicap +1.5_1', 'total_kill_handicap +1.5_2',
			'total_kill_handicap +10.5_1', 'total_kill_handicap +10.5_2', 'total_kill_handicap +11.5_1', 'total_kill_handicap +11.5_2',
			'total_kill_handicap +12.5_1', 'total_kill_handicap +12.5_2', 'total_kill_handicap +13.5_1', 'total_kill_handicap +13.5_2',
			'total_kill_handicap +14.5_1', 'total_kill_handicap +14.5_2', 'total_kill_handicap +2.5_1', 'total_kill_handicap +2.5_2',
			'total_kill_handicap +3.5_1', 'total_kill_handicap +3.5_2', 'total_kill_handicap +4.5_1', 'total_kill_handicap +4.5_2',
			'total_kill_handicap +5.5_1', 'total_kill_handicap +5.5_2', 'total_kill_handicap +6.5_1', 'total_kill_handicap +6.5_2',
			'total_kill_handicap +7.5_1', 'total_kill_handicap +7.5_2', 'total_kill_handicap +8.5_1', 'total_kill_handicap +8.5_2',
			'total_kill_handicap +9.5_1', 'total_kill_handicap +9.5_2', 'total_kill_handicap -0.5_1', 'total_kill_handicap -0.5_2',
			'total_kill_handicap -1.5_1', 'total_kill_handicap -1.5_2', 'total_kill_handicap -10.5_1', 'total_kill_handicap -10.5_2',
			'total_kill_handicap -11.5_1', 'total_kill_handicap -11.5_2', 'total_kill_handicap -12.5_1', 'total_kill_handicap -12.5_2',
			'total_kill_handicap -13.5_1', 'total_kill_handicap -13.5_2', 'total_kill_handicap -14.5_1', 'total_kill_handicap -14.5_2',
			'total_kill_handicap -15.5_1', 'total_kill_handicap -15.5_2', 'total_kill_handicap -2.5_1', 'total_kill_handicap -2.5_2',
			'total_kill_handicap -3.5_1', 'total_kill_handicap -3.5_2', 'total_kill_handicap -4.5_1', 'total_kill_handicap -4.5_2',
			'total_kill_handicap -5.5_1', 'total_kill_handicap -5.5_2', 'total_kill_handicap -6.5_1', 'total_kill_handicap -6.5_2',
			'total_kill_handicap -7.5_1', 'total_kill_handicap -7.5_2', 'total_kill_handicap -8.5_1', 'total_kill_handicap -8.5_2',
			'total_kill_handicap -9.5_1', 'total_kill_handicap -9.5_2', 'total_kill_handicap +15.5_1', 'total_kill_handicap +15.5_2'], 'handicap'),

			**dict.fromkeys(['game_time_45.00_over', 'game_time_45.00_under', 'kill_12.5_over', 'kill_12.5_under',
			'kill_13.5_over', 'kill_13.5_under', 'kill_14.5_over', 'kill_14.5_under',
			'kill_15.5_over', 'kill_15.5_under', 'kill_16.5_over', 'kill_16.5_under',
			'kill_17.5_over', 'kill_17.5_under', 'kill_18.5_over', 'kill_18.5_under',
			'kill_19.5_over', 'kill_19.5_under', 'kill_20.5_over', 'kill_20.5_under',
			'kill_21.5_over', 'kill_21.5_under', 'kill_22.5_over', 'kill_22.5_under',
			'kill_23.5_over', 'kill_23.5_under', 'kill_24.5_over', 'kill_24.5_under',
			'kill_25.5_over', 'kill_25.5_under', 'kill_26.5_over', 'kill_26.5_under',
			'kill_27.5_over', 'kill_27.5_under', 'kill_28.5_over', 'kill_28.5_under',
			'kill_29.5_over', 'kill_29.5_under', 'kill_30.5_over', 'kill_30.5_under',
			'kill_31.5_over', 'kill_31.5_under', 'kill_32.5_over', 'kill_32.5_under',
			'kill_33.5_over', 'kill_33.5_under', 'kill_34.5_over', 'kill_34.5_under',
			'kill_35.5_over', 'kill_35.5_under', 'kill_36.5_over', 'kill_36.5_under',
			'kill_37.5_over', 'kill_37.5_under', 'total_baron_1.5_over', 'total_baron_1.5_under',
			'total_dragon_4.5_over', 'total_dragon_4.5_under', 'total_inhib_1.50_over', 'total_inhib_1.50_under',
			'total_inhib_2.50_over', 'total_inhib_2.50_under', 'total_sets_played_2.50_over', 'total_sets_played_2.50_under',
			'total_sets_played_3.50_over', 'total_sets_played_3.50_under', 'total_sets_played_4.50_over', 'total_sets_played_4.50_under',
			'total_tower_11.50_over', 'total_tower_11.50_under', 'total_tower_12.50_over', 'total_tower_12.50_under'], 'over_under'),
			
			**dict.fromkeys(['both_team_baron_no', 'both_team_baron_yes', 'both_team_dragon_no', 'both_team_dragon_yes',
			'both_team_inhib_no', 'both_team_inhib_yes', 'both_team_tower_no', 'both_team_tower_yes'], 'both')
		}

	def get_dict(self, name='all'):
		if name == 'all':
			return {**self.leagueName_dict, **self.championName_dict, **self.teamName_dict, **self.playerName_dict, **self.betType_dict}
		elif name == 'league':
			return self.leagueName_dict
		elif name == 'champion':
			return self.championName_dict
		elif name == 'team':
			return self.teamName_dict
		elif name == 'player':
			return self.playerName_dict
		elif name == 'bet':
			return self.betType_dict
		else:
			raise ImportError('There is no dictionary for that name. Please choose from [all, league, champion, team, player, bet]!')
			
	def __repr__(self):
		return 'Dictionary List: [all, league, champion, team, player, bet]'

class GamepediaDict(GameDictionary):
	def __init__(self):
		super().__init__()

	def from_year_season_league(self, year, season, league):
		if (league == 'Dutch_League') | (league == 'DL'):
			self.teamName_dict['DYN'] = 'Dynasty'
		elif (league == 'LCK'):
			self.teamName_dict['DYN'] = 'Dynamics'
			self.teamName_dict['AF'] = 'Afreeca'
			self.teamName_dict['SPG'] = 'Awesome Spear'
			
		elif (league == 'CBLOL'):
			if (year == 2017):
				self.teamName_dict['PRG'] = 'ProGaming Esports'
			elif (year == 2018):
				self.teamName_dict['PRG'] = 'ProGaming Esports'
			elif (year == 2019):
				if (season == 'spring'):
					self.teamName_dict['PRG'] = 'ProGaming Esports'
				elif (season == 'summer'):
					self.teamName_dict['PRG'] = 'Prodigy'
			else:
				self.teamName_dict['PRG'] = 'Prodigy'
				self.teamName_dict['UP'] = 'Uppercut'
		elif (league == 'BRCC'):
			if (year == 2017):
				self.teamName_dict['PRG'] = 'ProGaming Esports'
			elif (year == 2019):
				self.teamName_dict['PRG'] = 'ProGaming Esports'
		elif (league == 'LEC'):
			self.teamName_dict['MAD'] = 'MAD'
			self.teamName_dict['UOL'] = 'Unicorns Of Love'
		elif (league == 'PCS') | (league == 'LMS') | (league == 'ECS'):
			self.teamName_dict['MAD'] = 'MAD Team'
			self.teamName_dict['RSG'] = 'Resurgence'
			self.teamName_dict['AF'] = 'ahq Fighter'
			self.teamName_dict['MCX'] = 'Machi Esports'
			self.teamName_dict['PSG'] = 'Talon Esports'
			if (year == 2017) & (league == 'ECS'):
				self.teamName_dict['MAD'] = 'MAD Dragon'
			elif (year == 2019) & (league == 'ECS'):
				self.teamName_dict['MCX'] = 'MachiX'
		elif (league == 'LDL'):
			self.teamName_dict['SG'] = 'Scorpio Game'
			self.teamName_dict['UP'] = 'Unlimited Potential'
			self.teamName_dict['RYL'] = 'Royal Club'
			self.teamName_dict['MSC'] = 'Moss Seven Club'
			self.teamName_dict['VP'] = 'VP Game'
		elif (league == 'LJL'):
			self.teamName_dict['SG'] = 'Sengoku Gaming'
			self.teamName_dict['PGM'] = 'PENTAGRAM'
		elif (league == 'TCL'):
			self.teamName_dict['RYL'] = 'Royal Youth'
			self.teamName_dict['IW'] = 'Istanbul Wildcats'
		elif (league == 'OCS'):
			self.teamName_dict['ABY'] = 'Abyss Academy'
		elif (league == 'OPL'):
			self.teamName_dict['ABY'] = 'Abyss'
			self.teamName_dict['SIN'] = 'Sin Gaming'
		elif (league == 'Challengers Korea'):
			self.teamName_dict['RSG'] = 'Rising Star Gaming'
			self.teamName_dict['SPG'] = 'Awesome Spear'
		elif (league == 'EM'):
			self.teamName_dict['PSG'] = 'Paris Saint-Germain'
			self.teamName_dict['CG'] = 'Cyber Gaming'
			self.teamName_dict['SIN'] = 'SINNERS Esports'
			self.teamName_dict['TS'] = 'Turing eSports'
			self.teamName_dict['IW'] = 'Iron Wolves'
			self.teamName_dict['DBL'] = 'Diabolus Esports'
			
			if (year == 2018):
				self.teamName_dict['MAD'] = 'MAD Lions E.C.'
				self.teamName_dict['SPG'] = 'SPGeSports'
			elif (year == 2019):
				self.teamName_dict['MAD'] = 'MAD Lions E.C.'
		elif (league == 'LCL'):
			self.teamName_dict['VP'] = 'Virtus.pro'
			self.teamName_dict['UOL'] = 'UOL.CIS'
			self.teamName_dict['CC'] = 'CrowCrowd'
		elif (league == 'LPLOL'):
			self.teamName_dict['CC'] = 'Cidade Curiosa Esports'
		elif (league == 'CIS_CL'):
			self.teamName_dict['CC'] = 'CrowCrowd'
		elif (league == 'LCS'):
			self.teamName_dict['CG'] = 'Clutch Gaming'
		elif (league == 'LCS_a'):
			self.teamName_dict['TS'] = 'Tempo Storm'
		elif (league == 'VCS'):
			self.teamName_dict['DBL'] = 'Saigon Buffalo'
			self.teamName_dict['TS'] = 'Team Secret'

		else:
			self.teamName_dict['MSC'] = 'Mid Season Cup'
		return

