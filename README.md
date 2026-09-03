# gym-app

## Optie 1: Docker (aanbevolen)

Zorgt dat backend + frontend in containers draaien, met hot reload op codewijzigingen.

```powershell
docker compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

**Wanneer moet je wat doen?**

| Situatie | Actie |
|---|---|
| Code aangepast (.py / .jsx) | Niks, hot reload pakt het automatisch op |
| Dependency toegevoegd (pyproject.toml / package.json) | `docker compose up --build` |
| `.env` aangepast | `docker compose restart backend` |
| Rare/vastgelopen staat | `docker compose down` gevolgd door `docker compose up --build` |

### Database resetten (Docker)

`database.db` staat gewoon op je eigen schijf (via de volume mount), dus:

```powershell
docker compose down
rm database.db
docker compose up --build
```

---

## Optie 2: Handmatig (zonder Docker)

### Backend

```powershell
# eenmalig: installeer packages
py -m pip install -r backend/requirements.txt
python -m pip install uv

# backend starten
uv run uvicorn backend.main:app --reload
# of
py -m uv run uvicorn backend.main:app --reload
```

Database resetten:

```powershell
rm database.db
```

### Frontend

```powershell
cd frontend
npm install
npm audit
npm audit fix
npm run dev
```