"""
Streamlit app: 詩意生成器
將使用者輸入轉寫成詩詞口吻，預設使用 OpenAI GPT。
"""

import os
import textwrap
from typing import Optional
import importlib.util

import aisuite as ai
import streamlit as st

# 預設使用 OpenAI，並提供其他選項。
DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o"
PROVIDER_KEY_ENV = {
    "openai": "OPENAI_API_KEY",
    "groq": "GROQ_API_KEY",
    "mistral": "MISTRAL",
    "google": "GOOGLE_API_KEY",
    "xai": "XAI_API_KEY",
}

MODEL_OPTIONS = {
    "openai": ["gpt-5", "gpt-4o", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini"],
    "google": ["gemini-3.0-pro", "gemini-3.0-flash", "gemini-2.0-pro-exp"],
    "xai": ["grok-4", "grok-3", "grok-2-vision-latest"],
}


@st.cache_resource
def get_client() -> ai.Client:
    # 使用快取避免每次互動都重新初始化。
    return ai.Client()


def generate_poem(
    user_text: str,
    provider: str = DEFAULT_PROVIDER,
    model: str = DEFAULT_MODEL,
    style: Optional[str] = None,
) -> str:
    system_prompt = textwrap.dedent(
        f"""
        你是一位善用中文意象的詩人。請將使用者的話改寫成短詩：
        - 保留原本主題與情緒，但用詩意的畫面與節奏呈現。
        - 形式可自由（古典/現代），盡量控制在 4 到 8 行。
        - 若提供風格提示，將其融入詩中。
        - 口吻優雅，避免直接命令語氣，不要解釋。
        """
    ).strip()

    user_prompt = (
        f"風格提示：{style}\n原文：{user_text}" if style else f"原文：{user_text}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    client = get_client()
    response = client.chat.completions.create(
        model=f"{provider}:{model}", messages=messages
    )
    return response.choices[0].message.content


def set_api_key(provider: str, api_key: str) -> None:
    """依 provider 設定對應環境變數，避免在日誌顯示。"""
    env_name = PROVIDER_KEY_ENV.get(provider.lower())
    if env_name and api_key:
        os.environ[env_name] = api_key


def ensure_provider_dependency(provider: str) -> None:
    """檢查必要套件是否已安裝，缺少則給出明確提示。"""
    provider = provider.lower()
    if provider == "openai" and importlib.util.find_spec("openai") is None:
        raise RuntimeError("缺少 openai 套件，請先執行 pip install openai 再重試。")
    if provider == "google" and importlib.util.find_spec("google.generativeai") is None:
        raise RuntimeError("缺少 google-generativeai 套件，請先執行 pip install google-generativeai。")
    # 其他 provider 依需要再補充檢查。


def main() -> None:
    st.set_page_config(page_title="詩意生成器", page_icon=":art:", layout="centered")
    st.title("🌿 詩意生成器")
    st.caption("將日常語句轉寫成詩詞的樣子，預設使用 GPT")

    with st.expander("模型設定", expanded=False):
        api_key = st.text_input(
            "API Key",
            value="",
            type="password",
            help="此欄位不會在畫面顯示，將寫入對應環境變數後呼叫模型。",
        )
        provider = st.selectbox(
            "Provider",
            options=list(MODEL_OPTIONS.keys()),
            index=list(MODEL_OPTIONS.keys()).index(DEFAULT_PROVIDER),
            help="選擇供應商（openai / google / xai）",
        )
        model = st.selectbox(
            "Model",
            options=MODEL_OPTIONS.get(provider, [DEFAULT_MODEL]),
            index=0,
            help="依據供應商可用的模型",
        )
        st.info(
            "可直接在此輸入 API key，或事先設定環境變數（OPENAI_API_KEY、GOOGLE_API_KEY、XAI_API_KEY 等）。"
        )

    user_text = st.text_area("輸入一句話或一段文字", height=140)
    style = st.text_input("可選擇輸入風格提示（例如：淡淡哀愁、現代自由詩、唐詩風格）")
    submit = st.button("生成詩意版本", type="primary")

    if submit:
        if not user_text.strip():
            st.warning("請先輸入內容，再點擊生成。")
            return
        set_api_key(provider, api_key)
        try:
            ensure_provider_dependency(provider)
        except RuntimeError as exc:
            st.error(str(exc))
            return
        with st.spinner("正在寫詩..."):
            try:
                poem = generate_poem(user_text, provider=provider, model=model, style=style)
                st.success("完成！")
                st.markdown(poem)
            except Exception as exc:  # pragma: no cover - runtime aid
                st.error(f"生成失敗：{exc}")


if __name__ == "__main__":
    # 提醒使用者需先設定 API key
    if not (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("GROQ_API_KEY")
        or os.getenv("MISTRAL")
    ):
        print("請在執行前設定對應的 API key，例如 OPENAI_API_KEY。")
    main()
