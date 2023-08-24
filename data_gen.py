odi_2022 = {}
odi_2022[2022] = ['/series/ireland-in-usa-and-west-indies-2021-22-1291182/west-indies-vs-ireland-1st-odi-1277085/full-scorecard']

data = []
spl_matches = []
# player_data_master = {}
summary_master ={}

espncricinfo = 'https://www.espncricinfo.com'

for year, match_links_list in all_odi_links.items():         
    print(year)
    for match_link in match_links_list:
        try:        
            scorecard_url = espncricinfo + match_link
            live_score_url = scorecard_url.replace('full-scorecard','live-cricket-score')
            url = live_score_url

            driver.get(url)    
            html = driver.page_source.encode('utf-8')
            page_num = 0
            content = driver.page_source
            page_soup = soup(driver.page_source, 'lxml')
            
            json_obj = {}
            stage_count = 1
            print(stage_count)
            stage_count += 1    

            # try:
            json_obj['year'] = year
            json_obj['match_id'] = scorecard_url.split('/')[-3].split('-')[-1]        
            json_obj['scorecard_link'] = scorecard_url
            json_obj['live_score_link'] = scorecard_url.replace('full-scorecard','live-cricket-score')
            json_obj['match_overs_link'] = scorecard_url.replace('full-scorecard','match-overs-comparison')
            json_obj['tournament_link'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[0]['href']
            json_obj['tournament_id'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[0]['href'].split('-')[-1]
            json_obj['tournament'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[0].text
            json_obj['team1'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[1].text
            json_obj['team1_id'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[1]['href'].split('-')[-1]
            json_obj['team2'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[2].text
            json_obj['team2_id'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[2]['href'].split('-')[-1]
            # json_obj['date'] = page_soup.findAll("span", {"class":"ds-text-tight-s ds-font-regular"})[4].text.split(' - ')[0]
            z = page_soup.findAll("div", {"class":"ds-text-tight-m ds-font-regular ds-text-typo-mid3"})
            json_obj['date'] = list(map(lambda x: x.text, z))
            # json_obj['day_or_night'] = page_soup.findAll("span", {"class":"ds-text-tight-s ds-font-regular"})[4].text.split(' - ')[1].split(' (')
            json_obj['venue_link'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[19]['href']
            json_obj['venue_id'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[19]['href'].split('-')[-1]
            json_obj['venue_name'] = page_soup.findAll("a", {"class":"ds-inline-flex ds-items-start ds-leading-none"})[19].text
            print(json_obj['match_id'] + '-' + json_obj['team1'] + ' vs ' + json_obj['team2'])
            # except Exception as e:
            #     print(e)
            #     pass
            
            # try:
            url = scorecard_url        
            driver.get(url)    
            html = driver.page_source.encode('utf-8')
            page_num = 0
            content = driver.page_source
            page_soup = soup(driver.page_source, 'lxml')
            
            json_obj['team1_overs'] = page_soup.findAll("span", {"class":"ds-font-regular ds-text-tight-s"})[0].text.split(" ")[0]
            json_obj['team2_overs'] = page_soup.findAll("span", {"class":"ds-font-regular ds-text-tight-s"})[2].text.split(" ")[0]
            #team_scores = page_soup.findAll("td", {"class":"ds-font-bold ds-bg-fill-content-alternate ds-text-tight-m ds-min-w-max ds-text-right ds-text-typo"})
            # team_scores = page_soup.findAll("span", {"class":"ds-font-regular ds-text-tight-s"})
            team_scores = page_soup.findAll("div", {"class":"ds-text-compact-m ds-text-typo ds-text-right ds-whitespace-nowrap"})
            json_obj['team1_runs'] = team_scores[0].text.split(" ")[-1].split('/')[0]
            json_obj['team1_wickets'] = (team_scores[0].text.split(" ")[-1].split('/')[1] if '/' in team_scores[0].text else 10)
            json_obj['team2_runs'] = team_scores[1].text.split(" ")[-1].split('/')[0]
            json_obj['team2_wickets'] = (team_scores[1].text.split(" ")[-1].split('/')[1] if '/' in team_scores[1].text else 10)
            print(stage_count) # 2
            stage_count += 1

            all_tables = page_soup.findAll("tbody")

            team1_batsmen = {}
            table_player_url = all_tables[0].findAll('a', attrs={'class': 'ds-inline-flex ds-items-start ds-leading-none'})
            table_player_url = list(map(lambda x: x['href'], table_player_url))
            ball_details = all_tables[0].findAll('td', attrs={'class': 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'})
            ball_details = list(map(lambda x: x.text, ball_details))
            runs_scored = all_tables[0].findAll('td', attrs={'class': 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-typo'})
            runs_scored = list(map(lambda x: x.text, runs_scored))
            for i in range(len(table_player_url)):
                id = table_player_url[i].split('-')[-1]
                team1_batsmen[id] = {'player_url': table_player_url[i], 'runs': runs_scored[i], 'balls': ball_details[5*i], \
                                    'minutes': ball_details[5*i+1], 'boundaries': int(ball_details[5*i+2]) + int(ball_details[5*i+3])}

            team2_batsmen = {}
            table_player_url = all_tables[2].findAll('a', attrs={'class': 'ds-inline-flex ds-items-start ds-leading-none'})
            table_player_url = list(map(lambda x: x['href'], table_player_url))
            ball_details = all_tables[2].findAll('td', attrs={'class': 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'})
            ball_details = list(map(lambda x: x.text, ball_details))
            runs_scored = all_tables[2].findAll('td', attrs={'class': 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-typo'})
            runs_scored = list(map(lambda x: x.text, runs_scored))
            for i in range(len(table_player_url)):
                id = table_player_url[i].split('-')[-1]
                team2_batsmen[id] = {'player_url': table_player_url[i], 'runs': runs_scored[i], 'balls': ball_details[5*i], \
                                    'minutes': ball_details[5*i+1], 'boundaries': int(ball_details[5*i+2]) + int(ball_details[5*i+3])}
            print(stage_count) # 3
            stage_count += 1

            team1_bowlers = {}
            table_player_url = all_tables[3].findAll('a', attrs={'class': 'ds-inline-flex ds-items-start ds-leading-none'})
            table_player_url = list(map(lambda x: x['href'], table_player_url))
            ball_details = all_tables[3].findAll('td', attrs={'class': 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'})
            ball_details = list(map(lambda x: x.text, ball_details))
            wickets_taken = all_tables[3].findAll('td', attrs={'class': 'ds-w-0 ds-whitespace-nowrap ds-text-right'})
            wickets_taken = list(map(lambda x: x.text, wickets_taken))
            for i in range(len(table_player_url)):
                id = table_player_url[i].split('-')[-1]
                team1_bowlers[id] = {'player_url': table_player_url[i], 'wickets': wickets_taken[i], 'overs': ball_details[9*i], \
                                    'runs_condeded': ball_details[9*i+2],'dots': ball_details[9*i+4], \
                                    'boundaries_conceded': int(ball_details[9*i+5]) + int(ball_details[9*i+6])}
                
            team2_bowlers = {}
            table_player_url = all_tables[1].findAll('a', attrs={'class': 'ds-inline-flex ds-items-start ds-leading-none'})
            table_player_url = list(map(lambda x: x['href'], table_player_url))
            ball_details = all_tables[1].findAll('td', attrs={'class': 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'})
            ball_details = list(map(lambda x: x.text, ball_details))
            wickets_taken = all_tables[1].findAll('td', attrs={'class': 'ds-w-0 ds-whitespace-nowrap ds-text-right'})
            wickets_taken = list(map(lambda x: x.text, wickets_taken))
            for i in range(len(table_player_url)):
                id = table_player_url[i].split('-')[-1]
                team2_bowlers[id] = {'player_url': table_player_url[i], 'wickets': wickets_taken[i], 'overs': ball_details[9*i], \
                                    'runs_condeded': ball_details[9*i+2],'dots': ball_details[9*i+4], \
                                    'boundaries_conceded': int(ball_details[9*i+5]) + int(ball_details[9*i+6])}
            print(stage_count) # 4
            stage_count += 1

            for table_data in [team1_batsmen, team2_batsmen, team1_bowlers, team2_bowlers]:
                for player_id, player in table_data.items():        
                        if player_id not in player_data_master.keys():
                            print('Record not available for ', player_id)
                            player_data_master[player_id] = {}
                            url = espncricinfo + player['player_url']
                            driver.get(url)    
                            html = driver.page_source.encode('utf-8')
                            page_num = 0
                            content = driver.page_source
                            page_soup = soup(driver.page_source, 'lxml')

                            player_detail_name = page_soup.findAll("p", {"class":"ds-text-tight-m ds-font-regular ds-uppercase ds-text-typo-mid3"})
                            player_detail_name = list(map(lambda x: x.text, player_detail_name))
                            player_detail_value = page_soup.findAll("span", {"class":"ds-text-title-s ds-font-bold ds-text-typo"})
                            player_detail_value = list(map(lambda x: x.text, player_detail_value))

                            for i in range(len(player_detail_name)):
                                player_data_master[player_id][player_detail_name[i]] = player_detail_value[i]
                                table_data[player_id][player_detail_name[i]] = player_detail_value[i]
                            print('Added record for '+ player_id + " " + player_data_master[player_id]['Full Name'])

                        else:
                            print('Record already available')
                            player_details = player_data_master[player_id]
                            player_detail_name = list(player_details.keys())
                            player_detail_value = list(player_details.values())

                            for i in range(len(player_detail_name)):
                                table_data[player_id][player_detail_name[i]] = player_detail_value[i]
                            print('Done for '+ player_id + " " + player_data_master[player_id]['Full Name'])

                if (count == 1):
                    team1_batsmen = table_data
                elif (count== 2):
                    team2_batsmen = table_data
                elif(count == 3):
                    team1_bowlers = table_data
                else:
                    team2_bowlers = table_data
                count += 1
            print(stage_count) # 5
            stage_count += 1
            
            # json_obj ={}
            match_player_data = {'team1_batsmen_': team1_batsmen, 'team2_batsmen_': team2_batsmen, 
                                'team1_bowlers_': team1_bowlers, 'team2_bowlers_': team2_bowlers}

            print(stage_count) # 6
            stage_count += 1

            for table_code, table_data in match_player_data.items():
                json_obj = initialize_json_values(table_code, json_obj)
                json_data = list(table_data.values())

                for player in json_data:
                    if('batsmen' in table_code):
                        if('runs' in player.keys()):
                            # Types of Batsmen
                            if('left' in player['Batting Style'].lower()):
                                print('left - ', player)
                                json_obj[table_code + 'left_handers'] += 1
                                json_obj[table_code + 'left_hander_runs_scored'] += int(player['runs'])
                                json_obj[table_code + 'left_hander_stamina'] += int(player['minutes'])
                                json_obj[table_code + 'left_hander_balls'] += int(player['balls'])
                                json_obj[table_code + 'left_hander_boundaries'] += int(player['boundaries'])                    
                            else:
                                print('right - ', player)
                                json_obj[table_code + 'right_handers'] += 1
                                json_obj[table_code + 'right_hander_runs_scored'] += int(player['runs'])
                                json_obj[table_code + 'right_hander_stamina'] += int(player['minutes'])
                                json_obj[table_code + 'right_hander_balls'] += int(player['balls'])
                                json_obj[table_code + 'right_hander_boundaries'] += int(player['boundaries'])   

                    if('bowler' in table_code):
                        if('wickets' in list(player.keys())):
                            # Types of Bowlers
                            if(('left' in player['Bowling Style'].lower()) and (('fast' in player['Bowling Style'].lower()) or ('medium' in player['Bowling Style'].lower()))):
                                print('leftquick - ', player)
                                json_obj[table_code + 'left_hand_quicks'] += 1
                                json_obj[table_code + 'left_hand_quick_overs'] += float(player['overs'])
                                json_obj[table_code + 'left_hand_quick_wickets'] += int(player['wickets'])
                                json_obj[table_code + 'left_hand_quick_dot_balls'] += int(player['dots'])
                                json_obj[table_code + 'left_hand_quick_runs_condeded'] += int(player['runs_condeded'])
                                json_obj[table_code + 'left_hand_quick_boundaries_condeded'] += int(player['boundaries_conceded'])                   
                            if(('right' in player['Bowling Style'].lower()) and (('fast' in player['Bowling Style'].lower()) or ('medium' in player['Bowling Style'].lower()))):
                                print('rightquick - ', player)
                                json_obj[table_code + 'right_hand_quicks'] += 1
                                json_obj[table_code + 'right_hand_quick_overs'] += float(player['overs'])
                                json_obj[table_code + 'right_hand_quick_wickets'] += int(player['wickets'])
                                json_obj[table_code + 'right_hand_quick_dot_balls'] += int(player['dots'])
                                json_obj[table_code + 'right_hand_quick_runs_condeded'] += int(player['runs_condeded'])
                                json_obj[table_code + 'right_hand_quick_boundaries_condeded'] += int(player['boundaries_conceded'])       
                            if(('spin' in player['Bowling Style'].lower()) or ('wrist' in player['Bowling Style'].lower()) or ('leg' in player['Bowling Style'].lower()) | \
                            ('orthodox' in player['Bowling Style'].lower()) or ('off' in player['Bowling Style'].lower()) or ('china' in player['Bowling Style'].lower())):
                                print('spin - ', player)
                                json_obj[table_code + 'spinners'] += 1
                                json_obj[table_code + 'spinner_overs'] += float(player['overs'])
                                json_obj[table_code + 'spinner_wickets'] += int(player['wickets'])
                                json_obj[table_code + 'spinner_dot_balls'] += int(player['dots'])
                                json_obj[table_code + 'spinner_runs_condeded'] += int(player['runs_condeded'])
                                json_obj[table_code + 'spinner_boundaries_condeded'] += int(player['boundaries_conceded'])

            z =  all_tables[0].findAll('a', attrs={'class': 'ds-inline-flex ds-items-start ds-leading-none'})
            json_obj['team1_player_ids'] = list(map(lambda x: x['href'].split('-')[-1], z))

            z =  all_tables[2].findAll('a', attrs={'class': 'ds-inline-flex ds-items-start ds-leading-none'})
            json_obj['team2_player_ids'] = list(map(lambda x: x['href'].split('-')[-1], z))

            print(stage_count) # 7
            stage_count += 1

            for team_code in ['team1_', 'team2_']:
                json_obj[team_code + 'batsmen_count'] = 0
                json_obj[team_code + 'bowler_count'] = 0
                json_obj[team_code + 'allrounder_count'] = 0

                for i in range(11):
                    team_player_data = player_data_master[json_obj[team_code + 'player_ids'][i]]

                    if('Bat' in team_player_data['Playing Role']):
                        json_obj[team_code + 'batsmen_count'] += 1
                    elif('Bowl' in team_player_data['Playing Role']):
                        json_obj[team_code + 'bowler_count'] += 1
                    else:
                        json_obj[team_code + 'allrounder_count'] += 1

            print(stage_count) # 8
            stage_count += 1

            # Getting Overwise data    

            url = json_obj['match_overs_link']
            id = json_obj['match_id']
            try:
                team1_overs = int(float(json_obj['team1_overs']))
            except:
                team1_overs = 0
            try:
                team2_overs = int(float(json_obj['team2_overs']))
            except: 
                team2_overs = 0
            print(team1_overs, team2_overs)
            driver.get(url)
            page_num = 0
            content = driver.page_source
            page_soup = soup(driver.page_source, 'lxml')

            over_details = page_soup.findAll("span", {"class": "ds-text-tight-s ds-font-regular ds-ml-1 ds-text-typo-mid3"})
            all_over_count = 1
            team1_ocount = 1
            team2_ocount = 1
            team1_runs = []
            team1_wickets = []
            team2_runs = []
            team2_wickets = []

            print(stage_count) # 9
            stage_count += 1

            over_details = page_soup.findAll("span", {"class": "ds-text-tight-s ds-font-regular ds-ml-1 ds-text-typo-mid2"})
            all_over_count = 1
            team1_ocount = 1
            team2_ocount = 1
            team1_runs = []
            team1_wickets = []
            team2_runs = []
            team2_wickets = []

            if(len(json_obj['team1_overs'].split('.'))==2):
                extra_one = 1
            else:
                extra_one = 0

            if(len(json_obj['team2_overs'].split('.'))==2):
                extra_two = 1
            else:
                extra_two = 0

            try:
                team1_overs = min(int(float(json_obj['team1_overs'])) + extra_one, 50)
            except:
                team1_overs = 0
            try:
                team2_overs = min(int(float(json_obj['team2_overs'])) + extra_two, 50)
            except: 
                team2_overs = 0

            driver.get(url)
            # print("Fetched Page", id)
            page_num = 0
            content = driver.page_source
            page_soup = soup(driver.page_source, 'lxml')
            print(len(over_details))
            team1_excess_flag = False
            team2_excess_flag = False

            for over in over_details:
                print('run ', str(all_over_count), '/', len(over_details))
                over_desc = over.text.replace("<!-- -->", "").replace("(", "").replace(")", "")
                if ((((all_over_count%2) == 0) or (team1_excess_flag)) and (team2_ocount <= team2_overs)):
                    team2_runs.append(over_desc.split(" ")[0])
                    team2_wickets.append(over_desc.split(" ")[2])
                    print('team2 ', team2_ocount)
                    team2_ocount += 1
                    # if(team2_ocount > team2_overs):
                    #     team2_excess_flag = False
                    
                elif (team1_ocount <= team1_overs):
                    team1_runs.append(over_desc.split(" ")[0])
                    team1_wickets.append(over_desc.split(" ")[2])
                    print('team1 ', team1_ocount)
                    team1_ocount += 1
                    if(team1_ocount > team1_overs):
                        team1_excess_flag = True            
                    
                all_over_count += 1

            # team1_runs = [eval(i) for i in team1_runs]
            # team2_runs = [eval(i) for i in team2_runs]
            # team1_wickets = [eval(i) for i in team1_wickets]
            # team2_wickets = [eval(i) for i in team2_wickets]

            print('Actual Overs', json_obj['team1_overs'], json_obj['team2_overs'])
            print('team1_overs',team1_overs, 'team2_overs', team2_overs)
            print('team1_runs',team1_runs)
            print('team2_runs',team2_runs)
            print('team1_wickets',team1_wickets)
            print('team2_wickets',team2_wickets)
            team1_pp_runs_scored = team1_middle_runs_scored = team1_death_runs_scored = 0
            team1_pp_wickets_lost = team1_middle_wickets_lost = team1_death_wickets_lost = 0

            team2_pp_runs_scored = team2_middle_runs_scored = team2_death_runs_scored = 0
            team2_pp_wickets_lost = team2_middle_wickets_lost = team2_death_wickets_lost = 0

            team1_ocount = 1
            team2_ocount = 1

            for i in range(50):
                if i<15:
                    if (team1_ocount <= team1_overs):
                        team1_pp_runs_scored += int(team1_runs[i])
                        team1_pp_wickets_lost += int(team1_wickets[i])
                        team1_ocount += 1
                    if (team2_ocount <= team2_overs):
                        team2_pp_runs_scored += int(team2_runs[i])
                        team2_pp_wickets_lost += int(team2_wickets[i])
                        team2_ocount += 1
                elif (15<=i<=35):
                    if (team1_ocount <= team1_overs):
                        team1_middle_runs_scored += int(team1_runs[i])
                        team1_middle_wickets_lost += int(team1_wickets[i])
                        team1_ocount += 1
                    if (team2_ocount <= team2_overs):
                        team2_middle_runs_scored += int(team2_runs[i])
                        team2_middle_wickets_lost += int(team2_wickets[i])
                        team2_ocount += 1
                elif i>35:
                    if (team1_ocount <= team1_overs):
                        team1_death_runs_scored += int(team1_runs[i])
                        team1_death_wickets_lost += int(team1_wickets[i])
                        team1_ocount += 1
                    if (team2_ocount <= team2_overs):
                        team2_death_runs_scored += int(team2_runs[i])
                        team2_death_wickets_lost += int(team2_wickets[i])
                        team2_ocount += 1

            json_obj['team1_pp_runs_scored'] = team1_pp_runs_scored 
            json_obj['team1_middle_runs_scored'] = team1_middle_runs_scored
            json_obj['team1_death_runs_scored'] = team1_death_runs_scored

            if(team1_overs>0):
                json_obj['team1_pp_run_rate'] = team1_pp_runs_scored/min(team1_overs, 15)
            else:
                json_obj['team1_pp_run_rate']
            if(team1_overs>15):
                json_obj['team1_middle_run_rate'] = team1_middle_runs_scored/min(team1_overs-15, 20)
            else:
                json_obj['team1_middle_run_rate'] = 0
            if(team2_overs>35):
                json_obj['team1_death_run_rate'] = team1_death_runs_scored/min(team1_overs-35, 15)
            else:
                json_obj['team1_death_run_rate'] = 0

            json_obj['team1_pp_wickets_lost'] = team1_pp_wickets_lost
            json_obj['team1_middle_wickets_lost'] = team1_middle_wickets_lost
            json_obj['team1_death_wickets_lost'] = team1_death_wickets_lost

            json_obj['team2_pp_runs_scored'] = team2_pp_runs_scored
            json_obj['team2_middle_runs_scored'] = team2_middle_runs_scored
            json_obj['team2_death_runs_scored'] = team2_death_runs_scored

            if(team2_overs>0):
                json_obj['team2_pp_run_rate'] = team2_pp_runs_scored/min(team2_overs, 15)
            else:
                json_obj['team2_pp_run_rate']
            if(team2_overs>15):
                json_obj['team2_middle_run_rate'] = team2_middle_runs_scored/min(team2_overs-15, 15)
            else:
                json_obj['team2_middle_run_rate'] = 0
            if(team2_overs>35):
                json_obj['team2_death_run_rate'] = team2_death_runs_scored/min(team2_overs-35, 15)
            else:
                json_obj['team2_death_run_rate'] = 0

            json_obj['team2_pp_wickets_lost'] = team2_pp_wickets_lost
            json_obj['team2_middle_wickets_lost'] = team2_middle_wickets_lost
            json_obj['team2_death_wickets_lost'] = team2_death_wickets_lost

            print(stage_count) # 10
            stage_count += 1

            data.append(json_obj)
            print("Match", len(data), "Over-wise done")
            print(json_obj)
    
        except Exception as e:
            spl_match = {}
            spl_match['id'] = id
            spl_match['url'] = url
            spl_match['stage'] = stage_count
            spl_match['error'] = e
            spl_matches.append(spl_match)
            print('--ERROR--')
            print(spl_match)
            pass
        
    match_pd = pd.DataFrame.from_dict(data)
    summary_master[year] = match_pd
    match_pd.to_csv(str(year) + '.csv', index=False)