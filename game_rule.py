import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from collections import deque

def prepareGame(field, medalBox, hand, bearPosition):
    stage1Medals = deque([1,2])
    stage1FieldMedals = deque([[2,1,3],[3,2,2],[2,3,1]])
    stage1FieldBear = [3,2]

    # 手配とメダルデッキの設定
    for number in range(len(stage1Medals)):
        if len(hand) <= 5 :
            hand.append(stage1Medals.popleft())
        else :
            medalBox.append(stage1Medals.popleft())

    # 川フィールドのメダルを配置
    for stage1FieldMedal in stage1FieldMedals:
        field[stage1FieldMedal[0]][stage1FieldMedal[1]] += stage1FieldMedal[2] 

    # クマを配置
    field[stage1FieldBear[0]][stage1FieldBear[1]] += 80
    bearPosition = [3,2]

    return field, medalBox, hand, bearPosition

def displayStatus(turn,medalBox,hand,field,bearPosition):
    # タイトル表示
    print("======================================")
    print("森クマメダル")
    print("======================================")
    
    # ステータス表示
    print("ターン:{}".format(turn))
    print("残りメダル:{}".format(len(medalBox)+len(hand)))
    print()

    # ハンド表示
    print("ハンド")
    print(hand)
    print()

    # フィールド表示
    for row in range(len(field)):
        print(field[row])
        if row == 0:
            print("------------------------------------")
    print()

    print("------------------------------------")
    print("クマは、{}行目,{}列目にいます。".format(bearPosition[0],bearPosition[1]+1))
    print("------------------------------------")
    print()

def selectDropMedal():
    print("[あなたのターンです]")

    # 選択入力1(1:1枚目,2:2枚目,3:3枚目,4:4枚目,5:5枚目,9:ゲーム終了)
    print("メダルを選択してください。")
    print("1:1枚目,2:2枚目,3:3枚目,4:4枚目,5:5枚目,9:ゲーム終了")
    print(">>", end="")

    selectMedal = int(input())
    if (selectMedal == 9):
        print("ゲームを終了します")
        sys.exit()
    else :
        print("ハンド{}番目のメダルを投入します ".format(selectMedal))

    print()

    # 選択入力2(1:レーン1,2:レーン2,3:レーン3、4:レーン4,5:レーン5)
    print("メダルを落とすレーンを選択してください。")
    print("1:レーン1,2:レーン2,3:レーン3、4:レーン4,5:レーン5")
    print(">>", end="")
    selectLane = int(input())

    return selectMedal, selectLane

def dropMedal(field,hand,selectMedal,selectLane):
    dropMedal = hand.pop(selectMedal-1)
    print("{}レーンに{}メダルが落下します。".format(selectLane,dropMedal))

    lene = []
    # レーンの情報を取得
    for column in field:
        lene.append(column[selectLane-1])

    # ゴールをのぞく
    lene = lene[1:]

    # 移動分の距離を作成
    moveLene = [10 for i in range(dropMedal)]
    # print("movelene",moveLene)

    # 落下メダルに応じてレーンを詰める
    for moveCount in range(dropMedal):
        if searchLeneIndex(lene,10) != -1:
            lene.remove(10)

    #print("lene",lene)

    for cell in lene:
        moveLene.append(cell)
    # print("movedlene",moveLene)

    lene = moveLene[:5]

    dropMedals = []
    for cell in reversed(moveLene[5:]):
        if cell != 10:
            dropMedals.append(cell)

    # 先頭にゴールをつける
    lene.insert(0, 10)

    #ずれた個所に落下メダル配置
    lene[dropMedal] += dropMedal
    # print(lene,dropMedals)

    #レーン情報を更新
    for index in range(len(lene)):
        field[index][selectLane-1] = lene[index]

    return field, hand, dropMedals

# TBD
def moveBear(field):
    print("[クマのターンです]")
    print("X,Xに移動しました")
    print("--------------------------------------")
    return field

def judgeGame(field,hand):
    if len(hand) == 0:
        return 2

    for i in range(5):
        if field[0][i] == 90 :
            return 1

    for column in field:
        for row in column : 
            if row > 90 :
                return 0

    if len(hand) == 0:
        return 2

    return 0

# TBD
def refillMedal(hand):
    return hand

def searchLeneIndex(lene, element, default=False):
    if element in lene:
        return lene.index(element)
    else:
        return -1