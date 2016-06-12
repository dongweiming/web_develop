{% if grains['os'] == 'RedHat' %}
   python-dev: python-devel
   git: git
{% elif grains['os'] in ('Debian', 'Ubuntu') %}
   python-dev: python-dev
   git: git-core
{% endif %}