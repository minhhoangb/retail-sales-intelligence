"""Independent CSV baseline. Optionally compare native Power BI query results."""
import argparse
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path


def divide(numerator, denominator):
    return None if numerator is None or not denominator else numerator / denominator


def metrics(rows):
    if not rows:
        return {name: (Decimal(0) if name == "Loss Lines" else None) for name in (
            "Total Sales", "Total Profit", "Total Orders", "Total Quantity", "Line Items",
            "Profit Margin", "Average Order Value", "Loss Lines", "Loss Line Rate")}
    sales = sum(Decimal(row["Sales"]) for row in rows)
    profit = sum(Decimal(row["Profit"]) for row in rows)
    orders = Decimal(len({row["Order ID"] for row in rows}))
    loss = Decimal(sum(Decimal(row["Profit"]) < 0 for row in rows))
    return {"Total Sales": sales, "Total Profit": profit, "Total Orders": orders,
            "Total Quantity": sum(Decimal(row["Quantity"]) for row in rows),
            "Line Items": Decimal(len(rows)), "Profit Margin": divide(profit, sales),
            "Average Order Value": divide(sales, orders), "Loss Lines": loss,
            "Loss Line Rate": divide(loss, Decimal(len(rows)))}


CONTEXTS = [
    ("All", None, None, None, None),
    ("2017", "2017", None, None, None),
    ("2017 West Technology", "2017", None, "West", "Technology"),
    ("2014-01", "2014", "01", None, None),
    ("2015-01", "2015", "01", None, None),
    ("No rows", "2017", None, "No such region", None),
]


def select(rows, year, month, region, category):
    return [r for r in rows if (year is None or r["Order Date"][:4] == year)
            and (month is None or r["Order Date"][5:7] == month)
            and (region is None or r["Region"] == region)
            and (category is None or r["Category"] == category)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--actual", type=Path, help="JSON array of native DAX results, keyed by Context and measure names")
    args = parser.parse_args()
    root = args.root.resolve()
    source = root / "data_cleaned/superstore_clean.csv"
    raw_hash = hashlib.sha256((root / "data_raw/Sample - Superstore.csv").read_bytes()).hexdigest()
    with source.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 9993 and len(rows[0]) == 21
    assert len({r["Order ID"] for r in rows}) == 5009
    assert len({r["Order Date"][:7] for r in rows}) == 48
    assert all(len(r["Postal Code"]) == 5 for r in rows)
    assert divide(Decimal(1), Decimal(0)) is None
    assert divide(Decimal(0), Decimal(2)) == 0
    assert metrics([])["Total Sales"] is None
    actual = {}
    if args.actual:
        data = json.loads(args.actual.read_text(encoding="utf-8-sig"))
        actual = {row["Context"]: row for row in data}
    output, failures = [], []
    query_parts = []
    measure_names = None
    for label, year, month, region, category in CONTEXTS:
        result = metrics(select(rows, year, month, region, category))
        previous = metrics(select(rows, str(int(year)-1), month, region, category))["Total Sales"] if year else None
        result["Sales Previous Year"] = previous
        current = result["Total Sales"]
        result["Sales YoY %"] = None if current is None or previous is None else divide(current-previous, previous)
        if label == "All":
            assert result["Total Orders"] == 5009
            assert result["Line Items"] == 9993
            assert result["Loss Lines"] == 1870
        if label == "2014-01": assert previous is None and result["Sales YoY %"] is None
        if label == "2015-01": assert previous is not None
        for measure, expected in result.items():
            native = actual.get(label, {}).get(measure)
            status, difference = "Pending native DAX", ""
            if args.actual:
                native_decimal = None if native is None else Decimal(str(native))
                if expected is None or native_decimal is None:
                    ok = expected is native_decimal
                else:
                    diff = abs(expected-native_decimal)
                    difference = str(diff)
                    tol = Decimal("1e-8") if measure in {"Profit Margin", "Loss Line Rate", "Sales YoY %"} else Decimal("0.01") if measure in {"Total Sales", "Total Profit", "Average Order Value", "Sales Previous Year"} else Decimal(0)
                    ok = diff <= tol
                status = "PASS" if ok and label in actual and measure in actual[label] else "FAIL"
                if status == "FAIL": failures.append((label, measure, expected, native))
            output.append({"Context":label,"Measure":measure,"Expected": "BLANK" if expected is None else str(expected),"Power BI": "" if not args.actual else "BLANK" if native is None else str(native),"Absolute difference":difference,"Status":status})
        measure_names = list(result)
        filters = []
        if year: filters.append('TREATAS ( {'+year+'}, \'Calendar\'[Year] )')
        if month: filters.append('TREATAS ( {"'+year+'-'+month+'"}, \'Calendar\'[Month] )')
        if region: filters.append('TREATAS ( {"'+region+'"}, Sales[Region] )')
        if category: filters.append('TREATAS ( {"'+category+'"}, Sales[Category] )')
        row_expr = 'ROW ( "Context", "'+label+'", '+', '.join('"'+name+'", ['+name+']' for name in result)+' )'
        query_parts.append('CALCULATETABLE ( '+row_expr+', '+', '.join(filters)+' )' if filters else row_expr)
    query = "EVALUATE\nUNION (\n    " + ",\n    ".join(query_parts) + "\n)\n"
    query_path = root / "pbix/validate_kpis.dax"
    query_path.write_text(query, encoding="utf-8")
    out = root / "docs/kpi_validation.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0])); writer.writeheader(); writer.writerows(output)
    assert hashlib.sha256((root/"data_raw/Sample - Superstore.csv").read_bytes()).hexdigest() == raw_hash
    print(json.dumps({"rows":len(rows),"orders":5009,"contexts":len(CONTEXTS),"comparisons":len(output),"native_compared":bool(args.actual),"failures":len(failures)},indent=2))
    if failures:
        for item in failures: print(item)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
