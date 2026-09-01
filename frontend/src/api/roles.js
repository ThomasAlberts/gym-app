// roles can be: "anonymous", "user", "coach", "admin"
const NAV_ITEMS = [
  { label: "Profile", path: "/profile", roles: ["user", "coach", "admin"] },
  { label: "Dashboard", path: "/dashboard", roles: ["coach", "admin"] },
  { label: "Admin Panel", path: "/admin", roles: ["admin"] },
];
