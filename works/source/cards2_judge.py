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

def main():
	num_player=3
	card_player=[[['As','Ad']for i in range(50)],[['8h','Th']for i in range(50)],[['2s','2d']for i in range(50)]]
	board_player=[['5d','8c','Ac','Jc','4d']for i in range(50)]
	playermovement=[[30,0,30,10,0],[0,0,30,70,0],[0,0,30,70,0]]
	percentage=[[0,0.2,0.15,0.4,0,0.2,0,0.05,0,0],[0,0,0,0.4,0.2,0,0,0.4,0,0],[0,0.3,0.5,0,0,0.2,0,0,0,0]]
	#playerrank=[[3731,3731,3731],[2487,2487,2487],[4974,4974,4974]]
	cardround=1
	oppobehave=[['call','check','call','call','raise','call'],['call','check','call','call','raise','call'],['call','check','call','call','raise','call']]
	oppobehavenum=[[100,0,200,200,300,300],[100,0,200,200,300,300],[100,0,200,200,300,300]]
	playerrank=[[]for row in range(num_player)]
	t1=time.clock()
	for i in range(num_player):
		for x in range(len(board_player)):
			card=[card_player[i][x][0],card_player[i][x][1],board_player[x][0],board_player[x][1],board_player[x][2],board_player[x][3],board_player[x][4]]
                        t11 = time.clock()
			rank_temp=cn.getRank4(card)
			playerrank[i].append(rank_temp) 
                        t12 = time.clock()
                        print 'get Rank one time : ', t12-t11
	t2=time.clock()
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
        print "total time is : ", t7-t1
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
def getPlayerThreat(num_player,playermovement,playerrank):
	threat=[None]*num_player
	for i in range(num_player):
		ave_move = float(playermovement[i][0]+2*playermovement[i][1]+3*playermovement[i][2]+4*playermovement[i][3]+5*playermovement[i][4])\
			/(playermovement[i][0]+playermovement[i][1]+playermovement[i][2]+playermovement[i][3]+playermovement[i][4])
		a=7461*len(playerrank[i])-sum(playerrank[i])
		b=len(playerrank[i])
		print "a,b is : %s"% a,b,ave_move
		ave_rank = float(a)/b
		temp=float(ave_rank/ave_move)
		if  temp<550:
			threat[i]=1
		elif temp >1850:
			threat[i]=3
		else :
			threat[i]=2
		#print "ave_rank/ sum_move is :%s"%temp
	print "threat is %s"%threat

	return threat


def makeDecisionBlindFinal(card,cardround,oppobehave,oppobehavenum,num_player,playermovement,card_player,playerrank):
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	if max(threat)==3:
		cc.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player)
	elif max(threat)==2:
		cn.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player)
	else:
		cs.makeDecisionBlind(card,cardround,oppobehave,oppobehavenum,num_player)


def makeDecisionFlopFinal(card,cardround,percentage,oppobehave,oppobehavenum,num_player,playermovement,playerrank):
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	global rank2 
	rank2 = getRank2(card)

	if max(threat)==3:
		cc.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2)
	elif max(threat)==2:
		cn.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2)
	else:
		cs.makeDecisionFlop(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2)


def makeDecisionTurnFinal(card,cardround,percentage,oppobehave,oppobehavenum,num_player,playermovement,playerrank):
	threat=getPlayerThreat(num_player,playermovement,playerrank)
	global rank3 
	rank3 = getRank3(card)
	if max(threat)==3:
		cc.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3)
	elif max(threat)==2:
		cn.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3)
	else:
		cs.makeDecisionTurn(card,cardround,percentage,oppobehave,oppobehavenum,num_player,rank2,rank3)

def makeDecisionRiverFinal(card,cardround,oppobehave,oppobehavenum,num_player,playermovement,playerrank):
	rank4 = getRank4(card)
	rankboard = getRankBoard(card)
	threat=getPlayerThreat(num_player,playermovement,playerrank)

	if max(threat)==3:
		cc.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard)
	elif max(threat)==2:
		cn.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard)
	else:
		cs.makeDecisionRiver(card,cardround,oppobehave,oppobehavenum,num_player,rank3,rank4,rankboard)

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




