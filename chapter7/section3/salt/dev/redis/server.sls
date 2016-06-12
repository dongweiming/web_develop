include:
  - redis.common


{% from "redis/map.jinja" import redis_settings with context %}

{% set cfg_version    = redis_settings.cfg_version -%}
{% set cfg_name       = redis_settings.cfg_name -%}
{% set pkg_name       = redis_settings.pkg_name -%}

redis_config:
  file.managed:
    - name: {{ cfg_name }}
    - template: jinja
    - source: salt://redis/files/redis-{{ cfg_version }}.conf.jinja
    - require:
      - pkg: {{ pkg_name }}


redis_service:
  service.{{ redis_settings.svc_state }}:
    - name: {{ redis_settings.svc_name }}
    - enable: {{ redis_settings.svc_onboot }}
    - watch:
      - file: {{ cfg_name }}
    - require:
      - pkg: {{ pkg_name }}
