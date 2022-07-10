---
permalink: /news/
---
### Что нового?

{% for category in site.categories %}
  {% if category[0] == "news" %}</h3>
  <ul>
    {% for post in category[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %}

<ul>
  {% for post in site.posts if site.categories == "news" %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
