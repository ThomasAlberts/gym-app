
// Page + card: fixes where content sits on the page.
export function PageLayout({ children }) {
  return (
    <div style={styles.page}>
      <div style={styles.card}>
          {children}
      </div>
    </div>
  );
}

// Two panels side by side, wrapping onto separate lines when too narrow.
export function SplitLayout({ left, right }) {
  return (
    <div style={styles.split}>
      <div style={styles.splitLeft}>{left}</div>
      <div style={styles.splitRight}>{right}</div>
    </div>
  );
}

// Centered loading / error message.
export function PageStatus({ children, error = false }) {
  return (
    <div style={styles.statusBlock}>
      <p style={{ ...styles.statusText, color: error ? "#B23A31" : "#8C7F6B" }}>
        {children}
      </p>
    </div>
  );
}

const styles = {
  page: {
    display: "flex",
    justifyContent: "center",
    padding: "24px 16px",
    minHeight: "100vh",
    boxSizing: "border-box",
  },
  card: {
    width: "100%",
    maxWidth: 920,
    background: "#FFFFFF",
    border: "1px solid #ECE6DA",
    borderRadius: 16,
    boxShadow: "0 1px 2px rgba(36,30,23,0.04), 0 10px 30px rgba(36,30,23,0.06)",
    padding: "26px 28px 30px",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
  },
  split: {
    display: "flex",
    flexWrap: "wrap",
    alignItems: "flex-start",
    gap: 32,
  },
  splitLeft: {
    flex: "1 1 320px",
    minWidth: 280,
    maxWidth: 460,
    margin: "0 auto",
  },
  splitRight: {
    flex: "1.15 1 300px",
    minWidth: 280,
  },
  statusBlock: {
    padding: "48px 0",
    textAlign: "center",
  },
  statusText: {
    margin: 0,
    fontSize: 14,
  },
};