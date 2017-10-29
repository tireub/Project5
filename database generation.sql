SET NAMES utf8;

DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Parenthood;
DROP TABLE IF EXISTS Elements;
DROP TABLE IF EXISTS Saved_searches;

CREATE TABLE Categories (
	id smallint(6) unsigned NOT NULL AUTO_INCREMENT,
	name varchar(40) NOT NULL,
	elem_count smallint(6) unsigned NOT NULL,
	PRIMARY KEY (id)
)
ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE Parenthood (
	category smallint(6) unsigned NOT NULL,
	parent_category smallint(6) unsigned NOT NULL
	PRIMARY KEY (category,parent_category)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Elements (
	id mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
	name varchar(40) NOT NULL,
	link varchar(200) NOT NULL,
	category_id smallint(6) unsigned NOT NULL,
	ingredients text,
	nutrition_grade AS grade tinyint(1) unsigned,
	brand varchar(40) DEFAULT NULL,
	stores varchar(40) DEFAULT NULL,
	PRIMARY KEY (id)
)
ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE Saved_searches (
	id smallint(6) unsigned NOT NULL AUTO_INCREMENT,
	search_date date,
	search_id smallint NOT NULL,
	serach_replacement mediumint NOT NULL,
	PRIMARY KEY (id)
)
ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
