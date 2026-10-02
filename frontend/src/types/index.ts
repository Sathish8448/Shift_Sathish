export interface Profile {
  id: string;
  full_name: string;
  mobile_number: string;
  role: 'admin' | 'user';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Shift {
  id: string;
  name: string;
  start_time: string;
  end_time: string;
  display_order: number;
  created_at: string;
}

export interface Schedule {
  id: string;
  user_id: string;
  shift_id: string;
  schedule_date: string;
  month_year: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface PlannedLeave {
  id: string;
  user_id: string;
  leave_date: string;
  reason: string | null;
  created_at: string;
  updated_at: string;
}

export interface PublicHoliday {
  id: string;
  holiday_date: string;
  name: string;
  created_at: string;
}

export interface Message {
  id: string;
  user_id: string;
  content: string;
  created_at: string;
}

export interface MessageReadStatus {
  user_id: string;
  last_read_at: string;
  created_at: string;
  updated_at: string;
}

export interface VisitorLog {
  id: string;
  user_id: string;
  visited_at: string;
  visit_date: string;
}
