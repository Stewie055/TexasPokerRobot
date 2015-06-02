# encoding: utf-8
import sys
sys.path.insert(0, '../libs/deuces/')

from deuces import Card
from deuces import Evaluator
from deuces import Deck
import cards2_normal as cn
import time
import cards2_careful as cc
import cards2_strong as cs

#playermovement[num_player][num_fold,num_check,num_call,num_raise,num_all_in]
#playerrank[num_player][rank1...rankn]
#card_player[num_player][7]
rank2 = None
rank3 = None
rank4 = None 
def main():

	num_player=3
	card=['Ks','Qd','Jh','Ts','9d','7s','2d']
	card_player=[[['As','Ad']for i in range(50)],[['8h','Th']for i in range(50)],[['2s','2d']for i in range(50)]]
	board_player=[['5d','8c','Ac','Jc','4d']for i in range(50)]
	playermovement=[[30,0,30,10,0],[0,0,30,70,0],[20,20,20,20,20]]
	percentage=[0,0.2,0.15,0.4,0,0.2,0,0.05,0,0]
		#playerrank=[[3731,3731,3731],[2487,2487,2487],[4974,4974,4974]]
	cardround=1
	oppobehave=[['call','check','call','call','raise','call'],['call','check','call','call','raise','call'],['call','check','call','call','raise','call']]
	oppobehavenum=[[100,0,200,200,300,300],[100,0,200,200,300,300],[100,0,200,200,300,300]]
	playerrank=[[3325 for i in range(50)],[4700 for i in range(50)],[2467 for i in range(50)]]
	my_money=[2000,8000]
	all_money=[14000,56000]
	my_bet_history=[100,100,0]


	t1=time.clock()

	rank_temp=cn.getRank4(card)
	t2=time.clock()
	'''
	for i in range(num_player):
		for x in range(len(board_player)):
			cardx=[card_player[i][x][0],card_player[i][x][1],board_player[x][0],board_player[x][1],board_player[x][2],board_player[x][3],board_player[x][4]]
			t1=time.clock()

			rank_temp=cn.getRank4(cardx)
			t2=time.clock()

			playerrank[i].append(rank_temp) 
	 '''
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	#print "playerrank is : %s"%playerrank
	#print "threat is : %s"%threat
	t3=time.clock()
'''
	decision1=makeDecisionBlindFinal(card,cardround,oppobehave,oppobehavenum,num_player,playermovement,card_player,playerrank)
	t4=time.clock()

	decision2=makeDecisionFlopFinal(card,cardround,percentage,oppobehave,oppobehavenum,num_player,playermovement,playerrank)
	t5=time.clock()

	decision3=makeDecisionTurnFinal(card,cardround,percentage,oppobehave,oppobehavenum,num_player,playermovement,playerrank)
	t6=time.clock()

	decision4=makeDecisionRiverFinal(card,cardround,oppobehave,oppobehavenum,num_player,playermovement,playerrank)
	t7=time.clock()
	print "getRank runtime: ",t2-t1
	print "getPlayerThreat runtime:	", t3-t2
	print "makeDecisionBlind runtime: ",t4-t3
	print "makeDecisionFlop runtime: ", t5-t4
	print "makeDecisionTurn runtime: ",t6-t5
	print "makeDecisionRiver runtime: ", t7-t6
	print "total runtime: ", t7-t1
'''
'''
def getRank(num_player,card_player,board_player,t):
	hand=[]*2
	board=[]*5
	for i in range(num_player):
		try:
			hand=[Card.new(card_player[i][t][0]),Card.new(card_player[i][t][1])]
		except:
			continue
		evaluator=Evaluator()
		board=[Card.new(board_player[t][0]),Card.new(board_player[t][1]),Card.new(board_player[t][2]),Card.new(board_player[t][3]),Card.new(board_player[t][4])]
		rank=evaluator.evaluate(board,hand)
			#print hand,rank,playerrank[i]
	#print playerrank
	return rank
'''

	#my_money[2000,8000]
	#all_money[14000,56000]
	#blind_flag----判断是否为盲注s
def calc_money(my_money,all_money):

	div_money=float(my_money[0])/sum(all_money)
	return div_money
#根据对手历史各轮的下注风格，推算对手的牌风，即下注威胁值
def getPlayerThreat(num_player,playermovement,playerrank):
	threat=[None]*num_player
	for i in range(num_player):
		if sum(playermovement[i])==0:
			threat[i]=1
		elif len(playerrank[i])==0:
			threat[i]=2
		else:
			ave_move = float(playermovement[i][0]+2*playermovement[i][1]+3*playermovement[i][2]+4*playermovement[i][3]+5*playermovement[i][4])\
				/(playermovement[i][0]+playermovement[i][1]+playermovement[i][2]+playermovement[i][3]+playermovement[i][4])
			a=7461*len(playerrank[i])-sum(playerrank[i])
			b=len(playerrank[i])
			print "a,b is : %s"% a,b,ave_move
			ave_rank = float(a)/b
			temp=float(ave_rank/ave_move)
			if  temp<750:
				threat[i]=1
			elif temp >1850:
				threat[i]=3
			else :
				threat[i]=2
		#print "ave_rank/ sum_move is :%s"%temp
	print "threat is %s"%threat

	return threat

