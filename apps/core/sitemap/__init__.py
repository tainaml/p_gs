from .users import UserSitemap
from .article import ArticleSitemap, ArticleOfficialSitemap
from .question import QuestionSitemap
from .community import CommunitySitemap
from .category import CategorySitemap

sitemaps = {
    'profiles': UserSitemap,
    'articles': ArticleSitemap,
    'official': ArticleOfficialSitemap,
    'questions': QuestionSitemap,
    'communities': CommunitySitemap,
    'categories': CategorySitemap,
}
