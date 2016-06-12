{% from "./redis/map.jinja" import redis_settings with context %}

install-redis:
  pkg.installed:
    - name: {{ redis_settings.pkg_name }}
    {% if redis_settings.version is defined %}
    - version: {{ redis_settings.version }}
    {% endif %}
