"""Lag fem selvstendige SVG-diagrammer fra sanitiserte begreper.

Krever bare Python 3. Ingen private filer eller nettverk brukes.
"""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent / "diagrammer"
INK = "#172b44"
MUTED = "#526477"
PUSH = "#a54b13"
PULL = "#08776f"
BLUE = "#2159a5"
PARTS = []


def text(x, y, value, size=18, color=INK, weight=400, anchor="start"):
    PARTS.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
                 f'font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')


def begin(title, subtitle, height, description):
    PARTS.clear()
    PARTS.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="{height}" '
                 f'viewBox="0 0 1040 {height}" role="img" aria-labelledby="title desc">')
    PARTS.append(f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>')
    PARTS.append('<defs>')
    for name, color in [("neutral", MUTED), ("push", PUSH), ("pull", PULL)]:
        PARTS.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                     f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                     f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>')
    PARTS.append('</defs><g font-family="Arial, Helvetica, sans-serif">')
    PARTS.append(f'<rect width="1040" height="{height}" rx="16" fill="#ffffff"/>')
    text(30, 37, title, 25, weight=700)
    text(30, 66, subtitle, 17, MUTED)


def box(x, y, w, h, title, lines=(), color=BLUE, fill="#eff5fd"):
    PARTS.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
                 f'fill="{fill}" stroke="{color}" stroke-width="1.4"/>')
    text(x + 17, y + 29, title, 19, color, 700)
    for i, line in enumerate(lines):
        text(x + 17, y + 56 + 23 * i, line, 17)


def arrow(points, kind="neutral", both=False, dashed=False):
    color = {"neutral": MUTED, "push": PUSH, "pull": PULL}[kind]
    pts = " ".join(f"{x},{y}" for x, y in points)
    extra = f' marker-start="url(#{kind})"' if both else ""
    extra += ' stroke-dasharray="6 5"' if dashed else ""
    PARTS.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.3" '
                 f'stroke-linejoin="round" marker-end="url(#{kind})"{extra}/>')


def end(name):
    PARTS.append('</g></svg>')
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text("\n".join(PARTS) + "\n", encoding="utf-8")


def domain():
    begin("Domene og data", "Begrepsmodell · syntetiske scenarioer · ingen database- eller API-modell", 435,
          "En pasient gjennomfører økter som gir treningsdata. Kildeapplikasjonen produserer treningsdata "
          "og ber om klinisk kontekst. EPJ-miljøet inneholder konteksten. Helsepersonell er tiltenkt bruker.")
    box(30, 113, 190, 90, "Pasient", ["Syntetisk identitet"])
    box(330, 113, 240, 90, "Treningsøkt", ["Én pasient per økt"])
    box(710, 113, 300, 90, "Treningsdata", ["Resultater fra økten"])
    box(30, 288, 250, 90, "Klinisk kontekst", ["Legemiddelinformasjon"])
    box(385, 288, 265, 90, "Simulert EPJ-miljø", ["Inneholder konteksten"])
    box(760, 288, 250, 90, "Kildeapplikasjon", ["Også konsument"])
    arrow([(220, 153), (330, 153)])
    text(275, 137, "har økter", 16, MUTED, anchor="middle")
    arrow([(570, 153), (710, 153)])
    text(640, 137, "gir", 16, MUTED, anchor="middle")
    arrow([(125, 288), (125, 203)])
    text(140, 250, "gjelder", 16, MUTED)
    arrow([(385, 333), (280, 333)])
    text(333, 317, "inneholder", 16, MUTED, anchor="middle")
    arrow([(885, 288), (885, 203)])
    text(899, 250, "produserer", 16, MUTED)
    arrow([(760, 333), (650, 333)])
    text(705, 309, "ber om", 16, MUTED, anchor="middle")
    text(705, 329, "kontekst", 16, MUTED, anchor="middle")
    text(30, 413, "Helsepersonell er tiltenkt bruker av informasjonen; klinisk bruk ble ikke evaluert.", 17, MUTED)
    end("01-domene.svg")


def architecture():
    begin("Felles arkitektur, to veier", "Logiske komponenter i den implementerte PoC-en", 578,
          "Kilde og konsument bruker integrasjonsgrensen. Push går via FHIR-serveren og Subscription "
          "til mapping og repository. Pull går direkte til mapping- og uthentingslaget. "
          "EPJ-tjenestene bruker PostgreSQL for persistens.")
    PARTS.append('<rect x="558" y="92" width="456" height="425" rx="14" fill="#f8fafc" '
                 'stroke="#aebaca" stroke-dasharray="7 5"/>')
    text(578, 119, "SIMULERT EPJ-MILJØ", 15, MUTED, 700)
    box(30, 233, 200, 104, "Kilde / konsument", ["Sender treningsdata", "Ber om kontekst"])
    box(298, 233, 210, 104, "Integrasjonsgrense", ["Validerer / tilpasser", "Koordinerer kall"])
    box(582, 150, 190, 102, "FHIR-server", ["Utveksling", "Subscription"], PUSH, "#fff4eb")
    box(582, 336, 190, 102, "Mapping", ["Modellskifte", "Uthenting / filter"])
    box(812, 336, 180, 102, "Repository", ["openEHR", "Lagrer / henter"])
    arrow([(230, 279), (298, 279)], both=True)
    arrow([(405, 233), (405, 192), (582, 192)], "push")
    text(414, 178, "PUSH", 16, PUSH, 700)
    arrow([(677, 252), (677, 336)], "push")
    text(692, 299, "Hendelse", 16, PUSH)
    arrow([(405, 337), (405, 387), (582, 387)], "pull", both=True)
    text(417, 374, "PULL", 16, PULL, 700)
    text(417, 414, "Forespørsel / svar", 16, PULL)
    arrow([(772, 387), (812, 387)], both=True)
    text(582, 483, "PostgreSQL: persistens for EPJ-tjenestene", 17, MUTED)
    text(30, 554, "Pull går direkte til uthentingslaget. Docker Compose samordnet det lokale miljøet.", 17, MUTED)
    end("02-arkitektur.svg")


