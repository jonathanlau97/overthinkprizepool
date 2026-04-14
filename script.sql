SELECT 
flt_num Flight_ID,
flt_date Flight_Date
,crew_id Crew_ID,
name Crew_Name,
crew_sold_qty Bottles_Sold_on_Flight,
(crew_sales_dutyfree+crew_sales_merchandise) crew_sold_quantity,
left(flt_num,2) Airline_Code 
FROM `airasia-opdatalake-prd.CREW_ANALYTICS.crew_insight_sales` 
where FLT_DATE >= "2026-03-01"
and LOWER(product_name) LIKE '%overthink%'

--Flight_ID,Flight_Date,Crew_ID,Crew_Name,Bottles_Sold_on_Flight,Airline_Code
