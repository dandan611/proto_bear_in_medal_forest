import time
import game_rule
from collections import deque

def testPrepareGame(field, medalBox, hand, bearPosition):
    stage1Medals = deque([1,2,3,4,5])
    stage1FieldMedals = deque([[1,1,2],[2,1,2],[3,1,3],[5,1,5],[3,2,2]])
    # deque([[1,1,2],[2,1,2],[3,1,3],[4,1,4],[5,1,5],[3,2,2]])
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


if __name__ == "__main__":

    # ゲームの準備
    turn = 1
    gameStatus = 0

    # 手配
    hand = []

    # 落ちたメダル
    dropMedals = []

    # 川フィールド
    field = [ [ 10 for j in range(5)]  for i in range(6)]

    # クマ座標
    bearPosition = [] 

    # メダル箱(デッキ)
    medalBox = []

    # ゲームの準備
    field, medalBox, hand, bearPosition = testPrepareGame(field, medalBox, hand,bearPosition)

    while(True):        
        time.sleep(1)


        # タイトル表示
        game_rule.displayStatus(turn,medalBox,hand,field,bearPosition)

        # プレイヤーのターン
        selectMedal, selectLane = game_rule.selectDropMedal()

        # メダル落下のターン
        field, hand,dropMedals = game_rule.dropMedal(field,hand,selectMedal,selectLane)

        print("落下したもの:",dropMedals)
        # クマが落ちてしまった場合はゲームオーバー(game_rule.judgeGameに入れたほうがいいかも)
        if len(dropMedals) > 0 and max(dropMedals) > 90 :
            gameStatus = 2
            break

        # 勝敗判定
        gameStatus = game_rule.judgeGame(field,hand)
        if gameStatus != 0 :
            break

        # ハンドのメダルを補充する
        hand = game_rule.refillMedal(hand)

        # ターンを進める
        turn += 1
        print()

if gameStatus == 1:
    print("ゲームクリアです")
else :
    if len(hand) == 0:
        print("メダルがなくなってしまったため、ゲームオーバーです")
    else :
        print("クマが滝に落ちてしまったので、ゲームオーバーです")

