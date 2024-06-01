import pandas as pd
import numpy as np
import requests
from io import StringIO
from sklearn.impute import KNNImputer
from datetime import datetime

# Data Ingestion
def fetch_datasets(csv_files, base_url):
    dataframes={}
    for file in csv_files:
        csv_url=base_url + file + '.csv'
        response=requests.get(csv_url)
        if response.status_code==200:
            df=pd.read_csv(StringIO(response.text))
            dataframes[file]=df
        else:
            raise Exception(f"Failed to fetch {file}.csv")
    return dataframes

# DB Data Type Correction
def correct_dtypes(dataframes):
    dataframes['address']['zip_code']=dataframes['address']['zip_code'].astype(int)
    dataframes['address']['zip_code']=dataframes['address']['zip_code'].astype('object')

    dataframes['client']['client_dob']=pd.to_datetime(dataframes['client']['client_dob'])
    
    dataframes['agent']['agent_dob']=pd.to_datetime(dataframes['agent']['agent_dob'])
    dataframes['agent']['hire_date']=pd.to_datetime(dataframes['agent']['hire_date'])
    
    dataframes['owner']['owner_dob']=pd.to_datetime(dataframes['owner']['owner_dob'])
    
    dataframes['features']['feature_id']=dataframes['features']['feature_id'].astype(int)
    dataframes['features']['no_bedrooms']=dataframes['features']['no_bedrooms'].astype(int)
    dataframes['features']['no_bathrooms']=dataframes['features']['no_bathrooms'].astype(int)
    dataframes['features']['no_kitchens']=dataframes['features']['no_kitchens'].astype(int)
    dataframes['features']['no_floors']=dataframes['features']['no_floors'].astype(int)
    dataframes['features']['year_built']=dataframes['features']['year_built'].astype(int)
    
    dataframes['property']['property_id']=dataframes['property']['property_id'].astype(int)
    dataframes['property']['address_id']=dataframes['property']['address_id'].astype(int)
    dataframes['property']['owner_id']=dataframes['property']['owner_id'].astype(int)
    dataframes['property']['agent_id']=dataframes['property']['agent_id'].astype(int)
    dataframes['property']['feature_id']=dataframes['property']['feature_id'].astype(int)
    dataframes['property']['listing_date']=pd.to_datetime(dataframes['property']['listing_date'])
    
    dataframes['maintenance']['maintenance_date']=pd.to_datetime(dataframes['maintenance']['maintenance_date'])
    dataframes['maintenance']['cost']=dataframes['maintenance']['cost'].astype(float)
    
    dataframes['visit']['visit_date']=pd.to_datetime(dataframes['visit']['visit_date'])
    
    dataframes['commission']['commission_id']=dataframes['commission']['commission_id'].astype(int)
    dataframes['commission']['payment_date']=pd.to_datetime(dataframes['commission']['payment_date'])
    
    dataframes['sale']['sale_date']=pd.to_datetime(dataframes['sale']['sale_date'])
    dataframes['sale']['sale_amount']=dataframes['sale']['sale_amount'].astype(float)
    
    dataframes['rent']['rent_id']=dataframes['rent']['rent_id'].astype(int)
    dataframes['rent']['client_id']=dataframes['rent']['client_id'].astype(int)
    dataframes['rent']['property_id']=dataframes['rent']['property_id'].astype(int)
    dataframes['rent']['commission_id']=dataframes['rent']['commission_id'].astype(int)
    dataframes['rent']['contract_id']=dataframes['rent']['contract_id'].astype(int)
    dataframes['rent']['agreement_date']=pd.to_datetime(dataframes['rent']['agreement_date'])
    dataframes['rent']['rent_start_date']=pd.to_datetime(dataframes['rent']['rent_start_date'])
    dataframes['rent']['rent_end_date']=pd.to_datetime(dataframes['rent']['rent_end_date'])
    
    return dataframes


# Data Cleaning
# Support Functions for Missing Value Fill Function
def knn_impute(df):
    imputer=KNNImputer()
    imputed_array=imputer.fit_transform(df)
    return pd.DataFrame(imputed_array,columns=df.columns)

