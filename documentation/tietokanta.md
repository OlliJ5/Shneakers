# Tietokanta

Sovelluksen kehityksessä on lokaalisti käytetty SQLiteä ja tuotannossa Herokussa on käytössä Herokun tarjoama PostgreSQL-tietokanta.

## Tietokantakaavio


<img src="https://github.com/OlliJ5/Shneakers/blob/master/documentation/tietokantakaavioUpdated.png" width="700">

Tietokantakaavio vastaa tällä hetkellä täysin sovelluksessa käytettävää tietokantaa. Kurssin alussa tehty [kaavio](https://github.com/OlliJ5/Shneakers/blob/master/documentation/Tietokantakaavio.png)
on hyvin samanlainen kuin lopullinen kaavio. Lopulliseen kaavioon on tehty kuitenkin joitain pieniä muutoksia.

## Create Table -lauseet

```
CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	role VARCHAR(144) NOT NULL, 
	PRIMARY KEY (id)
);
```

```
CREATE TABLE category (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	PRIMARY KEY (id)
);
```

```
CREATE TABLE thread (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	title VARCHAR(144) NOT NULL, 
	text VARCHAR(400) NOT NULL, 
	creator VARCHAR(144) NOT NULL, 
	category_name VARCHAR(144) NOT NULL, 
	account_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(category_id) REFERENCES category (id)
);
```

```
CREATE TABLE comment (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	text VARCHAR(144) NOT NULL, 
	creator VARCHAR(144) NOT NULL, 
	account_id INTEGER NOT NULL, 
	thread_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(thread_id) REFERENCES thread (id)
);
```

```
CREATE TABLE user_thread (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	account_id INTEGER, 
	thread_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(thread_id) REFERENCES thread (id)
);
```

```
CREATE TABLE collection (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	description VARCHAR(144), 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
);
```

```
CREATE TABLE shoe (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	model VARCHAR(144) NOT NULL, 
	brand VARCHAR(144) NOT NULL, 
	release_year INTEGER NOT NULL, 
	collection_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(collection_id) REFERENCES collection (id)
);
```

### Normalisointi

Tietokannan kaikki muut taulut ovat kolmannessa normaalimuodossa, paitsi thread, jossa sarakkeet creator ja category_name ovat 
transitiivisesti riippuvaisia pääavaimesta, sillä ne saa selvitettyä viiteavainten account_id ja category_id avulla. Taulun saisi 
komanteen normaalimuotoon poistamalla sarakkeet creator ja category_name ja selvittämällä ne ohjelmallisesti tietokannasta aina 
kun niitä tarvitsee (eli usein, jonka vuoksi päädyin lisämään ne tauluun alunperin)

### Indeksointi

