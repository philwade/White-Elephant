create table family (
    id integer primary key autoincrement,
    name string not null unique
);
create table year (
    id integer primary key autoincrement,
    name string not null unique
);
create table user (
    id integer primary key autoincrement,
    name string not null unique,
    email string not null unique,
    admin boolean default false,
    family_id integer references family(id) on delete set null
);
create table match (
    id integer primary key autoincrement,
    giver_id integer references user(id),
    receiver_id integer references user(id),
    year_id integer references year(id)
);