def flow(name, title, subtitle, labels, color, fill, kind, footer, desc):
    begin(title, subtitle, 444, desc)
    positions = [(30, 105), (385, 105), (740, 105), (740, 282), (385, 282), (30, 282)]
    for i, ((x, y), (head, lines)) in enumerate(zip(positions, labels), 1):
        box(x, y, 270, 105, f"{i}. {head}", lines, color, fill)
    arrow([(300, 157), (385, 157)], kind)
    arrow([(655, 157), (740, 157)], kind)
    arrow([(875, 210), (875, 282)], kind)
    arrow([(740, 334), (655, 334)], kind)
    arrow([(385, 334), (300, 334)], kind)
    text(30, 427, footer, 17, MUTED)
    end(name)


def quality():
    begin("Kvalitet gjennom begge flytene", "Dokumenterte kontrollnivåer · struktur, modellskifte og faktisk resultat", 395,
          "Begge flytene har inputvalidering og transformasjonstester. Push-verifikasjon omfatter "
          "FHIR-resultat og separat kontroll av openEHR-persistens. Pull-verifikasjon omfatter "
          "AQL-uthenting, tidsfiltrering og respons med data eller tom liste.")
    headers = ["VALIDER", "TRANSFORMER", "LAGRE / HENT", "VERIFISER"]
    for x, heading in zip([30, 285, 540, 795], headers):
        text(x, 108, heading, 16, MUTED, 700)
    push = [("Push · input", ["DTO-struktur", "API-grense"]),
            ("Mapping", ["Kilde → FHIR", "FHIR → openEHR"]),
            ("Persistens", ["FHIR-resultat", "EHRbase-inspeksjon"]),
            ("Sluttresultat", ["Forventet struktur", "i lagrede data"])]
    pull = [("Pull · forespørsel", ["Pasienttilknytning", "Tidsgrense"]),
            ("Mapping / parsing", ["openEHR → FHIR", "→ konsumentformat"]),
            ("Uthenting", ["AQL-verifikasjon", "Tidsfiltrering"]),
            ("Sluttresultat", ["Utvalgt kontekst", "eller tom liste"])]
    for y, data, color, fill, kind in [(124, push, PUSH, "#fff4eb", "push"),
                                      (244, pull, PULL, "#edf9f6", "pull")]:
        for i, (head, lines) in enumerate(data):
            x = 30 + i * 255
            box(x, y, 225, 100, head, lines, color, fill)
            if i < 3:
                arrow([(x + 225, y + 50), (x + 255, y + 50)], kind)
    text(30, 377, "Unit tests og API-tester + lokal E2E og manuell kontroll. Full-stack E2E var utenfor standard CI.", 17, MUTED)
    end("05-datakvalitet.svg")


if __name__ == "__main__":
    domain()
    architecture()
    flow("03-push.svg", "Push: nye treningsdata inn", "Initiert av kilden · les øvre rad mot høyre, deretter ned og tilbake", [
        ("Kilden sender", ["Syntetiske øktdata", "Knyttet til pasient"]),
        ("Integrasjonsgrense", ["Validerer input", "Kildeformat → FHIR"]),
        ("FHIR-server", ["Lagrer ressurs", "Subscription videresender"]),
        ("Mapping", ["Semantisk transformasjon", "FHIR → openEHR"]),
        ("Klinisk repository", ["Strukturert composition", "Persistent lagring"]),
        ("Kontroll av resultat", ["FHIR-representasjon", "Faktisk openEHR-innhold"]),
    ], PUSH, "#fff4eb", "push",
         "Kvittering ved innsending og kontroll av ferdig lagring er ulike verifikasjonspunkter.",
         "Syntetiske treningsdata går fra kilde via inputvalidering og FHIR-representasjon til "
         "Subscription, mapping til openEHR, lagring og kontroll av faktisk resultat.")
    flow("04-pull.svg", "Pull: klinisk kontekst tilbake", "Initiert av konsumenten · les øvre rad mot høyre, deretter ned og tilbake", [
        ("Konsumenten spør", ["Valgt pasient", "Sist kjente oppdatering"]),
        ("Integrasjonsgrense", ["Validerer forespørselen", "Koordinerer uthenting"]),
        ("Uthentingslag", ["Journaloppslag / tidsfilter", "AQL-basert uthenting"]),
        ("Klinisk repository", ["Strukturert klinisk kontekst", "openEHR"]),
        ("Mapping", ["openEHR → FHIR", "Legemiddelkontekst"]),
        ("Respons via grensen", ["FHIR → konsumentformat", "Data eller tom liste"]),
    ], PULL, "#edf9f6", "pull",
         "Verifikasjon: uthentet innhold, tidsfilter og respons. Ingen egen polling i integrasjonsgrensen.",
         "En validert forespørsel går til uthentingslaget og repositoryet. Utvalgt klinisk kontekst "
         "transformeres fra openEHR via FHIR til konsumentformat. Ingen nye data gir tom liste.")
    quality()
    print("Opprettet fem SVG-diagrammer i docs/diagrammer/.")
