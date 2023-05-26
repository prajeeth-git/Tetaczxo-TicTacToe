def checkwin(board):
    if ((board["0"] == board["1"] == board["2"] and board["0"]!="") ):
        return board["0"]
    elif (board["3"] == board["4"] == board["5"] and board["3"]!=""):
        return board["3"]
    elif (board["6"] == board["7"] == board["8"]  and board["6"]!=""):
        return board["6"]

    elif (board["0"] == board["3"] == board["6"] and board["0"]!="") :
        return board["0"]
    elif (board["1"] == board["4"] == board["7"] and board["1"]!="") :
        return board["1"]
    elif (board["2"] == board["5"] == board["8"]  and board["2"]!=""):
        return board["2"]

    elif (board["0"] == board["4"] == board["8"] and board["0"]!=""):
        return board["0"] 
    elif (board["2"] == board["4"] == board["6"] and board["2"]!=""):
        return board["2"]

    else:
        return None
    
    
def checkdraw(board):
    for i in board:
        if board[f"{i}"]=="":
            return False
    return True
            