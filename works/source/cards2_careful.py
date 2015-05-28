# encoding: utf-8
import sys
sys.path.insert(0, '../libs/deuces/')

from deuces import Card
from deuces import Evaluator
from deuces import Deck

#oppobehaveblind[num_player][cardround]
#oppobehaveflop[num_player][cardrpund]
#oppobehaveturn[num_player][cardround]
#oppobehaveriver[num_player][cardround]
#oppobehavenumblind[num_player][cardround]
#oppobehavenumflop[num_player][cardround]
#oppobehavenumturn[num_player][cardround]
#oppobehavenumriver[num_player][cardround]


def  getOppoStyle(oppobehave,oppobehavenum,num_player):
	oppostyle=[None]*num_player
	num_call=[None]*num_player
	num_raise=[None]*num_player
	num_all_in=[None]*num_player
	num_sum=[None]*num_player

	for i in range(num_player):
		num_call[i] = oppobehave[i].count('call')
		num_raise[i] = oppobehave[i].count('raise')
		num_all_in[i] = oppobehave[i].count('all_in')
		num_sum[i] = sum(oppobehavenum[i])
		if (num_raise[i]>=1  or num_all_in[i]>=1)and (num_sum[i]/(num_raise[i]+num_all_in[i]+num_call[i]))>=300.0:
			oppostyle[i] = 'aggresive'
		elif(num_raise[i]>=1  or num_all_in[i] >=1)and (num_sum[i]/(num_raise[i]+num_all_in[i]+num_call[i]))>=0.0:
			oppostyle[i] = 'attack'
		elif num_raise[i]==0 and num_call[i]>=3:
			oppostyle[i] = 'robust'
		elif num_raise[i]==0 and num_call[i]>=1:
			oppostyle[i] = 'normal'
		else:
			oppostyle[i] = 'weak'
	return oppostyle



def getCardPercentageRank(card,percentage):
	try:
		index1=percentage.index(max(percentage))
		temp_percentage2=percentage
		temp_percentage2.remove(max(percentage))
		index2=percentage.index(max(temp_percentage2))


	except:
		"value is not in the list"
	return index1,index2

