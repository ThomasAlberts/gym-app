import { useState, useEffect, useMemo, useRef } from "react";
import api from "../api/axios.js";
import BodyDiagram, { MUSCLE_GROUPS, STRAIN_LEVELS, strainLevel } from "../components/muscle_map/BodyDiagram.jsx";
import {PageLayout} from "../components/page_styling/PageLayout.jsx";

const GROUP_OF = {
  chest_upper: "chest",
  chest_mid: "chest",
  chest_lower: "chest",
  front_delts: "shoulders",
  side_delts: "shoulders",
  rear_delts: "shoulders",
  lats: "back",
  rhomboids: "back",
  biceps: "biceps",
  triceps: "triceps",
  forearms: "forearms",
  abs: "abs",
  obliques: "obliques",
  traps: "traps",
  upper_traps: "traps",
  mid_traps: "traps",
  lower_back: "lower_back",
  hip_flexors: "hip_flexors",
  glutes: "glutes",
  quads: "quads",
  adductors: "adductors",
  abductors: "abductors",
  hamstrings: "hamstrings",
  calves: "calves",
};

const LEAVES_OF_GROUP = Object.entries(GROUP_OF).reduce((acc, [leaf, group]) => {
  (acc[group] ||= []).push(leaf);
  return acc;
}, {});

const LEAF_LABEL = {
  chest_upper: "Chest (upper)",
  chest_mid: "Chest (mid)",
  chest_lower: "Chest (lower)",
  front_delts: "Front delts",
  side_delts: "Side delts",
  rear_delts: "Rear delts",
  lats: "Lats",
  rhomboids: "Rhomboids",
  traps: "Traps (general)",
  upper_traps: "Traps (upper)",
  mid_traps: "Traps (mid)",
};

const LEAF_LIMITS = {
  chest_upper: 10,
  chest_mid: 12,
  chest_lower: 10,
  front_delts: 10,
  side_delts: 10,
  rear_delts: 10,
  lats: 10,
  rhomboids: 10,
  biceps: 10,
  triceps: 10,
  forearms: 10,
  abs: 10,
  obliques: 10,
  traps: 10,
  upper_traps: 10,
  mid_traps: 10,
  lower_back: 10,
  hip_flexors: 10,
  glutes: 10,
  quads: 12,
  adductors: 10,
  abductors: 10,
  hamstrings: 10,
  calves: 10,
};

const DEFAULT_LIMITS = Object.entries(GROUP_OF).reduce((acc, [leaf, group]) => {
  acc[group] = (acc[group] || 0) + (LEAF_LIMITS[leaf] || 0);
  return acc;
}, {});

const LEVEL_COLOR = Object.fromEntries(STRAIN_LEVELS.map((l) => [l.id, l.color]));

function getLastMonday() {
  const now = new Date();
  const day = now.getDay(); // 0 = Sunday ... 6 = Saturday
  const diffFromMonday = day === 0 ? 6 : day - 1;
  const monday = new Date(now);
  monday.setHours(0, 0, 0, 0);
  monday.setDate(now.getDate() - diffFromMonday);
  return monday;
}

// Rolls leaf-level strain (keyed by raw backend Muscle values) up to
// panel-level strain (keyed by diagram panel id) for feeding BodyDiagram.
function groupStrainFrom(leafStrain) {
  const grouped = {};
  Object.entries(leafStrain).forEach(([leaf, value]) => {
    const group = GROUP_OF[leaf];
    if (!group) return;
    grouped[group] = (grouped[group] || 0) + value;
  });
  return grouped;
}

