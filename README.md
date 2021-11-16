# ris_gov_doorplate_crawler

## Description

爬取內政部戶政司全球資訊網 >> 公開資訊 >> 門牌資訊。
爬取過程會需要輸入驗證碼的反爬蟲機制，需透過 OCR 技術辨識驗證碼，並透過 POST 請求提交並取得結果。

## Development Process

- 對目標網址進行 POST 請求, 獲取驗證碼 ID
- 下載該 ID 的驗證碼圖片, 使用 OpenCV 對圖片做前處理
- 使用 pytesseract 對圖片進行辨識, 回傳辨識結果
- 再次對目標網址進行 POST 請求, 同時帶入對應的驗證碼 ID 及辨識結果等參數
- 若結果為多頁呈現, 利用回傳的 token 值, 再次對目標網址進行 POST 請求

## Usage

    docker build -t doorplate_crawler -f Dockerfile .

成功地建立 `doorplate_crawler` image, 接著執行以下指令來取得 CSV 檔資料

    docker run --rm doorplate_crawler python handler.py

## Issues & Improvement

- 爬取驗證碼圖片失敗 -> 使用 Proxy 來降低爬蟲被阻擋的機率
- 驗證碼圖片辨識成功率低 -> 使用 LSTM 神經網路來訓練辨識引擎
