from typing import TypedDict, Literal

class AgingReport(TypedDict):
    """老朽化レポートの構造定義"""
    crack_level: Literal[0, 1, 2, 3, 4, 5]  # ひび割れレベル（0-5）
    danger_level: Literal["低", "中", "高"]  # 危険度
    reasons: list[str]  # 問題点リスト（最大2つ）