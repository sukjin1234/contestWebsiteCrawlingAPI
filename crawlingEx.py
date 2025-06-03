import requests
from bs4 import BeautifulSoup

def get_contests_allforyoung() -> list:
    """
    요즘것들(allforyoung.com) 사이트에서 공모전 정보를 크롤링합니다.
    INPUT: 없음
    OUTPUT: 각 공모전 정보를 담은 dict의 리스트 [{...}, ...]
    - 예외 발생 시 시스템 종료 없이 빈 리스트를 반환하며, 오류 메시지를 출력합니다.
    - 정보가 없는 필드는 '미제공'으로 처리합니다.
    """
    url = "https://www.allforyoung.com/posts/competitions"
    contests = []

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 공모전 목록 전체를 가져오는 부분 (실제 구조 확인 필요)
        contest_items = soup.select('div.contest-list > a')  # 예시: 'a' 태그로 상세 이동

        for item in contest_items:
            try:
                link = "https://www.allforyoung.com" + item.get('href', '')
                img_tag = item.select_one('img')
                image = img_tag.get('src') if img_tag else "미제공"
                # 상세페이지 추가 파싱 필요 (공모전명, 주최, 대상 등은 상세에서 수집)
                title = item.select_one('.post-title').get_text(strip=True) if item.select_one('.post-title') else "미제공"

                # 상세페이지 추가 정보 파싱
                contest_detail = parse_contest_detail_allforyoung(link)

                contests.append({
                    "공모전 이름": title,
                    "주최측": contest_detail.get("주최측", "미제공"),
                    "대상": contest_detail.get("대상", "미제공"),
                    "접수기간": contest_detail.get("접수기간", "미제공"),
                    "문의처": contest_detail.get("문의처", "미제공"),
                    "공모전 링크": link,
                    "팜플렛 이미지": image,
                })

            except Exception as e:
                print(f"[공모전 파싱 오류] {e}")

    except Exception as e:
        print(f"[전체 크롤링 오류] {e}")

    return contests

def parse_contest_detail_allforyoung(detail_url: str) -> dict:
    """
    요즘것들 사이트의 공모전 상세 페이지에서 세부 정보를 추출합니다.
    INPUT: 상세 페이지 URL
    OUTPUT: {주최측, 대상, 접수기간, 문의처, ...}
    """
    info = {}
    try:
        resp = requests.get(detail_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 예시: 실제 HTML 구조 따라 수정
        info['주최측'] = soup.select_one('.company-name').get_text(strip=True) if soup.select_one('.company-name') else "미제공"
        info['대상'] = soup.select_one('.target').get_text(strip=True) if soup.select_one('.target') else "미제공"
        info['접수기간'] = soup.select_one('.period').get_text(strip=True) if soup.select_one('.period') else "미제공"
        info['문의처'] = soup.select_one('.contact').get_text(strip=True) if soup.select_one('.contact') else "미제공"
        # 실제 각 정보의 class/id는 F12로 확인하고 selector 수정해야 함

    except Exception as e:
        print(f"[상세페이지 파싱 오류] {detail_url} | {e}")

    return info
