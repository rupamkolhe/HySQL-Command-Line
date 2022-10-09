# HySQL-Command-Line


HySQL(hybrid sql) makes it easier to upload data from file to database and vice-versa. 
<hr>

> ## ***Syntax***

> ### General form
~~~ 
~~ <hysql command> ~~
~~~
> ## ***Commands***
> ### DISPLAY [\<file path>\]
<li>display first five rows of dataframe in tabular form</li>

~~~sql
~~ DISPLAY [GLAXO.csv] ~~
~~~
> ### ENABLE AUTOCOMMIT
<li>commits any changes automatically</li>

~~~sql
~~ ENABLE AUTOCOMMIT ~~
~~~
> ### DISABLE AUTOCOMMIT

~~~sql
~~ DISABLE AUTOCOMMIT ~~
~~~
> ### COMMIT 
<li>commits all the changes made</li>

~~~sql
~~ COMMIT ~~
~~~
> ### \<DQL command\> DUMP IN \<file path\> 
<li>dumps result set from dql in specified file</li>

~~~sql
SELECT * FROM mydb.cars; ~~ DUMP IN [cars.csv] ~~
~~~
> ### DUMP [\<table\>] IN [\<file path\>]
<li>dumps data from specified table in specified file</li>

~~~sql
~~ DUMP [mydb.cars] IN [cars.csv] ~~
~~~

> ### DUMP [\<file path\>] IN [\<table\>]
<li>dumps data from specified file in specified table</li>

~~~sql
~~ DUMP [cars.csv] IN [mydb.cars] ~~
~~~
























