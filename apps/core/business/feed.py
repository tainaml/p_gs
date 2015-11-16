from apps.taxonomy.service import business as BusinessTaxonomy

def save_taxonomies(feed_instance=None, data=None):

    taxs = []
    for item in feed_instance.communities.all():
        taxs.append(item.taxonomy)

    taxonomies = BusinessTaxonomy.save_taxonomies_for_model(feed_instance, taxs)
    return taxonomies


def save_communities(feed_instance=None, data=None):

    temp_communities = data.get('communities', [])
    feed_instance.communities = temp_communities
    feed_instance.save()
    return feed_instance