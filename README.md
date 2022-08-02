# flask_upload_csv
simple web application using any web framework  Flask. The application serves only one endpoint `/upload` which allows uploading input CSV file and returns transformed file in  Dockerized environment

a) Input file is UTF-8 CSV file with Unix line endings containing following columns: ID, release date (YYYY/MM/DD), 
   game name (in kebab-case), ISO 3166 alpha-3 country code, number of sold copies, price for each copy

b) Output file is UTF-8 CSV file with Unix line endings, column names and following columns: ID, Release Date (DD.MM.YYYY),
   Name (Capitalized), Country name, Copies Sold, Copy Price, Total Revenue (Copies Sold * Copy Price rounded to the nearest ones)
   Rows are sorted by date


### Sample input file

```
1,2012/3/6,mass-effect-3,ALA,123854,24.23 USD
2,1998/12/21,baldurs-gate,ABW,7777,15.23 USD
3,2017/7/21,fortnite,JAM,367,12.23 USD
4,2019/2/4,apex-legends,BEN,23,24.23 USD
5,2008/4/8,assasins-creed,FRA,123854,24.23 USD
```

### Sample output file

```
ID,Release Date,Name,Country,Copies Sold,Copy Price,Total Revenue
2,21.12.1998,Baldurs Gate,Aruba,7777,15.23 USD,118444 USD
5,08.04.2008,Assassins Creed,France,123854,4.23 USD,523902 USD
1,06.03.2012,Mass Effect 3,Åland Islands,123854,24.23 USD,3000982 USD
3,21.07.2017,Fortnite,Jamaica,367,12.23 USD,4489 USD 
4,04.02.2019,Apex Legends,Benin,23,24.23 USD,557 USD
```
