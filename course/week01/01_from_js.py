"""第 1 课：用 JavaScript 对照学 Python。

前端里你已经会的东西，在 Python 里几乎都有对应。
先跑通这一份，建立「原来就是换了层皮」的感觉。
运行：python 01_from_js.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    section("1. 变量和类型（JS: const / let）")
    speed = 80  # JS: const speed = 80
    modules = ["空调", "座椅", "充电"]  # JS: const modules = [...]
    car = {"brand": "东风", "ready": True}  # JS: { brand, ready: true }
    print("speed =", speed, type(speed))
    print("modules =", modules)
    print("car =", car)

    section("2. 函数（JS: const fn = (q) => ...）")

    def greet(name: str) -> str:
        # JS: function greet(name) { return `你好, ${name}` }
        return f"你好，{name}"

    print(greet("座舱助手"))

    section("3. 列表推导（JS: array.map / filter）")
    # JS: modules.filter(m => m !== "充电").map(m => m + "模块")
    labeled = [f"{m}模块" for m in modules if m != "充电"]
    print(labeled)

    section("4. 字典遍历（JS: Object.entries）")
    for key, value in car.items():
        print(f"{key} -> {value}")

    section("5. 空值（JS: null / undefined → Python: None）")
    answer = None
    print("有答案" if answer else "还没有检索到答案")

    section("6. 和前端接口最像的一段：处理一次问答")
    query = "玻璃起雾了"
    faq = {
        "M002": "打开前除雾键。系统会提高吹窗风量和温度。",
        "M001": "在空调面板点击 AUTO。",
    }
    hit = None
    for doc_id, text in faq.items():
        if "除雾" in text or "起雾" in query:
            hit = {"id": doc_id, "text": text}
            break
    print("query =", query)
    print("hit =", hit)

    print()
    print("跑通即可。下一份 02_search_faq.py 会用真实 CSV 做检索。")


if __name__ == "__main__":
    main()
