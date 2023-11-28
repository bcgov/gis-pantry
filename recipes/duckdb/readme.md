# duckdb show and tell
Included are two examples demonstrating a few uses for duckdb, an in-process database management system.
duckdb is fast and has a geospatial extension that supports both reading/writing spatial objects and basic spatial operations using sql.

Sample Notebooks  
-------
[reading csv](./duckdb-csv-query.ipynb)  
[reading geospatial](./duckdb-geospatial.ipynb)

## requirements
python-duckdb  
requests  
BeautifulSoup4  
pandas  
geopandas  

## setup environment creation with Mamba (or Conda)
```
mamba create -n uwrtools -c conda-forge python>=3.11 requests geospatial jupyterlab jupyter-book python-duckdb BeautifulSoup4
```

## start jupyter lab
```
jupyter lab .
```


