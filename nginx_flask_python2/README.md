# 系統需求
*  需要一個 python2 的環境
*  要有 nginx 及 uwsgi 的工具
*  image 不要太大

# 開啟 container
*  需要先設定 docker-compose.yml
  *  將需要放進來的flask project 掛在 /uwsgi/project/[project_name]
  *  將純static 資料夾放在 /uwsgi/static
*  直接從建好的 image 開一個 container 來用
```shell
## in dir nginx_flask_python2
sh build.sh
docker-compose -f ./docker-compose.yml up -d
```

# 參考
*  如何使用 alpine 裡面的 service call[link](https://www.cyberciti.biz/faq/how-to-enable-and-start-services-on-alpine-linux/)
*  自己寫的 nginx 設定方式[link](https://docs.google.com/document/d/1i253FLtXX2rAJWU8HLEqF5i6SB4Iff97ALEsJ19UdEs/edit)