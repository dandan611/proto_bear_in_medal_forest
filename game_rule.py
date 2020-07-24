import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from collections import deque
import copy

def prepareGame(field, bearPosition):
    stage1Medals = deque([1,2])
    stage1FieldMedals = deque([[2,1,3],[3,2,3],[2,3,1]])
    stage1FieldBear = [3,2]

    # 手配とメダルデッキの設定
    hand = []
    medalBox = []   
    for number in range(len(stage1Medals)):
        if len(hand) < 5 :
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

    # メダルデッキ表示
    print("メダルデッキ")
    print(medalBox)
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

    # 落下メダルに応じてレーンを詰める
    for moveCount in range(dropMedal):
        if searchLeneIndex(lene,10) != -1:
            lene.remove(10)

    for cell in lene:
        moveLene.append(cell)

    lene = moveLene[:5]

    dropMedals = []
    for cell in reversed(moveLene[5:]):
        if cell != 10:
            dropMedals.append(cell)

    # 先頭にゴールをつける
    lene.insert(0, 10)

    #ずれた個所に落下メダル配置
    lene[dropMedal] += dropMedal

    #レーン情報を更新
    for index in range(len(lene)):
        field[index][selectLane-1] = lene[index]

    return field, hand, dropMedals

def moveBear(field):
    print("[クマのターンです]")

    # 川フィールドからクマの座標を取得
    bearPosition = getBearPosition(field)
    print("{},{}にいます".format(bearPosition[0],bearPosition[1]+1))

    # クマの乗っているメダルの番号を取得
    bearMedal = field[bearPosition[0]][bearPosition[1]]-90
    # print("クマが乗っているメダル:",bearMedal)

    # 前方に移動できるか
    # bearPosition[0]-1 が 1行目(0以上)じゃない かつ　その先のメダルが、bearMedalの±1
    if bearPosition[0]-1 > 0 and abs((field[bearPosition[0]-1][bearPosition[1]]-10) - bearMedal) == 1:
        # 川フィールドとクマの座標を更新する
        field[bearPosition[0]][bearPosition[1]] -= 80
        bearPosition[0] -= 1
        field[bearPosition[0]][bearPosition[1]] += 80
        print("{},{}に移動しました".format(bearPosition[0],bearPosition[1]+1))
        print("--------------------------------------")
        return field, bearPosition

    # 右に移動できるか
    # bearPosition[1]+1 が 5列目(5以上)じゃない かつ　その先のメダルが、bearMedalの±1 かつ　メダルがある
    if bearPosition[1]+1 < 5 and abs((field[bearPosition[0]][bearPosition[1]+1]-10) - bearMedal) == 1 and field[bearPosition[0]][bearPosition[1]+1] != 10:
        # 川フィールドとクマの座標を更新する
        field[bearPosition[0]][bearPosition[1]] -= 80
        bearPosition[1] += 1
        field[bearPosition[0]][bearPosition[1]] += 80
        print("{},{}に移動しました".format(bearPosition[0],bearPosition[1]+1))
        print("--------------------------------------")
        return field, bearPosition

    # 左に移動できるか
    # bearPosition[1]-1 が 1列目じゃない(0以下) かつ　その先のメダルが、bearMedalの±1 かつ　メダルがある
    if bearPosition[1]-1 > -1 and abs((field[bearPosition[0]][bearPosition[1]-1]-10) - bearMedal) == 1 and field[bearPosition[0]][bearPosition[1]-1] != 10:
        # 川フィールドとクマの座標を更新する
        field[bearPosition[0]][bearPosition[1]] -= 80
        bearPosition[1] -= 1
        field[bearPosition[0]][bearPosition[1]] += 80
        print("{},{}に移動しました".format(bearPosition[0],bearPosition[1]+1))
        print("--------------------------------------")
        return field, bearPosition

    print("{},{}に留まり、移動しませんでした".format(bearPosition[0],bearPosition[1]+1))
    print("--------------------------------------")

    return field, bearPosition

def judgeGame(field, hand, bearPosition):
    # クマがゴールに到達している(ステージクリア)
    if isExploreGoal(field, bearPosition) :
        return 1

    # 置けるメダルがもうない(ゲームオーバー)
    if len(hand) == 0:
        return 3

    # フィールドにクマがいる(ゲーム続行)
    for column in field:
        for row in column : 
            if row > 90 :
                return 0

    return 2

def refillMedal(hand, medalBox):
    if len(hand) < 5 and len(medalBox) != 0:
        hand.append(medalBox[0])
        medalBox = medalBox[1:]

    return hand, medalBox

def searchLeneIndex(lene, element, default=False):
    if element in lene:
        return lene.index(element)
    else:
        return -1

def getBearPosition(field):
    for column in range(len(field)):
        for row in range(len(field[0])):
            if field[column][row] > 90:
                return [column,row]

    return [-1,-1]

def isExploreGoal(field, bearPosition):
    # 探索方向(下、右、上、左)をセット
    direct = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    
    # 探索マップ
    exploreField = copy.deepcopy(field) 

    # 探索リストにスタート位置をセット
    exploreList = [[bearPosition[0],bearPosition[1] , field[bearPosition[0]][bearPosition[1]]-90]]
    exploreField[bearPosition[0]][bearPosition[1]] -= 80

    # 探索スタート
    while len(exploreList) > 0:
        """
        # for debug 
        print("探索リスト",exploreList)
        print("探索マップ---")
        for row in range(len(exploreField)):
            print(field[row])
            if row == 0:
                print("------------------------------------")
        """

        x, y, currentMedal = exploreList. pop(0)
        
        # 探索済みとしてセット
        exploreField[x][y] += 50 

        # ゴール
        if x == 1:
            return True

        # 幅優先探索
        # 川フィールド内　かつ 探索済みでない　かつ メダル番号が±1
        # もし、奥行が1のゴール確定の位置だった場合、Trueを返す　
        # そうでなければ、探索リストに追加
        for d in direct:
            dx = d[0]
            dy = d[1]
            if 1 < x+dx  and x+dx < 5  and  -1 < y+dy and y+dy < 5:
                if exploreField[x+dx][y+dy] < 50 and abs((exploreField[x+dx][y+dy]-10) - currentMedal) == 1:
                    exploreList.append([x+dx,y+dy,exploreField[x+dx][y+dy]-10])
    """
    print("探索リスト",exploreList)
    print("探索マップ---")
    for row in range(len(exploreField)):
        print(field[row])
        if row == 0:
            print("------------------------------------")
    """

    return False

