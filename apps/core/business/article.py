from apps.taxonomy.service import business as Business

def save_taxonomies(article_instance=None, data=None):

    taxonomies = Business.save_taxonomies_for_model(article_instance, data['taxonomies'])