export default function MuscleMap() {
  const [leafStrain, setLeafStrain] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [hoveredGroup, setHoveredGroup] = useState(null);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const rowRefs = useRef({});

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get("/exercise/since-monday");
        if (cancelled) return;
        console.log(res)
        setLeafStrain(res.data?.muscle_strain || {});
      } catch (e) {
        console.error(e);
        if (!cancelled) setError("Could not load muscle data.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const since = useMemo(() => getLastMonday(), []);

  const strain = useMemo(() => groupStrainFrom(leafStrain), [leafStrain]);

  const rows = useMemo(() => {
    return MUSCLE_GROUPS.map(({ id, label }) => {
      const value = strain[id] || 0;
      const limit = DEFAULT_LIMITS[id] || 0;
      const ratio = limit > 0 ? value / limit : 0;
      return { id, label, value, limit, ratio, level: strainLevel(value, limit) };
    }).sort((a, b) => b.ratio - a.ratio || b.value - a.value);
  }, [strain]);

  // Per-leaf info (label/value/limit) handed to BodyDiagram so it can draw
  // the on-hover breakdown dropdown itself, without needing to know
  // anything about the backend Muscle enum.
  const leafInfo = useMemo(() => {
    const info = {};
    Object.keys(GROUP_OF).forEach((leaf) => {
      info[leaf] = {
        label: LEAF_LABEL[leaf] || leaf,
        value: leafStrain[leaf] || 0,
        limit: LEAF_LIMITS[leaf] || 0,
      };
    });
    return info;
  }, [leafStrain]);

  // Clicking a panel on the diagram pins a selection; scroll the matching
  // row in the breakdown list into view so the highlight is actually seen.
  useEffect(() => {
    if (selectedGroup && rowRefs.current[selectedGroup]) {
      rowRefs.current[selectedGroup].scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }, [selectedGroup]);

  const sinceLabel = since.toLocaleDateString("en-GB", { day: "numeric", month: "short" });

  return (
      <PageLayout>
        <header style={styles.header}>
          <div>
            <h2 style={styles.title}>Muscle load</h2>
            <p style={styles.subtitle}>Sets logged since {sinceLabel}</p>
          </div>
        </header>
        {loading ? (
          <div style={styles.statusBlock}>
            <p style={styles.statusText}>Loading muscle map…</p>
          </div>
        ) : error ? (
          <div style={styles.statusBlock}>
            <p style={{ ...styles.statusText, color: "#B23A31" }}>{error}</p>
          </div>
        ) : (
          <div style={styles.mainRow}>
            <div style={styles.diagramsCol}>
              <div style={styles.diagramWrap}>
                <div style={styles.diagramItem}>
                  <BodyDiagram
                    view="front"
                    values={strain}
                    limits={DEFAULT_LIMITS}
                    onHoverMuscle={setHoveredGroup}
                    selectedId={selectedGroup}
                    onSelectMuscle={setSelectedGroup}
                    leavesOf={LEAVES_OF_GROUP}
                    leafInfo={leafInfo}
                  />
                </div>
                <div style={styles.diagramItem}>
                  <BodyDiagram
                    view="back"
                    values={strain}
                    limits={DEFAULT_LIMITS}
                    onHoverMuscle={setHoveredGroup}
                    selectedId={selectedGroup}
                    onSelectMuscle={setSelectedGroup}
                    leavesOf={LEAVES_OF_GROUP}
                    leafInfo={leafInfo}
                  />
                </div>
              </div>

              <div style={styles.legend}>
                {STRAIN_LEVELS.map(({ id, label, color }) => (
                  <div key={id} style={styles.legendItem}>
                    <span style={{ ...styles.legendDot, background: color }} />
                    <span style={styles.legendLabel}>{label}</span>
                  </div>
                ))}
              </div>
            </div>

            <div style={styles.breakdownCol}>
              <h3 style={styles.breakdownTitle}>Breakdown by muscle</h3>
              <ul style={styles.rowList}>
                {rows.map(({ id, label, value, limit, ratio, level }) => {
                  const leaves = LEAVES_OF_GROUP[id] || [];
                  const isSelected = selectedGroup === id;
                  const expanded = (hoveredGroup === id || isSelected) && leaves.length > 1;
                  return (
                    <li key={id} ref={(el) => (rowRefs.current[id] = el)}>
                      <div
                        style={{ ...styles.row, ...(isSelected ? styles.rowSelected : null) }}
                        onClick={() => setSelectedGroup((current) => (current === id ? null : id))}
                      >
                        <span style={styles.rowLabel}>{label}</span>
                        <span style={styles.barTrack}>
                          <span
                            style={{
                              ...styles.barFill,
                              width: `${Math.min(ratio, 1) * 100}%`,
                              background: LEVEL_COLOR[level],
                            }}
                          />
                        </span>
                        <span style={styles.rowValue}>
                          {value.toFixed(1)}
                          <span style={styles.rowValueLimit}> / {limit || "–"}</span>
                        </span>
                      </div>
                      {expanded && (
                        <ul style={styles.subRowList}>
                          {leaves.map((leaf) => {
                            const leafValue = leafStrain[leaf] || 0;
                            const leafLimit = LEAF_LIMITS[leaf] || 0;
                            const leafRatio = leafLimit > 0 ? leafValue / leafLimit : 0;
                            const leafLevel = strainLevel(leafValue, leafLimit);
                            return (
                              <li key={leaf} style={styles.subRow}>
                                <span style={styles.subRowLabel}>{LEAF_LABEL[leaf] || leaf}</span>
                                <span style={styles.barTrack}>
                                  <span
                                    style={{
                                      ...styles.barFill,
                                      width: `${Math.min(leafRatio, 1) * 100}%`,
                                      background: LEVEL_COLOR[leafLevel],
                                    }}
                                  />
                                </span>
                                <span style={styles.rowValue}>
                                  {leafValue.toFixed(1)}
                                  <span style={styles.rowValueLimit}> / {leafLimit || "–"}</span>
                                </span>
                              </li>
                            );
                          })}
                        </ul>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        )}
      </PageLayout>
  );
}

const styles = {
    header: {
    display: "flex",
    alignItems: "flex-start",
    justifyContent: "space-between",
    gap: 12,
    marginBottom: 22,
  },
  title: {
    margin: 0,
    fontSize: 21,
    fontWeight: 650,
    letterSpacing: "-0.01em",
    color: "#241E17",
  },
  subtitle: {
    margin: "4px 0 0",
    fontSize: 13,
    color: "#8C7F6B",
  },
  statusBlock: {
    padding: "48px 0",
    textAlign: "center",
  },
  statusText: {
    fontSize: 14,
    color: "#8C7F6B",
    margin: 0,
  },
  // Two panels side by side when there's room; each has a sane min-width,
  // so the flex container wraps them onto their own line once the page
  // gets too narrow to fit both — no media query needed.
  mainRow: {
    display: "flex",
    flexWrap: "wrap",
    alignItems: "flex-start",
    gap: 32,
  },
  diagramsCol: {
    flex: "1 1 320px",
    minWidth: 280,
    maxWidth: 460,
    margin: "0 auto",
  },
  breakdownCol: {
    flex: "1.15 1 300px",
    minWidth: 280,
  },
  diagramWrap: {
    background: "#FFFFFF",
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
    alignItems: "flex-start",
    gap: 8,
  },
  diagramItem: {
    flex: "1 1 160px",
    minWidth: 150,
    maxWidth: 220,
  },
  legend: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px 18px",
    justifyContent: "center",
    padding: "18px 0 0",
    marginTop: 14,
    borderTop: "1px solid #EFEFEF",
  },
  legendItem: {
    display: "flex",
    alignItems: "center",
    gap: 6,
  },
  legendDot: {
    width: 9,
    height: 9,
    borderRadius: "50%",
    display: "inline-block",
  },
  legendLabel: {
    fontSize: 12,
    color: "#6E6252",
  },
  breakdownTitle: {
    margin: "0 0 12px",
    fontSize: 13,
    fontWeight: 600,
    color: "#4A4136",
  },
  rowList: {
    listStyle: "none",
    margin: 0,
    padding: 0,
    display: "flex",
    flexDirection: "column",
    gap: 9,
  },
  row: {
    display: "grid",
    gridTemplateColumns: "88px 1fr 62px",
    alignItems: "center",
    gap: 10,
    padding: "4px 6px",
    margin: "-4px -6px",
    borderRadius: 8,
    cursor: "pointer",
    transition: "background 0.15s ease, box-shadow 0.15s ease",
  },
  rowSelected: {
    background: "#EDF4FA",
    boxShadow: "inset 0 0 0 1.5px #2f6fa3",
  },
  rowLabel: {
    fontSize: 12.5,
    color: "#4A4136",
  },
  barTrack: {
    display: "block",
    height: 6,
    borderRadius: 4,
    background: "#F0F0F0",
    overflow: "hidden",
  },
  barFill: {
    display: "block",
    height: "100%",
    borderRadius: 4,
  },
  rowValue: {
    fontSize: 12,
    fontWeight: 600,
    color: "#4A4136",
    textAlign: "right",
    fontVariantNumeric: "tabular-nums",
  },
  rowValueLimit: {
    fontWeight: 400,
    color: "#A79A85",
  },
  subRowList: {
    listStyle: "none",
    margin: "6px 0 0",
    padding: "0 0 0 16px",
    display: "flex",
    flexDirection: "column",
    gap: 7,
    borderLeft: "2px solid #EFEFEF",
  },
  subRow: {
    display: "grid",
    gridTemplateColumns: "88px 1fr 62px",
    alignItems: "center",
    gap: 10,
  },
  subRowLabel: {
    fontSize: 11.5,
    color: "#8C7F6B",
  },
};
