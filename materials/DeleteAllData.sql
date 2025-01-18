DO
$$
DECLARE
    table_name RECORD;
BEGIN
    FOR table_name IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('TRUNCATE TABLE %I RESTART IDENTITY CASCADE;', table_name.tablename);
    END LOOP;
END;
$$;
