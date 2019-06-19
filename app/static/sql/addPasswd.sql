select *
from student

ALTER table student 
add COLUMN passwd CHAR(25)

alter TABLE student 
update student
set passwd=NULL

ALTER TABLE student
drop COLUMN passwd