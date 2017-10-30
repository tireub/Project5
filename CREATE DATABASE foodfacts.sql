CREATE DATABASE foodfacts;

SET NAMES utf8;

DROP TABLE IF EXISTS Saved_searches;
DROP TABLE IF EXISTS Parenthood;
DROP TABLE IF EXISTS Elements;
DROP TABLE IF EXISTS Categories;

CREATE TABLE Categories (
	id smallint(6) unsigned NOT NULL AUTO_INCREMENT,
	name varchar(80) NOT NULL,
	off_id varchar(80) NOT NULL,
	elem_count smallint(6) unsigned NOT NULL,
	PRIMARY KEY (id)
)
ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE Parenthood (
	category_id smallint(6) unsigned NOT NULL,
	parent_category_id smallint(6) unsigned NOT NULL
	)
ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Elements (
	id mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
	name varchar(40) NOT NULL,
	link varchar(200) NOT NULL,
	category_id smallint(6) unsigned NOT NULL,
	ingredients text,
	nutrition_grade tinyint(1) unsigned,
	brand varchar(40) DEFAULT NULL,
	stores varchar(40) DEFAULT NULL,
	PRIMARY KEY (id)
)
ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE Saved_searches (
	id smallint(6) unsigned NOT NULL AUTO_INCREMENT,
	search_date date,
	search_id smallint(6) unsigned NOT NULL,
	search_replacement smallint(6) unsigned NOT NULL,
	PRIMARY KEY (id)
)
ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


ALTER TABLE Parenthood ADD CONSTRAINT fk_parenthood_category_id FOREIGN KEY (category_id) REFERENCES 
Categories (id) ON DELETE CASCADE;

ALTER TABLE Parenthood ADD CONSTRAINT fk_parenthood_parent_category_id FOREIGN KEY (parent_category_id)
REFERENCES Categories (id) ON DELETE CASCADE;

ALTER TABLE Elements ADD CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Categories (id)
ON DELETE CASCADE;

ALTER TABLE Saved_searches ADD CONSTRAINT fk_search_id FOREIGN KEY (search_id) REFERENCES 
Categories (id) ON DELETE CASCADE;

ALTER TABLE Saved_searches ADD CONSTRAINT fk_search_replacement_id FOREIGN KEY (search_replacement) 
REFERENCES Categories (id) ON DELETE CASCADE;



