# Streamlit (ストリームリット) を使用してフロントエンドを実装する

1. ターミナルで以下のコマンドを実行してください

```
pip install streamlit 
```

1. app.py を開いて内容を確認します。
2. 以下のコマンドを実行して Streamlit を起動します。

```
streamlit run app.py --server.baseUrlPath /jupyterlab/default/proxy/absolute/8501
```
1. ブラウザの新しいタブを開き `https://(ラボ環境のURLを確認).studio.us-east-1.sagemaker.aws/jupyterlab/default/proxy/absolute/8501` の URL にアクセスします。
1. ラボで使用している JupyterLab の URL が
`https://abcd.studio.us-east-1.sagemaker.aws/jupyterlab/default/lab` だった場合、アクセスする URL は `https://abcd.studio.us-east-1.sagemaker.aws/jupyterlab/default/proxy/absolute/8501` となります。

1. 動作確認ができたら、ターミナルで `Ctrl + c ` を入力し、Streamlit を停止します



