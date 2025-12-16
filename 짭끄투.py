import random
import time
import sys
import re # 'r' was likely a typo for 're'

# 간단한 내장 한국어 단어 목록 (데모용)
# 실제로는 사용자 사전 업로드를 권장합니다.
DEFAULT_WORDS = [
    "사과","과일","일기","기도","도서","서랍","압력","력사","사랑","랑귀","귀가","가방","방앗간","간식","공구","식샤를합시다","카섹스","가족관계등록등에관한법률", "개를훔치는완벽한방법", "기교소녀는상처받지않아", "나는친구가적다", "내여동생이이렇게귀여울리가없어", "노랑뒤날개수염밤나비",
    "다이오드트랜지스터논리회로", "대기지구화학이상마당", "라틴아메리카통합연합", "리제로부터시작하는이세계생활", "마법소녀마도카마기카", "무엇이든가능하다옳", "비단꼭지거미불가사리",
    "사쿠라코씨의발밑에는시체가묻혀있다", "산타는교복을입을수밖에없어", "서울부산간고속국도", "섹스투스엠피리쿠스", "스리랑카민주사회주의공화국", "아이돌마스터신데렐라걸즈스타라이트스테이지", "어떤마술의금서목록",
    "역시내청춘러브코메디는잘못됐다","늣치","윰댕","을증배당이자소득세", "이것이리얼여자캐릭터가생각대로그려지는책", "인민민주주의독재정권", "자라투스트라는이렇게말했다", "자라투스트라는이렇게먹었다", "장난을잘치는타카기양", "장거리벨트컨베이어", "전성의케이에이에프케이에이술사", "정글은언제나맑음뒤흐림",
    "지금남편이무슨말을하는거지", "책상다리황새두렁넘기", "택배는이렇게탄생했다", "화순대곡리출토청동유물","까마귀궁정고등학교말괄량이오르피아","권가을","박정권",
    "식탁","탁구","구두","두부","꾼둑","부채","채소","소설","설탕","탕수육","육개장","장미","미술","술잔","섹스엔던전","이멋진세계의폭염을","그녀의플래그가꺾이면",
    "섹스엔던전우리집지하의에이치던전레벨의던전이출현했다","다메섹","믈ㅅ셕","션믈","도망쳐ㅅㅂ","셕듁화","장징궈","궈이","이렁셩","셩셕","다다이즘","즘승","기아타이거즈",
    "잔디","디딤돌","돌고래","래퍼","퍼즐","즐거움","움막","막걸리","리본","본능","능력","력대","공민영","공공기관","관동","관서","관종","종로구",
    "대문","문고리","리더","둑지꽈","더덕","덕후","후추","추억","억양","양말","말풍선","선물","물병","병원","숲의아이","이세계에서돌아온아저씨가부성스킬로파더콤아가씨들을헤롱헤롱",
    "원숭이","이불","불꽃","선생니","꽃병","병아리","리모컨","컨테이너","너구리","리어카","설민지","카메라","라디오","두정역","두개골","두부","두부외상",
    "오징어","어항","항공","꽝꽈","공책","님아그강을건너지마오","책상","상어","어서오세요","요리","리그","그림","임무","무지개","아가씨돌보기영애들이다니는명문학교에서제일가는아가씨생활력없음를남몰래돕는시중담당이되었습니다",
    "개새끼","끼발산","산노미야역","역삼역","역곡역","님아그버튼을누르지마오","역위탁가공무역","역시내청춘러브코메디는잘못됐다","다른사람과하는러브코미디는용서하지않을거니까",
    "까나리", "컴퓨터", "프로그래밍", "코딩", "인공지능", "데이터", "분석", "학습", "머신러닝","지독하게끌어안고지독하게키스하고", "알고리즘","감자왕","아이돌마스터제노그라시아","아이스스파클링워터드링크",
    "파이썬","탕아의샘은마르지않아","자바", "씨쁠쁠", "모바일", "개발", "서버", "클라이언트", "네트워크", "보안","아픈건싫으니까방어력에올인하려고합니다",
    "클라우드", "빅데이터", "블록체인", "가상현실", "증강현실", "로봇", "드론", "스마트폰", "앱","김원섭","섭식","김도영","입맛","맛자욱",
    "기술", "혁신", "미래", "과학", "공학", "수학", "물리", "화학", "생물", "지구과학", "역사","라라랜드","나경원",
    "지리", "사회", "윤리", "도덕", "국어", "영어", "음악", "미술", "체육", "한자", "일본어","이명박","박근혜","귀주대첩",
    "중국어", "불어", "독어", "스페인어", "아랍어", "러시아어", "베트남어", "태국어", "몽골어","욱일기","스리랑카민주사회주의인민공화국",
    "터키어", "인도네시아어", "말레이시아어", "필리핀어", "힌디어", "뱅골어", "우르두어", "페르시아어","북조선",
    "그리스어", "라틴어", "히브리어", "아르메니아어", "조지아어", "아이슬란드어", "노르웨이어", "스웨덴어","오타루","아사히카와","쿠시로",
    "핀란드어", "덴마크어", "네덜란드어", "벨기에어", "스위스어", "오스트리아어", "폴란드어", "체코어","나요로","나요로시","유바리","아사히카와시",
    "슬로바키아어", "헝가리어", "루마니아어", "불가리아어", "세르비아어", "크로아티아어", "슬로베니아어",
    "보스니아어", "알바니아어", "마케도니아어", "리투아니아어", "라트비아어", "에스토니아어", "우크라이나어",
    "벨라루스어", "몰도바어", "카자흐어", "우즈베크어", "키르기스어", "타지크어", "투르크멘어", "아제르바이잔어",
    "아프가니스탄어", "파키스탄어", "방글라데시어", "스리랑카어", "네팔어", "부탄어", "미얀마어", "캄보디아어",
    "라오스어", "싱가포르어", "브루나이어", "동티모르어", "파푸아뉴기니어", "피지어", "사모아어", "통가어","노인",
    "바누아투어", "솔로몬제도어", "키리바시어", "나우루어", "마셜제도어", "미크로네시아어", "팔라우어","쁠라쓰","쓰바씨보",
    "투발루어", "뉴질랜드어", "오스트레일리아어", "남아프리카공화국어", "이집트어", "수단어", "리비아어","보지","보수","보수주의",
    "튀니지어", "알제리어", "모로코어", "모리타니어도", "말리어", "니제르어", "차드어", "에리트레아어","혜자","혜민","오사카부",
    "지부티어", "소말리아어", "에티오피아어", "케냐어", "우간다어", "르완다어", "부룬디어", "탄자니아어","혜경궁","궁전",
    "콩고어", "앙골라어", "잠비아어", "짐바브웨어", "말라위어", "모잠비크어", "마다가스카르어", "코모로어","간사이국제공항",
    "세이셸어", "모리셔스어", "가나어", "토고어", "베냉어", "나이지리아어", "카메룬어", "중앙아프리카공화국어","각산역",
    "적도기니어", "가봉어", "상투메프린시페어", "시에라리온어", "라이베리아어", "기니어", "기니비사우어",
    "감비아어", "세네갈어", "카보베르데어", "말리어", "부르키나파소어", "코트디부아르어","한신타이거즈","니시노미야시","효고현",
    "라이트노벨", "이세계", "판타지", "던전", "마법", "용사", "악당", "소꿉친구", "여주인공", "남주인공",
    "치트", "능력자", "스킬", "레벨업", "상태창", "회귀", "전생", "환생", "먼치킨", "성좌",
    "시스템", "게임판타지", "현대판타지", "무협", "회귀물", "빙의", "책빙의", "겜판소", "아카데미물","나와그녀와그녀와그녀",
    "나와그녀와그녀와그녀의건전하지못한관계","가끔씩툭하고러시아어로부끄러워하는옆자리의아랴양", "가데스", "가든로스트", "가면을쓴소녀",
    "가미오로시", "가상영역의엘리시온", "가짜이야기", "가짜이야기상", "가짜이야기하", "가챠를돌려동료를늘리고최강의미소녀군단을만들자", "가출천사육성계약각"]