def makeDecisionBlind(card,cardround,oppobehaveblind,oppobehavenumblind,num_player):
	if cardround<=2:
		if card[0][0] in ['A','K','Q','J','T']  and card[1][0] in ['A','K','Q','J','T']  and card[0][0]==card[1][0]:#big pair
			return 'call'
		elif card[0][0]in ['A','K','Q','J'] and card[1][0]in ['A','K','Q','J'] and card[0][1]==card[1][1]:#big flush
			return 'call'
		elif (card[0][0] in ['A','K']  or card[1][0] in ['A','K'] ) and card[0][1]==card[1][1]:#mid flush
			return 'call'
		elif card[0][0]==card[1][0] and card[0][0] in ['9','8','7','6','5','4','3','2']: #small pair
			return  'call'
		elif card[0][1]==card[1][1] and card[0][0] in['T','9','8','7','6','5','4','3','2'] or card[1][0] in['T','9','8','7','6','5','4','3','2'] :#small flush
			return  'call'
		elif (card[0][0]in ['A','K','Q','J'] or card[1][0]in ['A','K','Q','J'] )and card[0][1]!=card[1][1] and card[0][0]!=card[1][0]:
			return 'call'
		elif card[0][0]in ['T','9','8','7','6','5','4','3','2'] and card[1][0]in  ['T','9','8','7','6','5','4','3','2'] and card[0][0]!=card[1][0] and card[0][1]==card[1][1]:
			return 'call'	
		elif card[0][0]in ['A','K','Q','J','T'] and card[1][0]in   ['A','K','Q','J','T'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in ['K','Q','J','T','9'] and card[1][0]in   ['K','Q','J','T','9'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in ['Q','J','T','9','8'] and card[1][0]in   ['Q','J','T','9','8'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in ['J','T','9','8','7'] and card[1][0]in   ['J','T','9','8','7'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in ['T','9','8','7','6'] and card[1][0]in   ['T','9','8','7','6']and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in ['9','8','7','6','5'] and card[1][0]in  ['9','8','7','6','5'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in['8','7','6','5','4']and card[1][0]in   ['8','7','6','5','4']  and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in ['7','6','5','4','3'] and card[1][0]in  ['7','6','5','4','3'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in ['6','5','4','3','2'] and card[1][0]in    ['6','5','4','3','2'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		elif card[0][0]in ['5','4','3','2','A'] and card[1][0]in    ['5','4','3','2','A'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
			return 'check'
		else:
			return 'fold' 
	elif cardround==3:
		oppostyleblind = getOppoStyle(oppobehaveblind,oppobehavenumblind,num_player)
		if oppostyleblind.count('aggresive')>=1 or oppostyleblind.count('attack')>=2:
			if card[0][0] in ['A','K','Q','J','T']  and card[1][0] in ['A','K','Q','J','T']  and card[0][0]==card[1][0]:#big pair
				return 'call'
			elif (card[0][0] in ['A','K','Q','J']  or card[1][0] in ['A','K','Q','J'] ) and card[0][1]==card[1][1]:#mid flush
				return 'call'
			elif card[0][0]==card[1][0] and card[0][0] in ['9','8','7','6','5','4','3','2']: #small pair
				return  'check'
			elif card[0][1]==card[1][1] and card[0][0] in['9','8','7','6','5','4','3','2'] or card[1][0] in['9','8','7','6','5','4','3','2'] :#small flush
				return  'check'
			elif card[0][0]in ['A','K','Q','J'] and card[1][0]in ['A','K','Q','J'] and card[0][1]==card[1][1]:#big flush
				return 'call'
			elif (card[0][0]in ['A','K','Q','J'] or card[1][0]in ['A','K','Q','J'] )and card[0][1]!=card[1][1] and card[0][0]!=card[1][0]:
				return 'call'
			elif card[0][0]in ['T','9','8','7','6','5','4','3','2'] and card[1][0]in  ['T','9','8','7','6','5','4','3','2'] and card[0][0]!=card[1][0] and card[0][1]==card[1][1]:
				return 'check'	
			elif card[0][0]in ['A','K','Q','J','T'] and card[1][0]in   ['A','K','Q','J','T'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['K','Q','J','T','9'] and card[1][0]in   ['K','Q','J','T','9'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['Q','J','T','9','8'] and card[1][0]in   ['Q','J','T','9','8'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['J','T','9','8','7'] and card[1][0]in   ['J','T','9','8','7'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['T','9','8','7','6'] and card[1][0]in   ['T','9','8','7','6']and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['9','8','7','6','5'] and card[1][0]in  ['9','8','7','6','5'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in['8','7','6','5','4']and card[1][0]in   ['8','7','6','5','4']  and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['7','6','5','4','3'] and card[1][0]in  ['7','6','5','4','3'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['6','5','4','3','2'] and card[1][0]in    ['6','5','4','3','2'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'fold'
			elif card[0][0]in ['5','4','3','2','A'] and card[1][0]in    ['5','4','3','2','A'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'fold'
			else:
				return 'fold' 
		elif oppostyleblind.count('attack')>=1:
			if card[0][0] in ['A','K','Q','J','T']  and card[1][0] in ['A','K','Q','J','T']  and card[0][0]==card[1][0]:#big pair
				return 'raise 100'
			elif (card[0][0] in ['A','K','Q','J']  or card[1][0] in ['A','K','Q','J'] ) and card[0][1]==card[1][1]:#mid flush
				return 'call'
			elif card[0][0]==card[1][0] and card[0][0] in ['9','8','7','6','5','4','3','2']: #small pair
				return  'call'
			elif card[0][1]==card[1][1] and card[0][0] in['9','8','7','6','5','4','3','2'] or card[1][0] in['9','8','7','6','5','4','3','2'] :#small flush
				return  'call'
			elif card[0][0]in ['A','K','Q','J'] and card[1][0]in ['A','K','Q','J'] and card[0][1]==card[1][1]:#big flush
				return 'raise 100'
			elif (card[0][0]in ['A','K','Q','J'] or card[1][0]in ['A','K','Q','J'] )and card[0][1]!=card[1][1] and card[0][0]!=card[1][0]:
				return 'call'
			elif card[0][0]in ['T','9','8','7','6','5','4','3','2'] and card[1][0]in  ['T','9','8','7','6','5','4','3','2'] and card[0][0]!=card[1][0] and card[0][1]==card[1][1]:
				return 'call'	
			elif card[0][0]in ['A','K','Q','J','T'] and card[1][0]in   ['A','K','Q','J','T'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['K','Q','J','T','9'] and card[1][0]in   ['K','Q','J','T','9'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['Q','J','T','9','8'] and card[1][0]in   ['Q','J','T','9','8'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['J','T','9','8','7'] and card[1][0]in   ['J','T','9','8','7'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['T','9','8','7','6'] and card[1][0]in   ['T','9','8','7','6']and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['9','8','7','6','5'] and card[1][0]in  ['9','8','7','6','5'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in['8','7','6','5','4']and card[1][0]in   ['8','7','6','5','4']  and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['7','6','5','4','3'] and card[1][0]in  ['7','6','5','4','3'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['6','5','4','3','2'] and card[1][0]in    ['6','5','4','3','2'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			elif card[0][0]in ['5','4','3','2','A'] and card[1][0]in    ['5','4','3','2','A'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'check'
			else:
				return 'fold' 
		else:
			if card[0][0] in ['A','K','Q','J','T']  and card[1][0] in ['A','K','Q','J','T']  and card[0][0]==card[1][0]:#big pair
				return 'raise 200'
			elif (card[0][0] in ['A','K','Q','J']  or card[1][0] in ['A','K','Q','J'] ) and card[0][1]==card[1][1]:#mid flush
				return 'raise 100'
			elif card[0][0]==card[1][0] and card[0][0] in ['9','8','7','6','5','4','3','2']: #small pair
				return  'call'
			elif card[0][1]==card[1][1] and card[0][0] in['9','8','7','6','5','4','3','2'] or card[1][0] in['9','8','7','6','5','4','3','2'] :#small flush
				return  'call'
			elif card[0][0]in ['A','K','Q','J'] and card[1][0]in ['A','K','Q','J'] and card[0][1]==card[1][1]:#big flush
				return 'raise 200'
			elif (card[0][0]in ['A','K','Q','J'] or card[1][0]in ['A','K','Q','J'] )and card[0][1]!=card[1][1] and card[0][0]!=card[1][0]:
				return 'call'
			elif card[0][0]in ['T','9','8','7','6','5','4','3','2'] and card[1][0]in  ['T','9','8','7','6','5','4','3','2'] and card[0][0]!=card[1][0] and card[0][1]==card[1][1]:
				return 'call'	
			elif card[0][0]in ['A','K','Q','J','T'] and card[1][0]in   ['A','K','Q','J','T'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['K','Q','J','T','9'] and card[1][0]in   ['K','Q','J','T','9'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['Q','J','T','9','8'] and card[1][0]in   ['Q','J','T','9','8'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['J','T','9','8','7'] and card[1][0]in   ['J','T','9','8','7'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['T','9','8','7','6'] and card[1][0]in   ['T','9','8','7','6']and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['9','8','7','6','5'] and card[1][0]in  ['9','8','7','6','5'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in['8','7','6','5','4']and card[1][0]in   ['8','7','6','5','4']  and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['7','6','5','4','3'] and card[1][0]in  ['7','6','5','4','3'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['6','5','4','3','2'] and card[1][0]in    ['6','5','4','3','2'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			elif card[0][0]in ['5','4','3','2','A'] and card[1][0]in    ['5','4','3','2','A'] and card[0][0]!=card[1][0] and card[0][1]!=card[1][1]:
				return 'call'
			else:
				return 'fold' 
	else:
		return 'call'

def makeDecisionFlop(card,cardround,percentage,oppobehaveflop,oppobehavenumflop,num_player,rank2):
	(index1,index2)= getCardPercentageRank(card,percentage)
	del_index = index2-index1
	if cardround==1:
			if rank2<=322 :
				return 'raise 100'
			elif rank2<=1599 and rank2>322:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'check'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'check'		
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'check'			
			else:
				return 'fold'
	elif cardround==2:
			if rank2<=322 :
				return 'raise 100'
			elif rank2<=1599 and rank2>322:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'fold'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'check'
			else:
				return 'fold'
	elif cardround<=5:
		oppostyleflop = getOppoStyle(oppobehaveflop,oppobehavenumflop,num_player)
		if oppostyleflop.count('aggresive')>=1:
			if rank2<=322 :
				return 'raise 200'
			elif rank2<=1599 and rank2>322:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'check'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'check'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'check'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'fold'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'call'
			else:
				return 'fold'
		elif oppostyleflop.count('aggresive')==0 and  oppostyleflop.count('attack')>=1:
			if rank2<=322 :
				return 'raise 300'
			elif rank2<=1599 and rank2>322:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'check'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'check'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'check'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'fold'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'call'
			else:
				return 'fold'
		elif oppostyleflop.count('aggresive')==0 and oppostyleflop.count('attack')==0 and  oppostyleflop.count('robust')>=1:
			if rank2<=322 :
				return 'raise 300'
			elif rank2<=1599 and rank2>322:
				return 'raise 200'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'check'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'call'
			else:
				return 'fold'
		else:
			if rank2<=322 :
				return 'raise 200'
			elif rank2<=1599 and rank2>322:
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'raise 100'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'raise 100'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'raise 100'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'check'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'call'
			else:
				return 'fold'

	elif cardround>5:
		oppostyleflop = getOppoStyle(oppobehaveflop,oppobehavenumflop,num_player)
		if oppostyleflop.count('aggresive')>=1:
			if rank2<=322 :
				return 'raise 100'
			elif rank2<=1599 and rank2>322:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'check'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'check'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'fold'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'check'
			else:
				return 'fold'
		elif oppostyleflop.count('aggresive')==0 and oppostyleflop.count('attack')>=1:
			if rank2<=322 :
				return 'raise 100'
			elif rank2<=1599 and rank2>322:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'check'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'check'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'check'
			else:
				return 'fold'
		elif oppostyleflop.count('aggresive')==0 and oppostyleflop.count('attack')==0 and  oppostyleflop.count('robust')>=1:
			if rank2<=322 :
				return 'raise 200'
			elif rank2<=1599 and rank2>322:
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'check'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'check'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'call'
			else:
				return 'fold'
		else:
			if rank2<=322 :
				return 'raise 200'
			elif rank2<=1599 and rank2>322:
				return 'raise 100'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
				return 'call'
			elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=4 and percentage[index1]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
				return 'call'	
			elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
				return 'call'
			elif rank2<6185 and rank2>=2467 and del_index<=0:
				return 'check'
			elif rank2>=6185 and index1>=4 and percentage[index1]>0.3:
				return 'check'
			else:
				return 'fold'

def makeDecisionRiver(card,cardround,oppobehaveriver,oppobehavenumriver,num_player,rank3,rank4,rankboard):

		if cardround==1:
			if rank4<rank3 and rank4<rankboard:	
				if rank4<=166:
					return 'all_in'
				elif rank4<=322 and rank4>166:
					return 'raise 500'
				elif rank4<=1599 and rank4>322:
					return 'raise 200'
				elif rank4<=2467 and rank4>1599:
					return 'raise 100'
				elif rank4<6185 and rank4>=2467:
					return 'call'
				else:
					return 'fold'
			elif rank4==rank3 and rank4<rankboard:
				if rank4<=166:
					return 'raise 500'
				elif rank4<=322 and rank4>166:
					return 'raise 200'
				elif rank4<=1599 and rank4>322:
					return 'raise 100'
				elif rank4<=2467 and rank4>1599:
					return 'call'
				elif rank4<6185 and rank4>=2467:
					return 'check'
				else:
					return 'fold'
			else:
				return 'fold'
		elif cardround<=3:
			if rank4<rank3 and rank4<rankboard:	
				if rank4 <=322:
					return 'raise 100'
				elif rank4<=1609:
					return 'call'
				elif rank4 <=3325:
					return 'check'
				else:
					return 'fold'
			elif rank4==rank3 and rank4<rankboard:
				if rank4 <=322:
					return 'raise 100'
				elif rank4<=1609:
					return 'call'
				elif rank4<=2467:
					return 'check'
				else:
					return 'fold'
			else:
				return 'fold'
		elif cardround<=8:
			oppostyleriver=getOppoStyle(oppobehaveriver,oppobehavenumriver,num_player)
			if oppostyleriver.count('aggresive')>=1:
				if rank4<rank3 and rank4<rankboard:	
					if rank4<=322:
						return 'call'
					elif rank4 <=1609:
						return 'check'
					else:
						return 'fold'
				elif rank4==rank3 and rank4<rankboard:
					if rank4<=322:
						return 'call'
					elif rank4<=1609:
						return 'check'
					else:
						return 'fold'
				else:
					return 'fold'
			elif oppostyleriver.count('attack')>=1:
				if rank4<rank3 and rank4<rankboard:	
					if rank4<=322:
						return 'call'
					elif rank4 <=1609:
						return 'check'
					else:
						return 'fold'
				elif rank4==rank3 and rank4<rankboard:
					if rank4<=166:
						return 'call'
					elif rank4<=1609:
						return 'check'
					else:
						return 'fold'
				else:
					return 'fold'
			elif oppostyleriver.count('robust')>=1:
				if rank4<rank3 and rank4<rankboard:	
					if rank4<=322:
						return 'raise 200'
					elif rank4 <=1609:
						return 'call'
					elif rank4 <=2467:
						return 'check'
					else:
						return 'fold'
				elif rank4==rank3 and rank4<rankboard:
					if rank4<=322:
						return 'call'
					elif rank4<=2467:
						return 'check'
					elif rank4 <=3325:
						return 'check'
					else:
						return 'fold'
				else:
					return 'fold'
			else:
				if rank4<rank3 and rank4<rankboard:	
					if rank4<=322:
						return 'raise 200'
					elif rank4 <=2467:
						return 'raise 100'
					elif rank4 <=3325:
						return 'call'
					else:
						return 'fold'
				elif rank4==rank3 and rank4<rankboard:
					if rank4<=322:
						return 'raise 100'
					elif rank4<=2467:
						return 'call'
					elif rank4 <=3325:
						return 'check'
					else:
						return 'fold'
				else :
					return 'fold'
		elif cardround<=20:
			if rank4<=166:
				return 'call'
			elif rank4 <=322:
				return 'check'
			else:
				return 'fold'
		else:
			if rank4<=166:
				return 'call'
			else:
				return 'fold'

def makeDecisionTurn(card,cardround,percentage,oppobehaveturn,oppobehavenumturn,num_player,rank2,rank3):
		rank2 = getRank2(card)
		rank3 = getRank3(card)
		(index1,index2)= getCardPercentageRank(card,percentage)
		del_index = index2-index1
		if cardround==1:
			if rank3<rank2:
				if rank2<=322 :
					return 'raise 200'
				elif rank2<=1599 and rank2>322:
					return 'raise 100'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
					return 'raise 100'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
					return 'raise 100'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
					return 'raise 100'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
					return 'raise 100'
				elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
					return 'call'
				elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=5 and percentage[index1]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=5 and percentage[index1]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and del_index<=0:
					return 'check'
				elif rank2>=6185 and index1>=5 and percentage[index1]>0.18:
					return 'check'
				else:
					return 'fold'
			else:
				if rank2<=322 :
					return 'raise 200'
				elif rank2<=1599 and rank2>322:
					return 'raise 100'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
					return 'raise 100'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
					return 'raise 100'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
					return 'raise 100'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]>0.3:
					return 'call'
				elif rank2<6185 and rank2>=2467 and del_index>0 and percentage[index2]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=5 and percentage[index1]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=5 and percentage[index1]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and del_index<=0 and index1>=3 and percentage[index1]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and del_index<=0:
					return 'check'
				elif rank2>=6185 and index1>=5 and percentage[index1]>0.18:
					return 'check'
				else:
					return 'fold'
		elif cardround>1 and rank3<=166:
			return 'call'
		elif cardround>1 and rank3>166:
			oppostyleturn=getOppoStyle(oppobehaveturn,oppobehavenumturn,num_player)
			if oppostyleturn.count('aggresive')>=1:
				if rank2<=322 :
					return 'call'
				elif rank2<=1599 and rank2>322:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
					return 'call'
				elif rank2<6185 and rank2>=2467 and index1>=5 and percentage[index1]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and index1>=5 and percentage[index1]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and index1>=3 and del_index>0 and percentage[index2]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and index1>=3 and del_index>0 and percentage[index2]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 :
					return 'check'
				else:
					return 'fold'
			elif oppostyleturn.count('attack')>=2:
				if rank2<=322 :
					return 'call'
				elif rank2<=1599 and rank2>322:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
					return 'call'
				elif rank2<6185 and rank2>=2467 and index1>=5 and percentage[index1]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and index1>=5 and percentage[index1]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and index1>=3 and del_index>0 and percentage[index2]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and index1>=3 and del_index>0 and percentage[index2]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 :
					return 'check'
				else:
					return 'fold'
			elif oppostyleturn.count('robust')>=3:
				if rank2<=322 :
					return 'call'
				elif rank2<=1599 and rank2>322:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
					return 'call'
				elif rank2<6185 and rank2>=2467 and index1>=5 and percentage[index1]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and index1>=5 and percentage[index1]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 and index1>=3 and del_index>0 and percentage[index2]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and index1>=3 and del_index>0 and percentage[index2]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 :
					return 'check'
				else:
					return 'fold'		
			else:
				if rank2<=322 :
					return 'call'
				elif rank2<=1599 and rank2>322:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]>=0.3:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index>0 and percentage[index2]<0.3:
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]>0.3 :
					return 'call'
				elif rank2<=2467 and rank2>1599 and del_index<=0 and percentage[index1]<=0.3:
					return 'call'
				elif rank2<6185 and rank2>=2467 and index1>=5 and percentage[index1]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and index1>=5 and percentage[index1]<=0.3:
					return 'call'
				elif rank2<6185 and rank2>=2467 and index1>=3 and del_index>0 and percentage[index2]>0.3:
					return 'call'	
				elif rank2<6185 and rank2>=2467 and index1>=3 and del_index>0 and percentage[index2]<=0.3:
					return 'check'
				elif rank2<6185 and rank2>=2467 :
					return 'check'
				else:
					return 'fold'		

def getRank2(card):
	hand=[Card.new(card[0]),Card.new(card[1])]
	evaluator=Evaluator()
	board=[Card.new(card[2]),Card.new(card[3]),Card.new(card[4])]
	rank2=evaluator.evaluate(board,hand)
	return rank2

def getRank3(card):
	hand=[Card.new(card[0]),Card.new(card[1])]
	evaluator=Evaluator()
	board=[Card.new(card[2]),Card.new(card[3]),Card.new(card[4]),Card.new(card[5])]
	rank3=evaluator.evaluate(board,hand)
	return rank3

def getRank4(card):
	hand=[Card.new(card[0]),Card.new(card[1])]
	evaluator=Evaluator()
	board=[Card.new(card[2]),Card.new(card[3]),Card.new(card[4]),Card.new(card[5]),Card.new(card[6])]
	rank4=evaluator.evaluate(board,hand)
	return rank4
def getRankBoard(card):
	board1=[Card.new(card[2]),Card.new(card[3])]
	evaluator=Evaluator()
	board2=[Card.new(card[4]),Card.new(card[5]),Card.new(card[6])]
	rankboard=evaluator.evaluate(board1,board2)
	return rankboard

