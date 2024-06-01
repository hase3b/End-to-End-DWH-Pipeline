import pandasql as psql
import pandas as pd
from tabulate import tabulate

def dimquery(Dim_Date, Dim_Location, Dim_Agent, Dim_PropertyDetails, Dim_Listing, Fact_Transaction):
    # 1. What was the total commission generated through agents handling rental listings in the first quarter of 2021?
    query1="""
    SELECT SUM(ft.CommissionValue) AS Total_Commission
    FROM Fact_Transaction ft
    JOIN Dim_Date dd ON ft.DateID = dd.DateID
    JOIN Dim_Listing dl ON ft.ListingID = dl.ListingID
    WHERE dd.Year = 2022 AND dd.Quarter = 1 AND dl.ListingType = 'Rental';
    """
    result1=psql.sqldf(query1, locals())

    # 2. What was the average time taken to close a listing by agents handling sale listings in all four quarters of 2022?
    query2="""
    SELECT AVG(ft.ClosingDays) AS Avg_ClosingDays
    FROM Fact_Transaction ft
    JOIN Dim_Date dd ON ft.DateID = dd.DateID
    JOIN Dim_Listing dl ON ft.ListingID = dl.ListingID
    WHERE dd.Year = 2022 AND dl.ListingType = 'Sale';
    """
    result2=psql.sqldf(query2, locals())

    # 3. What was average commission rate of the top 5 cities with the most sale transactions in 2023?
    query3="""
    SELECT dl.City, AVG(ft.CommissionRate) AS Avg_CommissionRate
    FROM Fact_Transaction ft
    JOIN Dim_Date dd ON ft.DateID = dd.DateID
    JOIN Dim_Location dl ON ft.LocationID = dl.LocationID
    JOIN Dim_Listing dlst ON ft.ListingID = dlst.ListingID
    WHERE dd.Year = 2023 AND dlst.ListingType = 'Sale'
    GROUP BY dl.City
    ORDER BY COUNT(*) DESC
    LIMIT 5;
    """
    result3=psql.sqldf(query3, locals())

    # 4. What was the average time spent in negotiations by agents for the top 3 states with the most rental transactions in 2022 and 2023?
    query4="""
    SELECT dl.State AS State,AVG(ft.NegotiationDays) AS Avg_NegotiationDays
    FROM Fact_Transaction ft
    JOIN Dim_Date dd ON ft.DateID = dd.DateID
    JOIN Dim_Location dl ON ft.LocationID = dl.LocationID
    JOIN Dim_Listing dlst ON ft.ListingID = dlst.ListingID
    WHERE dd.Year > 2021 AND dlst.ListingType = 'Rental'
    GROUP BY dl.State
    ORDER BY COUNT(*) DESC
    LIMIT 3;
    """
    result4=psql.sqldf(query4, locals())

    # 5. What was the average commission generated by middle-aged male and female agents in 2022?
    query5="""
    SELECT da.Gender AS Gender, AVG(ft.CommissionValue) AS Avg_Commission
    FROM Fact_Transaction ft
    JOIN Dim_Date dd ON ft.DateID = dd.DateID
    JOIN Dim_Agent da ON ft.AgentID = da.AgentID
    WHERE dd.Year = 2022 AND da.AgeCat = 'Middle Aged'
    GROUP BY da.Gender;
    """
    result5=psql.sqldf(query5, locals())

    # 6. What was the average transaction value for Broker Associate in the fourth quarter of 2023?
    query6="""
    SELECT AVG(ft.TransactionValue) AS Avg_TransactionValue
    FROM Fact_Transaction ft
    JOIN Dim_Date dd ON ft.DateID = dd.DateID
    JOIN Dim_Agent da ON ft.AgentID = da.AgentID
    WHERE dd.Year = 2023 AND dd.Quarter = 4 AND da.Position = 'Broker Associate';
    """
    result6=psql.sqldf(query6, locals())

    # 7. What was average number of transactions handled by agents who've joined in the past two years?
    query7="""
    SELECT AVG(t.Transactions) AS Avg_Transactions
    FROM (
        SELECT COUNT(ft.TransactionID) AS Transactions
        FROM Fact_Transaction ft
        JOIN Dim_Agent da ON ft.AgentID = da.AgentID
        WHERE da.AgentSince <= 2
        GROUP BY da.AgentID
    ) t;
    """
    result7=psql.sqldf(query7, locals())

    # 8. What was the average time taken to close a sale listing where property size was greater 3000 sqft and had more than 4 bedrooms in 2021?
    query8="""
    SELECT AVG(ft.ClosingDays) AS Avg_ClosingDays
    FROM Fact_Transaction ft
    JOIN Dim_Date dd ON ft.DateID = dd.DateID
    JOIN Dim_Listing dl ON ft.ListingID = dl.ListingID
    JOIN Dim_PropertyDetails dpd ON ft.PropertyDetailsID = dpd.PropertyDetailsID
    WHERE dd.Year = 2022 AND dl.ListingType = 'Sale' AND dpd.LotArea > 3000 AND dpd.Bedrooms > 4;
    """
    result8=psql.sqldf(query8, locals())

    # 9. What is the average maintenance cost and demand price discount for properties which are built in last two decades?
    query9="""
    SELECT AVG(ft.MaintenanceExp) AS Avg_MaintenanceCost, 
           AVG((ft.AskedAmount - ft.TransactionValue) / ft.AskedAmount) * 100 AS Avg_DemandPriceDiscount
    FROM Fact_Transaction ft
    JOIN Dim_PropertyDetails dpd ON ft.PropertyDetailsID = dpd.PropertyDetailsID
    WHERE dpd.BuiltSince <= 20;
    """
    result9=psql.sqldf(query9, locals())

    # 10. What is the average time taken to close a listing which has a property in a poor condition?
    query10="""
    SELECT AVG(ft.ClosingDays) AS Avg_ClosingDays
    FROM Fact_Transaction ft
    JOIN Dim_PropertyDetails dpd ON ft.PropertyDetailsID = dpd.PropertyDetailsID
    WHERE dpd.Condition = 'Poor';
    """
    result10=psql.sqldf(query10, locals())

    for i in range(1,11):
        print(f'Query {i}')
        result=eval("result"+f"{i}")
        print(tabulate(result,tablefmt='psql'),"\n\n")