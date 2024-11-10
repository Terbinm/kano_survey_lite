# KANO 問卷調查系統

這是一個基於 Flask 的 KANO 模型問卷調查系統，用於收集和分析用戶對產品或服務特性的評價。系統支援問卷管理、資料收集、結果統計和個別回應查看等功能。

## 功能特點

- 📝 問卷管理：新增、編輯、刪除問卷題目
- 📊 統計分析：自動計算 KANO 分類結果
- 👥 使用者友善：直覺的問卷填寫界面
- 📱 響應式設計：支援各種設備尺寸
- 🔍 詳細記錄：查看個別問卷回應
- 📈 視覺化呈現：統計結果圖表展示
- 🛠️ 批量導入：支援批量導入問題

## 系統需求

- Python 3.8+
- SQLite3
- 現代網頁瀏覽器

## 本地安裝與運行

### Dockerfile 說明：
1. 使用 `python:3.9-slim` 作為基礎映像，這是一個輕量級的 Python 3.9 映像
2. 設定環境變數防止 Python 生成 `.pyc` 檔案並確保輸出不被緩衝
3. 安裝必要的系統依賴
4. 建立並設定 `/app/instance` 目錄用於存放 SQLite 資料庫
5. 設定適當的檔案權限
6. 暴露 12345 端口

### docker-compose.yml 說明：
1. 定義一個名為 `web` 的服務
2. 將容器的 12345 端口映射到主機的 12345 端口
3. 使用 volumes 持久化資料庫和靜態檔案
4. 設定自動重啟機制
5. 設定環境變數

### 部署步驟：

1. 執行以下命令建立和啟動容器：
```bash
# 建立和啟動容器
docker-compose up -d

# 查看容器日誌
docker-compose logs -f
```

2. 停止和移除容器：
```bash
docker-compose down
```

### 注意事項：
1. 資料庫檔案會被保存在 `instance` 目錄中
2. 靜態檔案會被掛載到容器中的 `/app/static` 目錄
3. 系統會在 http://localhost:12345 上執行
4. 容器會自動重啟（如果發生錯誤或系統重啟）

如果需要進入容器執行指令：
```bash
docker exec -it kano_survey_lite bash
```

這個配置已經考慮到：
- 資料持久化
- 安全性設定
- 效能優化
- 錯誤恢復
- 方便的維護和更新

要更新應用程式時，只需要：
1. 修改程式碼
2. 重新建立映像：`docker-compose build`
3. 重新啟動容器：`docker-compose up -d`

## 專案結構

```
kano-survey-system/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py              # 主應用程式
├── config.py           # 配置檔案
├── constants.py        # 常數定義
├── models.py           # 資料模型
├── requirements.txt    # 依賴包列表
├── static/            # 靜態資源
│   └── img/          
├── templates/         # 模板檔案
│   ├── base.html
│   ├── manage_questions.html
│   ├── responses.html
│   ├── results.html
│   └── survey.html
└── data/             # 資料存儲
    └── kano_survey.db
```

## 資料備份

Docker 容器中的資料庫檔案位於 `/app/data` 目錄，建議定期備份該目錄：

```bash
# 備份資料
docker cp kano-survey-app:/app/data ./backup

# 還原資料
docker cp ./backup/. kano-survey-app:/app/data
```

## 環境變數

可以通過環境變數配置以下參數：

- `FLASK_APP`: Flask 應用入口（預設：app.py）
- `FLASK_ENV`: 執行環境（development/production）
- `SECRET_KEY`: 應用程式金鑰

## 常見問題解決

1. 資料庫連接錯誤：
   - 確保 data 目錄具有正確的讀寫權限
   - 檢查 SQLite 資料庫檔案是否存在

2. 端口衝突：
   - 修改 app.py 中的端口號
   - 或修改 Docker 映射端口

3. Docker 容器無法啟動：
   - 檢查 logs：`docker logs kano-survey-app`
   - 確保沒有其他服務佔用相同端口

## 安全性建議

1. 生產環境部署時：
   - 修改 `config.py` 中的 `SECRET_KEY`
   - 設定適當的檔案權限
   - 使用 HTTPS
   - 配置適當的防火牆規則

2. 定期備份：
   - 設定自動備份機制
   - 保存多個備份版本

## License

MIT License - see [LICENSE](LICENSE) file for details

## 貢獻指南

1. Fork 專案
2. 建立特性分支：`git checkout -b feature/amazing-feature`
3. 提交變更：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 發起 Pull Request

## 聯絡方式

如有問題或建議，請提交 Issue 或聯絡專案維護者。

---

🔗 **相關文件：**
- [Flask 文檔](https://flask.palletsprojects.com/)
- [KANO 模型介紹](https://zh.wikipedia.org/wiki/KANO%E6%A8%A1%E5%9E%8B)
### 顏色設定參考
https://tailwindcss.com/docs/customizing-colors