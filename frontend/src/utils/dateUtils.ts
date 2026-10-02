const IST_TIMEZONE = 'Asia/Kolkata';

/**
 * Get current date/time as a Date object.
 */
export const getISTNow = (): Date => {
  return new Date();
};

/**
 * Get today's date string in IST as 'YYYY-MM-DD'.
 */
export const getISTDateString = (): string => {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: IST_TIMEZONE,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date());
};

/**
 * Get current month-year in IST as 'YYYY-MM' (matches database month_year column).
 */
export const getISTMonthYear = (): string => {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: IST_TIMEZONE,
    year: 'numeric',
    month: '2-digit',
  }).formatToParts(new Date());
  const year = parts.find(p => p.type === 'year')?.value;
  const month = parts.find(p => p.type === 'month')?.value;
  return `${year}-${month}`;
};

/**
 * Format a date string for short display: '23 Sep 2026'
 */
export const formatDateIST = (dateStr: string): string => {
  const date = new Date(dateStr + 'T00:00:00');
  return new Intl.DateTimeFormat('en-IN', {
    timeZone: IST_TIMEZONE,
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(date);
};

/**
 * Format a datetime string for display: '23 Sep 2026, 2:30 PM'
 */
export const formatDateTimeIST = (dateStr: string): string => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('en-IN', {
    timeZone: IST_TIMEZONE,
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  }).format(date);
};

/**
 * Format a date string for full display: 'Tuesday, 23 September 2026'
 */
export const formatFullDateIST = (dateStr: string): string => {
  const date = new Date(dateStr + 'T00:00:00');
  return new Intl.DateTimeFormat('en-IN', {
    timeZone: IST_TIMEZONE,
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(date);
};

/**
 * Format time for display: '2:30 PM'
 */
export const formatTimeIST = (dateStr: string): string => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('en-IN', {
    timeZone: IST_TIMEZONE,
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  }).format(date);
};

/**
 * Convert 'YYYY-MM' to display format: 'September 2026'
 */
export const getMonthYearDisplay = (monthYear: string): string => {
  const [year, month] = monthYear.split('-');
  const date = new Date(parseInt(year), parseInt(month) - 1, 1);
  return new Intl.DateTimeFormat('en-IN', {
    month: 'long',
    year: 'numeric',
  }).format(date);
};

/**
 * Get previous month in 'YYYY-MM' format.
 */
export const getPrevMonth = (monthYear: string): string => {
  const [year, month] = monthYear.split('-');
  const date = new Date(parseInt(year), parseInt(month) - 1, 1);
  date.setMonth(date.getMonth() - 1);
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  return `${y}-${m}`;
};

/**
 * Get next month in 'YYYY-MM' format.
 */
export const getNextMonth = (monthYear: string): string => {
  const [year, month] = monthYear.split('-');
  const date = new Date(parseInt(year), parseInt(month) - 1, 1);
  date.setMonth(date.getMonth() + 1);
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  return `${y}-${m}`;
};

/**
 * Format a time string like '06:00:00' to '6:00 AM'
 */
export const formatShiftTime = (timeStr: string | null): string => {
  if (!timeStr) return '';
  const [hours, minutes] = timeStr.split(':').map(Number);
  const period = hours >= 12 ? 'PM' : 'AM';
  const displayHour = hours % 12 || 12;
  return `${displayHour}:${String(minutes).padStart(2, '0')} ${period}`;
};
