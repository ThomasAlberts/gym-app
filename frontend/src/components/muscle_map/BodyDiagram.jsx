import { useState } from "react";

export const MUSCLE_GROUPS = [
  { id: "shoulders", label: "Shoulders" },
  { id: "chest", label: "Chest" },
  { id: "biceps", label: "Biceps" },
  { id: "triceps", label: "Triceps" },
  { id: "forearms", label: "Forearms" },
  { id: "abs", label: "Abs" },
  { id: "obliques", label: "Obliques" },
  { id: "back", label: "Back" },
  { id: "traps", label: "Traps" },
  { id: "lower_back", label: "Lower back" },
  { id: "hip_flexors", label: "Hip flexors" },
  { id: "glutes", label: "Glutes" },
  { id: "quads", label: "Quads" },
  { id: "adductors", label: "Adductors" },
  { id: "hamstrings", label: "Hamstrings" },
  { id: "calves", label: "Calves" },
];

// Single source of truth for the four load states, shared with any legend.
export const STRAIN_LEVELS = [
  { id: "none", label: "Not trained", color: "#E4D6BC" },
  { id: "low", label: "Building volume", color: "#82A374" },
  { id: "mid", label: "Nearing limit", color: "#E0A857" },
  { id: "high", label: "At or over limit", color: "#BD4C41" },
];

const SKIN = "#EAD9C0";
const OUTLINE = "#2A1B10";
const OUTLINE_W = 3;
const LEVEL_COLOR = Object.fromEntries(STRAIN_LEVELS.map((l) => [l.id, l.color]));
const LABEL_BY_ID = Object.fromEntries(MUSCLE_GROUPS.map((g) => [g.id, g.label]));

export function strainLevel(value, limit) {
  if (!value || value <= 0) return "none";
  if (!limit || limit <= 0) return "low";
  const ratio = value / limit;
  if (ratio >= 1) return "high";
  if (ratio >= 0.7) return "mid";
  return "low";
}