# 한글만 사용하도록 간단 필터
HANGUL_REGEX = re.compile(r'^[가-힣]+$')

def is_korean_word(w: str) -> bool:
    return bool(HANGUL_REGEX.match(w))

def last_char(word: str) -> str:
    return word[-1]

def first_char(word: str) -> str:
    return word[0]

def normalize_word(w: str) -> str:
    return w.strip()

# Define equivalence groups for Korean initial sound rule (두음법칙)
# Characters within the same set are considered equivalent for matching purposes in the game.
DU_EUM_EQUIVALENCE_GROUPS = [
    {'라', '나', '아'}, # '라' -> '나' or '아'. Also '나' can be equivalent to '아' for games.
    {'랴', '야'},
    {'려', '여', '녀'}, # '려' -> '여', '녀' -> '여'. All three are equivalent.
    {'례', '예'},
    {'료', '요', '뇨'}, # '료' -> '요', '뇨' -> '요'. All three are equivalent.
    {'류', '유', '뉴'}, # '류' -> '유', '뉴' -> '유'. All three are equivalent.
    {'리', '이', '니'}, # '리' -> '이', '니' -> '이'. All three are equivalent.
]

def are_du_eum_equivalent(char1: str, char2: str) -> bool:
    """
    Checks if two Korean characters are equivalent according to the simplified
    두음법칙 for a word chain game.
    """
    if char1 == char2:
        return True
    for group in DU_EUM_EQUIVALENCE_GROUPS:
        if char1 in group and char2 in group:
            return True
    return False

