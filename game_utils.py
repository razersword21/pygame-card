import json
def write_game_records(rank_list,main_role,rounds):
    if not any(player['name'] == main_role.name for player in rank_list):
        rank_list.append({"name":main_role.name,"score":str(rounds)})
    else:
        for player in rank_list:
            if player['name'] == main_role.name and int(player['score']) < rounds:
                player['score'] = str(rounds)
    rank_list = sorted(rank_list, key=lambda k: k['score'], reverse=True)
    if len(rank_list) > 9:
        rank_list.pop(-1)
    with open('draw_source/rankings.json','w') as f:
        json.dump(rank_list, f)