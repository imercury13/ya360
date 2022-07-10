---
permalink: /news/
---
# Что нового?

{% assign filtered_posts = site.posts | where: "categories == 'news'" %}

{% for post in filtered_posts %}
  {{ post.title }}
{% endfor %}

{% for category in site.categories %}
  {% if category[0] == "news" %}
  <ul>
    {% for post in category[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a> {{ post.date | date: "%d.%m.%Y" }}</li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %}
