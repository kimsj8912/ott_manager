
"""OTT 고객/콘텐츠 관리 함수 모음"""


def register_customer(
    customers: list[dict],
    customer_id: str,
    name: str,
    age: int,
    gender: str,
    country: str,
    plan: bool,
    last_watch_title: str | None,
) -> tuple[bool, str]:
    # 고객 ID 중복 여부를 먼저 확인합니다.
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return (False, f"등록 실패: 이미 존재하는 customer_id 입니다. ({customer_id})")

    new_customer = {
        "customer_id": customer_id,
        "name": name,
        "age": age,
        "gender": gender,
        "country": country,
        "plan": plan,
        "last_watch_title": last_watch_title,
    }
    customers.append(new_customer)
    return (True, f"고객 등록 완료: {customer_id}")


def get_last_watched(customers: list[dict], customer_id: str) -> str | None:
    # 고객 목록이 비었거나 고객이 없으면 None을 반환합니다.
    if not customers:
        return None

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer["last_watch_title"]
    return None


def update_watch_history(
    customers: list[dict], customer_id: str, new_title: str | None
) -> tuple[bool, str]:
    if not customers:
        return (False, "수정 실패: 고객 데이터가 없습니다.")

    for customer in customers:
        if customer["customer_id"] == customer_id:
            old_title = customer["last_watch_title"]
            customer["last_watch_title"] = new_title
            return (
                True,
                f"시청 기록 수정 완료: {customer_id} (이전: {old_title}, 현재: {new_title})",
            )

    return (False, f"수정 실패: customer_id {customer_id} 를 찾을 수 없습니다.")


def delete_customer(customers: list[dict], customer_id: str) -> tuple[bool, str]:
    if not customers:
        return (False, "삭제 실패: 고객 데이터가 없습니다.")

    for index, customer in enumerate(customers):
        if customer["customer_id"] == customer_id:
            customers.pop(index)
            return (True, f"고객 삭제 완료: {customer_id}")

    return (False, f"삭제 실패: customer_id {customer_id} 를 찾을 수 없습니다.")


def end_movie_license(contents: list[dict], title: str, customers: list[dict]) -> tuple[bool, str]:
    if not contents:
        return (False, "제공 종료 실패: 콘텐츠 데이터가 없습니다.")

    removed = False
    for index, content in enumerate(contents):
        if content["title"] == title:
            contents.pop(index)
            removed = True
            break

    if not removed:
        return (False, f"제공 종료 실패: 제목이 {title} 인 콘텐츠가 없습니다.")

    updated_count = 0
    for customer in customers:
        if customer["last_watch_title"] == title:
            customer["last_watch_title"] = None
            updated_count += 1

    return (
        True,
        f"콘텐츠 제공 종료 완료: {title} (고객 시청기록 초기화 {updated_count}건)",
    )


def calculate_content_ranking(customers: list[dict]) -> list[tuple[str, int]]:
    # 마지막 시청 기록이 None 인 고객은 집계에서 제외합니다.
    ranking_dict: dict[str, int] = {}

    for customer in customers:
        title = customer["last_watch_title"]
        if title is None:
            continue
        ranking_dict[title] = ranking_dict.get(title, 0) + 1

    # (콘텐츠 제목, 시청 수) 튜플 리스트를 시청 수 기준 내림차순으로 정렬합니다.
    ranking: list[tuple[str, int]] = sorted(
        ranking_dict.items(), key=lambda item: item[1], reverse=True
    )
    return ranking


def print_content_ranking(ranking: list[tuple[str, int]]) -> str:
    # 직접 print 하지 않고, 여러 줄 문자열을 만들어 반환합니다.
    if not ranking:
        return "콘텐츠 순위 데이터가 없습니다."

    lines: list[str] = ["[콘텐츠 시청 순위]"]
    for order, (title, view_count) in enumerate(ranking, start=1):
        lines.append(f"{order}위 | 제목: {title} | 시청 수: {view_count}")

    return "\n".join(lines)





