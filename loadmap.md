# Load Map

## about here
---
この研究をする場合、簡単にではあるものの**神経工学**に関する知識が必要となります。そのため、神経工学やSTDPを理解するために参考にした資料や論文、「この順番で読むと良さそう」的なものを残しておきます。

## 1. メカ屋のための脳科学入門-脳をリバースエンジニアリングする-

神経工学の入門書。何より普通に面白い本(主観)。**最初に読め**

ニューロンの基本的な動きや、脳内での情報表現方法がわかりやすく書いてあります。

## 2. 続 メカ屋のための脳科学入門-記憶・学習/意識 編-

先ほどの本の続編。

ヘブ則やSTDP、長期増強や長期抑制についても説明があります。

## 2.5 [すごい学生のScrapbox](https://scrapbox.io/AGI/Spiking_Neural_Network)

京大から東大院に言ってるすごい人のメモ。

見つけたのがかなり後半だったこともあり、私は参考にできたかったもののドメイン知識の概形は綺麗に捕らえられている。

分からない用語の取っ掛かりとしては便利そう。

## 3. [スパイキングニューラルネットワークにおける深層学習](https://www.jstage.jst.go.jp/article/seisankenkyu/71/2/71_159/_pdf)

SNNについてのサーベイ論文。

様々な手法について**日本語**で記されている。

## 4. [SNNのGithub](https://github.com/Shikhargupta/Spiking-Neural-Network)

叩き台として使用したコード。

理論は、*スパイキングニューラルネットワークにおける深層学習*の*4.2	 二層 SNN における教師なし学習例*が使用されている。また、私の論文冒頭の先行研究に記している*Unsupervised learning of digit recognition using spike-timing-dependent plasticity*を一部実装したものでもある。

## 5. 先行研究欄の研究
がんばれ

## 6. +α

色々な知識

### [脳内情報表現に関する一般的な命題](https://www.jstage.jst.go.jp/article/jnns/9/1/9_1_16/_pdf)

### [Philosophy of the Spike: Rate-Based vs. Spike-Based Theories of the Brain](https://www.frontiersin.org/articles/10.3389/fnsys.2015.00151/full)
* レートコーディング or テンポラルコーディング
* おばあちゃん細胞表現 or 分散表現
