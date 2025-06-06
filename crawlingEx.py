import json
import requests
from bs4 import BeautifulSoup

def get_allforyoung_contest_links():
    """
    1. 메인 목록 페이지에서 모든 공모전 상세페이지 링크를 수집
    OUTPUT: 상세 페이지 전체 URL의 리스트
    """
    url = "https://www.allforyoung.com/posts/contest?tags=20"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 목록에서 상세링크 추출
        links = []
        for a in soup.select('a.cursor-newtab'):
            href = a.get('href')
            if href and href.startswith('/posts/'):
                full_url = "https://www.allforyoung.com" + href
                links.append(full_url)
        return links
    except Exception as e:
        print(f"[목록 페이지 오류] {e}")
        return []

def parse_allforyoung_contest_detail(detail_url):
    """
    2. 상세 페이지에서 공모전 정보를 파싱
    OUTPUT: dict (공모전 이름, 주최측, 대상, 접수기간, 문의처, 링크, 이미지)
    """
    try:
        resp = requests.get(detail_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        target = "미제공" 
        title = soup.select_one('h2').get_text(strip=True) if soup.select_one('h2') else "미제공"
        host = soup.select_one('div.space-y-4 > h3.font-medium').get_text(strip=True) if soup.select_one('div.space-y-4 > h3.font-medium') else "미제공"
        period = soup.select_one('div.flex>p').get_text(strip=True) if soup.select_one('div.flex>p') else "미제공"
        contact = "미제공"
        image = "미제공"

        # 썸네일 이미지
        img_tag = soup.select_one('img.object-cover')
        if img_tag and img_tag.get('src'):
            image = img_tag['src']
            if image.startswith('/'):
                image = "https://www.allforyoung.com" + image

        return {
            "공모전 이름": title,
            "주최측": host,
            "대상": target,
            "접수기간": period,
            "문의처": contact,
            "공모전 링크": detail_url,
            "팜플렛 이미지": image,
        }
    except Exception as e:
        print(f"[상세페이지 오류] {detail_url} | {e}")
        return {
            "공모전 이름": "미제공",
            "주최측": "미제공",
            "대상": "미제공",
            "접수기간": "미제공",
            "문의처": "미제공",
            "공모전 링크": detail_url,
            "팜플렛 이미지": "미제공",
        }

def get_allforyoung_contests():
    """
    전체 공모전 정보를 한 번에 반환
    """
    contests = []
    links = get_allforyoung_contest_links()
    for link in links:
        contest = parse_allforyoung_contest_detail(link)
        contests.append(contest)
    return contests

if __name__ == "__main__":
    data = get_allforyoung_contests()
    
     # 크롤링 결과를 data.txt로 저장
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    for contest in data:
        print(contest)
