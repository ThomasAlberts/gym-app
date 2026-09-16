// BodyDiagram.jsx
// Purely presentational: draws a blocky, arcade/voxel-style body (think
// Minecraft skin proportions) and colors each muscle group based on
// `values` vs `limits`.
//
// Usage:
//   <BodyDiagram view="front" values={{ chest: 8, biceps: 3 }} limits={{ chest: 16, biceps: 12 }} />
//
// Construction notes (why it's built this way):
// - Every body part is a flat-sided rectangle (rx=0), not an organic curve.
//   That's the whole "arcade" bit: square head, square torso, square limbs,
//   like a voxel/pixel-art character instead of an anatomically realistic one.
// - Each rectangle gets a bold, fully-opaque outline (not a thin translucent
//   one). Bold outlines between adjacent blocks are what make it read as a
//   grid of colored panels (like a skin texture) rather than a smudge.
// - Muscle-group panels are sized to exactly TILE the torso/limb regions
//   they belong to (no gaps, no overlaps), so the whole figure is always
//   fully covered by either a muscle color or a plain skin block.
// - A generic `shade()` overlay (semi-transparent white top/left band +
//   semi-transparent black bottom/right band) is layered on every block.
//   Because it's alpha-blended rather than a fixed color, it fakes simple
//   voxel lighting on top of ANY fill color, including the dynamic strain
//   colors — no need to precompute a lighter/darker variant per state.
// - Arms/legs are each split into two stacked panels (upper/lower) so two
//   different muscle groups (e.g. biceps vs forearms) can still be shown
//   per limb, even though the limb itself is just two rectangles.
//
// Figure layout (all coordinates in the 240x440 viewBox):
//   head   y  6- 60   x  90-150
//   torso  y 60-180   x  82-158
//   arms   y 60-202   x  48- 82 (left) / 158-192 (right)
//   legs   y180-376   x  84-114 (left) / 126-156 (right)

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
  { id: "glutes", label: "Glutes" },
  { id: "quads", label: "Quads" },
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

export default function BodyDiagram({ view = "front", values = {}, limits = {}, onHoverMuscle }) {
  const [hoveredId, setHoveredId] = useState(null);

  const colorFor = (id) => LEVEL_COLOR[strainLevel(values[id] || 0, limits[id])];
  const titleFor = (id) =>
    `${LABEL_BY_ID[id] || id}: ${(values[id] || 0).toFixed(1)} / ${limits[id] || 0} sets`;

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

  // A muscle-group panel: fill comes from strain color, title carries the
  // tooltip, and it gets the same voxel shading as everything else. When
  // this id matches the currently-hovered muscle, it gets a brighter
  // outline plus a translucent white wash on top — alpha-blended, so it
  // pops the same way regardless of the underlying strain color.
  const muscle = (id, x, y, w, h, key) => {
    const isHovered = hoveredId === id;
    return (
      <g
        key={key || id}
        onMouseEnter={() => {
          setHoveredId(id);
          onHoverMuscle?.(id);
        }}
        onMouseLeave={() => {
          setHoveredId((current) => (current === id ? null : current));
          onHoverMuscle?.(null);
        }}
        style={{ cursor: "pointer" }}
      >
        <rect
          x={x}
          y={y}
          width={w}
          height={h}
          fill={colorFor(id)}
          stroke={isHovered ? "#fff6e6" : OUTLINE}
          strokeWidth={isHovered ? OUTLINE_W + 2 : OUTLINE_W}
        >
          <title>{titleFor(id)}</title>
        </rect>
        {shade(x, y, w, h)}
        {isHovered && (
          <rect x={x} y={y} width={w} height={h} fill="#ffffff" opacity="0.22" pointerEvents="none" />
        )}
      </g>
    );
  };

  const front = view === "front";

  return (
    <svg
      viewBox="0 0 240 440"
      width="100%"
      style={{ maxWidth: 320, display: "block", margin: "0 auto", background: "#ffffff" }}
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
          {skinBlock(82, 146, 76, 34, "pelvis")}
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
      {muscle(front ? "quads" : "hamstrings", 84, 180, 30, 88, "upperleg-l")}
      {muscle("calves", 84, 268, 30, 86, "calf-l")}
      {skinBlock(82, 354, 34, 22, "foot-l")}

      {/* ---- RIGHT LEG ---- */}
      {muscle(front ? "quads" : "hamstrings", 126, 180, 30, 88, "upperleg-r")}
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
    </svg>
  );
}
