import re
import os
import webbrowser
import time

def parseHH( handID ):
	HHPath = handHistoryPath + '\\' + x
	handhistory = open(HHPath, 'r')
	historyLines = handhistory.readlines()
	players = []
	playerName = []
	playerStacks = []
	seatOrder = []
	finalOrderStacks = []

	#scan file and process data

	for index in reversed(range(len(historyLines))):
		if re.search(r'(Hand #\d+)', historyLines[index]):
			startLine = index
			break

	blindLevel = re.search(r'(\d+)', re.search(r'(\(\d+\/\d+\))', historyLines[startLine]).group()).group()
	tourneyNumber = re.search(r'\d+', re.search(r'Tournament #\d+', historyLines[startLine]).group()).group()
	handNumber = re.search(r'\d+', re.search(r'Hand #\d+', historyLines[startLine]).group()).group()
	buttonSeat = re.search(r'\d', re.search(r'Seat #\d is the button', historyLines[startLine+1]).group()).group()
	action = False
	collectedDone = False
	removedBlinds = False

	if handNumber == handID:
		return handNumber

	ante = (2*int(blindLevel)) * 0.2

	for index in range(startLine, len(historyLines)):
		players.extend(re.findall(r'(Seat .+ in chips\))', historyLines[index]))


 		#work out stacks after all preflop betting
		if action:
			if not removedBlinds:
				removedBlinds = True

				#remove blinds and antes
				for index1 in range(len(seatOrder)):

					playerStacks[index1] = int(playerStacks[index1]) - ante

					if seatOrder[index1] == buttonSeat:
						if index1 + 1 > len(seatOrder)-1:
							index1 = index1 - len(seatOrder)

						index1 = index1 + 1

						playerStacks[index1] = int(playerStacks[index1]) - int(blindLevel)

						if index1 + 1 > len(seatOrder)-1:
							index1 = index1 - len(seatOrder)

						index1 = index1 + 1

						playerStacks[index1] = int(playerStacks[index1]) - int(blindLevel) * 2

						if index1 + 1 > len(seatOrder)-1:
							index1 = index1 - len(seatOrder)

						index1 = index1 + 1

						if index1 + 1 > len(seatOrder)-1:
							index1 = index1 - len(seatOrder)

						index1 = index1 + 1

						nextHandStart = index1;

			if re.search('raises', historyLines[index]):
				raiseName = re.search(r'\w+', historyLines[index]).group()
				raiseAmount = re.search(r'\d+', re.search(r'to \d+', historyLines[index]).group()).group()

				for index2 in range(len(playerName)):
					if playerName[index2] == raiseName:
						playerStacks[index2] = int(playerStacks[index2]) - int(raiseAmount)

			elif re.search('calls', historyLines[index]):
				callName = re.search(r'\w+', historyLines[index]).group()
				callAmount = re.search(r' \d+', historyLines[index]).group()

				for index3 in range(len(playerName)):
					if playerName[index3] == callName:
						playerStacks[index3] = int(playerStacks[index3]) - int(callAmount)

		#update stack of winning player(s)
		elif re.search('collected', historyLines[index]) and not collectedDone:

			winningPlayer = re.search(r'\w+', re.search(r'(\w+ collected)', historyLines[index]).group()).group()
			winningAmount = re.search(r'\d+', re.search(r'(collected \d+)', historyLines[index]).group()).group()
			collectedDone = True

			for index4 in range(len(playerName)):
				if playerName[index4] == winningPlayer:
					if playerStacks[index4] < 0:
						playerStacks[index4] = 0
					playerStacks[index4] = int(playerStacks[index4]) + int(winningAmount)

		if re.search('Dealt', historyLines[index]):

			action = True

			for items in players:
				playerName.append(re.search(r'(: .+ \()', items).group())
				playerName[len(playerName)-1] = playerName[len(playerName)-1].replace(": ", "")
				playerName[len(playerName)-1] = playerName[len(playerName)-1].replace(" (", "")
				playerStacks.append(re.search(r'\d+', re.search(r'\(\d+', items).group()).group())
				seatOrder.append(re.search(r'\d', items).group())

		elif re.search(r'(\*\*\* FLOP \*\*\*)', historyLines[index]) or re.search(r'Uncalled', historyLines[index]):
			action = False
			if re.search(r'Uncalled', historyLines[index]):
				returnedTo = re.search(r'\w+', re.search(r' \w+', re.search(r'to \w+', historyLines[index]).group()).group()).group()
				returnedAmount = re.search(r'\d+', historyLines[index]).group()

				for index5 in range(len(playerName)):
					if playerName[index5] == returnedTo:
						playerStacks[index5] = int(playerStacks[index5]) + int(returnedAmount)



	for index6 in range(len(playerStacks)):
		if nextHandStart+index6 > len(playerStacks)-1:
			nextHandStart = nextHandStart - len(playerStacks)

		if nextHandStart+index6 > len(playerStacks)-1:
			nextHandStart = nextHandStart - len(playerStacks)

		finalOrderStacks.append(playerStacks[index6 + nextHandStart]);

	removed = 0

	for index7 in range(len(playerStacks)):
		index7 = index7 - removed
		if (index7 == len(finalOrderStacks)-3 or index7 == len(finalOrderStacks)-2 or index7 == len(finalOrderStacks)-1) and int(finalOrderStacks[index7]) <= 0:
			finalOrderStacks.pop(index7)
			temp = finalOrderStacks[0]
			finalOrderStacks.pop(0)
			finalOrderStacks.append(temp)

	removed = 0

	for index8 in range(len(finalOrderStacks)):
		index8 = index8 - removed
		if int(finalOrderStacks[index8]) <= 0:

			finalOrderStacks.pop(index8)
			removed = removed + 1

	for num in range(0, 5):
		if len(finalOrderStacks) < 6:
			finalOrderStacks.append('')

	finalOrderStacks.append(int(blindLevel))
	finalOrderStacks.append(tourneyNumber)

	httpRequest(finalOrderStacks)

	return handNumber



