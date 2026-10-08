import { PageLayout } from "../components/page_styling/PageLayout.jsx";

const honesty = [
  "Alleen de meeste happy paths zijn getest. Doe je iets onverwachts, dan kan er iets stukgaan.",
  "Er ligt een backlog met bekende bugs. Sommige ga je tegenkomen.",
];
const knownIssues = [
  {
    title: "Bugs",
    items: [
      "Na een refresh van de pagina binnen de workout page verdwijnt niet-opgeslagen data (nog te beslissen: fixen of accepteren)",
      'Bij het klikken op "New workout" staat er soms al een oefening voordat hij is begonnen',
      "Na het openen van een opgeslagen workout toont een oefening de volledige geschiedenis, terwijl alleen de relevante geschiedenis nodig is (bijvoorbeeld: een oefening van een latere datum wordt getoond bij een eerdere workout)",
      "Bij het openen van een opgeslagen workout loopt de timer door; alleen bij pauze staat hij stil. Oplossing: een aparte pagina om een workout alleen in te zien, of zorgen dat de timer niet doorloopt",
      "Tab in een set gaat van reps naar weight, maar je tabt ook langs de tijdvelden, waardoor je extra moet tabben om bij het gewenste veld te komen",
      'Als de lijst op het dashboard leeg is, staat er "kan niet laden" in plaats van dat de lijst leeg is',
    ],
  },
  {
    title: "Ontbrekende features",
    items: [
      "Workouts vooraf aanmaken en plannen voor later",
      "Gebruikers zelf oefeningen laten creëren, nu kunnen ze alleen kiezen uit bestaande, vooraf gedefinieerde oefeningen",
      "Vooraf gemaakte workouts verdelen en plannen over een week, maand of jaar",
      "Een mailsysteem voor info, accountaanmaak, bugmeldingen en feature-aanvragen",
      "Een set toevoegen neemt reps en weight over van de vorige set",
      "De functie suggest exercise uitbreiden naar suggest workout: met AI en eerdere workouts een workout voorstellen, met keuze uit spiergroepen die je nog niet getraind hebt, of gewoon een full-body workout",
      "RPE toevoegen: vooraf bepalen bij het plannen en de ervaren RPE vastleggen tijdens de workout",
      "Een alternatief voor tijdgebonden oefeningen zoals planks, dat goed in het systeem past (oefeningen bestaan nu alleen uit sets en reps)",
      "Statistieken op basis van je workouts, oefeningen, reps en kg's",
      "Gewichtsmeter (lichaamsgewicht bijhouden)",
      "Samenstelbare info op je profiel die je wilt delen met andere gebruikers",
    ],
  },
  {
    title: "Verbeteringen",
    items: [
      "De navbar aanpassen en aanvullen (eerst afstemmen met Anek)",
      "De notes bij een oefening anders tonen, de huidige weergave is onhandig",
      "Het dashboard aanpassen of samenvoegen met het profiel",
    ],
  },
  {
    title: "Technisch (achter de schermen)",
    items: [
      "Componenten kleiner maken, vooral WorkoutSession",
      "Meer testen op authenticatie en rechten",
      "Meer testdekking buiten de happy paths",
      "Een alternatief zoeken voor de huidige AI-prompts, die soms traag zijn (gratis versie)",
    ],
  },
];

function GroupList({ groups }) {
  return (
    <>
      {groups.map((group) => (
        <div key={group.title}>
          <h3>{group.title}</h3>
          <ul>
            {group.items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ))}
    </>
  );
}

export default function Welcome() {
  return (
    <PageLayout>
      <h1>Welkom! 👋</h1>
      <p>
        Leuk dat je mijn app uitprobeert. Hij is gemaakt om je trainingen en
        oefeningen bij te houden, en hij werkt: <strong>zolang je de gebaande
        paden volgt.</strong>
      </p>

      <section>
        <h2>🎯 Focus voor nu</h2>
        <p>
          Voor nu: features uitbreiden, bugs fixen, alles testen en als laatste
          de styling. Zo krijg ik sneller input van de app testers en meer inzicht
          in gaten in de app. Het doel is het gebruikersgemak te vergroten.
        </p>
      </section>

      <section>
        <h2>🎨 Over het uiterlijk</h2>
        <p>
          De styling staat op de allerlaatste plaats van mijn prioriteitenlijst,
          en eerlijk gezegd mis ik op dat vlak ook de ambitie. De app is
          functioneel, niet mooi. Dat is een bewuste keuze, geen ongelukje.
        </p>
      </section>

      <section>
        <h2>⚠️ Even eerlijk zijn</h2>
        <ul>
          {honesty.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>🐛 Bekende bugs &amp; ontbrekende features</h2>
        <GroupList groups={knownIssues} />
      </section>

      <section>
        <h2>🐞 Iets gevonden?</h2>
        <p>
          Meld het gerust, dan gaat het op de backlog. Of in elk geval: op de
          lijst.
        </p>
      </section>
    </PageLayout>
  );
}
