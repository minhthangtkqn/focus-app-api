create table cards (
    _id VARCHAR(255),
    title VARCHAR(255),
    description VARCHAR(255),
    _created VARCHAR(255),
	_updated VARCHAR(255)
);


insert into cards (_id, title, description, _created, _updated) 
values 
	('420e72a4-7a71-4045-b29d-a5a3f8aff4bf', 'Table', 'a device with four legs and a flat surface.', '2025-01-12T07:50:32.019992+00:00', null),
	('6984c72a-6e24-4d6c-b4d5-a7e00add74ff', 'Chair', 'a seat for one person that has a back, usually four legs, and sometimes two arms.', '2025-01-12T07:50:32.019992+00:00', null),
	('13997e6d-0d5f-4841-8451-8f59886740da', 'Comb', 'a flat piece of plastic, wood, or metal with a thin row of long, narrow parts along one side, used to tidy and arrange your hair.', '2025-01-12T07:50:32.019992+00:00', null),
	('4010f0a9-0112-4c89-9b81-9698624cc7ae', 'Paper', 'thin, flat material made from crushed wood or cloth, used for writing, printing, or drawing on.', '2025-01-12T07:50:32.019992+00:00', null),
	('4010f0a9-0112-4c89-9b81-9698624cc7ab', 'Smartphone', 'A pocket-sized computer that combines a mobile phone with internet access, a camera, and various apps.', '2025-01-12T07:50:32.019992+00:00', null),
	('4010f0a9-0112-4c89-9b81-9698624cc7ac', 'Bottle', 'A container, usually made of glass or plastic, with a narrow neck for holding liquids.', '2025-01-12T07:50:32.019992+00:00', null),
	('4010f0a9-0112-4c89-9b81-9698624cc7aa', 'Monitor', 'A display device that visually presents information from a computer.', '2025-01-12T07:50:32.019992+00:00', null),
	('dbc4910d-229b-49d2-8ac6-bf76ea468a50', 'month', 'a period of about four weeks, especially one of the twelve periods into which a year is divided.', '2025-01-12T07:50:32.019992+00:00', null),
	('550ca6b1-0cad-4a11-aa02-b4d21f73e3c2', 'Piano', 'A keyboard musical instrument with 88 keys, producing sounds through hammers striking strings.', '2025-01-12T07:50:32.019992+00:00', null),
	('5d8888ad-f62e-424c-95e3-894d6fca3ed1', 'Coat', 'An outer garment worn for warmth and protection from the elements.', '2025-01-12T07:50:32.019992+00:00', null),
	('4b76d2c0-e44d-48f8-99b1-79d649ba1263', 'Shirt', 'A garment worn on the upper body, typically with sleeves.', '2025-01-12T07:50:32.019992+00:00', null),
	('a90c6adb-1832-4249-b6f0-d1911b9f0e94', 'Ruler', 'A flat, straight tool used for measuring length or drawing straight lines.', '2025-01-12T07:50:32.019992+00:00', null),
	('37f90f13-06c3-47ab-b27d-389892ab93d2', 'Pen', 'A writing instrument that uses ink to create marks on paper.', '2025-01-12T07:50:32.019992+00:00', null),
	('ddbe2885-cc6d-4058-9345-16a58da086fc', 'Window', 'An opening in a wall or vehicle that allows light and air to pass through.', '2025-01-12T07:50:32.019992+00:00', null),
	('9c9a84eb-5db0-45dd-aa60-0663d295fa21', 'Cup', 'A small, open container used for drinking, typically made of ceramic, glass, or plastic.', '2025-01-12T07:50:32.019992+00:00', null),
	('90650070-c2a8-4fdb-8338-480b2ff163b7', 'CPU', 'Brain of the computer, performs calculations.', '2025-01-12T07:50:32.019992+00:00', null)
;

-- alter table cards 
-- add _updated VARCHAR(255);
-- delete from cards;
-- select * from cards where _id = '420e72a4-7a71-4045-b29d-a5a3f8aff4bf';

