CREATE TABLE auth_info (
  user_name TEXT NOT NULL,
  email TEXT NOT NULL,
  pwd_hash TEXT NOT NULL,
  security_question_id TEXT NOT NULL,
  sq_answer TEXT NOT NULL,
  role_id INTEGER NOT NULL,
  PRIMARY KEY (user_name),
  UNIQUE (user_name)
);

CREATE TABLE ptc_client_task (
  ctask_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  ptask_id INTEGER NOT NULL,
  task_name TEXT DEFAULT NULL,
  points INTEGER DEFAULT NULL,
  data TEXT NOT NULL,
  FOREIGN KEY (ptask_id) REFERENCES ptc_publisher_task (ptask_id)
);

CREATE TABLE ptc_publisher_task (
  ptask_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  user_name TEXT NOT NULL,
  task_name TEXT DEFAULT NULL,
  number_of_slots INTEGER DEFAULT NULL,
  task_type TEXT DEFAULT NULL,
  points INTEGER DEFAULT NULL,
  description TEXT DEFAULT NULL,
  task_data TEXT DEFAULT NULL,
  FOREIGN KEY (user_name) REFERENCES auth_info (user_name)
);

CREATE TABLE user_info (
  user_name TEXT NOT NULL,
  email TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  date_of_birth DATE NOT NULL,
  address_line1 TEXT DEFAULT NULL,
  address_line2 TEXT DEFAULT NULL,
  area_code TEXT NOT NULL,
  PRIMARY KEY (user_name),
  UNIQUE (email)
);

CREATE TABLE user_role (
  role_id INTEGER NOT NULL,
  role TEXT DEFAULT NULL,
  PRIMARY KEY (role_id),
  UNIQUE (role_id)
);