def mode_impute(df):
    for col in df.columns:
        if df[col].isna().sum()>0:
            mode_value=df[col].mode()[0]
            df[col].fillna(mode_value,inplace=True)
    return df

# Missing Value Fill Function
def fill_mv(dataframes):
    # Logical Missing Value Fill
    if dataframes['commission']['commission_rate'].isna().sum() > 0:
        missing_com_id = dataframes['commission'][dataframes['commission']['commission_rate'].isna()]['commission_id']
        for i in missing_com_id:
            if i in dataframes['sale']['commission_id'].values and not pd.isna(dataframes['sale'][dataframes['sale']['commission_id'] == i]['sale_amount'].values[0]):
                sale_amount = dataframes['sale'][dataframes['sale']['commission_id'] == i]['sale_amount'].values[0]
                commission_amount = dataframes['commission'][dataframes['commission']['commission_id'] == i]['commission_amount'].values[0]
                commission_rate = (commission_amount / sale_amount) * 100
                dataframes['commission'].loc[dataframes['commission']['commission_id'] == i, 'commission_rate'] = commission_rate
            elif i in dataframes['rent']['commission_id'].values and not pd.isna(dataframes['rent'][dataframes['rent']['commission_id'] == i]['rent_amount'].values[0]):
                rent_amount = dataframes['rent'][dataframes['rent']['commission_id'] == i]['rent_amount'].values[0]
                commission_amount = dataframes['commission'][dataframes['commission']['commission_id'] == i]['commission_amount'].values[0]
                commission_rate = (commission_amount / rent_amount) * 100
                dataframes['commission'].loc[dataframes['commission']['commission_id'] == i, 'commission_rate'] = commission_rate

    if dataframes['commission']['commission_amount'].isna().sum() > 0:
        missing_com_id = dataframes['commission'][dataframes['commission']['commission_amount'].isna()]['commission_id']
        for i in missing_com_id:
            if i in dataframes['sale']['commission_id'].values and not pd.isna(dataframes['sale'][dataframes['sale']['commission_id'] == i]['sale_amount'].values[0]):
                sale_amount = dataframes['sale'][dataframes['sale']['commission_id'] == i]['sale_amount'].values[0]
                commission_rate = dataframes['commission'][dataframes['commission']['commission_id'] == i]['commission_rate'].values[0]
                commission_amount = (commission_rate * sale_amount) / 100
                dataframes['commission'].loc[dataframes['commission']['commission_id'] == i, 'commission_amount'] = commission_amount
            elif i in dataframes['rent']['commission_id'].values and not pd.isna(dataframes['rent'][dataframes['rent']['commission_id'] == i]['rent_amount'].values[0]):
                rent_amount = dataframes['rent'][dataframes['rent']['commission_id'] == i]['rent_amount'].values[0]
                commission_rate = dataframes['commission'][dataframes['commission']['commission_id'] == i]['commission_rate'].values[0]
                commission_amount = (commission_rate * rent_amount) / 100
                dataframes['commission'].loc[dataframes['commission']['commission_id'] == i, 'commission_amount'] = commission_amount

    if dataframes['rent']['rent_amount'].isna().sum() > 0:
        missing_rent_id = dataframes['rent'][dataframes['rent']['rent_amount'].isna()]['rent_id']
        for i in missing_rent_id:
            comm_id = dataframes['rent'][dataframes['rent']['rent_id'] == i]['commission_id'].values[0]
            commission_amount = dataframes['commission'][dataframes['commission']['commission_id'] == comm_id]['commission_amount'].values[0]
            commission_rate = dataframes['commission'][dataframes['commission']['commission_id'] == comm_id]['commission_rate'].values[0]
            if not pd.isna(commission_rate) and not pd.isna(commission_amount):
                rent_amount = commission_amount / (commission_rate / 100)
                dataframes['rent'].loc[dataframes['rent']['rent_id'] == i, 'rent_amount'] = rent_amount

    if dataframes['sale']['sale_amount'].isna().sum() > 0:
        missing_sale_id = dataframes['sale'][dataframes['sale']['sale_amount'].isna()]['sale_id']
        for i in missing_sale_id:
            comm_id = dataframes['sale'][dataframes['sale']['sale_id'] == i]['commission_id'].values[0]
            commission_amount = dataframes['commission'][dataframes['commission']['commission_id'] == comm_id]['commission_amount'].values[0]
            commission_rate = dataframes['commission'][dataframes['commission']['commission_id'] == comm_id]['commission_rate'].values[0]
            if not pd.isna(commission_rate) and not pd.isna(commission_amount):
                sale_amount = commission_amount / (commission_rate / 100)
                dataframes['sale'].loc[dataframes['sale']['sale_id'] == i, 'sale_amount'] = sale_amount

    # KNN Imputation
    for key in dataframes.keys():
            df=dataframes[key]
            numeric_df=df.select_dtypes(include=[np.number])
            non_numeric_df=df.select_dtypes(exclude=[np.number])
            if numeric_df.isna().sum().sum()>0:
                imputed_numeric_df=knn_impute(numeric_df)
                for col in numeric_df.columns:
                    df[col]=imputed_numeric_df[col]
        
            if non_numeric_df.isna().sum().sum()>0:
                imputed_non_numeric_df=mode_impute(non_numeric_df)
                for col in non_numeric_df.columns:
                    df[col]=imputed_non_numeric_df[col]
                
    return dataframes

