from flask import render_template
from fourtitude import app, route_restrictions
from fourtitude.article_forms import ArticleForm
from fourtitude.article_models import Article
from fourtitude.managed_object import manage_object, delete_object


def get_article_registry():
    return {
        'Article': {
            'class_name': Article,
            'class_form': ArticleForm
        },
    }


@app.route('/article', methods=['GET', 'POST'])
def list_articles(admin=False):
    all_articles = Article.query.all()
    return render_template(
        'article/page.html',
        admin=admin,
        articles=all_articles,
        title='Articles')


@app.route('/article/manage', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='article_admin')
def article_admin():
    return list_articles(admin=True)


@app.route('/article/manage/<object_class>/', methods=['GET', 'POST'], defaults={'object_id': None})
@app.route('/article/manage/<object_class>/<int:object_id>', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='article_admin')
def manage_article_object(object_class, object_id):
    return manage_object(get_article_registry(), object_class, object_id, 'article_admin')


@app.route('/article/delete/<object_class>/<int:object_id>', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='article_admin')
def delete_article_object(object_class, object_id):
    return delete_object(get_article_registry(), object_class, object_id, 'article_admin')