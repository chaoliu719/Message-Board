drop table if exists entries;
drop table if exists user;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null,
  rec datetime not null,
  user text not null
);
create table user (
  username text primary key,
  password text not null
);
INSERT INTO user VALUES ('admin', 'default');