from customer_functions import (
    calculate_content_ranking,
    delete_customer,
    end_movie_license,
    get_last_watched,
    print_content_ranking,
    register_customer,
    update_watch_history,
)


# 초기 고객 데이터 예시 (메모리에서 직접 관리)
customers: list[dict] = [
    {
        "customer_id": "001",
        "name": "김민지",
        "age": 29,
        "gender": "F",
        "country": "KR",
        "plan": True,
        "last_watch_title": "오징어게임",
    },
    {
        "customer_id": "002",
        "name": "이준호",
        "age": 34,
        "gender": "M",
        "country": "KR",
        "plan": True,
        "last_watch_title": "더 글로리",
    },
    {
        "customer_id": "003",
        "name": "박서연",
        "age": 26,
        "gender": "F",
        "country": "KR",
        "plan": False,
        "last_watch_title": "킹덤",
    },
    {
        "customer_id": "004",
        "name": "최민수",
        "age": 41,
        "gender": "M",
        "country": "KR",
        "plan": True,
        "last_watch_title": "무빙",
    },
]


# 초기 콘텐츠 데이터 예시 (메모리에서 직접 관리)
contents: list[dict] = [
    {"title": "오징어게임", "genre": "스릴러", "running_time": 60, "age_rating": 19},
    {"title": "더 글로리", "genre": "드라마", "running_time": 50, "age_rating": 19},
    {"title": "킹덤", "genre": "스릴러", "running_time": 45, "age_rating": 19},
    {"title": "무빙", "genre": "액션", "running_time": 55, "age_rating": 15},
]


def _normalize(value: str) -> str:
    return value.strip()


def _normalize_menu(value: str) -> str:
    return _normalize(value).upper()


def _parse_plan_input(value: str) -> bool | None:
    normalized = _normalize_menu(value)
    if normalized in {"Y", "YES", "TRUE", "T", "1"}:
        return True
    if normalized in {"N", "NO", "FALSE", "F", "0"}:
        return False
    return None


def _print_menu() -> None:
    print("\n=== OTT Manager 메뉴 ===")
    print("A. 고객 신규 가입")
    print("B. 마지막 시청 기록 조회")
    print("C. 시청 기록 업데이트")
    print("D. 고객 탈퇴")
    print("E. 제공 영화 판권 종료")
    print("F. 콘텐츠 순위 출력")
    print("G. 종료")


def main() -> None:
    print("OTT Manager CLI를 시작합니다.")
    print(f"초기 고객 수: {len(customers)}")
    print(f"초기 콘텐츠 수: {len(contents)}")

    while True:
        _print_menu()
        menu = _normalize_menu(input("메뉴를 선택하세요 (A-G): "))

        if menu == "A":
            customer_id = _normalize(input("고객 ID: "))
            name = _normalize(input("이름: "))
            age_input = _normalize(input("나이: "))
            gender = _normalize_menu(input("성별 (M/F): "))
            country = _normalize_menu(input("국가 코드 (예: KR): "))
            plan_input = _normalize(input("요금제 가입 여부 (Y/N): "))
            last_watch_title = _normalize(input("마지막 시청 제목: "))

            if not age_input.isdigit():
                print("[오류] 나이는 숫자로 입력해야 합니다.")
                continue

            plan = _parse_plan_input(plan_input)
            if plan is None:
                print("[오류] 요금제 가입 여부는 Y/N 형태로 입력해야 합니다.")
                continue

            ok, message = register_customer(
                customers,
                customer_id=customer_id,
                name=name,
                age=int(age_input),
                gender=gender,
                country=country,
                plan=plan,
                last_watch_title=last_watch_title,
            )
            print(f"[고객 신규 가입] 성공 여부: {ok}, 메시지: {message}")

        elif menu == "B":
            customer_id = _normalize(input("조회할 고객 ID: "))
            last_title = get_last_watched(customers, customer_id)
            if last_title is None:
                print(f"[마지막 시청 기록 조회] 고객 ID {customer_id}를 찾을 수 없습니다.")
            else:
                print(f"[마지막 시청 기록 조회] 고객 ID {customer_id}, 결과: {last_title}")

        elif menu == "C":
            customer_id = _normalize(input("고객 ID: "))
            new_title = _normalize(input("새 시청 제목: "))
            ok, message = update_watch_history(customers, customer_id, new_title)
            print(f"[시청 기록 업데이트] 성공 여부: {ok}, 메시지: {message}")

        elif menu == "D":
            customer_id = _normalize(input("탈퇴할 고객 ID: "))
            ok, message = delete_customer(customers, customer_id)
            print(f"[고객 탈퇴] 성공 여부: {ok}, 메시지: {message}")

        elif menu == "E":
            title = _normalize(input("판권 종료할 콘텐츠 제목: "))
            ok, message = end_movie_license(contents, title, customers)
            print(f"[제공 영화 판권 종료] 성공 여부: {ok}, 메시지: {message}")

        elif menu == "F":
            ranking = calculate_content_ranking(customers)
            ranking_text = print_content_ranking(ranking)
            print(ranking_text)

        elif menu == "G":
            print("프로그램을 종료합니다.")
            break

        else:
            print("[오류] 유효한 메뉴 알파벳(A-G)을 입력하세요.")


if __name__ == "__main__":
    main()
