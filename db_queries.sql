use PTC;
select * from user_info;
select * from auth_info;
delete from auth_info where user_name='user_name';
select count(user_name) from auth_info where user_name = 'user_name';
CALL register_user('example_user', 'example@example.com', 'hashed_password', 1, 'answer', 1, @output_message);
DELIMITER $$
CREATE DEFINER=`dbs`@`localhost` PROCEDURE `register_user`(
in user_name VARCHAR(20), 
in email VARCHAR(20), 
in pwd_hash VARCHAR(256), 
in security_question_id varchar(45),
in sq_answer varchar(30),
in role_id int,
out message varchar(60)
)
BEGIN
	DECLARE user_count INT;

    -- Check if the user already exists
    SELECT COUNT(*) INTO user_count
    FROM auth_info
    WHERE user_name = user_name;
	
    -- If the user does not exist, insert a new record
    IF user_count = 0 THEN
        INSERT INTO auth_info (user_name, email, pwd_hash, security_question_id, sq_answer, role_id)
        VALUES (user_name, email, pwd_hash, security_question_id, sq_answer, role_id);
        SET message = 'User successfully registered.';
    ELSE
        -- If the user already exists, set the return message
        SET message = 'User already exists.';
    END IF;
    
    select message;
END$$
DELIMITER ;
SELECT @output_message;


INSERT INTO auth_info (user_name, email, pwd_hash, security_question_id, sq_answer, role_id) 
values ('user_name', 'name@gmail.com', 'pwd', 'q01', 'Answer1', 1);

use PTC;
CREATE TABLE user_info(
  `user_name` varchar(30) NOT NULL,
  `email` varchar(45) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `date_of_birth` date NOT NULL,
  `address_line1` varchar(30) DEFAULT NULL,
  `address_line2` varchar(30) DEFAULT NULL,
  `area_code` varchar(10) NOT NULL,
  PRIMARY KEY (`user_name`),
  UNIQUE KEY `email_UNIQUE` (`email`)
);


CREATE TABLE task_template(
  `content_id` INT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(30) NOT NULL,
  `name` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `field_count` INT NULL,
  `field_list` JSON NULL,
  PRIMARY KEY (`content_id`),
  FOREIGN KEY (`user_name`) REFERENCES `publisher_info`(`user_name`)
);

CREATE TABLE ptc_publisher_task (
	ptask_id int not null auto_increment,
    content_id int not null,
    task_name varchar(60),
    number_of_slots INT,
    task_type varchar(30),
    points INT,
    PRIMARY KEY (`ptask_id`),
    foreign key (`content_id`) references task_template(`content_id`)
    );
    
create table ptc_client_task (
	ctask_id int not null auto_increment,
    ptask_id int not null,
    task_name varchar(60),
    points INT,
    primary key(`ctask_id`),
    foreign key(`ptask_id`) references ptc_publisher_task(`ptask_id`)
);


CREATE TABLE authentication (
	auth_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(30) NOT NULL unique,
    hashed_pwd varchar(256) NOT NULL,
    security_question varchar(80) NOT NULL,
    sq_answer varchar(80) NOT NULL,
    role_id INT,
    primary key (`auth_id`),
    foreign key (`user_name`) references user_info(`user_name`)
);

CREATE TABLE user_role (
	role_id INT NOT NULL unique,
    role varchar(20),    
    primary key (`role_id`)    
);

