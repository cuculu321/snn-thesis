# Spiking Neural Network

## 環境
---
* python3
* Pipenv

のある環境で
```
pipenv install
```
を使用することで環境は自動で構築されます

## 実行方法
---

2layer_voice_reco上で
```
pipenv run python run-CPU/learning.py
```
を実行することで、実行時間のフォルダが生成されその中に様々な出力データが追加されていきます。

## 各フォルダについて
---
## 2layer_voice_reco
色々なプログラムが詰まっているフォルダ

## PASL-DSR
文章音声の音声データ

## souddata
各単音節のデータ

## 2020-01-23-11-45
出力データの1例


## 出力データ
---

## 1-2synapse(timestamp).txt
STDP学習済みの1-2層シナプス

## 2-3synapse(timestamp).txt
対応付け済みリスト

## answer(timestamp).txt
各単音節の類似度の評価(割合表記)

## end(timestamp).txt


## initial(timestamp).txt
初期シナプスの状態

## nohup.out
nohupコマンドで実行した際に生成されるやつ。プリント出力の内容が全て表示されています。

nohupコマンドについては[こちら](https://www.atmarkit.co.jp/ait/articles/1708/24/news022.html)

## run_parameters.txt
実行時のパラメーター。ちょくちょく変えていた値のみ表示してる

