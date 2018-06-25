# Käyttötapaukset

## Ilman kirjautumista

### Käyttäjä voi luoda tunnuksen
```
INSERT INTO account (date_created, date_modified, name, username, password, role) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?)
```
### Käyttäjä voi luoda uuden langan
```
INSERT INTO thread (date_created, date_modified, title, text, creator, category_name, account_id, category_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?)
```
### Käyttäjä voi kirjoittaa kommentteja lankoihin
```
INSERT INTO comment (date_created, date_modified, text, creator, account_id, thread_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?)
```

### Käyttäjä voi poistaa kommentteja
```
DELETE FROM comment WHERE comment.id = ?
```

### Käyttäjä voi poistaa lankoja (jolloin kommentitkin poistuvat)
```
DELETE FROM comment WHERE comment.thread_id = ?
```
```
DELETE FROM thread WHERE thread.id = ?
```

### Käyttäjä voi muokata kommenttia
```
UPDATE comment SET date_modified=CURRENT_TIMESTAMP, text=? WHERE comment.id = ?
```

### Käyttäjä voi muokata langan sisältöä
```
UPDATE thread SET date_modified=CURRENT_TIMESTAMP, text=? WHERE thread.id = ?
```

### Käyttäjänä voin luoda kenkäkokoelmia profiiliini
```
INSERT INTO collection (date_created, date_modified, name, description, account_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)
```

### Käyttäjänä voin lisätä kenkiä kokoelmiin
```
INSERT INTO shoe (date_created, date_modified, model, brand, release_year, collection_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?)
```

### Käyttäjä voi filtteröidä lankoja kategorian perusteella, jotta löydän helpommin minua kiinnostavia asioita
```
 SELECT thread.id AS thread_id, thread.date_created AS thread_date_created, thread.date_modified AS thread_date_modified, thread.title AS thread_title, thread.text AS thread_text, thread.creator AS thread_creator, thread.category_name AS thread_category_name, thread.account_id AS thread_account_id, thread.category_id AS thread_category_id 
FROM thread 
WHERE thread.category_name = ? ORDER BY thread.date_created DESC
```

### Moderaattorina voin poistaa käyttäjiä (poistaa myös kaiken niihin liittyvän tiedon)
* Poistaa käyttäjän luomat kommentit
```
DELETE FROM comment WHERE comment.account_id = ?
```
* Poistaa kommentit jotka liittyvät käyttäjän luomiin lankoihin
```
DELETE FROM comment WHERE comment.thread_id = ?
```
* Poistaa käyttäjän luomat langat
```
DELETE FROM thread WHERE thread.account_id = ?
```
* Poistaa kengät, jotka liittyvät käyttäjän luomiin kokoelmiin
```
DELETE FROM shoe WHERE shoe.collection_id = ?
```
* Poistaa käyttäjän luomat kokoelmat
```
DELETE FROM collection WHERE collection.account_id = ?
```


### Moderaattorina voin lisätä uusia kategorioita langoille
```
INSERT INTO category (date_created, date_modified, name) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)
```

### Moderaattorina voin luoda uusia admin-käyttäjiä
```
INSERT INTO account (date_created, date_modified, name, username, password, role) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?)
```



