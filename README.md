# docker-chatbot-niko
https://twitter.com/DekiruNiko

かすみんだってできますけどbot(https://twitter.com/nakasu_kasu )と多分同じです。


## 使い方
1. twitter APIのアカウントを取得します。
2. workflow/src/commonにあるconfig.json.bakをconfig.jsonにコピーします
3. workflow/src/common/config.jsonの中を編集します。db, dbuser, dbpass, dbhost: 接続先MySQLの、DB、user, password及びホスト名(IPアドレス可)
4. 接続先のMySQLで、2で設定したdbを作成し、dbuserに権限を付与します。MySQLは事前に立てておく必要があります。残りのconsumer_tokenとconsumer_token_secretは1で取得したものを使ってください。です。

コマンド

mysql> CREATE USER hogehoge IDENTIFIED BY 'password';

mysql> CREATE DATABASE yazawa_niko;

mysql> grant all privileges on yazawa_niko.* to hogehoge;

mysql> flush privileges;

5. docker-chatbot-nikoルートで次のコマンドを実行します。

$ docker-compose up

(以下不足点あるので修正中。具体的に言うと一旦botコンテナ立ち上げてworkflow/src/common/auth_api.pyを呼ぶ必要があり)

6. 別ターミナルでdigdagマシンに接続します。

$ docker exec -it docker-chatbot-niko_digdag_1 /bin/bash

docker-chatbot-niko_digdag_1は環境によって名前は変わると思います。とにかくdigdagと付いたコンテナに接続してください。接続したらジョブファイルをdigdag pushします。

$ cd /tmp/bot/workflow

$ digdag push 任意の実行プロジェクト名

あとは一定の間隔で実行されるはずです。実行結果は4でdocker-composeを実行したターミナル上に表示されます。ただしこれだとターミナルを閉じた時に終了するので、その場合はdocker-compose up -dを実行してください。

## 注意点

現状だとPostgreSQLのユーザパスワードがいい加減なのになっているので、修正が必要です。