def load_dictionary(custom_list=None):
    # 사용자 제공 리스트가 없으면 기본 사전 사용
    words = set(DEFAULT_WORDS if custom_list is None else custom_list)
    # 한글만 추려서 길이 1 단어 제외
    words = {normalize_word(w) for w in words if is_korean_word(w) and len(w) >= 2}
    # 시작 글자 인덱스 구축
    index = {}
    for w in words:
        index.setdefault(first_char(w), set()).add(w)
    return words, index

def pick_bot_word(required_start: str, unused_words_index: dict, used: set):
    # Find all characters equivalent to required_start, including itself
    potential_start_chars_for_bot_search = {required_start}
    for group in DU_EUM_EQUIVALENCE_GROUPS:
        if required_start in group:
            potential_start_chars_for_bot_search.update(group)
            break # Assume a character belongs to only one 'primary' group for lookup

    candidates = set()
    for char_variant in potential_start_chars_for_bot_search:
        candidates.update(unused_words_index.get(char_variant, set()))

    pool = [w for w in candidates if w not in used]
    if not pool:
        return None

    # Bot's scoring logic: Prioritize words whose last char allows many next options for the player (or bot itself)
    scored = []
    for w in pool:
        nxt = last_char(w)

        # Calculate how many unused words could follow 'w's last character 'nxt', considering du-eum
        next_potential_start_chars_for_next_turn = {nxt}
        for group in DU_EUM_EQUIVALENCE_GROUPS:
            if nxt in group:
                next_potential_start_chars_for_next_turn.update(group)
                break

        next_pool_size = 0
        for next_char_variant in next_potential_start_chars_for_next_turn:
            # Count only truly unused words for the next turn's possibilities
            for word_candidate in unused_words_index.get(next_char_variant, set()):
                if word_candidate not in used:
                    next_pool_size += 1

        scored.append((next_pool_size, w))

    scored.sort(reverse=True)
    top_k = [w for _, w in scored[:5]] if len(scored) >= 5 else [w for _, w in scored]
    return random.choice(top_k)

