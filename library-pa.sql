-- drop the existing database if it exists
DROP DATABASE IF EXISTS library;

-- create a new database
CREATE DATABASE library;
Use library;

CREATE TABLE `books` (
  `bookid` int NOT NULL AUTO_INCREMENT,
  `booktitle` varchar(45) DEFAULT NULL,
  `author` varchar(45) DEFAULT NULL,
  `category` varchar(15) DEFAULT NULL,
  `yearofpublication` int DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`bookid`)
);

CREATE TABLE `borrowers` (
  `borrowerid` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(45) NOT NULL,
  `familyname` varchar(45) NOT NULL,
  `dateofbirth` date DEFAULT NULL,
  `housenumbername` varchar(15) DEFAULT NULL,
  `street` varchar(20) DEFAULT NULL,
  `town` varchar(25) DEFAULT NULL,
  `city` varchar(25) DEFAULT NULL,
  `postalcode` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`borrowerid`)
);

CREATE TABLE `bookcopies` (
  `bookcopyid` int NOT NULL AUTO_INCREMENT,
  `bookid` int NOT NULL,
  `format` varchar(12) NOT NULL,
  PRIMARY KEY (`bookcopyid`),
  KEY `bookid_idx` (`bookid`),
  CONSTRAINT `bookid` FOREIGN KEY (`bookid`) REFERENCES `books` (`bookid`) ON DELETE CASCADE
);

CREATE TABLE `loans` (
  `loanid` int NOT NULL AUTO_INCREMENT,
  `bookcopyid` int NOT NULL,
  `borrowerid` int NOT NULL,
  `loandate` date NOT NULL,
  `returned` tinyint DEFAULT NULL,
  PRIMARY KEY (`loanid`),
  KEY `borrowedbook_idx` (`bookcopyid`),
  KEY `borrower_idx` (`borrowerid`),
  CONSTRAINT `borrowedbook` FOREIGN KEY (`bookcopyid`) REFERENCES `bookcopies` (`bookcopyid`),
  CONSTRAINT `borrower` FOREIGN KEY (`borrowerid`) REFERENCES `borrowers` (`borrowerid`)
);

INSERT INTO books VALUES(56,'Harry Potter and the Order of the Phoenix','J. K. Rowling','Fiction',2011,"Dark times have come to Hogwarts. After the Dementors' attack on his cousin Dudley, Harry Potter knows that Voldemort will stop at nothing to find him. There are many who deny the Dark Lord's return, but Harry is not alone: a secret order gathers at Grimmauld Place to fight against the Dark forces. Harry must allow Professor Snape to teach him how to protect himself from Voldemort's savage assaults on his mind. But they are growing stronger by the day and Harry is running out of time ...");
INSERT INTO books VALUES(34,'The Wind in the Willows','Kenneth Grahame ','Fiction',1908, "The Wind in the Willows is a children's novel by Kenneth Grahame, first published in England in 1908. The story focuses on four anthropomorphized animals in a pastoral version of Edwardian England. The novel is notable for its mixture of mysticism, adventure, morality and camaraderie, and celebrated for its evocation of the nature of the Thames Valley. It is a delightful and captivating tale that is sure to delight.");
INSERT INTO books VALUES(7455, 'Python Crash Course', 'Eric Matthes', 'Non-Fiction', 2019, "A fast-paced, no-nonsense, updated guide to programming in Python.");

INSERT INTO bookcopies VALUES (3, 56, 'Hardcover');
INSERT INTO bookcopies VALUES (11, 56, 'Paperback');
INSERT INTO bookcopies VALUES (27, 56, 'eBook');
INSERT INTO bookcopies VALUES (81, 56, 'Audio Book');
INSERT INTO bookcopies VALUES (19, 56, 'Paperback');
INSERT INTO bookcopies VALUES (93, 56, 'Paperback');
INSERT INTO bookcopies VALUES (56, 56, 'Paperback');
INSERT INTO bookcopies VALUES (4, 7455, 'Paperback');
INSERT INTO bookcopies VALUES (25, 7455, 'Hardcover');
INSERT INTO bookcopies VALUES (34, 7455, 'Paperback');
INSERT INTO bookcopies VALUES (49, 7455, 'Paperback');
INSERT INTO bookcopies VALUES (234, 7455, 'Paperback');
INSERT INTO bookcopies VALUES (47, 34, 'Paperback');
INSERT INTO bookcopies VALUES (4789, 34, 'Illustrated');
INSERT INTO bookcopies VALUES (7, 34, 'Paperback');


INSERT INTO borrowers VALUES (7523, 'Simon', 'Charles', '1980-07-24', 'Elizabeth Lodge','Elmwood Drive','Lincoln', 'Lincoln', '7608');
INSERT INTO borrowers VALUES (65233, 'Charlie', 'Venz', '2013-11-05', '2', 'Windsor Rd', 'Hoon Hay', 'Christchurch', '8034');
INSERT INTO borrowers VALUES (533, 'Zhe', 'Wang', '2001-04-12', 'Apartment 3', 'Prebblewood Drive', 'Prebbleton', 'Prebbleton','7601');
INSERT INTO borrowers VALUES (659, 'Di', 'Wang', '2003-11-25', '26', 'Kahu Rd', 'Lincoln', 'Lincoln', '7608');

INSERT INTO loans VALUES(2333546,  93 , 7523,'2022-11-30', 0);
INSERT INTO loans VALUES(2355546,  4789 , 65233,'2022-10-10', 0);
INSERT INTO loans VALUES(2395546,  4789 , 533,'2022-01-01', 1);
INSERT INTO loans VALUES(236,  4789 , 7523,'2021-12-10', 1);
INSERT INTO loans VALUES(54656,  47 , 659,'2022-07-28', 0);
INSERT INTO loans VALUES(5468956,  34 , 659,'2022-07-28', 1);
