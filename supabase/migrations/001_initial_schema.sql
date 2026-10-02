-- ============================================================
-- Shift Schedule Management — Database Schema
-- Run this entire script in Supabase SQL Editor
-- ============================================================

-- 1. Helper: auto-update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- 2. PROFILES TABLE
-- ============================================================
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    mobile_number TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Prevent users from changing their own role via RLS update
CREATE OR REPLACE FUNCTION prevent_role_change()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.role IS DISTINCT FROM OLD.role THEN
        -- Only allow if the update is done via service_role (bypasses RLS)
        -- Through RLS, normal users hit this trigger, so we block role changes
        NEW.role = OLD.role;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_role_change_prevention
    BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION prevent_role_change();

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- 3. Admin check helper
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM profiles
        WHERE id = auth.uid() AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = public;

-- Profiles RLS policies
CREATE POLICY "profiles_select" ON profiles
    FOR SELECT TO authenticated
    USING (auth.uid() = id OR is_admin());

CREATE POLICY "profiles_update_own" ON profiles
    FOR UPDATE TO authenticated
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- ============================================================
-- 4. SHIFTS TABLE
-- ============================================================
CREATE TABLE shifts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    start_time TIME,
    end_time TIME,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE shifts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "shifts_select" ON shifts
    FOR SELECT TO authenticated USING (true);
CREATE POLICY "shifts_insert" ON shifts
    FOR INSERT TO authenticated WITH CHECK (is_admin());
CREATE POLICY "shifts_update" ON shifts
    FOR UPDATE TO authenticated USING (is_admin());
CREATE POLICY "shifts_delete" ON shifts
    FOR DELETE TO authenticated USING (is_admin());

-- Seed default shift types
INSERT INTO shifts (name, start_time, end_time, display_order) VALUES
    ('Morning', '06:00:00', '14:00:00', 1),
    ('Evening', '14:00:00', '22:00:00', 2),
    ('Night',   '22:00:00', '06:00:00', 3),
    ('General', '09:00:00', '18:00:00', 4);

-- ============================================================
-- 5. SCHEDULES TABLE
-- ============================================================
CREATE TABLE schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    shift_id UUID NOT NULL REFERENCES shifts(id) ON DELETE RESTRICT,
    schedule_date DATE NOT NULL,
    month_year TEXT NOT NULL,  -- e.g. '2026-09' for fast month queries
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, schedule_date)
);

CREATE INDEX idx_schedules_date ON schedules(schedule_date);
CREATE INDEX idx_schedules_month ON schedules(month_year);
CREATE INDEX idx_schedules_user ON schedules(user_id);

CREATE TRIGGER update_schedules_updated_at
    BEFORE UPDATE ON schedules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE schedules ENABLE ROW LEVEL SECURITY;

CREATE POLICY "schedules_select" ON schedules
    FOR SELECT TO authenticated USING (true);
CREATE POLICY "schedules_insert" ON schedules
    FOR INSERT TO authenticated WITH CHECK (is_admin());
CREATE POLICY "schedules_update" ON schedules
    FOR UPDATE TO authenticated USING (is_admin());
CREATE POLICY "schedules_delete" ON schedules
    FOR DELETE TO authenticated USING (is_admin());

-- ============================================================
-- 6. PLANNED LEAVES TABLE
-- ============================================================
CREATE TABLE planned_leaves (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    leave_date DATE NOT NULL,
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_leaves_date ON planned_leaves(leave_date);
CREATE INDEX idx_leaves_user ON planned_leaves(user_id);

CREATE TRIGGER update_planned_leaves_updated_at
    BEFORE UPDATE ON planned_leaves
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE planned_leaves ENABLE ROW LEVEL SECURITY;

CREATE POLICY "leaves_select" ON planned_leaves
    FOR SELECT TO authenticated USING (true);
CREATE POLICY "leaves_insert" ON planned_leaves
    FOR INSERT TO authenticated WITH CHECK (is_admin());
CREATE POLICY "leaves_update" ON planned_leaves
    FOR UPDATE TO authenticated USING (is_admin());
CREATE POLICY "leaves_delete" ON planned_leaves
    FOR DELETE TO authenticated USING (is_admin());

-- ============================================================
-- 7. PUBLIC HOLIDAYS TABLE
-- ============================================================
CREATE TABLE public_holidays (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    holiday_date DATE NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_holidays_date ON public_holidays(holiday_date);

ALTER TABLE public_holidays ENABLE ROW LEVEL SECURITY;

CREATE POLICY "holidays_select" ON public_holidays
    FOR SELECT TO authenticated USING (true);
CREATE POLICY "holidays_insert" ON public_holidays
    FOR INSERT TO authenticated WITH CHECK (is_admin());
CREATE POLICY "holidays_update" ON public_holidays
    FOR UPDATE TO authenticated USING (is_admin());
CREATE POLICY "holidays_delete" ON public_holidays
    FOR DELETE TO authenticated USING (is_admin());

-- ============================================================
-- 8. MESSAGES TABLE
-- ============================================================
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_created ON messages(created_at);

ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "messages_select" ON messages
    FOR SELECT TO authenticated USING (true);
CREATE POLICY "messages_insert" ON messages
    FOR INSERT TO authenticated
    WITH CHECK (user_id = auth.uid());
CREATE POLICY "messages_delete" ON messages
    FOR DELETE TO authenticated USING (is_admin());

-- Enable Supabase Realtime for messages
ALTER PUBLICATION supabase_realtime ADD TABLE messages;

-- ============================================================
-- 9. MESSAGE READ STATUS TABLE
-- ============================================================
CREATE TABLE message_read_status (
    user_id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
    last_read_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_message_read_status_updated_at
    BEFORE UPDATE ON message_read_status
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE message_read_status ENABLE ROW LEVEL SECURITY;

CREATE POLICY "read_status_select" ON message_read_status
    FOR SELECT TO authenticated USING (user_id = auth.uid());
CREATE POLICY "read_status_insert" ON message_read_status
    FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid());
CREATE POLICY "read_status_update" ON message_read_status
    FOR UPDATE TO authenticated USING (user_id = auth.uid());

-- ============================================================
-- 10. VISITOR LOGS TABLE
-- ============================================================
CREATE TABLE visitor_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    visited_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    visit_date DATE NOT NULL
);

CREATE INDEX idx_visitors_date ON visitor_logs(visit_date);
CREATE INDEX idx_visitors_user ON visitor_logs(user_id);

ALTER TABLE visitor_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "visitors_insert" ON visitor_logs
    FOR INSERT TO authenticated
    WITH CHECK (user_id = auth.uid());
CREATE POLICY "visitors_select" ON visitor_logs
    FOR SELECT TO authenticated USING (is_admin());