class WordChainGame:
    def __init__(self, dictionary_words=None, time_limit_sec=None):
        self.words, self.index = load_dictionary(dictionary_words)
        self.time_limit_sec = time_limit_sec
        self.used = set()
        self.turn = "player"  # 'player' 또는 'bot'
        self.current_required_start = None
        self.player_score = 0
        self.bot_score = 0
        self.game_over = False
        self.start_time = None

    def _reset_game(self):
        self.used = set()
        self.turn = "player"
        self.current_required_start = None
        self.player_score = 0
        self.bot_score = 0
        self.game_over = False
        self.start_time = None

    def _can_use_word(self, w: str) -> (bool, str):
        w = normalize_word(w)
        if not is_korean_word(w):
            return False, "한글 단어만 입력해주세요."
        if len(w) < 2:
            return False, "두 글자 이상의 단어를 입력해주세요."
        if w not in self.words:
            return False, f"'{w}'은(는) 사전에 없는 단어입니다."
        if w in self.used:
            return False, f"'{w}'은(는) 이미 사용된 단어입니다."

        # Check if the word matches the required starting character, considering du-eum beopchik
        if self.current_required_start:
            if not are_du_eum_equivalent(first_char(w), self.current_required_start):
                return False, f"'{self.current_required_start}'(으)로 시작하거나 두음법칙에 해당하는 단어를 입력해야 합니다."

        return True, "유효함"

    def _process_player_turn(self):
        if self.time_limit_sec and (time.time() - self.start_time > self.time_limit_sec):
            print("시간 초과! 아쉽게도 게임 오버입니다.")
            self.game_over = True
            return

        prompt = f"\n[플레이어 차례 - 점수: {self.player_score}]"
        if self.current_required_start:
            prompt += f" '{self.current_required_start}'(으)로 시작하는 단어를 입력하세요: "
        else:
            prompt += " 아무 단어나 입력하세요: "

        player_word = input(prompt).strip()

        is_valid, message = self._can_use_word(player_word)

        if is_valid:
            print(f"플레이어: {player_word}")
            self.used.add(player_word)
            self.current_required_start = last_char(player_word)
            # Apply new scoring rules
            word_length = len(player_word)
            if 2 <= word_length <= 8:
                self.player_score += 1
            elif 9 <= word_length <= 11:
                self.player_score += 2
            elif 12 <= word_length <= 15:
                self.player_score += 4
            elif word_length >= 16:
                self.player_score += 8
            self.turn = "bot"
        else:
            print(f"오류: {message}")
            self.game_over = True # 플레이어가 틀리면 게임 오버
            print("잘못된 단어를 입력하여 게임이 종료됩니다.")

    def _process_bot_turn(self):
        print(f"\n[봇 차례 - 점수: {self.bot_score}]")
        bot_word = pick_bot_word(self.current_required_start, self.index, self.used)

        if bot_word:
            print(f"봇: {bot_word}")
            self.used.add(bot_word)
            self.current_required_start = last_char(bot_word)
            # Apply new scoring rules
            word_length = len(bot_word)
            if 2 <= word_length <= 8:
                self.bot_score += 1
            elif 9 <= word_length <= 11:
                self.bot_score += 2
            elif 12 <= word_length <= 15:
                self.player_score += 4
            elif word_length >= 16:
                self.bot_score += 8
            self.turn = "player"
        else:
            print(f"봇이 '{self.current_required_start}'(으)로 시작하는 단어를 찾지 못했습니다. 플레이어 승리!")
            self.game_over = True

    def play(self):
        self._reset_game()
        print("=" * 30)
        print("  끝말잇기 게임을 시작합니다!")
        print("=" * 30)
        print("규칙")
        print("1. 두 글자 이상의 한글 단어만 입력할 수 있습니다.")
        print("2. 이미 사용된 단어는 사용할 수 없습니다.")
        print("3. 이전 단어의 마지막 글자로 시작하는 단어를 입력해야 합니다.")
        print("4. 두음법칙이 적용됩니다. (예: '리'로 끝나면 '이'나 '니'로 시작하는 단어도 가능)")
        print("5. 단어 길이에 따라 점수가 다릅니다: 2~8글자 1점, 9~11글자 2점, 12~15글자 4점, 16글자 이상 8점.")
        if self.time_limit_sec:
            print(f"6. 한 턴당 {self.time_limit_sec}초 안에 입력해야 합니다.")
        print("게임을 종료하려면 잘못된 단어를 입력하거나, 단어를 찾지 못하면 됩니다.")
        print("-" * 30)

        self.start_time = time.time()

        # Choose a random starting word if it's the very first turn
        if not self.current_required_start:
            initial_word_candidates = [w for w in self.words if w not in self.used and len(w) >= 2]
            if not initial_word_candidates:
                print("사전에 시작할 단어가 없습니다. 게임을 시작할 수 없습니다.")
                self.game_over = True
                return

            # Pick an initial word that allows for follow-ups (score it like the bot)
            scored_initial_words = []
            for w in initial_word_candidates:
                nxt = last_char(w)
                next_potential_start_chars_for_next_turn = {nxt}
                for group in DU_EUM_EQUIVALENCE_GROUPS:
                    if nxt in group:
                        next_potential_start_chars_for_next_turn.update(group)
                        break
                next_pool_size = 0
                for next_char_variant in next_potential_start_chars_for_next_turn:
                    for word_candidate in self.index.get(next_char_variant, set()):
                        if word_candidate not in self.used and word_candidate != w:
                            next_pool_size += 1
                scored_initial_words.append((next_pool_size, w))

            scored_initial_words.sort(reverse=True)
            if not scored_initial_words:
                print("시작할 단어가 없거나 다음 단어를 이어갈 수 있는 단어가 없습니다.")
                self.game_over = True
                return

            # Select from top_k initial words to introduce more randomness
            top_k_initial_words = [w for _, w in scored_initial_words[:5]] if len(scored_initial_words) >= 5 else [w for _, w in scored_initial_words]
            chosen_initial_word = random.choice(top_k_initial_words)

            print(f"봇이 먼저 시작합니다: {chosen_initial_word}")
            self.used.add(chosen_initial_word)
            self.current_required_start = last_char(chosen_initial_word)
            # Apply new scoring rules for initial word
            word_length = len(chosen_initial_word)
            if 2 <= word_length <= 8:
                self.bot_score += 1
            elif 9 <= word_length <= 11:
                self.bot_score += 2
            elif word_length >= 12:
                self.bot_score += 3
            self.turn = "player" # Bot starts, then player's turn

        while not self.game_over:
            try:
                if self.turn == "player":
                    self._process_player_turn()
                elif self.turn == "bot":
                    self._process_bot_turn()

            except EOFError: # User pressed Ctrl+D or interrupted
                print("\n게임이 강제로 종료되었습니다.")
                self.game_over = True
            except KeyboardInterrupt: # User pressed Ctrl+C
                print("\n게임이 강제로 종료되었습니다.")
                self.game_over = True

            # Check for game end condition (no more words for current_required_start) if game_over is not set by other means
            if not self.game_over and self.current_required_start:
                # Check if there are any words left for the next player to use
                possible_next_words_exist = False
                potential_next_start_chars = {self.current_required_start}
                for group in DU_EUM_EQUIVALENCE_GROUPS:
                    if self.current_required_start in group:
                        potential_next_start_chars.update(group)
                        break

                for char_variant in potential_next_start_chars:
                    if any(w not in self.used for w in self.index.get(char_variant, set())):
                        possible_next_words_exist = True
                        break

                if not possible_next_words_exist:
                    print(f"'{self.current_required_start}'(으)로 시작하는 더 이상 사용할 수 있는 단어가 없습니다!")
                    if self.turn == "player": # If bot just played and no words left for player
                        print("플레이어 패배! 봇 승리!")
                        self.game_over = True
                    else: # If player just played and no words left for bot
                        print("봇 패배! 플레이어 승리!")
                        self.game_over = True

        print("\n" + "=" * 30)
        print("  게임 종료!")
        print(f"  최종 점수 - 플레이어: {self.player_score}, 봇: {self.bot_score}")
        if self.player_score > self.bot_score:
            print("  플레이어 승리!")
        elif self.bot_score > self.player_score:
            print("  봇 승리!")
        else:
            print("  무승부!")
        print("=" * 30)

        
game = WordChainGame()
game.play()