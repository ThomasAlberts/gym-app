import { useNavigate } from "react-router-dom";
import Authenticator from "../authenticator/Authenticator";
import NavBarItems from "./NavItems";

export default function Navbar() {
  const navigate = useNavigate();

  return (
    <nav
      style={{
        padding: "1rem",
        background: "#eee",
        display: "flex",
        justifyContent: "space-between",
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        zIndex: 1000,
        boxSizing: "border-box",
      }}
    >
      <div style={{ cursor: "pointer" }} onClick={() => navigate("/")}>
        Gym App
      </div>

      <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
        <NavBarItems />
        <Authenticator />
      </div>
    </nav>
  );
}
