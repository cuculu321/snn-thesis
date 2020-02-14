# Spiking Neural Network

## 目次
---
1. 実行環境

1. 実行方法

1. 各フォルダについて

1. 出力データについて

1. 各プログラムの概要

## 1. 環境
---
* python3
* Pipenv

のある環境で
```
pipenv install
```
を使用することで環境は自動で構築されます

## 2. 実行方法
---

2layer_voice_reco上で
```
pipenv run python run-CPU/learning.py
```
を実行することで、実行時間のフォルダが生成されその中に様々な出力データが追加されていきます。

## 3. 各フォルダについて
---
### 2layer_voice_reco
色々なプログラムが詰まっているフォルダ

### PASL-DSR
文章音声の音声データ

### souddata
各単音節のデータ

### 2020-01-23-11-45
出力データの1例


## 4. 出力データについて
---

### 1-2synapse(timestamp).txt
STDP学習済みの1-2層シナプス

### 2-3synapse(timestamp).txt
対応付け済みリスト

### answer(timestamp).txt
各単音節の類似度の評価(割合表記)

### end(timestamp).txt
なにこれ？

### initial(timestamp).txt
初期シナプスの状態

### nohup.out
nohupコマンドで実行した際に生成されるやつ。プリント出力の内容が全て表示されています。

nohupコマンドについては[こちら](https://www.atmarkit.co.jp/ait/articles/1708/24/news022.html)

### run_parameters.txt
実行時のパラメーター。ちょくちょく変えていた値のみ表示してる

## 5. 各プログラムの概要
---
何をするのか、単体での実行方法があるものは実行方法と出力を書いていく。

### color_map
* カラーマップの生成・出力を行う
```
pipenv run python run-CPU/color_map.py 対象のフォルダ
```
出力：カラーマップのpngファイル

### console_write
これを使うとプリントの速度が上がるらしい。何となく関数化してある

### export_parameter
各パラメーターの出力

### get_current_directory
音声データのパスを読み込む

```
pipenv run python run-CPU/get_current_directory.py
```
出力：音声データのパスをプリント

### get_logmelspectrum
メル周波数スペクトル係数を得る

```
pipenv run python run-CPU/get_logmelspectrum.py
```
出力：女性音声1の単音節「あ」の中心部分から抽出したメル周波数スペクトル係数を表示

### label_sort
単音節ラベルによるソート

### learning
中心部分

実行方法は2. 実行方法に記載済み

### mapping
興奮性ニューロンと、そのニューロンが示す音響特徴の対応づけ

```
pipenv run python run-CPU/mapping.py
```
出力：各単音節によって、どのニューロンが発火していたのかをプリント

### neuron
積分発火モデルのニューロンクラス

### parameters
各種パラメーターの設定

### record_synapse
シナプスの出力と読み込みに関わる関数セット

### rl
STDP学習則

### spike_train
レートコーディング方法
```
pipenv run python run-CPU/spike_train.py
```
出力：女性音声1の単音節「が」の中心部分の特徴値から生成されたスパイク

### third_layer
コサイン類似度による分類

* 学習(test)
```
pipenv run python run-CPU/third_layer.py -t 対象のフォルダ
```
入力：1-2synapse
出力：2-3synapse

* 精度の確認(check)
```
pipenv run python run-CPU/third_layer.py -c 対象のフォルダ
```
入力：1-2synapse、2-3synapse
出力：end、answer

### var_th
ニューロンの膜電位の設定

### wav_split
音声の分割

* 静的分割：0.04s毎の分割
* 動的分割：単音節を14分割