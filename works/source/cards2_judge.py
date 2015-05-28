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
#根据对手历史各轮的下注风格，推算对手的牌风，即下注威胁值
def getPlayerThreat(num_player,playermovement,playerrank):
	threat=[None]*num_player
	for i in range(num_player):
		if sum(playermovement[i])==0:
			threat[i]=1
		else:
			ave_move = float(playermovement[i][0]+2*playermovement[i][1]+3*playermovement[i][2]+4*playermovement[i][3]+5*playermovement[i][4])\
				/(playermovement[i][0]+playermovement[i][1]+playermovement[i][2]+playermovement[i][3]+playermovement[i][4])
			a=7461*len(playerrank[i])-sum(playerrank[i])
			b=len(playerrank[i])
			if b == 0:
			    threat[i] = 2
			    continue
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
def makeDecisionBlindFinal(card,cardround,oppobehave,oppobehavenum,num_player,playermovement,card_player,playerrank):

	threat=getPlayerThreat(num_player,playermovement,playerrank)
	if max(threat)==3:
		b=cc.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player)
		print "b1=%s"%b
	elif max(threat)==2:
		b=cn.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player)
		print "b2=%s"%b
	else:
		b = cs.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player)
		print "b3=%s"%b
	return b

#公共牌阶段最终决策函数
def makeDecisionFlopFinal(card,cardround,percentage,oppobehave,oppobehavenum,num_player,playermovement,playerrank):
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	global rank2 
	rank2 = getRank2(card)

	if max(threat)==3:
		f=cc.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2)
		print "f1=%s"%f

	elif max(threat)==2:
		f=cn.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2)
		print "f2=%s"%f

	else:
		f=cs.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2)
		print "f3=%s"%f
	return f

#转牌阶段最终决策函数
def makeDecisionTurnFinal(card,cardround,percentage,oppobehave,oppobehavenum,num_player,playermovement,playerrank):
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	global rank3 
	rank3 = getRank3(card)
	if max(threat)==3:
		t  = cc.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3)
		print "t1=%s"%t 

	elif max(threat)==2:
		t  = cn.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3)
		print "t2=%s"%t 

	else:
		t  = cs.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3)
		print "t3=%s"%t 
	return t

#河牌阶段最终决策函数
def makeDecisionRiverFinal(card,cardround,oppobehave,oppobehavenum,num_player,playermovement,playerrank):
	global rank4
	rank4 = getRank4(card)
	rankboard = getRankBoard(card)
	threat=getPlayerThreat(num_player,playermovement,playerrank)

	if max(threat)==3:
		r  = cc.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard)
		print "r1=%s"%r 

	elif max(threat)==2:
		r  = cn.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard)
		print "r2=%s"%r 

	else:
		r  = cs.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard)
		print "r3=%s"%r 
	return r

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
