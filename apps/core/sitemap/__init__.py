from .users import UserSitemap
from .article import ArticleSitemap, ArticleOfficialSitemap
from .question import QuestionSitemap

sitemaps = {
    'profiles': UserSitemap,
    'articles': ArticleSitemap,
    'official': ArticleOfficialSitemap,
    'questions': QuestionSitemap,
}
