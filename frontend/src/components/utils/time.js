/**
 * Formats a duration in seconds as "mm:ss", or "h:mm:ss" once it's an hour
 * or longer. Used by anything displaying a running or completed timer.
 */
export const formatTime = (totalSeconds = 0) => {
  const hrs = Math.floor(totalSeconds / 3600);
  const mins = Math.floor((totalSeconds % 3600) / 60);
  const secs = totalSeconds % 60;

  const mm = String(mins).padStart(2, "0");
  const ss = String(secs).padStart(2, "0");

  return hrs > 0 ? `${hrs}:${mm}:${ss}` : `${mm}:${ss}`;
};

/**
 * Parses a "mm:ss" or plain-seconds string (as typed into an editable timer
 * field) back into a whole number of seconds. Invalid input parses to 0.
 */
export const parseTime = (str) => {
  if (typeof str === "string" && str.includes(":")) {
    const [m, s] = str.split(":").map(Number);
    return (m || 0) * 60 + (s || 0);
  }
  return Number(str) || 0;
};
