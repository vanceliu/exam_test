Drop SCHEMA IF EXISTS Test;
Create schema Test;
Use Test;
CREATE TABLE test_table
(
    id         Int(10)    NOT NULL AUTO_INCREMENT,
    name       varchar(60) NOT NULL,
    status     BOOLEAN    NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

INSERT INTO `test_table` (`id`, `name`, `status`)
	VALUES (1, 'name', 0);