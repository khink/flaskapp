-- sqlite 2 here, so no "if exists" or "autoincrement"
drop table students;
create table students (
  id integer primary key,
  name text not null,
  class text not null
);