from db import Database

db = Database()

if not db.table_exists('courses'):

    install = """
    CREATE TABLE `courses` (
      `id` int(11) NOT NULL,
      `name` varchar(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    INSERT INTO `courses` (`id`, `name`) VALUES
    (1, 'Python-Base'),
    (2, 'Python-Database'),
    (3, 'HTML'),
    (4, 'Java-Base'),
    (5, 'JavaScript-Base');

    CREATE TABLE `user` (
      `id` int(11) NOT NULL,
      `name` varchar(255) NOT NULL,
      `email` varchar(255) NOT NULL,
      `phone` varchar(255) NOT NULL,
      `phone_mob` varchar(255) NOT NULL,
      `status` int(11) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    CREATE TABLE `user_courses` (
      `id` int(11) NOT NULL,
      `user_id` int(11) NOT NULL,
      `course_id` int(11) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    ALTER TABLE `courses`
      ADD PRIMARY KEY (`id`);

    ALTER TABLE `user`
      ADD PRIMARY KEY (`id`);

    ALTER TABLE `user_courses`
      ADD PRIMARY KEY (`id`)
    """

    for q in install.split(';'):
        db.query(q)
