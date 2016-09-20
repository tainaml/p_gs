CREATE OR REPLACE FUNCTION article_trigger() RETURNS trigger AS $$
begin
  new.search_vector :=
     setweight(to_tsvector(COALESCE(new.title, '')), 'A')  || 
     setweight(to_tsvector(COALESCE(new.text, '')), 'B');
  return new;
end
$$ LANGUAGE plpgsql;


CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON article_article FOR EACH ROW EXECUTE PROCEDURE article_trigger();

update article_article set search_vector =  (setweight(to_tsvector(COALESCE(article_article.title, '')), 'A')  || 
     setweight(to_tsvector(COALESCE(article_article.text, '')), 'B'));

vacuum full;

