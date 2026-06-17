# Building the Power BI Dashboard

I built this dashboard from the cleaned data the Python script produces, and these are
basically my own notes from doing it. The finished file is `sales_dashboard.pbix` and
there's a screenshot of it in `charts/powerbi_dashboard.png` if you just want to see
the result.

If you want to rebuild it yourself, you'll need Power BI Desktop (it's free on the
Microsoft Store, but Windows only). Everything else is already prepared, you just point
it at `data/superstore_clean.csv`.

## Loading the data

Open Power BI Desktop and go to Get Data > Text/CSV, then pick
`data/superstore_clean.csv` and hit Load.

One thing worth checking in the Data view: make sure `Order Date` and `Ship Date` came
in as dates and the money columns (`Sales`, `Profit`, `Discount`, `Profit Margin`) came
in as decimals. Mine were fine straight away because the Python step already parses the
dates and fixes the types, so there's no need to mess around in Power Query.

## The three measures

I added these under Modeling > New measure, one at a time:

```DAX
Total Revenue = SUM(superstore_clean[Sales])
```
```DAX
Total Profit = SUM(superstore_clean[Profit])
```
```DAX
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
```

Heads up on the margin one: it shows as `0.12` at first, which threw me for a second.
That's correct, it's just not formatted. Select the measure, go to the Measure tools
tab and click the % button and it turns into 12.47%.

## The visuals

The layout I went with is three KPI cards across the top, the revenue trend underneath,
and then the product and region charts side by side at the bottom.

KPI cards: a Card visual for each measure (Revenue, Profit, Margin %). The raw numbers
have a lot of decimals, so I rounded them down to 1 place in the formatting pane to keep
it readable.

Revenue trend: a line chart with `Order Month Name` on the X axis and `Total Revenue` on
the Y. I tried `Order Date` first but it defaulted to showing just the four years, so
using the month field gives the nicer month-by-month line with the seasonal bumps.

Top 10 products: a clustered bar chart, `Product Name` on the Y axis and `Total Revenue`
on the X. By default it lists every product, which is unusable. The fix is in the
Filters pane, change the filter type on `Product Name` to Top N, set it to top 10 by
Total Revenue, and apply.

Sales by region: I used a donut chart with `Region` as the legend and `Total Revenue` as
the value. A filled map on `State` also works if you want it fancier, but the donut was
enough.

## The slicer

I dropped in a Slicer visual on `Category`. Clicking a category filters the whole page,
which is the bit that actually makes it feel like a dashboard rather than a static
report. Worth having for a demo.

## Saving and exporting

Title text box at the top ("Superstore Sales Dashboard 2015-2018"), then File > Save As
into the repo root as `sales_dashboard.pbix`. I also took a screenshot of the full page
and saved it as `charts/powerbi_dashboard.png` so the README can show it without needing
Power BI open.

## Sanity check

If the data loaded right, the cards should match the numbers from the SQL queries:

| Metric | Value |
|---|---|
| Total Revenue | $2,297,200.65 |
| Total Profit | $286,396.54 |
| Profit Margin | 12.47% |
| Orders | 5,009 |
| Customers | 793 |
| Top region | West (~$725K) |
| Top category | Technology / Phones |

A couple of things the data actually showed that I found interesting: discounts above
about 20% push the average order into a loss, and Furniture is by far the weakest
category on margin (around 2.5%) even though it sells fine.
