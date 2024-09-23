{% macro generate_schema_name(custom_schema_name, model) %}
    {% if custom_schema_name is none %}
        {{ model['schema'] }}
    {% else %}
        {{ custom_schema_name }}
    {% endif %}
{% endmacro %}