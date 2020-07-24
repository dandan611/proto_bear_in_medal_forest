import time
import game_rule

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
    field, medalBox, hand, bearPosition = game_rule.prepareGame(field, bearPosition)

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

        # クマ移動のターン
        field, bearPosition = game_rule.moveBear(field)

        # 勝敗判定
        gameStatus = game_rule.judgeGame(field, hand, bearPosition)
        if gameStatus != 0 :
            break

        # ハンドのメダルを補充する
        hand, medalBox = game_rule.refillMedal(hand, medalBox)

        # ターンを進める
        turn += 1
        print()

# ゲーム終了時の情報
game_rule.displayStatus(turn,medalBox,hand,field,bearPosition)

if gameStatus == 1:
    print("ゲームクリアです")
else :
    if gameStatus == 3:
        print("残りメダル数:",len(hand)+len(medalBox))
        print("メダルがなくなってしまったため、ゲームオーバーです")
    else :
        print("落ちたもの：",dropMedals)
        print("クマが滝に落ちてしまったので、ゲームオーバーです")
