import pandas as pd

def create_fact_snapshot(Dim_Date, Dim_Location, Dim_Agent, Dim_PropertyDetails, Dim_Listing, Fact_Transaction):
    Fact_Snap=pd.merge(Fact_Transaction,Dim_Date,on='DateID',how='left').drop(['DateID'],axis=1)
    Fact_Snap=pd.merge(Fact_Snap,Dim_Location,on='LocationID',how='left').drop(['LocationID'],axis=1)
    Fact_Snap=pd.merge(Fact_Snap,Dim_Agent,on='AgentID',how='left').drop(['AgentID'],axis=1)
    Fact_Snap=pd.merge(Fact_Snap,Dim_PropertyDetails,on='PropertyDetailsID',how='left').drop(['PropertyDetailsID'],axis=1)
    Fact_Snap=pd.merge(Fact_Snap,Dim_Listing,on='ListingID',how='left').drop(['ListingID'],axis=1)
    Fact_Snap=Fact_Snap[['TransactionID', 'Date', 'Year', 'Quarter', 'Month', 'Week', 'Day','State', 'City', 'ZipCode', 'Gender', 'AgeCat', 'AgentSince', 'Position',
                         'LotArea', 'Bedrooms','Bathrooms', 'Kitchens', 'Floors', 'ParkingArea', 'BuiltSince', 'Condition', 'ListingType', 'NumVisits', 'MaintenanceExp',
                         'AskedAmount', 'TransactionValue', 'CommissionRate', 'CommissionValue', 'NegotiationDays', 'ClosingDays']]
    return Fact_Snap