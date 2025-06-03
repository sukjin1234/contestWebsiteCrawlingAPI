from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json

app = FastAPI()

def load_contest_data(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("[오류] 데이터 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"[오류] 데이터 파일 읽기 실패: {e}")
        return []

@app.get("/contests")
def get_contests():
    data = load_contest_data("data.txt")
    if not data:
        raise HTTPException(status_code=404, detail="서버에 공모전 데이터가 없습니다.")
    return JSONResponse(content=data, status_code=200)
