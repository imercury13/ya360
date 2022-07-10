---
permalink: /news/
---
# Что нового?

{% assign filtered_posts = site.posts | where: 'categories', 'categories == news' %}

{% filtered_posts %}

{% for category in site.categories %}
  {% if category[0] == "news" %}
  <ul>
    {% for post in category[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a> {{ post.date | date: "%d.%m.%Y" }}</li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %}