def httpRequest(stackList):
	seat1 = str(stackList[0])
	seat2 = str(stackList[1])
	seat3 = str(stackList[2])
	seat4 = str(stackList[3])
	seat5 = str(stackList[4])
	seat6 = str(stackList[5])

	smallBlind = stackList[6]

	webbrowser.open('http://www.holdemresources.net/h/web-calculators/nashicm/results.html?action=calculate&bb=' + str(smallBlind*2) + '&sb=' + str(smallBlind) + '&ante=' + str((smallBlind*2)*0.2) + '&structure=1&s1=' + seat1 + '&s2=' + seat2+ '&s3=' + seat3+ '&s4=' + seat4+ '&s5=' + seat5 + '&s6=' + seat6 + '&s7=&s8=&s9=&s10=')
	return

# TODO:
# Blinds going up next hand?
#cant multitable as the handIDs clash
# cant compute if pot is chopped as it doesnt check for collected twice


tournSummaryPath = 'C:\Users\Adrian\AppData\Local\PokerStars.UK\TournSummaryadiman999'
handHistoryPath = 'C:\Users\Adrian\AppData\Local\PokerStars.UK\HandHistoryadiman999'

match = False
handID = 0



#Main
while(1):
	time.sleep(2)

	longCurrentHandHistories = [f for f in os.listdir(handHistoryPath) if f.endswith('.txt')]
	longFinishedTourns = [f for f in os.listdir(tournSummaryPath) if f.endswith('.txt')]

	if longFinishedTourns:

		for x in longCurrentHandHistories:
			for y in longFinishedTourns:

				currentMTTHH = re.search(r'(T\d+)', x).group()
				finishedMTTHH = re.search(r'(T\d+)', y).group()

				if currentMTTHH == finishedMTTHH:
					match = True

			if not match:
				handID = parseHH( handID )

			match = False

	else:
		#run code for this HH. It is an active HH
		for x in longCurrentHandHistories:
			handID = parseHH( handID )

