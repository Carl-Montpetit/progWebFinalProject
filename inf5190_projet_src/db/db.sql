drop table if exists piscines_installations_aquatiques;
drop table if exists glissades;
drop table if exists patinoires;

create table piscines_installations_aquatiques
(
    id             integer primary key autoincrement,
    id_uev         integer,
    type           varchar(100),
    nom            varchar(100),
    arrondissement varchar(100),
    adresse        varchar(100),
    propriete      varchar(100),
    gestion        varchar(100),
    point_x        integer,
    point_y        integer,
    equipement     varchar(100),
    longitude      integer,
    latitude       integer
);

create table glissades
(
    id        integer primary key autoincrement,
    nom       varchar(200),
    nom_arr   varchar(100),
    cle       varchar(100),
    date_maj  text,
    ouvert    numeric,
    deblaye   numeric,
    condition varchar(100)
);

create table patinoires
(
    id         integer primary key autoincrement,
    nom_arr    varchar(200),
    nom_pat    varchar(100),
    date_heure text,
    ouvert     numeric,
    deblaye    numeric,
    arrose     numeric,
    resurface  numeric
);