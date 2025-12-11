# G1-IoT-HW4-Deep-Learning-AIGC

## ABSTRACT
本專案提供以 Streamlit 介面呈現的「詩意生成器」，使用 aisuite 整合多家生成式語言模型，將使用者輸入的日常語句轉寫成四至八行的中文詩。介面支援輸入 API Key、下拉選擇供應商與模型，預設 OpenAI gpt-4o，也可切換到 gpt-5、Gemini 3.x、XAI Grok-4 等較新版本，並在缺少套件時提示安裝。輸入框接受文字與可選風格提示，提交後呼叫模型返回詩意結果；若未填入內容則提醒補充。`requirements.txt` 列出 aisuite、streamlit、openai、google-generativeai 依賴，可依需求新增其他供應商；預設樣式保持簡潔，便於後續自訂或佈署。

運行流程簡單：先以 `pip install -r requirements.txt` 安裝依賴，執行 `streamlit run streamlit_poetry.py`，在頁面「模型設定」輸入 API Key，選擇供應商與模型即可開始生成。系統在每次提交前會自動寫入對應環境變數並檢查必要套件，缺失時顯示友善提示，避免隱晦錯誤。使用者可輸入風格提示（如現代自由詩、唐詩風、淡淡哀愁），模型會在保留主題與情緒的前提下，產出詩意的意象與節奏。應用預設保持清爽佈局，便於整合至教學示範、工作坊或社群互動場景，亦可視需求擴充更多 provider、模型與版面樣式。
