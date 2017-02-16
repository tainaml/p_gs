CREATE OR REPLACE FUNCTION article_trigger() RETURNS trigger AS $$
begin
  new.search_vector :=
     setweight(to_tsvector(COALESCE(new.title, '')), 'A')  || 
     setweight(to_tsvector(COALESCE(new.text, '')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION question_trigger() RETURNS trigger AS $$
begin
  new.search_vector :=
     setweight(to_tsvector(COALESCE(new.title, '')), 'A')  ||
     setweight(to_tsvector(COALESCE(new.description, '')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION profilestatus_trigger() RETURNS trigger AS $$
begin
  new.search_vector :=
     setweight(to_tsvector(COALESCE(new.text, '')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;


CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON article_article FOR EACH ROW EXECUTE PROCEDURE article_trigger();

CREATE TRIGGER tsvectorupdate_question BEFORE INSERT OR UPDATE
    ON question_question FOR EACH ROW EXECUTE PROCEDURE question_trigger();


CREATE TRIGGER tsvectorupdate_profilestatus BEFORE INSERT OR UPDATE
    ON feed_profilestatus FOR EACH ROW EXECUTE PROCEDURE profilestatus_trigger();


update article_article set search_vector =  (setweight(to_tsvector(COALESCE(article_article.title, '')), 'A')  || 
     setweight(to_tsvector(COALESCE(article_article.text, '')), 'B'));

update question_question set search_vector =  (setweight(to_tsvector(COALESCE(question_question.title, '')), 'A')  ||
     setweight(to_tsvector(COALESCE(question_question.description, '')), 'B'));

update feed_profilestatus set search_vector =  setweight(to_tsvector(COALESCE(feed_profilestatus.text, '')), 'B');

vacuum full;

