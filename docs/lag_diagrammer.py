"""Lag ni selvstendige SVG-diagrammer fra sanitiserte begreper.

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
    sheet("Implementert arkitektur", "Samme komponenter, to forskjellige veier gjennom løsningen", 790,
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
    sheet("Push – faktisk komponentsekvens", "Treningsdata inn · les fra øverst mot nederst", 1030,
          "Kilden sender treningsdata. Klienten validerer og mapper til FHIR før innsending til HAPI FHIR. "
          "HAPI FHIR lagrer og utløser Subscription. Bridge-laget mottar, fordeler, mapper og bygger openEHR "
          "mot template-struktur, finner eller oppretter journal og lagrer gjennom EHRbase. Sluttresultatet verifiseres separat.")
    lane(110,175,"Kilde og integrasjonsklient")
    for x,w,title,lines in [(40,210,"Kilde",["Treningsdata", "Pasienttilknytning"]),
                           (330,220,"API / service",["Validerer input", "Koordinerer"]),
                           (625,220,"Mapper",["Input → FHIR"]),
                           (930,230,"Adapter / klient",["Sender FHIR"])]:
        technical_box(x,165,w,99,title,lines,"#fff0df")
    for a,b in [(250,330),(550,625),(845,930)]: arrow([(a,215),(b,215)],"push")
    lane(320,125,"HAPI FHIR")
    technical_box(930,350,230,75,"Lagrer ressurs",["FHIR"],"#fff0df")
    arrow([(1045,264),(1045,350)],"push")
    lane(490,180,"Bridge- og mappinglag")
    for x,w,title,lines in [(930,230,"Mottak / fordeling",["Relevant hendelse"]),
                           (635,230,"Mapper",["Tolker FHIR-innhold"]),
                           (335,230,"Bygger composition",["openEHR / template"]),
                           (40,230,"Repository-klient",["Finn / opprett journal"] )]:
        technical_box(x,540,w,99,title,lines,"#fff0df")
    arrow([(1045,425),(1045,540)],"push")
    text(1060,477,"Subscription",17,PUSH)
    for a,b in [(930,865),(635,565),(335,270)]: arrow([(a,590),(b,590)],"push")
    lane(720,145,"EHRbase")
    technical_box(40,765,300,80,"Lagrer composition",["Persistens i PostgreSQL"],"#e5f3e5")
    arrow([(155,639),(155,765)],"push")
    text(173,695,"openEHR",17,PUSH)
    text(410,792,"Forutsetning: syntetisk pasient er opprettet før innsending.",18,MUTED)
    text(410,822,"HAPI FHIR lagrer også sine ressurser i PostgreSQL.",18,MUTED)
    panel(20,920,1160,85,"#f2f3f5",dashed=True)
    text(40,950,"VERIFIKASJON · separat kontrollaktivitet",19,weight=700)
    text(40,980,"Kontroller FHIR-resultatet og lagret openEHR-innhold. API-kvittering er ikke bevis på fullført kjede.",18,MUTED)
    arrow([(190,845),(190,920)],dashed=True)
    end("05-push.svg")


def pull_flow():
    sheet("Pull – faktisk forespørsel og respons", "Klinisk kontekst ut · stiplet forespørsel, heltrukket respons", 1080,
          "Konsumenten ber om pasientens oppdateringer. Klienten validerer og sender til bridge-laget. "
          "Bridge-laget koordinerer journaloppslag og tidsfiltrert AQL mot EHRbase. Resultatet parses og mappes til FHIR. "
          "Klienten mapper til konsumentformat og returnerer data eller tom liste. Verifikasjon av utvalg og respons er separat.")
    # Vertikale lanes viser ansvar; tiden går nedover.
    centers=[140,440,740,1040]
    for x,title,sub in [(20,"Konsument","Initierer"),(320,"Integrasjonsklient","Validerer / mapper"),
                        (620,"Bridge / uthenting","Oppslag / mapping"),(920,"EHRbase","Klinisk repository")]:
        panel(x,110,260,840,"#f3f7fb")
        centered(x+130,145,[title,sub],19,700)
    def step(col,y,lines):
        panel(centers[col]-115,y,230,65,"#e7f4e9")
        centered(centers[col],y+27,lines,17)
    def message(a,b,y,label,request=False):
        arrow([(centers[a],y),(centers[b],y)],"pull",dashed=request)
        text((centers[a]+centers[b])/2,y-12,label,17,PULL,anchor="middle")
    step(0,195,["Ber om oppdateringer","Pasient og tidspunkt"])
    message(0,1,295,"Forespørsel",True)
    step(1,315,["Validerer forespørsel","Service / adapter"])
    message(1,2,415,"Uthentingsbehov",True)
    step(2,435,["Koordinerer oppslag","Finner pasientens journal"])
    message(2,3,535,"AQL / tidsfilter",True)
    step(3,555,["Henter klinisk kontekst","Lagret openEHR"])
    message(3,2,655,"Resultat fra repository")
    step(2,675,["Parser resultatet","Mapper til FHIR"])
    message(2,1,775,"FHIR-basert respons")
    step(1,795,["Mapper til","konsumentformat"])
    message(1,0,910,"Data eller tom liste")
    panel(20,985,1160,70,"#f2f3f5",dashed=True)
    text(40,1013,"VERIFIKASJON · riktig utvalg, tidsfilter, transformasjon og respons",19,weight=700)
    text(40,1040,"Separate tester og API-/AQL-kontroller. Konsumenten styrer når den spør; ingen egen polling i klienten.",17,MUTED)
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
          "I dag: software- og integrasjonsbakgrunn. Første tid: lære domene, team og dataplattform gjennom avgrensede leveranser. "
          "Etter to til tre år: selvstendig ansvar for større deler av dataprodukter med kvalitet og drift.")
    for x,title,lines,fill in [(30,"I DAG",["Software / integrasjon","API-er, databaser og testing","Erfaring fra lokal PoC"],"#eaf3ff"),
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
    text(30, 407, "Unit tests og API-tester ble supplert med lokal E2E og manuell verifikasjon av den samlede flyten.", 18, MUTED)
    end("08-datakvalitet.svg")


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
    print("Opprettet ni SVG-diagrammer i docs/diagrammer/.")
