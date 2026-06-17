-- =====================================================================
-- Business Queries  —  Superstore Sales Analytics
-- Table: sales_clean  (produced by src/clean_data.py)
-- =====================================================================


-- 1. Headline KPIs --------------------------------------------------
SELECT
    ROUND(SUM(Sales), 2)        AS total_revenue,
    ROUND(SUM(Profit), 2)       AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    COUNT(DISTINCT "Order ID")  AS total_orders,
    COUNT(DISTINCT "Customer ID") AS total_customers
FROM sales_clean;


-- 2. Revenue & profit by region ------------------------------------
SELECT
    Region,
    ROUND(SUM(Sales), 2)  AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS margin_pct
FROM sales_clean
GROUP BY Region
ORDER BY revenue DESC;


-- 3. Revenue & profit by category and sub-category -----------------
SELECT
    Category,
    "Sub-Category",
    ROUND(SUM(Sales), 2)  AS revenue,
    ROUND(SUM(Profit), 2) AS profit
FROM sales_clean
GROUP BY Category, "Sub-Category"
ORDER BY revenue DESC;


-- 4. Top 10 products by revenue ------------------------------------
SELECT
    "Product Name",
    ROUND(SUM(Sales), 2)  AS revenue,
    ROUND(SUM(Profit), 2) AS profit
FROM sales_clean
GROUP BY "Product Name"
ORDER BY revenue DESC
LIMIT 10;


-- 5. Top 10 loss-making products (profit leaks) --------------------
SELECT
    "Product Name",
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(AVG(Discount) * 100, 1) AS avg_discount_pct
FROM sales_clean
GROUP BY "Product Name"
HAVING profit < 0
ORDER BY profit ASC
LIMIT 10;


-- 6. Monthly sales trend -------------------------------------------
SELECT
    "Order Month Name" AS month,
    ROUND(SUM(Sales), 2)  AS revenue,
    ROUND(SUM(Profit), 2) AS profit
FROM sales_clean
GROUP BY month
ORDER BY month;


-- 7. Year-over-year revenue growth ---------------------------------
WITH yearly AS (
    SELECT "Order Year" AS yr, SUM(Sales) AS revenue
    FROM sales_clean
    GROUP BY yr
)
SELECT
    yr,
    ROUND(revenue, 2) AS revenue,
    ROUND(revenue - LAG(revenue) OVER (ORDER BY yr), 2) AS yoy_change,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY yr))
          / LAG(revenue) OVER (ORDER BY yr) * 100, 1) AS yoy_growth_pct
FROM yearly
ORDER BY yr;


-- 8. Customer segments by value -----------------------------------
SELECT
    Segment,
    COUNT(DISTINCT "Customer ID") AS customers,
    ROUND(SUM(Sales), 2)          AS revenue,
    ROUND(SUM(Sales) / COUNT(DISTINCT "Customer ID"), 2) AS revenue_per_customer
FROM sales_clean
GROUP BY Segment
ORDER BY revenue DESC;


-- 9. Top 10 customers by lifetime revenue --------------------------
SELECT
    "Customer Name",
    COUNT(DISTINCT "Order ID") AS orders,
    ROUND(SUM(Sales), 2)       AS lifetime_revenue
FROM sales_clean
GROUP BY "Customer Name"
ORDER BY lifetime_revenue DESC
LIMIT 10;


-- 10. Discount impact on profitability -----------------------------
SELECT
    CASE
        WHEN Discount = 0            THEN '0%'
        WHEN Discount <= 0.20        THEN '1-20%'
        WHEN Discount <= 0.40        THEN '21-40%'
        ELSE '40%+'
    END AS discount_band,
    COUNT(*)              AS order_lines,
    ROUND(AVG(Profit), 2) AS avg_profit,
    ROUND(SUM(Profit), 2) AS total_profit
FROM sales_clean
GROUP BY discount_band
ORDER BY avg_profit DESC;
