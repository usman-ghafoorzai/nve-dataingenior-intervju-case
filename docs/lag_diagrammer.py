"""Lag elleve selvstendige SVG-diagrammer fra sanitiserte begreper.

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
    PARTS.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" '
                 f'viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">')
    PARTS.append(f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>')
    PARTS.append('<defs>')
    for name, color in [("neutral", MUTED), ("push", PUSH), ("pull", PULL)]:
        PARTS.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                     f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                     f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>')
    PARTS.append('</defs><g font-family="Arial, Helvetica, sans-serif">')
    PARTS.append(f'<rect width="1200" height="{height}" rx="0" fill="#ffffff"/>')
    text(30, 37, title, 30, "#111111", weight=700)
    text(30, 66, subtitle, 17, MUTED)


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


def sheet(title, subtitle, height, description):
    begin(title, subtitle, height, description)


def panel(x, y, w, h, fill="#eaf3ff", dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    PARTS.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" '
                 f'fill="{fill}" stroke="#87919c" stroke-width="1.2"{dash}/>')


def centered(x, y, lines, size=19, weight=400, color=INK):
    for i, line in enumerate(lines):
        text(x, y + i * 25, line, size, color, weight, "middle")


def concept(x, y, w, h, lines, fill="#dcecff"):
    panel(x, y, w, h, fill)
    centered(x + w / 2, y + h / 2 - (len(lines)-1)*12.5 + 7, lines, 20, 700)


def association(points, label=None, lx=0, ly=0):
    pts = " ".join(f"{x},{y}" for x, y in points)
    PARTS.append(f'<polyline points="{pts}" fill="none" stroke="#444444" stroke-width="2"/>')
    if label:
        text(lx, ly, label, 17, MUTED, anchor="middle")


def actor(x, y, label, color):
    PARTS.append(f'<circle cx="{x}" cy="{y}" r="17" fill="#ffffff" stroke="{color}" stroke-width="3"/>')
    association([(x, y+17), (x, y+69)])
    association([(x-31, y+37), (x+31, y+37)])
    association([(x-29, y+109), (x, y+69), (x+29, y+109)])
    text(x, y+140, label, 20, weight=700, anchor="middle")


def use_case():
    sheet("Use Case", "Hvem trenger å gjøre hva?", 575,
          "Kildeapplikasjonen overfører treningsdata til strukturert lagring. Konsumenten henter relevant "
          "klinisk kontekst. Det simulerte EPJ-miljøet deltar som støttesystem for begge handlinger.")
    panel(300, 100, 555, 405)
    centered(577, 135, ["Integrasjonsløsning"], 22, 700)
    actor(130, 163, "Kildeapplikasjon", PUSH)
    actor(130, 356, "Konsument", PULL)
    concept(948, 260, 222, 110, ["Simulert", "EPJ-miljø"], "#fff3cd")
    association([(130, 232), (377, 232)])
    association([(130, 425), (377, 425)])
    association([(778, 232), (905, 232), (905, 292), (948, 292)])
    association([(778, 425), (905, 425), (905, 340), (948, 340)])
    for cy, lines, color, fill in [(232, ["Overføre treningsdata", "til strukturert lagring"], PUSH, "#ffe6c9"),
                                   (425, ["Hente relevant", "klinisk kontekst"], PULL, "#dff2e2")]:
        PARTS.append(f'<ellipse cx="577" cy="{cy}" rx="200" ry="61" fill="{fill}" stroke="{color}" stroke-width="2"/>')
        centered(577, cy-7, lines, 22)
    text(30, 550, "Aktørene viser systemroller. Samme applikasjon kan være både kilde og konsument.", 18, MUTED)
    end("01-use-case.svg")


def domain():
    sheet("Domenemodell", "Hva betyr dataene?", 350,
          "En pasient gjennomfører treningsøkter som gir treningsdata. Klinisk kontekst gjelder samme pasient, men er et annet datasett.")
    concept(40, 115, 240, 80, ["Pasient"])
    concept(455, 115, 250, 80, ["Treningsøkt"], "#fff2bf")
    concept(900, 115, 260, 80, ["Treningsdata"], "#f6dde2")
    concept(40, 260, 240, 65, ["Klinisk kontekst"], "#eaddf4")
    arrow([(280, 155), (455, 155)])
    text(367, 140, "gjennomfører", 17, MUTED, anchor="middle")
    arrow([(705, 155), (900, 155)])
    text(802, 140, "gir", 17, MUTED, anchor="middle")
    arrow([(160, 260), (160, 195)])
    text(178, 232, "gjelder", 17, MUTED)
    text(455, 289, "Push: treningsdata. Pull: legemiddelkontekst.", 20, weight=700)
    text(455, 319, "Ulike datasett knyttet til en pasient i testscenarioet.", 18, MUTED)
    end("02-domene.svg")


def information():
    sheet("Informasjonsflyt", "Hvilken informasjon skal flyte hvor?", 568,
          "Treningsdata går fra kilde via integrasjonsgrensen til EPJ. Konsumenten ber om klinisk "
          "kontekst og får denne tilbake via integrasjonsgrensen. Dette er forskjellige datasett.")
    for x, w, label, fill in [(30, 255, "Kilde / konsument", "#eaf3ff"),
                              (465, 260, "Integrasjonsgrense", "#f0eafa"),
                              (905, 265, "Simulert EPJ-miljø", "#e8f3e8")]:
        panel(x, 110, w, 372, fill)
        text(x+w/2, 144, label, 21, weight=700, anchor="middle")
    centered(157, 213, ["Treningsdata", "oppstår her"], 20, 700)
    centered(595, 213, ["Formidler", "treningsdata"], 20, 700)
    centered(1037, 213, ["Treningsdata", "lagres strukturert"], 20, 700)
    for a,b in [(285,465),(725,905)]:
        arrow([(a, 247), (b, 247)], "push")
        text((a+b)/2, 230, "Treningsdata", 18, PUSH, anchor="middle")
    centered(157, 393, ["Konsumenten trenger", "klinisk kontekst"], 20, 700)
    centered(595, 393, ["Formidler utvalgt", "klinisk kontekst"], 20, 700)
    centered(1037, 393, ["Klinisk kontekst", "finnes her"], 20, 700)
    for a,b in [(285,465),(725,905)]:
        arrow([(a, 320), (b, 320)], "pull", dashed=True)
        text((a+b)/2, 303, "Ber om kontekst", 17, PULL, anchor="middle")
        arrow([(b, 445), (a, 445)], "pull")
        text((a+b)/2, 430, "Klinisk kontekst", 17, PULL, anchor="middle")
    text(30, 523, "Heltrukket pil: dataretning. Stiplet pil: forespørselen som initierer pull.", 18, MUTED)
    text(30, 550, "Pull gjelder legemiddelkontekst, ikke en retur av treningsdataene fra push.", 18, MUTED)
    end("03-informasjonsflyt.svg")


def technical_box(x, y, w, h, title, lines, fill="#ffffff"):
    panel(x, y, w, h, fill)
    centered(x+w/2, y+29, [title], 20, 700)
    centered(x+w/2, y+56, lines, 18)


def architecture():
    sheet("Implementert løsning – to dataflyter", "Samme komponenter, to forskjellige veier gjennom løsningen", 790,
          "Push går fra kilde gjennom integrasjonsklient og HAPI FHIR til bridge- og mappinglaget, EHRbase og persistens. "
          "Pull går fra konsument gjennom integrasjonsklient til bridge-laget og EHRbase, og returnerer transformert respons. "
          "HAPI FHIR og EHRbase bruker PostgreSQL. Komponentene gjentas for å vise hver flyt tydelig.")
    text(30, 112, "PUSH · ny treningsinformasjon", 20, PUSH, 700)
    panel(470, 127, 710, 296, "#f3f7fb", dashed=True)
    text(490, 153, "Simulert EPJ-miljø", 17, MUTED, 700)
    xs=[30,260,490,720,950]
    nodes=[("Kilde",["Treningsdata"]),("Integrasjonsklient",["Validerer / mapper"]),
           ("HAPI FHIR",["Lagrer FHIR"]),("Bridge / mapping",["FHIR → openEHR"]),("EHRbase",["openEHR repository"])]
    for x,(title,lines) in zip(xs,nodes):
        technical_box(x,185,210,90,title,lines,"#fff0df")
    for a,b,label in [(240,260,""),(470,490,""),(930,950,"")]:
        arrow([(a,230),(b,230)],"push")
    arrow([(595,185),(595,170),(825,170),(825,185)],"push")
    text(785, 158, "Subscription / event", 16, PUSH, anchor="middle")
    technical_box(605, 340, 410, 65, "PostgreSQL", ["Underliggende persistens"], "#eaf3ff")
    arrow([(595,275),(595,372),(605,372)])
    arrow([(1055,275),(1055,372),(1015,372)])
    text(285,303,"Input → FHIR",17,PUSH)
    text(30, 472, "PULL · konsumenten ber om klinisk kontekst", 20, PULL, 700)
    panel(630, 492, 550, 222, "#f3f7fb", dashed=True)
    text(648, 518, "Simulert EPJ-miljø", 17, MUTED, 700)
    for x,title,lines in [(30,"Konsument",["Data / tom respons"]),(340,"Integrasjonsklient",["Validerer / mapper"]),
                          (650,"Bridge / uthenting",["AQL / mapping"]),(950,"EHRbase",["openEHR-kontekst"])]:
        technical_box(x,570,210,90,title,lines,"#e7f4e9")
    for a,b in [(240,340),(550,650),(860,950)]:
        arrow([(a,588),(b,588)],"pull",dashed=True)
        arrow([(b,642),(a,642)],"pull")
    text(600,550,"Separat forespørselsstyrt uthentingsvei",17,PULL,anchor="middle")
    text(285,688,"Konsumentformat",16,PULL,anchor="middle")
    text(600,688,"FHIR",16,PULL,anchor="middle")
    text(905,688,"openEHR",16,PULL,anchor="middle")
    text(30,749,"Stiplet grønn: forespørsel. Heltrukket grønn: respons. HAPI FHIR inngår ikke i implementert pull.",18,MUTED)
    text(30,776,"Komponentene er vist på nytt for pull. Persistensen er den samme som i øvre del.",17,MUTED)
    end("04-arkitektur.svg")


def lane(y,h,title):
    panel(20,y,1160,h,"#f3f7fb")
    text(38,y+29,title,20,weight=700)


def push_flow():
    sheet("Push – implementert flyt", "Treningsdata inn – les fra øverst mot nederst", 1740,
          "Origo dashboard sender Game session data til PushController, PushService, GameSessionObservationMapper og HapiFhirClient. "
          "HAPI FHIR lagrer Observation og bruker Subscription callback til CustomController. ResourceRoutingService ruter til "
          "GameSessionResultObservationHandler, GameSessionResultObservationMapper og GameSessionResultCompositionBuilder. "
          "EhrbaseHelper lagrer openEHR composition i EHRbase.")
    def box(x,y,title,lines,fill="#fff0df"):
        panel(x,y,520,110,fill)
        centered(x+260,y+30,[title],21,700)
        centered(x+260,y+59,lines,19)
    def flow(points,label=None,lx=0,ly=0):
        arrow(points,"push")
        if label: text(lx,ly,label,18,PUSH,anchor="middle")
    lane(105,530,"Origo + Integration Client")
    box(40,155,"Origo dashboard",["Game session data"])
    box(640,155,"PushController",["POST /push/game-results"])
    flow([(560,210),(640,210)],"Game session data",600,145)
    box(640,325,"PushService",["Coordinates request"])
    flow([(900,265),(900,325)])
    box(40,325,"GameSessionObservationMapper",["CreateGameSessionDTO → FHIR Observation"])
    flow([(640,380),(560,380)])
    box(40,495,"HapiFhirClient",["Post Observation"])
    flow([(300,435),(300,495)])
    lane(690,190,"HAPI FHIR")
    box(40,740,"HAPI FHIR",["Stores Observation, triggers subscription","Observation?status=final"])
    flow([(300,605),(300,740)],"FHIR Observation",415,666)
    lane(940,570,"FHIR Bridge")
    box(40,990,"CustomController",["Receives Observation"])
    flow([(300,850),(300,990)],"Subscription callback",430,917)
    box(640,990,"ResourceRoutingService",["Routes Observation to matching handler"])
    flow([(560,1045),(640,1045)])
    box(640,1170,"GameSessionResultObservationHandler",["Coordinates map → build → post"])
    flow([(900,1100),(900,1170)])
    box(40,1170,"GameSessionResultObservationMapper",["FHIR Observation → DTO"])
    flow([(640,1225),(560,1225)])
    box(40,1350,"GameSessionResultCompositionBuilder",["Builds openEHR composition","Aible_Game_Session_Result.v1"])
    flow([(300,1280),(300,1350)])
    box(640,1350,"EhrbaseHelper",["GET/create EHR","POST composition"])
    flow([(560,1405),(640,1405)])
    lane(1570,150,"EHRbase")
    box(640,1605,"EHRbase",["Stored openEHR composition"],"#e7f4e9")
    flow([(900,1460),(900,1605)],"Post composition",1015,1535)
    end("05-push.svg")


def pull_flow():
    sheet("Pull – implementert flyt", "Klinisk kontekst ut – forespørsel og respons", 2060,
          "Origo dashboard sender patientId + lastUpdatedAt til PullController, PullService og FhirBridgeClient. "
          "MedicationPullController og MedicationPullService koordinerer EhrbaseHelper og EhrbaseMedicationQueryClient. "
          "AQL rows fra EHRbase parses av MedicationOrderAqlRowParser til MedicationOrderAqlRowDto og mappes av "
          "MedicationRequestMapper til FHIR MedicationRequest. FHIR Bundle returneres til MedicationPullMapper, "
          "som lager PullMedicationResponseDto med patientId, pulledAt og medications[] til Origo.")
    xs=[20,320,620,920]
    centers=[150,450,750,1050]
    for x,title in zip(xs,["Origo dashboard","Integration Client","FHIR Bridge","EHRbase"]):
        panel(x,110,260,1910,"#f3f7fb")
        centered(x+130,150,[title],21,700)
    def box(col,y,title,lines):
        x=xs[col]+10
        panel(x,y,240,110,"#e7f4e9")
        centered(x+120,y+25,title,18,700)
        centered(x+120,y+28+25*len(title),lines,16)
    def msg(a,b,y,label):
        arrow([(centers[a],y),(centers[b],y)],"pull",dashed=a<b)
        text((centers[a]+centers[b])/2,y-12,label,17,PULL,anchor="middle")
    def down(col,a,b): arrow([(centers[col],a),(centers[col],b)],"pull")
    box(0,195,["Origo dashboard"],["Requests medication updates"])
    down(0,305,345)
    msg(0,1,345,"patientId + lastUpdatedAt")
    down(1,345,370)
    box(1,370,["PullController"],["GET /pull/medications"])
    down(1,480,515)
    box(1,515,["PullService"],["Coordinates request"])
    down(1,625,660)
    box(1,660,["FhirBridgeClient"],["Request to FHIR Bridge"])
    down(1,770,810)
    msg(1,2,810,"patient + lastUpdatedAt")
    down(2,810,835)
    box(2,835,["MedicationPullController"],["/custom/MedicationRequest"])
    down(2,945,980)
    box(2,980,["MedicationPullService"],["Patient lookup, AQL query,","mapping, FHIR bundle creation"])
    down(2,1090,1125)
    box(2,1125,["EhrbaseHelper"],["patientId → ehrId"])
    down(2,1235,1270)
    box(2,1270,["EhrbaseMedication", "QueryClient"],["Executes AQL query","Applies lastUpdated filter"])
    down(2,1380,1420)
    msg(2,3,1420,"AQL query")
    down(3,1420,1445)
    box(3,1445,["EHRbase"],["Stored medication order","composition"])
    down(3,1555,1595)
    msg(3,2,1595,"AQL rows")
    down(2,1595,1620)
    box(2,1620,["MedicationOrder", "AqlRowParser"],["AQL row →","MedicationOrderAqlRowDto"])
    down(2,1730,1765)
    box(2,1765,["MedicationRequestMapper"],["DTO → FHIR MedicationRequest"])
    down(2,1875,1915)
    msg(2,1,1915,"FHIR Bundle")
    # Responsen følger klientens venstre side oppover til konsumenten.
    box(1,1700,["MedicationPullMapper"],["FHIR Bundle →","PullMedicationResponseDto"])
    arrow([(450,1915),(450,1810)],"pull")
    box(1,1490,["PullMedication", "ResponseDto"],["patientId, pulledAt","medications[]"])
    arrow([(450,1700),(450,1600)],"pull")
    arrow([(450,1490),(450,1370),(295,1370),(295,250),(270,250)],"pull")
    text(375,1355,"Response to Origo",16,PULL,anchor="middle")
    end("06-pull.svg")


def organization():
    sheet("Kode, modeller og konfigurasjon", "Ulike ansvar krever tydelige grenser og eksplisitte modellskifter",650,
          "API-grensen delegerer til service som koordinerer mapper og adapter. Push modelleres som input til FHIR til openEHR/template. "
          "Pull går fra openEHR via FHIR til konsumentformat. Miljøkonfigurasjon er separat fra forretningslogikk.")
    lane(105,185,"Kode · integrasjonsklient")
    technical_box(40,175,230,80,"API-grense",["Controller / DTO"])
    technical_box(350,175,230,80,"Service",["Koordinerer brukstilfelle"])
    technical_box(680,150,220,65,"Mapper",["Transformasjon"])
    technical_box(950,210,210,65,"Adapter / klient",["Ekstern kommunikasjon"])
    arrow([(270,215),(350,215)])
    arrow([(580,195),(630,195),(630,182),(680,182)])
    arrow([(580,235),(630,235),(630,265),(920,265),(920,242),(950,242)])
    lane(325,175,"Modeller · to retninger, forskjellige datasett")
    for y,label,items,kind in [(403,"Push",["Input / DTO","FHIR","openEHR / template"],"push"),
                              (465,"Pull",["openEHR-data","FHIR","Konsumentformat"],"pull")]:
        text(40,y,label,19,{"push":PUSH,"pull":PULL}[kind],700)
        for x,value in zip([300,650,1000],items): text(x,y,value,20,weight=700,anchor="middle")
        arrow([(440,y-7),(535,y-7)],kind)
        arrow([(725,y-7),(835,y-7)],kind)
    panel(20,540,1160,85,"#eaf3ff")
    text(40,571,"Konfigurasjon · separat fra forretningslogikken",20,weight=700)
    text(40,603,"Docker Compose koordinerer EPJ-tjenestene. Miljø og testdata klargjøres for repeterbar verifikasjon.",18,MUTED)
    end("07-kode-modeller-konfig.svg")


def journey():
    sheet("Min utviklingsreise i NVE", "Fra software og integrasjon til ansvar for større deler av dataprodukter",420,
          "Utgangspunkt: software- og integrasjonsbakgrunn. Første tid: lære domene, team og dataplattform gjennom avgrensede leveranser. "
          "Etter to til tre år: selvstendig ansvar for større deler av dataprodukter med kvalitet og drift.")
    for x,title,lines,fill in [(30,"UTGANGSPUNKT",["Software / integrasjon","API-er, databaser og testing","Erfaring fra lokal PoC"],"#eaf3ff"),
                              (450,"FØRSTE TID I NVE",["Domene, brukere og team","Lære plattformen i praksis","Avgrensede leveranser"],"#f0eafa"),
                              (870,"ETTER 2–3 ÅR",["Selvstendig dataingeniør","Større deler av dataprodukter","Kvalitet, vedlikehold og drift"],"#e7f4e9")]:
        panel(x,135,300,185,fill)
        centered(x+150,175,[title],21,700)
        centered(x+150,223,lines,18)
    arrow([(330,225),(450,225)])
    arrow([(750,225),(870,225)])
    text(30,372,"Gradvis mer ansvar, faglig samarbeid og kunnskapsdeling gjennom hele reisen.",20,weight=700)
    end("09-utviklingsreise-nve.svg")


def quality():
    sheet("Datakvalitet og verifisering", "Kontrollmodell for begge flytene – ikke et teknisk sekvensdiagram", 425,
          "Validering, transformasjon og lagring eller uthenting skilles fra kontrollen av resultatet. "
          "Push kontrolleres med FHIR-resultat og EHRbase-inspeksjon. Pull kontrolleres med "
          "AQL/API-verifikasjon av utvalg og forventet respons, inkludert tom liste.")
    xs = [30, 325, 620, 915]
    for x, heading in zip(xs, ["VALIDER", "TRANSFORMER", "LAGRE / HENT", "VERIFISER"]):
        text(x+10, 114, heading, 19, weight=700)
    push = [("Push · input", ["DTO-struktur", "API-grense"]),
            ("Mapping", ["Kilde → FHIR", "FHIR → openEHR"]),
            ("Persister", ["openEHR composition", "i klinisk repository"]),
            ("Kontroller persistens", ["FHIR-resultat og", "EHRbase-inspeksjon"])]
    pull = [("Pull · forespørsel", ["Pasienttilknytning", "Tidsgrense"]),
            ("Mapping / parsing", ["openEHR → FHIR", "→ konsumentformat"]),
            ("Hent utvalg", ["Pasient og tidsfilter", "fra klinisk repository"]),
            ("Kontroller respons", ["AQL-/API-kontroll", "Riktig utvalg / tom liste"])]
    for y, data, fill in [(133, push, "#fff0df"), (264, pull, "#e7f4e9")]:
        panel(20, y, 1160, 108, fill)
        for i, (head, lines) in enumerate(data):
            x = xs[i]
            text(x+10, y+30, head, 19, weight=700)
            for j, line in enumerate(lines):
                text(x+10, y+58+j*24, line, 18)
            if i<3:
                arrow([(x+246, y+53), (x+287, y+53)])
    text(30, 407, "Enhetstester og API-tester ble supplert med lokal E2E og manuell verifikasjon av den samlede flyten.", 18, MUTED)
    end("08-datakvalitet.svg")


def lifecycle():
    sheet("Dataproduktets livsløp", "Gradvis ansvar for større deler av kjeden, en generell modell", 500,
          "Kilde, innhenting, transformasjon, modellering, datakvalitet, tilgjengeliggjøring, konsument og drift og overvåking. "
          "Testing, CI/CD, observability og dokumentasjon støtter arbeidet gjennom livsløpet. Dette er ikke NVEs interne arkitektur.")
    labels=[["Kilde"],["Innhenting"],["Transformasjon"],["Modellering"],
            ["Datakvalitet"],["Tilgjengeliggjøring"],["Konsument"],["Drift og overvåking"]]
    xs=[30,330,630,930]
    for i,lines in enumerate(labels):
        x=xs[i%4];y=135 if i<4 else 295
        concept(x,y,240,75,lines,"#eaf3ff" if i<4 else "#e7f4e9")
        if i%4<3: arrow([(x+240,y+37),(x+300,y+37)])
    arrow([(1050,210),(1050,252),(150,252),(150,295)])
    panel(30,410,1140,65,"#f0eafa")
    centered(600,437,["Testing, CI/CD, observability og dokumentasjon", "Støtter arbeidet gjennom livsløpet"],19)
    end("10-dataprodukt-livslop.svg")


def development():
    sheet("Tre sider av utviklingen", "Slik håper jeg å ha utviklet meg etter 2–3 år", 525,
          "Faglig: lære plattformen, bli tryggere og jobbe mer selvstendig. Ansvar: fra avgrensede oppgaver til større leveranser og ansvar fra behov til drift. "
          "Arbeidsmiljø: bli kjent med kollegene, bli en del av miljøet og bidra til trivsel og inkludere andre.")
    rows=[(115,"FAGLIG",[["Lære plattformen"],["Bli tryggere"],["Jobbe mer","selvstendig"]],"#eaf3ff"),
          (245,"ANSVAR",[["Avgrensede oppgaver"],["Større leveranser"],["Mer ansvar fra","behov til drift"]],"#f0eafa"),
          (375,"ARBEIDSMILJØ",[["Bli kjent med","kollegene"],["Bli en del av miljøet"],["Bidra til trivsel","og inkludere andre"]],"#e7f4e9")]
    for y,label,steps,fill in rows:
        text(30,y+50,label,19,weight=700)
        for x,lines in zip([240,570,900],steps): concept(x,y,270,95,lines,fill)
        arrow([(510,y+47),(570,y+47)])
        arrow([(840,y+47),(900,y+47)])
    end("11-utvikling-faglig-ansvar-sosialt.svg")


if __name__ == "__main__":
    use_case()
    domain()
    information()
    architecture()
    push_flow()
    pull_flow()
    organization()
    quality()
    journey()
    lifecycle()
    development()
    print("Opprettet elleve SVG-diagrammer i docs/diagrammer/.")
