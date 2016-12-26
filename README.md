# Line Weather Bot In Taiwan With Flask

## 使用方法
* 字詞中出現天氣以以下情況處理
    * 時間分為三種情況
        * 如果句中包含今天，則返回今日的天氣
        * 如果句中包含明天，則返回明日的天氣
        * 如果句中以上情況都不包含，則返回今日的天氣
    * 地點則為輸入XX(市、縣)請注意"臺"必須為此繁體字
* 其他則是照原句返回
## 環境架設
* 預先準備
    * [LINE Messange Api 帳號](https://business.line.me/zh-hant/services/bot)
    * [Heroku 帳號](https://dashboard.heroku.com/)
    * [氣象資料開放平臺 帳號](http://opendata.cwb.gov.tw/index)
* Python --version=2.7.12
    需要的套件位於 requirements.txt 使用
    ```
    pip install -r requirements.txt
    ```
    安裝相關套件
* Heroku
    首先先設定帳號的環境變數，因為它們不應被寫死在code中
    ```
    heroku config:set "LINE_CHANNEL_SECRET"="your_line_secret"
    
    heroku config:set "LINE_CHANNEL_ACCESS_TOKEN"="your_access_token"
    
    heroku config:set "API_KEY"="氣象資料開放平台 授權碼"
    ```
    接下來將整份專案push到heroku上完成
    ```
    git add .
    git commit -m "Herokuuuuu"
    git push heroku master
    ```
* Finnal
    將LINE developers 上的 webhook設定成heroku的網址
    ```
    https://"your heroku".herokuapp.com/callback
    ```
    最後用LINE ID加入你的chatbot and
    ENJOY IT!!!!
