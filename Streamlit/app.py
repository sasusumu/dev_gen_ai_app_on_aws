# pip install streamlit 
# streamlit run app.py --server.baseUrlPath /jupyterlab/default/proxy/absolute/8501

import uuid
import json
import boto3
import streamlit as st
import asyncio
import nest_asyncio
import os
import time
import re

nest_asyncio.apply()

USER = "user"
ASSISTANT = "assistant"

# model ID の設定
model_id = "amazon.nova-lite-v1:0"

# システムメッセージの設定
system_prompt = "あなたは優秀なアシスタントです。質問に日本語で回答して下さい。"

@st.cache_resource
def get_bedrock_client():
    # client
    bedrock_client = boto3.client('bedrock-runtime', region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    return bedrock_client

def generate_response(messages):
    bedrock_client = get_bedrock_client()
    system_prompts = [{"text": system_prompt}]

    inference_config = {
        "maxTokens": 1000,
        "temperature": 0,
        "topP": 0.9
    }

    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config
    )

    return response["output"]["message"]

# <thinking>タグを除去する関数
def remove_thinking_tags(text):
    return re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)

# タイプライター効果でテキストを表示する関数
def typewriter_effect(text, placeholder, delay=0.02):
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(delay)

# チャット履歴保存用のセッションを初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# タイトル設定
st.title("Streamlit デモ")

if prompt := st.chat_input("質問を入力してください。"):
    # 以前のチャットログを表示（<thinking>タグを除去）
    messages = st.session_state.chat_log
    for message in messages:
        if message["content"] and "text" in message["content"][0]:
            filtered_text = remove_thinking_tags(message["content"][0]["text"])
            # <thinking>タグを除去すると Client の回答が空になるケースもあるので、空ではない場合のみチャットに表示する。
            if filtered_text and filtered_text.strip() != "":
                with st.chat_message(message["role"]):
                    st.write(filtered_text)

    with st.chat_message(USER):
        st.markdown(prompt)

    with st.chat_message(ASSISTANT):
        with st.spinner("回答を生成中..."):
            input_msg = {"role": "user", "content": [{"text": prompt}]}
            st.session_state.chat_log.append(input_msg)

            # チャットログをすべて含めてモデルを呼び出す
            response = generate_response(st.session_state.chat_log)

            # <thinking>タグを除去
            text = str(response["content"][0]["text"])
            filtered_response = remove_thinking_tags(text)

            # タイプライター効果で表示
            message_placeholder = st.empty()
            typewriter_effect(filtered_response, message_placeholder)

    # セッションの履歴に基盤モデルの回答を追加
    st.session_state.chat_log.append(response)