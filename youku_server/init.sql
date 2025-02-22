create table User(
    id int auto_increment primary key,
    name varchar(255),
    pwd varchar(255),
    is_vip int,
    is_locked int,
    user_type varchar(255),
    register_time timestamp
);

CREATE table Movie(
  id int auto_increment primary key,
  name varchar(255),
  path varchar(255),
  is_free int,
  file_md5 varchar(255),
  user_id int,
  is_delete int,
  upload_time timestamp
);

create table Notice(
    id int auto_increment primary key ,
    title varchar(255),
    content varchar(255),
    user_id int,
    create_time timestamp
);

CREATE TABLE DownloadRecord (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    download_time TIMESTAMP
);


