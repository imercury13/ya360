---
permalink: /news/
---
# Что нового?

{% for category in site.categories %}
  {% if category[0] == "news" %}
  <ul>
    {% for post in category[1] %}
      <li><a href="{{ post.url }}">{{ post.title }} {{ post.date | date: "%-d %B %Y" }}</a></li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %}
