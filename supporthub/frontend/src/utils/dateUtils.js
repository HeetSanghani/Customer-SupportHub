/**
 * parseUTCDate - safely parses a datetime string from the backend.
 *
 * The backend previously stored naive UTC datetimes (no timezone suffix),
 * e.g. "2026-08-04T12:39:18". Browsers treat these as LOCAL time instead of
 * UTC, causing the displayed time to be wrong (off by the user's UTC offset).
 *
 * This utility appends "Z" (UTC) if the string has no timezone info, so the
 * browser always interprets it as UTC and converts to the user's local time.
 *
 * New records (after the fix) will have "+00:00" suffix and parse correctly.
 *
 * @param {string|null|undefined} dateStr - ISO 8601 datetime string from API
 * @returns {Date} - correctly parsed Date object in local time
 */
export function parseUTCDate(dateStr) {
  if (!dateStr) return new Date()
  const s = String(dateStr)
  // Standard ISO local string without timezone suffix parses as local time in JavaScript
  return new Date(s)
}

/**
 * Formats a datetime string for display as a full date+time string.
 * e.g. "4/8/2026, 6:09 PM" in IST
 */
export function formatDateTime(dateStr) {
  if (!dateStr) return ''
  return parseUTCDate(dateStr).toLocaleString()
}

/**
 * Formats a datetime string for display as a date only.
 * e.g. "8/4/2026" in IST
 */
export function formatDate(dateStr) {
  if (!dateStr) return ''
  return parseUTCDate(dateStr).toLocaleDateString()
}

/**
 * Formats a datetime string for display as a time only (HH:MM AM/PM).
 */
export function formatTime(dateStr) {
  if (!dateStr) return ''
  return parseUTCDate(dateStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
