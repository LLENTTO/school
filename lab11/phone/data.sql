CREATE OR REPLACE FUNCTION search_phonebook(pattern VARCHAR)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone
    FROM phonebook p
    WHERE p.first_name ILIKE '%' || pattern || '%'
       OR p.last_name ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%'
    ORDER BY p.first_name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_first_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE phonebook
    SET phone = p_phone
    WHERE first_name = p_first_name;

    IF NOT FOUND THEN
        INSERT INTO phonebook (first_name, phone)
        VALUES (p_first_name, p_phone)
        ON CONFLICT (phone) DO NOTHING;
    END IF;
    COMMIT;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_multiple_users(
    p_names VARCHAR[],
    p_phones VARCHAR[],
    OUT invalid_data JSON
)
LANGUAGE plpgsql AS $$
DECLARE
    i INTEGER;
    temp_invalid JSONB[] := '{}';
    phone_pattern VARCHAR := '^[0-9]{10}$';
BEGIN
    CREATE TEMP TABLE temp_invalid (name VARCHAR, phone VARCHAR) ON COMMIT DROP;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ phone_pattern THEN
            INSERT INTO phonebook (first_name, phone)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            INSERT INTO temp_invalid (name, phone)
            VALUES (p_names[i], p_phones[i]);
        END IF;
    END LOOP;

    SELECT json_agg(json_build_object('name', name, 'phone', phone))
    INTO invalid_data
    FROM temp_invalid;

    IF invalid_data IS NULL THEN
        invalid_data := '[]'::json;
    END IF;

    COMMIT;
END;
$$;

CREATE OR REPLACE FUNCTION get_phonebook_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone
    FROM phonebook p
    ORDER BY p.first_name
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_phonebook_entry(
    p_field VARCHAR,
    p_value VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_field = 'username' THEN
        DELETE FROM phonebook WHERE first_name = p_value;
    ELSIF p_field = 'phone' THEN
        DELETE FROM phonebook WHERE phone = p_value;
    ELSE
        RAISE EXCEPTION 'Invalid field: must be "username" or "phone"';
    END IF;
    
    IF NOT FOUND THEN
        RAISE NOTICE 'No records found to delete.';
    END IF;
    
    COMMIT;
END;
$$;