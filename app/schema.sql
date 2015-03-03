drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	title text not null,
	ingredients text not null,
	review text not null
);
