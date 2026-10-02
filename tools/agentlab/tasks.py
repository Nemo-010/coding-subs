"""Eight real bug-fix tasks across three difficulty bands. Each fails before the fix
and passes after it; the file content is the ONLY thing the agent gets."""
TASKS = {}

def T(tid, diff, note, files, test):
    TASKS[tid] = {"diff": diff, "note": note, "files": files, "test": test}

RUNNER = '''import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
'''

T("e1_range", "easy", "off-by-one in a range endpoint",
  {"src/ranges.py": '''def inclusive_range(a, b):
    """All integers from a to b, inclusive."""
    return list(range(a, b))
'''},
  RUNNER + '''from ranges import inclusive_range
def test():
    assert inclusive_range(1, 5) == [1,2,3,4,5], inclusive_range(1,5)
    assert inclusive_range(3, 3) == [3], inclusive_range(3,3)
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL inclusive_range:", e); sys.exit(1)
''')

T("e2_discount", "easy", "strict inequality where inclusive is meant",
  {"src/pricing.py": '''def apply_discount(price, pct):
    """A discount of pct percent, clamped so the result is never below 0."""
    if price <= 0:
        return 0
    out = price * (1 - pct)
    return max(out, 0)
'''},
  RUNNER + '''from pricing import apply_discount
def test():
    assert apply_discount(100, 100) == 0, apply_discount(100, 100)
    assert apply_discount(200, 50) == 100, apply_discount(200, 50)
    assert apply_discount(0, 50) == 0, apply_discount(0, 50)
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL apply_discount:", e); sys.exit(1)
''')

T("m1_default", "medium", "mutable default argument shared across calls",
  {"src/cart.py": '''def add_item(item, cart=[]):
    """Append item to cart and return the cart."""
    cart.append(item)
    return cart
'''},
  RUNNER + '''from cart import add_item
def test():
    a = add_item("apple")
    b = add_item("pear")
    assert a == ["apple"], a
    assert b == ["pear"], b
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL add_item:", e); sys.exit(1)
''')

T("m2_available", "medium", "reservation checked against stock instead of free stock",
  {"src/inventory.py": '''class Inventory:
    def __init__(self):
        self.stock = {}
        self.reserved = {}
    def receive(self, sku, qty):
        self.stock[sku] = self.stock.get(sku, 0) + qty
        return self.stock[sku]
    def reserve(self, sku, qty):
        if qty > self.stock.get(sku, 0):
            raise ValueError("insufficient")
        self.reserved[sku] = self.reserved.get(sku, 0) + qty
        return self.reserved[sku]
    def available(self, sku):
        return self.stock.get(sku, 0) - self.reserved.get(sku, 0)
'''},
  RUNNER + '''from inventory import Inventory
def test():
    i = Inventory(); i.receive("A", 10); i.reserve("A", 4)
    try:
        i.reserve("A", 7)
    except ValueError:
        pass
    else:
        raise AssertionError("reserving 7 with 6 free should raise")
    assert i.available("A") == 6, i.available("A")
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL reserve:", e); sys.exit(1)
''')

T("m3_tiebreak", "medium", "unstable sort loses the alphabetical tie-break",
  {"src/rank.py": '''def rank(counts, n=3):
    """The n highest-count keys, ties broken alphabetically (stable, deterministic)."""
    items = list(counts.items())
    items.sort(key=lambda kv: kv[1])
    return [k for k, _ in items[:n]]
'''},
  RUNNER + '''from rank import rank
def test():
    assert rank({"a": 1, "b": 1, "c": 1, "d": 5}, 3) == ["d", "a", "b"], rank({"a":1,"b":1,"c":1,"d":5},3)
    assert rank({"z": 2, "y": 2}, 2) == ["y", "z"], rank({"z":2,"y":2},2)
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL rank:", e); sys.exit(1)
''')

T("m4_strip", "medium", "rstrip strips a character set instead of a suffix",
  {"src/slug.py": '''def slugify(name):
    """Lowercase, spaces to hyphens, and drop a trailing '.md' if present."""
    s = name.strip().lower().replace(" ", "-")
    return s.rstrip(".md")
'''},
  RUNNER + '''from slug import slugify
def test():
    assert slugify("Hello World.md") == "hello-world", slugify("Hello World.md")
    assert slugify("Notes") == "notes", slugify("Notes")
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL slugify:", e); sys.exit(1)
''')

T("h1_twobooks", "hard", "ship must decrement both stock and reserved",
  {"src/ledger.py": '''class Ledger:
    def __init__(self):
        self.stock = {}
        self.reserved = {}
    def receive(self, sku, qty):
        self.stock[sku] = self.stock.get(sku, 0) + qty
    def reserve(self, sku, qty):
        if qty > self.stock.get(sku, 0) - self.reserved.get(sku, 0):
            raise ValueError("insufficient")
        self.reserved[sku] = self.reserved.get(sku, 0) + qty
    def ship(self, sku, qty):
        if qty > self.reserved.get(sku, 0):
            raise ValueError("not reserved")
        self.reserved[sku] -= qty
    def available(self, sku):
        return self.stock.get(sku, 0) - self.reserved.get(sku, 0)
'''},
  RUNNER + '''from ledger import Ledger
def test():
    l = Ledger(); l.receive("A", 10); l.reserve("A", 4); l.ship("A", 3)
    assert l.stock["A"] == 7, l.stock["A"]
    assert l.reserved["A"] == 1, l.reserved["A"]
    assert l.available("A") == 6, l.available("A")
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL ship:", e); sys.exit(1)
''')

T("h2_cache", "hard", "cached value not invalidated when the input changes",
  {"src/config.py": '''class Config:
    def __init__(self, values):
        self.values = values
        self._cache = None
    def get(self, key, default=None):
        if self._cache is None:
            self._cache = {}
            for k, v in self.values.items():
                self._cache[k] = v
        return self._cache.get(key, default)
    def set(self, key, value):
        self.values[key] = value
'''},
  RUNNER + '''from config import Config
def test():
    c = Config({"a": 1})
    assert c.get("a") == 1, c.get("a")
    c.set("a", 2)
    assert c.get("a") == 2, c.get("a")
    c.set("b", 9)
    assert c.get("b") == 9, c.get("b")
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL config:", e); sys.exit(1)
''')

if __name__ == "__main__":
    print(f"{len(TASKS)} tasks")
    for t, d in TASKS.items():
        print(f"  {d['diff']:6} {t:12} {d['note']}")
