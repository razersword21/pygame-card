# 卡牌遊戲 [beta]

挑戰能到達第幾Rounds

```bash
pip install -r requirements.txt

python main.py
```

### 遊戲說明
* 每次擊敗敵人，可以從隨機3項加成選其中一個，當然敵人也會隨機增強
* 商店可購買能力值加成
* 敵人使用卡牌的戰鬥情形顯示在戰鬥歷程中

### 包成執行檔
```bash
pyinstaller -w main.py -n 無限輪迴 -p src -i source/game_ico.ico
pyinstaller main.py -n 無限輪迴 -p src -i source/game_ico.ico
```

### 未完成
* 玩家 敵人 buff debuff美術圖
* +職業 or +技能
* 商店金幣 很卡 選擇獎勵
