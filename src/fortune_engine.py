#!/usr/bin/env python3
"""
麦门抽签 - 运势引擎
Fortune Engine for McDonald's Fortune-Telling Ordering Skill

This module handles:
1. Budget-based random meal matching (following McDonald's official combo rules)
2. Fortune generation based on selected meals
3. Formatted output for display
"""

import json
import random
import os
from itertools import combinations
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class FortuneResult:
    """Result of a single fortune draw."""
    fortune_id: str
    combo_name: str
    items: list  # [{"name": str, "code": str, "price": float, "category": str}]
    total_price: float
    budget: float
    fortune_name: str
    auspicious: list
    inauspicious: list
    wealth_stars: int
    love_stars: int
    career_stars: int
    lucky_color: str
    lucky_number: int
    reading: str
    extra_fortune: str
    available_coupons: list = field(default_factory=list)


class FortuneEngine:
    """Core engine for McDonald's fortune-telling ordering."""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir
        self.meal_catalog = self._load_json("meal_catalog.json")
        self.fortune_templates = self._load_json("fortune_templates.json")
        self._build_name_lookup()

    def _load_json(self, filename: str) -> dict:
        path = os.path.join(self.data_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_name_lookup(self):
        self.name_to_info = {}
        for category in ["burgers", "snacks", "drinks", "desserts", "combos"]:
            for name, info in self.meal_catalog.get(category, {}).items():
                info["name"] = name
                self.name_to_info[name] = info

    def draw(self, budget: float, store_code: str = None, available_coupons: list = None) -> FortuneResult:
        """
        Draw a fortune: randomly select meals within budget and generate fortune.

        Args:
            budget: User's budget in yuan (e.g., 30.0)
            store_code: McDonald's store code (for reference)
            available_coupons: List of available coupon names

        Returns:
            FortuneResult with meal combo and fortune reading
        """
        items = self._match_meals(budget)
        total_price = sum(item["price"] for item in items)
        fortune = self._generate_fortune(items, budget, total_price)

        result = FortuneResult(
            fortune_id=self._generate_fortune_id(),
            combo_name=self._name_combo(items),
            items=items,
            total_price=total_price,
            budget=budget,
            fortune_name=fortune["fortune_name"],
            auspicious=fortune["auspicious"],
            inauspicious=fortune["inauspicious"],
            wealth_stars=fortune["wealth"],
            love_stars=fortune["love"],
            career_stars=fortune["career"],
            lucky_color=fortune["lucky_color"],
            lucky_number=fortune["lucky_number"],
            reading=fortune["reading"],
            extra_fortune=self._pick_extra_fortune(),
            available_coupons=available_coupons or [],
        )
        return result

    def _match_meals(self, budget: float) -> list:
        """
        Select meals within budget, following McDonald's official combo rules:
        - <20: snacks only
        - 20-30: burger+snack or burger+drink
        - 30-40: burger+fries/snack+drink
        - 40-50: burger+fries+snack+drink
        - 50+: rich combo
        """
        if budget < 20:
            return self._pick_snacks_only(budget)
        elif budget < 30:
            return self._pick_burger_plus_one(budget)
        elif budget < 40:
            return self._pick_burger_snack_drink(budget)
        elif budget < 50:
            return self._pick_full_combo(budget)
        else:
            return self._pick_rich_combo(budget)

    def _pick_snacks_only(self, budget: float) -> list:
        """<20 yuan: pick 1-2 snacks within budget."""
        snacks = list(self.meal_catalog["snacks"].items())
        random.shuffle(snacks)
        picked = []
        remaining = budget
        for _ in range(2):
            available = [(n, i) for n, i in snacks if i["price"] <= remaining and n not in [p["name"] for p in picked]]
            if available:
                name, info = random.choice(available)
                picked.append(self._make_item(name, info))
                remaining -= info["price"]
        if not picked:
            picked.append(self._make_item("苹果片", self.meal_catalog["snacks"]["苹果片"]))
        return picked

    def _pick_burger_plus_one(self, budget: float) -> list:
        """20-30 yuan: burger + snack or burger + drink."""
        burgers = list(self.meal_catalog["burgers"].items())
        random.shuffle(burgers)
        for bname, binfo in burgers:
            remaining = budget - binfo["price"]
            if remaining < 5:
                continue
            sides = []
            for sname, sinfo in self.meal_catalog["snacks"].items():
                if sinfo["price"] <= remaining:
                    sides.append((sname, sinfo))
            for dname, dinfo in self.meal_catalog["drinks"].items():
                if dinfo["price"] <= remaining:
                    sides.append((dname, dinfo))
            for dname, dinfo in self.meal_catalog["desserts"].items():
                if dinfo["price"] <= remaining:
                    sides.append((dname, dinfo))
            if sides:
                sname, sinfo = random.choice(sides)
                return [self._make_item(bname, binfo), self._make_item(sname, sinfo)]
        return self._pick_snacks_only(budget)

    def _pick_burger_snack_drink(self, budget: float) -> list:
        """30-40 yuan: burger + snack + drink (or combo)."""
        combos = [(n, i) for n, i in self.meal_catalog["combos"].items() if i["price"] <= budget]
        if combos and random.random() < 0.4:
            name, info = random.choice(combos)
            return [self._make_item(name, info)]
        burgers = list(self.meal_catalog["burgers"].items())
        random.shuffle(burgers)
        for bname, binfo in burgers:
            remaining = budget - binfo["price"]
            if remaining < 15:
                continue
            snack_options = [(n, i) for n, i in self.meal_catalog["snacks"].items() if i["price"] < remaining - 7]
            drink_options = [(n, i) for n, i in self.meal_catalog["drinks"].items() if i["price"] <= remaining - 7]
            if snack_options and drink_options:
                sname, sinfo = random.choice(snack_options)
                remaining2 = remaining - sinfo["price"]
                drink_candidates = [(n, i) for n, i in drink_options if i["price"] <= remaining2]
                if drink_candidates:
                    dname, dinfo = random.choice(drink_candidates)
                    return [
                        self._make_item(bname, binfo),
                        self._make_item(sname, sinfo),
                        self._make_item(dname, dinfo),
                    ]
        return self._pick_burger_plus_one(budget)

    def _pick_full_combo(self, budget: float) -> list:
        """40-50 yuan: burger + fries + snack + drink."""
        combos = [(n, i) for n, i in self.meal_catalog["combos"].items() if i["price"] <= budget]
        if combos and random.random() < 0.5:
            name, info = random.choice(combos)
            items = [self._make_item(name, info)]
            remaining = budget - info["price"]
            extras = []
            for sname, sinfo in self.meal_catalog["desserts"].items():
                if sinfo["price"] <= remaining:
                    extras.append((sname, sinfo))
            for sname, sinfo in self.meal_catalog["snacks"].items():
                if sinfo["price"] <= remaining:
                    extras.append((sname, sinfo))
            if extras:
                ename, einfo = random.choice(extras)
                items.append(self._make_item(ename, einfo))
            return items
        return self._pick_burger_snack_drink(budget)

    def _pick_rich_combo(self, budget: float) -> list:
        """>50 yuan: rich combo, prefer non-repeating items."""
        combos = [(n, i) for n, i in self.meal_catalog["combos"].items() if i["price"] <= budget]
        if combos:
            name, info = random.choice(combos)
            items = [self._make_item(name, info)]
            remaining = budget - info["price"]
            extras_pool = []
            for sname, sinfo in self.meal_catalog["snacks"].items():
                if sinfo["price"] <= remaining:
                    extras_pool.append((sname, sinfo))
            for dname, dinfo in self.meal_catalog["desserts"].items():
                if dinfo["price"] <= remaining:
                    extras_pool.append((dname, dinfo))
            for dname, dinfo in self.meal_catalog["drinks"].items():
                if dinfo["price"] <= remaining:
                    extras_pool.append((dname, dinfo))
            random.shuffle(extras_pool)
            for ename, einfo in extras_pool:
                if einfo["price"] <= remaining:
                    items.append(self._make_item(ename, einfo))
                    remaining -= einfo["price"]
                if len(items) >= 4:
                    break
            return items
        return self._pick_full_combo(budget)

    def _make_item(self, name: str, info: dict) -> dict:
        return {
            "name": name,
            "code": info["code"],
            "price": info["price"],
            "category": info.get("category", "unknown"),
        }

    def _generate_fortune(self, items: list, budget: float, total_price: float) -> dict:
        """Generate fortune reading based on selected items."""
        templates = self.fortune_templates
        primary = items[0]
        primary_name = primary["name"]

        fortune = None
        for category in ["burgers", "snacks", "drinks", "desserts", "combos"]:
            if primary_name in templates.get(category, {}):
                fortune = templates[category][primary_name].copy()
                break

        if fortune is None:
            fortune = {
                "fortune_name": "麦门随心签",
                "auspicious": ["随心", "自在", "不设限"],
                "inauspicious": ["纠结", "患得患失"],
                "wealth": 3,
                "love": 3,
                "career": 3,
                "lucky_color": "麦门金",
                "lucky_number": random.randint(0, 9),
                "reading": "今日你与麦门有缘，随心搭配，随遇而安。运势不在签文里，在每一口咬下里。",
            }

        wealth = min(5, fortune["wealth"] + sum(1 for i in items if i["category"] in ("snack", "burger")))
        love = min(5, fortune["love"] + sum(1 for i in items if i["category"] in ("dessert", "drink")))
        career = min(5, fortune["career"] + sum(1 for i in items if i["category"] in ("burger", "combo")))
        fortune["wealth"] = wealth
        fortune["love"] = love
        fortune["career"] = career

        return fortune

    def _name_combo(self, items: list) -> str:
        if len(items) == 1:
            return items[0]["name"]
        return " + ".join(i["name"] for i in items)

    def _generate_fortune_id(self) -> str:
        signs = ["上上签", "上签", "中上签", "中签", "中下签", "下签"]
        weight = [1, 3, 4, 3, 2, 1]
        sign = random.choices(signs, weights=weight)[0]
        num = random.randint(1, 999)
        return f"{sign} 第{num:03d}号"

    def _pick_extra_fortune(self) -> str:
        return random.choice(self.fortune_templates.get("extra_fortunes", ["麦门庇佑"]))

    def format_result(self, result: FortuneResult) -> str:
        """Format the fortune result as a decorative text card."""
        def stars(n):
            return "*" * n + "." * (5 - n)

        lines = []
        lines.append("=" * 52)
        lines.append("        麦门今日运势 - 抽签结果")
        lines.append("=" * 52)
        lines.append("")
        lines.append(f"  麦签号: {result.fortune_id}")
        lines.append(f"  签名套餐: {result.combo_name}")
        lines.append("")
        lines.append("  --- 套餐明细 ---")
        for item in result.items:
            lines.append(f"    {item['name']:20s}  {item['price']:>6.1f}")
        lines.append(f"    {'':20s}  ------")
        lines.append(f"    {'合计':20s}  {result.total_price:>6.1f}")
        lines.append(f"  预算: {result.budget:.1f} 元")
        if result.budget >= result.total_price:
            lines.append(f"  实付: {result.total_price:.1f} 元 (省 {result.budget - result.total_price:.1f} 元)")
        else:
            lines.append(f"  实付: {result.total_price:.1f} 元 (超 {result.total_price - result.budget:.1f} 元)")
        lines.append("")
        lines.append("  --- 运势解读 ---")
        lines.append(f"  今日宜: {'  '.join(result.auspicious)}")
        lines.append(f"  今日忌: {'  '.join(result.inauspicious)}")
        lines.append(f"  财运指数: {stars(result.wealth_stars)}")
        lines.append(f"  桃花运:   {stars(result.love_stars)}")
        lines.append(f"  事业运:   {stars(result.career_stars)}")
        lines.append(f"  幸运色:   {result.lucky_color}")
        lines.append(f"  幸运数字: {result.lucky_number}")
        lines.append("")
        lines.append("  --- 麦签解语 ---")
        for i in range(0, len(result.reading), 46):
            lines.append(f"  {result.reading[i:i+46]}")
        lines.append("")
        lines.append(f"  [{result.extra_fortune}]")
        if result.available_coupons:
            lines.append("")
            lines.append("  --- 可用优惠券 ---")
            for c in result.available_coupons:
                lines.append(f"    - {c}")
        lines.append("")
        lines.append("=" * 52)
        return "\n".join(lines)


def main():
    import sys
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
    engine = FortuneEngine()
    result = engine.draw(budget)
    print(engine.format_result(result))


if __name__ == "__main__":
    main()
