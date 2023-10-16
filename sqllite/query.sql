-- Active: 1687099515824@@127.0.0.1@3306

SELECT * FROM boxes;

SELECT * FROM freight;

insert into
    boxes (box_name, height, width, length)
values ('b1', 2, 2, 1)
insert into
    boxes (box_name, height, width, length)
values ('k2', 1, 3, 1)
insert into
    boxes (box_name, height, width, length)
values ('4', 2, 1, 1)
insert into
    freight (container_id, box_id)
values ('cont1', 2);

insert into freight (container_id, box_id) values ('cont1', 3);

insert into freight (container_id, box_id) values ('cont2', 2);

CREATE VIEW IF NOT EXISTS CONTAINERS AS 
	select
	    container_id,
	    round(sum(x * y * z), 2) as occupied_volume
	from freight f
	    left join boxes b on f.box_id = b.id
	group by
CONTAINER_ID; 

select * from containers;