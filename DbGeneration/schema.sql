CREATE TABLE professors (
	id INTEGER PRIMARY KEY,
	name text,
	profile_full_text text,
	dept text
);
CREATE UNIQUE INDEX unique_name on professors(name);
CREATE TABLE profile_links (
	id INTEGER PRIMARY KEY,
	link text,
	type text,
       	scraped int default(0),
       	name_found default(0)
);
CREATE UNIQUE INDEX unique_link on profile_links(link);
