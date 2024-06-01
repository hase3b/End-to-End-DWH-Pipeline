from Pipeline_Support.ETL_SupportFunctions import fetch_datasets, correct_dtypes, fill_mv, create_star_schema

def etl_master():
    # Data Ingestion
    csv_files=['address', 'client', 'agent', 'owner', 'features', 'property', 'maintenance', 'visit', 'commission', 'sale', 'contract', 'rent', 'admin']
    base_url='https://raw.githubusercontent.com/hase3b/End-to-End-DWH-Pipeline/main/Database/Datasets/'
    dataframes=fetch_datasets(csv_files, base_url)
    
    # Fill Missing Values
    dataframes=fill_mv(dataframes)

    # Data Type Correction
    dataframes=correct_dtypes(dataframes)

    # Creating Star Schema
    Dim_Date, Dim_Location, Dim_Agent, Dim_PropertyDetails, Dim_Listing, Fact_Transaction=create_star_schema(sale=dataframes['sale'], rent=dataframes['rent'],
    maintenance=dataframes['maintenance'], property=dataframes['property'], commission=dataframes['commission'], visit=dataframes['visit'], features=dataframes['features'],
    address=dataframes['address'], agent=dataframes['agent'], start_date='2022-01-01', end_date='2024-12-31')

    return Dim_Date, Dim_Location, Dim_Agent, Dim_PropertyDetails, Dim_Listing, Fact_Transaction