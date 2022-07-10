---
permalink: /news/
---
### Что нового?
<ul>
  {% for post in site.posts if site.posts.categories == "news" %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
