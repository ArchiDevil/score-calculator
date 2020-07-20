DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS stats;
DROP TABLE IF EXISTS login_password;

CREATE TABLE team (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team_name TEXT UNIQUE NOT NULL
);

CREATE TABLE member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  member_name TEXT NOT NULL,
  factor REAL NOT NULL CHECK (factor<=1.0 AND factor>=0.0),
  number_team INTEGER NOT NULL
);

CREATE TABLE stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team_id INTEGER NOT NULL,
  sprint_name TEXT NOT NULL,
  result INTEGER NOT NULL
);

CREATE TABLE login_password (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userlogin TEXT UNIQUE NOT NULL,
  userpassword TEXT NOT NULL,
  id_command INTEGER NOT NULL
);

INSERT INTO login_password (userlogin, userpassword, id_command) VALUES ("good", "pbkdf2:sha256:150000$dFGNPY9B$b17f13b33dc62b0ca95126c6a100fad9b15d7cf73072dfe6b289833b1199bb41", 3);
INSERT INTO login_password (userlogin, userpassword, id_command) VALUES ("bad", "pbkdf2:sha256:150000$6hzyuS0V$beab9a20230e3eb2555fa66c0d6666fdb0dba8bf60e272f7d29414c5e555ed9d", 2);

INSERT INTO member (member_name, factor, number_team) VALUES ("Anna", 0.2, 1);
INSERT INTO member (member_name, factor, number_team) VALUES ("Alisa", 0.3, 1);

INSERT INTO member (member_name, factor, number_team) VALUES ("Sasha", 0.4, 2);
INSERT INTO member (member_name, factor, number_team) VALUES ("Stepan", 0.5, 2);

INSERT INTO member (member_name, factor, number_team) VALUES ("Tasha", 0.6, 3);
INSERT INTO member (member_name, factor, number_team) VALUES ("Tomas", 0.7, 3);

INSERT INTO stats (team_id, sprint_name, result) VALUES (1, "Ollala", 15);
INSERT INTO stats (team_id, sprint_name, result) VALUES (1, "Oppapa", 45);
