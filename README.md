# G1-IoT-HW4-Deep-Learning-AIGC

## ABSTRACT
本專案提供以 Streamlit 介面呈現的「詩意生成器」，使用 aisuite 整合多家生成式語言模型，將使用者輸入的日常語句轉寫成四至八行的中文詩。介面支援輸入 API Key、下拉選擇供應商與模型，預設 OpenAI gpt-4o，也可切換到 gpt-5、Gemini 3.x、XAI Grok-4 等較新版本，並在缺少套件時提示安裝。輸入框接受文字與可選風格提示，提交後呼叫模型返回詩意結果；若未填入內容則提醒補充。`requirements.txt` 已列出 aisuite、streamlit、openai、google-generativeai 依賴，可依需求新增其他供應商；預設樣式保持簡潔，便於後續自訂或佈署。
