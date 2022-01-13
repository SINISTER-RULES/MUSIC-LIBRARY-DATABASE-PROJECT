To use the MUSIC LIBRARY PROJECT follow these simple steps:

------------------------------STEP 1------------------------------

1. Run "pip install -r /your project folder/requirements.txt" to install all the modules



------------------------------STEP 2------------------------------

1.  Setup you MySQL Server with username='root' and password='pass123'

2.  Create database using the following command:
    create database music_library;

3.  Traverse into the database
    use music_library;

4.  Create the tables:
    1.  create table users(
            username varchar(100),
            password varchar(100),
            primary key(username, password)
        );

    2.  create table song(
            name varchar(100),
            genre varchar(100),
            singer varchar(100),
            rating double,
            rel_year int(4),
            duration double,
            primary key(name, singer)
        );

    3.  create table singer(
            name varchar(100),
            song_name varchar(100),
            rating double,
            primary key(name, song_name),
            foreign key(name, song_name) references song(singer, name) on delete cascade
        );

    4.  create table album(
            genre varchar(100),
            song_name varchar(100),
            singer_name varchar(100),
            primary key(genre, song_name),
            foreign key(genre, song_name) references song(genre, name) on delete cascade
        );

    5.  create table playlist(
            name varchar(100),
            song_name varchar(100),
            rating double,
            duration double,
            primary key(name, song_name),
            foreign key(name, song_name) references song(singer, name) on delete cascade
        );


------------------------------STEP 3------------------------------

1.  After creating the tables just run the run.py file and ENJOY!!!!