export default function BodyDiagram({
  view = "front",
  values = {},
  limits = {},
  onHoverMuscle,
  selectedId = null,
  onSelectMuscle,
  leavesOf = {},
  leafInfo = {},
}) {
  // `hover` carries both the id (for cross-instance highlighting, since
  // left/right panels of a group share one id) and the exact rect that
  // was entered (for anchoring the breakdown dropdown).
  const [hover, setHover] = useState(null);
  const hoveredId = hover?.id ?? null;

  const colorFor = (id) => LEVEL_COLOR[strainLevel(values[id] || 0, limits[id])];

  // Fake voxel lighting: a light band along the top/left edge, a dark band
  // along the bottom/right edge. Alpha-blended so it works over any fill.
  const shade = (x, y, w, h) => {
    const vBand = Math.max(2, Math.min(h * 0.14, 10));
    const hBand = Math.max(2, Math.min(w * 0.14, 10));
    return (
      <g pointerEvents="none">
        <rect x={x} y={y} width={w} height={vBand} fill="#ffffff" opacity="0.16" />
        <rect x={x} y={y} width={hBand} height={h} fill="#ffffff" opacity="0.12" />
        <rect x={x} y={y + h - vBand} width={w} height={vBand} fill="#000000" opacity="0.14" />
        <rect x={x + w - hBand} y={y} width={hBand} height={h} fill="#000000" opacity="0.12" />
      </g>
    );
  };

  // A plain skin-colored panel (no muscle group attached).
  const skinBlock = (x, y, w, h, key) => (
    <g key={key}>
      <rect x={x} y={y} width={w} height={h} fill={SKIN} stroke={OUTLINE} strokeWidth={OUTLINE_W} />
      {shade(x, y, w, h)}
    </g>
  );

  const muscle = (id, x, y, w, h, key) => {
    const isHovered = hoveredId === id;
    const isSelected = selectedId === id;

    let stroke = OUTLINE;
    let strokeWidth = OUTLINE_W;
    if (isSelected) {
      stroke = "#2f6fa3";
      strokeWidth = OUTLINE_W + 2;
    }
    if (isHovered) {
      stroke = "#fff6e6";
      strokeWidth = OUTLINE_W + 2;
    }

    return (
      <g
        key={key || id}
        onPointerEnter={() => {
          setHover({ id, x, y, w, h });
          onHoverMuscle?.(id);
        }}
        onPointerLeave={() => {
          setHover((current) => (current?.id === id ? null : current));
          onHoverMuscle?.(null);
        }}
        onPointerCancel={() => {
          setHover((current) => (current?.id === id ? null : current));
          onHoverMuscle?.(null);
        }}
        onClick={() => onSelectMuscle?.(selectedId === id ? null : id)}
        style={{ cursor: "pointer", touchAction: "manipulation", WebkitTapHighlightColor: "transparent" }}
      >
        <rect x={x} y={y} width={w} height={h} fill={colorFor(id)} stroke={stroke} strokeWidth={strokeWidth} />
        {shade(x, y, w, h)}
        {isSelected && !isHovered && (
          <rect x={x} y={y} width={w} height={h} fill="#3a86c8" opacity="0.16" pointerEvents="none" />
        )}
        {isHovered && (
          <rect x={x} y={y} width={w} height={h} fill="#ffffff" opacity="0.22" pointerEvents="none" />
        )}
      </g>
    );
  };

  const renderHoverBreakdown = () => {
    if (!hover) return null;
    const leaves = leavesOf[hover.id];
    if (!leaves || leaves.length === 0) return null;

    const isMulti = leaves.length > 1;
    const width = 138;
    const rowH = 15;
    const headerH = isMulti ? 18 : 0;
    const rows = isMulti ? leaves : [null]; // null = "just show the group itself"
    const height = headerH + rows.length * rowH + (isMulti ? 8 : 12);

    let tx = hover.x + hover.w + 6;
    if (tx + width > 236) tx = hover.x - width - 6;
    tx = Math.max(4, Math.min(tx, 240 - width - 4));
    const ty = Math.max(4, Math.min(hover.y, 440 - height - 4));

    const font = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";

    return (
      <g pointerEvents="none">
        <rect x={tx} y={ty} width={width} height={height} rx="4" fill="#241E17" opacity="0.95" stroke="#000000" strokeWidth="1" />
        {isMulti && (
          <text x={tx + 8} y={ty + 13} fontFamily={font} fontSize="10.5" fontWeight="700" fill="#ffffff">
            {LABEL_BY_ID[hover.id] || hover.id}
          </text>
        )}
        {rows.map((leaf, i) => {
          // Multi-leaf: one row per leaf muscle. Solo: one row for the
          // group itself, using its own aggregate value/limit.
          const label = leaf ? leafInfo[leaf]?.label || leaf : LABEL_BY_ID[hover.id] || hover.id;
          const value = leaf ? leafInfo[leaf]?.value || 0 : values[hover.id] || 0;
          const limit = leaf ? leafInfo[leaf]?.limit || 0 : limits[hover.id] || 0;
          const rowY = ty + headerH + i * rowH + (isMulti ? 10 : 17);
          const color = LEVEL_COLOR[strainLevel(value, limit)];
          return (
            <g key={leaf || "self"}>
              <rect x={tx + 8} y={rowY - 8} width="7" height="7" fill={color} stroke="#000000" strokeWidth="0.5" />
              <text x={tx + 19} y={rowY} fontFamily={font} fontSize={isMulti ? "9.5" : "10.5"} fontWeight={isMulti ? "400" : "700"} fill="#f5ede0">
                {label}
              </text>
              <text x={tx + width - 8} y={rowY} textAnchor="end" fontFamily={font} fontSize="9.5" fill="#c9bda8">
                {value.toFixed(1)}/{limit || 0}
              </text>
            </g>
          );
        })}
      </g>
    );
  };

  const front = view === "front";

  return (
    <svg
      viewBox="0 0 240 440"
      width="100%"
      style={{
        maxWidth: 320,
        display: "block",
        margin: "0 auto",
        background: "#ffffff",
        WebkitTapHighlightColor: "transparent",
      }}
    >
      <rect x="0" y="0" width="240" height="440" fill="#ffffff" />
      <ellipse cx="120" cy="398" rx="66" ry="8" fill="#000" opacity="0.08" />

      {/* ---- HEAD ---- */}
      {skinBlock(90, 6, 60, 54, "head")}
      {front ? (
        <>
          <rect x="102" y="26" width="9" height="9" fill="#2a1b10" />
          <rect x="129" y="26" width="9" height="9" fill="#2a1b10" />
          <rect x="111" y="44" width="18" height="4" fill="#7a3b2e" />
        </>
      ) : (
        <rect x="90" y="6" width="60" height="18" fill="#6b4a34" stroke={OUTLINE} strokeWidth={OUTLINE_W} />
      )}

      {/* ---- LEFT ARM ---- */}
      {muscle("shoulders", 48, 60, 34, 18, "shoulder-l")}
      {muscle(front ? "biceps" : "triceps", 48, 78, 34, 52, "upperarm-l")}
      {muscle("forearms", 48, 130, 34, 50, "forearm-l")}
      {skinBlock(52, 180, 26, 22, "hand-l")}

      {/* ---- RIGHT ARM ---- */}
      {muscle("shoulders", 158, 60, 34, 18, "shoulder-r")}
      {muscle(front ? "biceps" : "triceps", 158, 78, 34, 52, "upperarm-r")}
      {muscle("forearms", 158, 130, 34, 50, "forearm-r")}
      {skinBlock(162, 180, 26, 22, "hand-r")}

      {/* ---- TORSO ---- */}
      {front ? (
        <>
          {muscle("chest", 82, 60, 36, 30, "chest-l")}
          {muscle("chest", 122, 60, 36, 30, "chest-r")}
          {muscle("obliques", 82, 90, 10, 56, "oblique-l")}
          {muscle("abs", 92, 90, 56, 56, "abs")}
          {muscle("obliques", 148, 90, 10, 56, "oblique-r")}
          {muscle("hip_flexors", 82, 146, 18, 34, "hipflexor-l")}
          {skinBlock(100, 146, 40, 34, "pelvis")}
          {muscle("hip_flexors", 140, 146, 18, 34, "hipflexor-r")}
        </>
      ) : (
        <>
          {muscle("traps", 82, 60, 76, 14, "traps")}
          {muscle("back", 82, 74, 76, 64, "back")}
          <line x1="120" y1="76" x2="120" y2="136" stroke="rgba(0,0,0,0.18)" strokeWidth="2" />
          {muscle("lower_back", 82, 138, 76, 26, "lower-back")}
          {muscle("glutes", 82, 164, 76, 16, "glutes")}
        </>
      )}

      {/* ---- LEFT LEG ---- */}
      {front ? (
        <>
          {muscle("quads", 84, 180, 20, 88, "upperleg-l")}
          {muscle("adductors", 104, 180, 10, 88, "adductor-l")}
        </>
      ) : (
        muscle("hamstrings", 84, 180, 30, 88, "upperleg-l")
      )}
      {muscle("calves", 84, 268, 30, 86, "calf-l")}
      {skinBlock(82, 354, 34, 22, "foot-l")}

      {/* ---- RIGHT LEG ---- */}
      {front ? (
        <>
          {muscle("adductors", 126, 180, 10, 88, "adductor-r")}
          {muscle("quads", 136, 180, 20, 88, "upperleg-r")}
        </>
      ) : (
        muscle("hamstrings", 126, 180, 30, 88, "upperleg-r")
      )}
      {muscle("calves", 126, 268, 30, 86, "calf-r")}
      {skinBlock(124, 354, 34, 22, "foot-r")}

      <text
        x="120"
        y="422"
        textAnchor="middle"
        fontFamily="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
        fontSize="12"
        fontWeight="600"
        letterSpacing="0.5"
        fill="#a89a86"
      >
        {front ? "Front" : "Back"}
      </text>
      {renderHoverBreakdown()}
    </svg>
  );
}
