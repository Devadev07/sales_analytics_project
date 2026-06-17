-- Total Revenue

SELECT
ROUND(SUM(Sales),2) AS total_revenue
FROM sales;


-- Total Profit

SELECT
ROUND(SUM(Profit),2) AS total_profit
FROM sales;


-- Revenue By Region

SELECT
Region,
ROUND(SUM(Sales),2) revenue
FROM sales
GROUP BY Region
ORDER BY revenue DESC;