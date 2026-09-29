import math

#输出棋盘
def the_broad(broad):
    for each in broad:
        print('|'.join(each))
    print()

#判断胜利
def is_win(broad,char):
    for i in range(3):
        ans=ans1=0
        for j in range(3):
            if broad[i][j]==char:
                ans+=1
            if broad[j][i]==char:
                ans1+=1
        if ans==3 or ans1==3:
            return True
    ans = ans2 = 0
    for i in range(3):
        if broad[i][i]==char:
            ans+=1
        if broad[i][2-i]==char:
            ans2+=1
        if ans==3 or ans2==3:
            return True
    return False
#判断是否平局
def is_tie(broad):
    for i in range(3):
        for j in range(3):
            if broad[i][j]==" ":
                return False
    return True

#选手下棋
def get_player(broad):
    while True:
        row, col = input("row&col:").split(" ")
        row = int(row)
        col = int(col)
        if broad[row][col] == " ":
            return row, col
        else:
            print("try again")

#MinMax+alpha/beta剪枝
def minmax(broad,depth,play_char,ai_char,alpha,beta,is_max):
    if is_win(broad,play_char):
        return -10+depth,None
    if is_win(broad,ai_char):
        return 20-2*depth,None
    if is_tie(broad):
        return 0,None
    #ai下棋，求最大
    if is_max :
        best_score = -math.inf
        best_move = None
        for row in range(3):
            for col in range(3):
                if broad[row][col] == " ":
                    broad[row][col] = ai_char
                    score,_=minmax(broad,depth-1,play_char,ai_char,alpha,beta,False)
                    broad[row][col]=" "
                    if score>best_score:
                        best_score=score
                        best_move=row,col
                    alpha=max(alpha,score)
                    if beta<=alpha:
                        break
        return best_score,best_move
    #玩家下棋，求最小
    else:
        best_score = math.inf
        best_move = None
        for row in range(3):
            for col in range(3):
                if broad[row][col] == " ":
                    broad[row][col] = play_char
                    score,_=minmax(broad,depth-1,play_char,ai_char,alpha,beta,True)
                    broad[row][col]=" "
                    if score<best_score:
                        best_score=score
                        best_move=row,col
                    beta=min(beta,score)
                    if beta<=alpha:
                        break
        return best_score,best_move

#开始游戏界面
def start_game():
    broad=[[" " for row in range(3)] for col in range(3)]
    the_broad(broad)
    #用户输入，选定角色，默认”X“先手
    while True:
        player_char=input("X/O?")
        if player_char.upper() == "X":
            player_char=player_char.upper()
            break
        elif player_char.upper() == "O":
            player_char=player_char.upper()
            break
        else :
            print("try again")

    #判断先手
    if player_char=="X":
        while not is_win(broad,player_char) and not is_tie(broad):
            row, col = get_player(broad)
            broad[row][col] = "X"
            the_broad(broad)
            if is_win(broad,player_char):
                print("hh,you is win!")
                return
            if is_tie(broad):
                print("hh,we all win!")
                return
            print("hh,AI's brain is thinking...")
            _,(row,col)=minmax(broad,9,player_char,"O",-math.inf,math.inf,True)
            print(f"AI choose ({row}, {col})")
            broad[row][col]="O"
            the_broad(broad)
            if is_win(broad,"O"):
                print("hh,AI is win!")
                return
            if is_tie(broad):
                print("hh,we all win!")
                return
    else:
        while not is_win(broad,player_char) and not is_tie(broad):
            print("hh,AI's brain is thinking...")
            _, (row, col) = minmax(broad, 9, player_char, "X", -math.inf, math.inf, True)
            print(f"AI choose ({row}, {col})")
            broad[row][col] = "X"
            the_broad(broad)
            if is_win(broad, "X"):
                print("hh,AI is win!")
                return
            if is_tie(broad):
                print("hh,we all win!")
                return
            row, col = get_player(broad)
            broad[row][col] = player_char
            the_broad(broad)
            if is_win(broad, player_char):
                print("hh,you is win!")
                return
            if is_tie(broad):
                print("hh,we all win!")
                return



if __name__ == '__main__':
    start_game()