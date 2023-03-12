from typing import Union

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root(text: str = ''):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ja,ja-JP;q=0.9,und;q=0.8',
        'origin': 'https://hiroyuki.coefont.cloud',
        'referer': 'https://hiroyuki.coefont.cloud/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }
    # Text-to-Speech を実行
    result = requests.post(
        url='https://tgeedx93af.execute-api.ap-northeast-1.amazonaws.com/production/hiroyuki/text2speech',
        headers=headers,
        json={
            'coefont': '19d55439-312d-4a1d-a27b-28f0f31bedc5',  # ひろゆきの CoeFont 固定
            'text': text,
        },
    )
    if result.status_code == 200 and result.json()['statusCode'] == 200 and result.json()['body']['success'] is True:
        wav_key: str = result.json()['body']['wav_key']
        url: str = f'https://tgeedx93af.execute-api.ap-northeast-1.amazonaws.com/production/chore/get_presigned_url?wav_key={wav_key}'

        return {"ok": True, "url": url}

    return {"ok": False}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
