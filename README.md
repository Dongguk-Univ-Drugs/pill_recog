<darknet 사용시>
cpu=1, cv=1 을 이용하여 빌드하기 때문에 
LIBSO=1 으로 해야 python 모듈 사용 가능

Dockerfile.base 를 이용해 base image 생성


docker build -t dgu_pill_recog .

docker run -it --rm --volume="$(PWD):/app" dgu_pill_recog
# docker run -it --rm --volume="$(PWD):/app" dgu_pill_recog bash bash로 들어가고 싶은 경우


base 빌드시 pytesseract가 설치되지 않는 이슈가 있음.

---
# Usages
## 💡 Running
`main.py`가 있는 디렉토리에서 아래 명령어를 입력
```bash
uvicorn main:app --reload
```
- `--reload` 옵션을 추가하면 코드 수정 시 서버 종료 후 재시작

## 💡 Docs
인터넷 주소창에 아래와 같이 입력
``` plain
http://127.0.0.1:8000/docs
```
문서안에 multi-part에서 요구되는 Header, endpoint에 대한 설명이 나와있음
👉  `file`이 아마 `key` 값일 것으로 예상

## 💡 Redoc
``` plain
http://127.0.0.1:8000/redoc
```
input/ouput에 대해서 더 상세히 볼 수 있음, 하지만 API 시도는 못해봄

---

# Updates
## Text-Recognition
``` python
base_URL = 'https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq='

    return {
        'result': [base_URL + code for code in text] if len(text) > 0 else '',
        'time': f'{end - start}s'
    }
```
👉  후보군을 찾았다면 바로 접속할 수 있는 주소와 함께 반환하게 해놨음
👉  아직 클라이언트 모델이 만들어지지 않아서 우선 주소만 보내두었음, input/ouput 구조를 맞춘다면 언제든지 가능

## Color-Recognition
**범위 수정**
이미지 크기에 맞게 동적으로 생성하게 유도
``` python
if min(img_height, img_width) * img_channel * 10 < area < img_height * img_width:
```
최소 값을 `4000`으로 잡았을 때 결과가 가깝게 나왔던 것을 기반으로 `channel` $\times$ `10` 을 해주었음