#盲注阶段最终决策函数
def makeDecisionBlindFinal(card,cardround,oppobehave,oppobehavenum,num_player,playermovement,card_player,playerrank,my_money,all_money,blind_flag):
	div_money=calc_money(my_money,all_money)
	print my_money,all_money,div_money
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	print "oppobehavenumblind=%s"%oppobehavenum	

	if div_money<0.01:
		low_b1=cc.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player,blind_flag)
		print 'ow_b1=%s'%low_b1
		return low_b1
	elif div_money>0.7:
		high_b1=cc.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player,blind_flag)
		print 'high_b1=%s'%high_b1
		return high_b1
	else:
		if max(threat)==3:
			b1=cc.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player,blind_flag)
			print "b1=%s"%b1
			return b1
		elif max(threat)==2:
			b2=cn.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player,blind_flag)
			print "b2=%s"%b2
			return b2
		else:
			b3=cs.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player,blind_flag)
			print "b3=%s"%b3
			return b3


#公共牌阶段最终决策函数


def makeDecisionFlopFinal(card,cardround,percentage,oppobehave,oppobehavenum,num_player,playermovement,playerrank,my_money,all_money,my_bet_history):
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	global rank2 
	rank2 = getRank2(card)
	print rank2	
	div_money=calc_money(my_money,all_money)

	print my_money,all_money,div_money
	print 'my_bet_history=%s'%my_bet_history
	print "oppobehavenumflop=%s"%oppobehavenum	

	if div_money<0.01:
		low_f1=cc.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,my_bet_history)
		print"low_f1=%s"%low_f1
		return low_f1
	elif div_money>0.7:
		high_f1=cc.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,my_bet_history)
		print"high_f1=%s"%high_f1
		return high_f1
	else:
		if max(threat)==3:
			f1=cc.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,my_bet_history)
			print "f1=%s"%f1
			return f1
		elif max(threat)==2:
			f2=cn.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,my_bet_history)
			print "f2=%s"%f2
			return f2
		else:
			f3=cs.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2)
			print "f3=%s"%f3
			return f3


#转牌阶段最终决策函数
def makeDecisionTurnFinal(card,cardround,percentage,oppobehave,oppobehavenum,num_player,playermovement,playerrank,my_money,all_money,my_bet_history):
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	global rank3 
	rank3 = getRank3(card)
	print rank3	
	div_money=calc_money(my_money,all_money)
	print my_money,all_money,div_money
	print 'my_bet_history=%s'%my_bet_history
	print "oppobehavenumturn=%s"%oppobehavenum	

	if div_money<0.01:
		low_t1 = cc.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3,my_bet_history)
		print"low_t1=%s"%low_t1		
		return low_t1
	elif div_money>0.7:
		high_t1 = cc.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3,my_bet_history)
		print"high_t1=%s"%high_t1				
		return high_t1
	else:	

		if max(threat)==3:
			t1 = cc.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3,my_bet_history)
			print "t1=%s"%t1
			return t1

		elif max(threat)==2:
			t2 = cn.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3,my_bet_history)
			print "t2=%s"%t2
			return t2


		else:
			t3 = cs.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3)
			print "t3=%s"%t3
			return t3


#河牌阶段最终决策函数
def makeDecisionRiverFinal(card,cardround,oppobehave,oppobehavenum,num_player,playermovement,playerrank,my_money,all_money,my_bet_history):
	global rank4
	rank4 = getRank4(card)
	rankboard = getRankBoard(card)
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	print rank4	
	div_money=calc_money(my_money,all_money)
	print my_money,all_money,div_money
	print "my_bet_history=%s"%my_bet_history
	print "oppobehavenumriver=%s"%oppobehavenum	

	if div_money<0.01:
		low_r1=cc.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard,my_bet_history)
		print "low_r1=%s"%low_r1
	
		return low_r1
	elif div_money>0.7:
		high_r1=cc.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard,my_bet_history)
		print "high_r1=%s"%high_r1
		
		return high_r1
	else:


		if max(threat)==3:
			r1 = cc.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard,my_bet_history)
			print "r1=%s"%r1
			return r1


		elif max(threat)==2:
			r2 = cn.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard,my_bet_history)
			print "r2=%s"%r2
			return r2


		else:
			r3 = cs.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard)
			print "r3=%s"%r3
			return r3


#计算公共牌阶段牌力
def getRank2(card):
	hand=[Card.new(card[0]),Card.new(card[1])]
	evaluator=Evaluator()
	board=[Card.new(card[2]),Card.new(card[3]),Card.new(card[4])]
	rank2=evaluator.evaluate(board,hand)
	return rank2
#计算转牌阶段牌力
def getRank3(card):
	hand=[Card.new(card[0]),Card.new(card[1])]
	evaluator=Evaluator()
	board=[Card.new(card[2]),Card.new(card[3]),Card.new(card[4]),Card.new(card[5])]
	rank3=evaluator.evaluate(board,hand)
	return rank3
#计算河牌阶段牌力
def getRank4(card):
	hand=[Card.new(card[0]),Card.new(card[1])]
	evaluator=Evaluator()
	board=[Card.new(card[2]),Card.new(card[3]),Card.new(card[4]),Card.new(card[5]),Card.new(card[6])]
	rank4=evaluator.evaluate(board,hand)
	return rank4
#计算桌面上所有五张明牌的牌力
def getRankBoard(card):
	board1=[Card.new(card[2]),Card.new(card[3])]
	evaluator=Evaluator()
	board2=[Card.new(card[4]),Card.new(card[5]),Card.new(card[6])]
	rankboard=evaluator.evaluate(board1,board2)
	return rankboard