# Creating Dimensional Tables
def create_date_dim(start_date,end_date):
    date_range=pd.date_range(start=start_date,end=end_date,freq='D')
    date_dim=pd.DataFrame(date_range,columns=['Date'])
    date_dim['Year']=date_dim['Date'].dt.year
    date_dim['Quarter']=date_dim['Date'].dt.quarter
    date_dim['Month']=date_dim['Date'].dt.month
    date_dim['Week']=date_dim['Date'].apply(lambda x: (x - pd.Timestamp(x.year, 1, 1)).days//7 + 1)
    date_dim['Day']=date_dim['Date'].dt.day
    date_dim['DateID']=range(1,len(date_dim)+1)
    return date_dim

def create_loc_dim(address):
    location_dim=address[['address_id','zip_code','city','state']].drop_duplicates().reset_index(drop=True)
    location_dim['LocationID']=location_dim['zip_code'].astype('str') + '_' + location_dim['city'] + '_' + location_dim['state']
    location_dim.rename(columns={'zip_code': 'ZipCode','city': 'City','state': 'State'},inplace=True)
    location_dim=location_dim[['address_id','LocationID','ZipCode','City','State']]
    location_dim['LocationID'] = pd.factorize(location_dim['LocationID'])[0] + 1

    location_dim['address_id']=location_dim['address_id'].astype(int)
    location_dim['LocationID']=location_dim['LocationID'].astype(int)
    location_dim['ZipCode']=location_dim['ZipCode'].astype('str')
    location_dim['City']=location_dim['City'].astype('str')
    location_dim['State']=location_dim['State'].astype('str')

    return location_dim

def create_agent_dim(agent):
    agent_dim=agent.copy()
    agent_dim['Age']=datetime.now().year-agent_dim['agent_dob'].dt.year
    agent_dim['AgeCat']=pd.cut(agent_dim['Age'], bins=[0, 20, 45, 65, np.inf],labels=['Young', 'Adult', 'Middle Aged', 'Senior'],right=False)
    agent_dim['AgentSince']=datetime.now().year-agent_dim['hire_date'].dt.year
    agent_dim.rename(columns={'agent_gender': 'Gender','title': 'Position'},inplace=True)
    agent_dim=agent_dim[['agent_id','Gender','AgeCat','AgentSince','Position']].drop_duplicates().reset_index(drop=True)
    agent_dim['AgentID']=agent_dim['Gender'] + '_' + agent_dim['AgeCat'].astype('str') + '_' + agent_dim['AgentSince'].astype('str') + '_' + agent_dim['Position']
    agent_dim['AgentID'] = pd.factorize(agent_dim['AgentID'])[0] + 1

    agent_dim['agent_id']=agent_dim['agent_id'].astype(int)
    agent_dim['AgentID']=agent_dim['AgentID'].astype(int)
    agent_dim['Gender']=agent_dim['Gender'].astype('str')
    agent_dim['AgeCat']=agent_dim['AgeCat'].astype('str')
    agent_dim['AgentSince']=agent_dim['AgentSince'].astype(int)
    agent_dim['Position']=agent_dim['Position'].astype('str')

    return agent_dim

def create_propdet_dim(features):
    features_dim=features.copy()
    features_dim['Condition']=pd.cut(features_dim['condition_rating'], bins=[-0.1, 3.1, 7.1, 10.1],labels=['Poor', 'Average', 'Excellent'],right=True)
    features_dim['BuiltSince']=datetime.now().year-features_dim['year_built']
    features_dim.rename(columns={'feature_id': 'PropertyDetailsID','no_bedrooms': 'Bedrooms','no_bathrooms': 'Bathrooms','no_kitchens': 'Kitchens','no_floors': 'Floors',
                                               'parking_area_sqft': 'ParkingArea','lot_area_sqft': 'LotArea','built_since': 'BuiltSince','condition': 'Condition'},
                                               inplace=True)
    
    features_dim['PropertyDetailsID']=features_dim['PropertyDetailsID'].astype(int)
    features_dim['LotArea']=features_dim['LotArea'].astype(int)
    features_dim['Bedrooms']=features_dim['Bedrooms'].astype(int)
    features_dim['Bathrooms']=features_dim['Bathrooms'].astype(int)
    features_dim['Kitchens']=features_dim['Kitchens'].astype(int)
    features_dim['Floors']=features_dim['Floors'].astype(int)
    features_dim['ParkingArea']=features_dim['ParkingArea'].astype(int)
    features_dim['BuiltSince']=features_dim['BuiltSince'].astype(int)
    features_dim['Condition']=features_dim['Condition'].astype('str')
    
    return features_dim

def create_listing_dim(property,visit):
    visits=visit.groupby('property_id').size().reset_index(name='NumVisits')
    listing_dim=pd.merge(property, visits, on='property_id', how='left')
    listing_dim.reset_index(drop=True,inplace=True)
    listing_dim['NumVisits']=listing_dim['NumVisits'].fillna(0).astype(int)
    listing_dim.rename(columns={'listing_type':'ListingType'},inplace=True)
    listing_dim=listing_dim[['property_id','ListingType', 'NumVisits']].drop_duplicates().reset_index(drop=True)
    listing_dim['ListingID']=listing_dim['ListingType'] + '_' + listing_dim['NumVisits'].astype('str')
    listing_dim['ListingID'] = pd.factorize(listing_dim['ListingID'])[0] + 1


    listing_dim['property_id']=listing_dim['property_id'].astype(int)
    listing_dim['ListingID']=listing_dim['ListingID'].astype(int)
    listing_dim['ListingType']=listing_dim['ListingType'].astype('str')
    listing_dim['NumVisits']=listing_dim['NumVisits'].astype(int)

    return listing_dim

# Creating Fact Table
def create_fact_trans(sale, rent, maintenance, property, commission, visit, start_date, end_date, dimdate, dimloc, dimagent, dimprodet, dimlisting):
    transactions=pd.concat([sale.assign(TransactionType='Sale'),rent.assign(TransactionType='Rent')], ignore_index=True)

    transactions['TransactionDate']=transactions['sale_date']
    transactions.loc[transactions['TransactionType']=='Rent','TransactionDate']=transactions['agreement_date']
    transactions['TransactionAmount']=transactions['sale_amount']
    transactions.loc[transactions['TransactionType']=='Rent','TransactionAmount']=transactions['rent_amount']
    transactions.drop(['sale_date','agreement_date','sale_amount','rent_amount'],axis=1,inplace=True)
    
    transactions=pd.merge(transactions, property[['property_id','asking_amount']], on='property_id', how='left')

    maintenance_exp=maintenance[['property_id','cost']].groupby('property_id').sum()
    transactions=pd.merge(transactions, maintenance_exp, on='property_id', how='left')
    transactions['cost']=transactions['cost'].fillna(0).astype(int)
    
    transactions=pd.merge(transactions, commission[['commission_id', 'commission_rate', 'commission_amount']], on='commission_id', how='left')
    
    transactions=pd.merge(transactions, property[['property_id', 'listing_date']], on='property_id', how='left')
    
    last_visit=visit[['property_id','visit_date']].groupby('property_id').max()
    transactions=pd.merge(transactions, last_visit, on='property_id', how='left')
    transactions['NegotiationDays']=(transactions['TransactionDate'] - transactions['visit_date']).dt.days
    transactions['NegotiationDays']=transactions['NegotiationDays'].fillna(0).astype(int)
    transactions['ClosingDays']=(transactions['TransactionDate'] - transactions['listing_date']).dt.days
    
    transactions=transactions[(transactions['TransactionDate']>=pd.Timestamp(start_date)) & (transactions['TransactionDate']<=pd.Timestamp(end_date))]
    transactions=transactions[['property_id','TransactionDate','TransactionAmount','asking_amount','cost','commission_rate','commission_amount','NegotiationDays','ClosingDays']]
    
    transactions=pd.merge(transactions,property[['property_id','address_id','agent_id','feature_id']],on='property_id',how='left')
    transactions.rename(columns={'TransactionDate':'Date'},inplace=True)
    transactions=pd.merge(transactions,dimdate[['Date','DateID']],on='Date',how='left').drop(['Date'],axis=1)
    transactions=pd.merge(transactions,dimloc[['address_id','LocationID']],on='address_id',how='left').drop(['address_id'],axis=1)
    transactions=pd.merge(transactions,dimagent[['agent_id','AgentID']],on='agent_id',how='left').drop(['agent_id'],axis=1)
    transactions.rename(columns={'feature_id':'PropertyDetailsID'},inplace=True)
    transactions=pd.merge(transactions,dimprodet[['PropertyDetailsID']],on='PropertyDetailsID',how='left')
    transactions=pd.merge(transactions,dimlisting[['property_id','ListingID']],on='property_id',how='left').drop(['property_id'],axis=1)
    transactions.rename(columns={'TransactionAmount':'TransactionValue','asking_amount':'AskedAmount','cost':'MaintenanceExp','commission_rate':'CommissionRate',
                                 'commission_amount':'CommissionValue'},inplace=True)
    
    transactions['NegotiationDays']=transactions['NegotiationDays'].apply(lambda x: max(x, 0))
    transactions['ClosingDays']=transactions['ClosingDays'].apply(lambda x: max(x, 0))

    transactions['TransactionID']=range(1,len(transactions)+1)
    transactions=transactions[['TransactionID','DateID','LocationID','AgentID','PropertyDetailsID','ListingID','MaintenanceExp','AskedAmount','TransactionValue',
                               'CommissionRate','CommissionValue','NegotiationDays','ClosingDays']]
    
    return transactions


# Creating Star Schema
def create_star_schema(sale, rent, maintenance, property, commission, visit, features, address, agent, start_date, end_date):
    dimdate=create_date_dim(start_date=start_date,end_date=end_date)
    dimloc=create_loc_dim(address=address)
    dimagent=create_agent_dim(agent=agent)
    dimprodet=create_propdet_dim(features=features)
    dimlisting=create_listing_dim(property=property,visit=visit)
    transactions=create_fact_trans(sale=sale,rent=rent,maintenance=maintenance,property=property,commission=commission,visit=visit,start_date=start_date,end_date=end_date,
                                   dimdate=dimdate,dimloc=dimloc,dimagent=dimagent,dimprodet=dimprodet,dimlisting=dimlisting)
    
    dimloc=dimloc.drop(['address_id'],axis=1).drop_duplicates().reset_index(drop=True)
    dimagent=dimagent.drop(['agent_id'],axis=1).drop_duplicates().reset_index(drop=True)
    dimlisting=dimlisting.drop(['property_id'],axis=1).drop_duplicates().reset_index(drop=True)
    
    dimdate=dimdate[['DateID','Date','Year','Quarter','Month','Week','Day']]
    dimloc=dimloc[['LocationID','State','City','ZipCode']]
    dimagent=dimagent[['AgentID','Gender','AgeCat','AgentSince','Position']]
    dimprodet=dimprodet[['PropertyDetailsID', 'LotArea', 'Bedrooms', 'Bathrooms', 'Kitchens','Floors', 'ParkingArea', 'BuiltSince', 'Condition']]
    dimlisting=dimlisting[['ListingID','ListingType','NumVisits']]

    return dimdate, dimloc, dimagent, dimprodet, dimlisting, transactions