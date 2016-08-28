from db import Database

db = Database()

"""
CREATE TABLE `user` IF NOT EXISTS (
`id` INT(11) NOT NULL AUTO_INCREMENT ,
`name` VARCHAR(255) NOT NULL ,
`email` VARCHAR(255) NOT NULL ,
`phone` VARCHAR(255) NOT NULL ,
`phone_mob` VARCHAR(255) NOT NULL ,
`status` INT(11) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
"""