DO $$ 
DECLARE
    tbl_name text;
BEGIN
    FOR tbl_name IN
        SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP TABLE IF EXISTS %I CASCADE;', tbl_name);
    END LOOP;
END $$;