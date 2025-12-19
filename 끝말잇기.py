import pygame
import sys
import random
import csv

# -----------------------------
# CSV에서 단어 불러오기
# -----------------------------
def load_words_from_csv(filename: str) -> list[str]:
    words = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # 빈 줄 방지
                words.append(row[0].strip())
    return words

# -----------------------------
# 설정
# -----------------------------
WIDTH, HEIGHT = 900, 600
BG_COLOR = (20, 22, 28)
TEXT_COLOR = (240, 240, 240)
ACCENT_COLOR = (0, 170, 255)
ERROR_COLOR = (255, 80, 80)
OK_COLOR = (100, 220, 120)

# CSV 파일에서 단어 불러오기
KOREAN_WORDS = load_words_from_csv("words.csv")

# -----------------------------
# 유틸 함수
# -----------------------------
def pick_font():
    candidates = ["Malgun Gothic", "맑은 고딕", "Apple SD Gothic Neo", "Noto Sans CJK KR", "NanumGothic", "나눔고딕"]
    for name in candidates:
        try:
            f = pygame.font.SysFont(name, 28)
            if f:
                return name
        except:
            pass
    return None

def get_last_char(word: str) -> str:
    return word[-1] if word else ""

def is_valid_player_word(word: str, expected_start: str, used: set) -> (bool, str):
    if not word:
        return False, "단어를 입력하세요."
    if " " in word:
        return False, "공백 없이 한 단어만 입력하세요."
    if expected_start and not word.startswith(expected_start):
        return False, f"현재는 '{expected_start}'로 시작하는 단어여야 합니다."
    if word in used:
        return False, "이미 사용된 단어입니다."
    return True, ""

def cpu_choose_word(start_char: str, used: set) -> str | None:
    candidates = [w for w in KOREAN_WORDS if w.startswith(start_char) and w not in used]
    return random.choice(candidates) if candidates else None

# -----------------------------
# 이후 로직은 앞서 보여드린 Pygame 코드와 동일
# -----------------------------
