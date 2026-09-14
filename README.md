# NVE – 2. gangsintervju

**Usman Ghafoorzai**

## Case 1 – Strukturert datautveksling i to retninger

Jeg tar utgangspunkt i **én interoperabilitetsløsning med to komplementære dataflyter** fra bachelorprosjektet: treningsdata inn til strukturert lagring og klinisk kontekst ut til konsumenten.

Vi var to studenter som begge deltok gjennom hele prosjektløpet, fra behovsforståelse, forprosjekt og krav til modellering, arkitektur, implementasjon, testing og rapportering. Konkrete oppgaver ble fordelt underveis, og jeg arbeidet på tvers av analyse, design, implementasjon, verifikasjon og dokumentasjon.

> **Ramme:** Lokal PoC, simulert EPJ-miljø og syntetiske data. Autentisering, autorisasjon og komplett synkronisering var utenfor implementasjonen. Produksjonsintegrasjon og klinisk validering inngikk ikke.

### Problem, formål og verdi

Treningsdata og klinisk kontekst finnes i forskjellige systemer og representasjoner. Pasienttilknytning, struktur, tidspunkt og betydning må bevares slik at mottakeren kan bruke informasjonen. Formålet var å demonstrere strukturert utveksling i begge retninger.

- **Demonstrert verdi:** Redusert teknisk usikkerhet ved å vise at data kunne valideres, transformeres, lagres, hentes og verifiseres.
- **Potensiell virksomhetsverdi:** Informasjon fra separate systemer kan bli tilgjengelig der den trengs. Mindre manuell innhenting og overføring er mulige gevinster, ikke målte kliniske, økonomiske eller produksjonsmessige effekter.

### Use Case – hvem trenger å gjøre hva?

Kilden sender treningsdata til strukturert lagring. Konsumenten henter klinisk kontekst gjennom integrasjonsløsningen og det simulerte EPJ-miljøet.

![Use Case: sende treningsdata og hente klinisk kontekst.](docs/diagrammer/01-use-case.svg)

### Domene – hva betyr dataene?

Handlingene gjelder en pasient, treningsøkter og klinisk kontekst. **Pull hentet legemiddelinformasjon, ikke treningsdataene fra push.**

![Domene: pasient, treningsøkt, treningsdata og klinisk kontekst med sine relasjoner.](docs/diagrammer/02-domene.svg)

### Informasjonsflyt – fra opprinnelse til bruk

![Informasjonsflyt: treningsdata går inn til EPJ; en forespørsel utløser klinisk kontekst tilbake til konsumenten.](docs/diagrammer/03-informasjonsflyt.svg)

Flytene ga fire sentrale krav: validere input, transformere representasjoner, gjøre sluttresultatet etterprøvbart og ha et testbart, repeterbart miljø. Arkitekturen måtte fordele disse oppgavene mellom komponentene.

### Arkitekturen vi implementerte

![Implementert arkitektur: push via integrasjonsklient, HAPI FHIR og Subscription til bridge- og mappinglag og EHRbase; pull mellom klient, bridge og EHRbase. Begge repository-tjenestene bruker PostgreSQL.](docs/diagrammer/04-arkitektur.svg)

| Komponent / rolle | Teknologi og ansvar |
|---|---|
| Integrasjonsklient | **NestJS / TypeScript:** API-/DTO-grense, koordinering og tilpasning til konsumentformat. |
| Utveksling | **FHIR:** utvekslingsrepresentasjon. **HAPI FHIR:** ressurslagring og Subscription for push. |
| Bridge- og mappinglag | **Java / Spring:** transformasjon, journaloppslag og koordinering av lagring/uthenting. |
| Klinisk representasjon | **openEHR og template:** avgrenser forventet klinisk struktur for persistens. |
| Repository og persistens | **EHRbase:** openEHR-tjeneste. **PostgreSQL:** underliggende lagring for EHRbase og HAPI FHIR. |

Push brukte HAPI FHIR før bridge-laget. Pull brukte en separat uthentingsvei mellom integrasjonsklienten og bridge-laget. Applikasjonslogikken brukte tjenestegrensesnitt; PostgreSQL var underliggende persistens.

### Push – fra treningsdata til persistens

![Push-swimlane: input valideres i klienten og mappes til FHIR. HAPI FHIR lagrer og varsler bridge-laget, som bygger openEHR-struktur og lagrer gjennom EHRbase. Verifikasjon skjer separat.](docs/diagrammer/05-push.svg)

En syntetisk pasient var opprettet før innsending. Klienten validerte input, koordinerte flyten og mappet treningsdata til FHIR før videresending. HAPI FHIR lagret ressursen og utløste Subscription.

Bridge-laget fordelte mottaket til riktig behandling, hentet ut innholdet og bygde en openEHR composition mot forventet template-struktur. Journalen ble funnet eller opprettet før lagring gjennom EHRbase. Vi kontrollerte FHIR-resultatet og faktisk persistens separat fra kvitteringen ved inngangen.

### Pull – fra klinisk kontekst til konsument

![Pull-swimlane: validert forespørsel til bridge-laget; journaloppslag og tidsfiltrert AQL-uthenting fra EHRbase; parsing og mapping til FHIR før klienten lager konsumentrespons.](docs/diagrammer/06-pull.svg)

Konsumenten ba om oppdateringer for en pasient og et tidspunkt. Klienten validerte forespørselen; bridge-laget koordinerte journaloppslag og tidsfiltrert uthenting med **AQL** fra EHRbase.

Resultatet ble parset og mappet fra openEHR-data til en FHIR-basert representasjon. Klienten mappet videre til konsumentformat og returnerte data eller tom liste. Vi verifiserte utvalg, tidsfilter og respons. Konsumenten styrte når den spurte; klienten hadde ingen egen periodisk polling.

**Forskjellen:** Push startet med nye data og endte i strukturert persistens. Pull startet med konsumentbehov og endte i en filtrert respons. Hendelsesdrevet videresending og forespørselsstyrt uthenting krevde ulike mekanismer.

### Hvordan vi organiserte løsningen

#### Kode

Integrasjonsklientens **controller/DTO** håndterte API-grensen, **service** koordinerte brukstilfellet, **mapper** transformerte data og **adapter/client** håndterte ekstern kommunikasjon. Det skilte ansvar, begrenset kobling til transportdetaljer og gjorde endringer og testing enklere.

Bridge-laget hadde separat push- og pull-logikk for mapping og uthenting, med delt EHRbase-kommunikasjon der ansvaret var felles.

![Organisering: service koordinerer mapper og klient; modellskiftene er forskjellige i push og pull; miljøkonfigurasjon holdes separat.](docs/diagrammer/07-kode-modeller-konfig.svg)

#### Modeller

**DTO** definerte forventet API-struktur, **FHIR** representerte informasjon under utveksling, og **openEHR/template** avgrenset den kliniske strukturen ved persistens. **Konsumentformatet** ga mottakeren det utvalget den trengte. Ulike ansvar krevde ulike modeller og eksplisitt mapping mellom dem.

#### Konfigurasjon

**Docker Compose** koordinerte det lokale EPJ-miljøet med separate database-, FHIR-, bridge- og EHR-tjenester. Miljøkonfigurasjon var skilt fra forretningslogikken. Miljøet kunne startes og resettes med klargjorte testdata for repeterbar verifikasjon.

Når data krysser disse grensene, må både struktur og betydning kontrolleres gjennom representasjonsskiftene.

### Datakvalitet gjennom flyten

![Datakvalitet: valider, transformer, lagre/hent og verifiser. Persistens og kontroll av persistens er forskjellige aktiviteter.](docs/diagrammer/08-datakvalitet.svg)

- **API → FHIR:** DTO-validering kontrollerte input. Unit tests, blant annet med **Jest**, kontrollerte mapping og logikk; API-kontroller undersøkte FHIR-resultatet.
- **FHIR → openEHR:** Template-strukturen avgrenset representasjonen. Mappingtester og inspeksjon i **EHRbase** undersøkte om innholdet faktisk fikk forventet struktur og ble lagret. En template alene garanterer ikke datakvalitet eller klinisk riktighet.
- **openEHR → konsument:** AQL-verifikasjon, lokale E2E-tester og API-kontroller undersøkte uthenting, transformasjon, tidsfiltrering og tom respons. **Swagger/OpenAPI** støttet dokumentasjon og manuell kontroll.

Identifikatorer, responser og lagret/hentet innhold gjorde testdataene sporbare. **200 OK ved inngangen betyr ikke at hele dataflyten er korrekt.** Kontrollene gjaldt utvalgte tekniske scenarioer med syntetiske data.

### Ansvar, dataopprinnelse og kontrakter

Kildeapplikasjonen produserte treningsdataene; EPJ-miljøet var kilden til klinisk kontekst. Integrasjonslaget validerte, transformerte og formidlet. Det var ingen ny autoritativ kilde eller permanent klinisk lagring.

Vi hadde komponentansvar og tekniske kontrakter ved **DTO/API-, FHIR- og openEHR/repository-grensene**. Formelt dataeierskap, SLA og driftsansvar var ikke etablert som i produksjon. Jeg ville formalisert eiere, versjonering, kvalitetskrav og ansvar for feil og endringer.

### Største utfordring og designvalg

**Problem:** Ett felles FHIR-lag skulle støtte både hendelsesdrevet push og forespørselsstyrt pull. Subscription reagerte på ressursendringer og løste ikke uthentingsbehovet.

**Alternativ:** Endre FHIR-serverens interne oppførsel. Det ville økt kompleksiteten og omfanget.

**Beslutning:** Beholde Subscription for push og bruke en separat forespørselsstyrt uthentingsvei for pull.

**Trade-off:** Begge retninger kunne implementeres og verifiseres, men pull var ikke et fullt standardkompatibelt FHIR-søk. Standardisert søk og validering fulgte ikke automatisk med denne veien.

**Læring:** En felles representasjon betyr ikke at samme transportmekanisme dekker alle behov. Begge retninger må prøves før arkitekturen låses.

### Utviklingsflyt og CI/CD

**Avgrenset endring → PR → automatiserte tester og byggkontroller → merge/integrasjon.** GitHub Actions støttet dette. Full Docker-E2E lå utenfor standard CI, så vi supplerte med lokal verifikasjon gjennom flytene. Dette var ingen automatisert produksjonsleveranse.

### Resultat, læring og videre arbeid

Den lokale PoC-en verifiserte strukturert push og selektiv pull med syntetiske data. Resultatet viste teknisk gjennomførbarhet, ikke klinisk effekt.

Jeg lærte å forstå dataenes betydning, plassere ansvar ved systemgrenser og behandle mapping som en sentral engineering-oppgave. **Verifiser det konsumenten faktisk får, og det som faktisk blir lagret.**

Videre ville jeg prioritert bedre standardtilpasning av pull, automatisert E2E, kvalitetskrav og observability. Tilgangskontroll, domenevalidering og testing i et produksjonsnært miljø måtte også på plass.

---

## Case 2 – Etter 2–3 år som dataingeniør i NVE

Case 1 er utgangspunktet mitt: erfaring med å følge data gjennom systemgrenser. I NVE vil jeg bygge videre fra software og integrasjon til dataprodukter som også skal fungere stabilt i daglig bruk.

![Min utviklingsreise i NVE: fra software- og integrasjonsbakgrunn via domene- og plattformlæring til selvstendig ansvar for større deler av dataprodukter.](docs/diagrammer/09-utviklingsreise-nve.svg)

### I dag – software og integrasjon

Jeg har en software- og integrasjonsprofil med Java, TypeScript, SQL/databaser, API-er, modellering, testing og grunnlag i CI/CD. Bachelorprosjektet ga erfaring med systemdesign og med å følge data fra input til lagring og konsumentrespons.

Styrken jeg tar med er å dele en løsning i forståelige ansvar, undersøke feil og teste det mottakeren faktisk får. Jeg har samtidig mer å lære om dataplattformer, analysemodeller og produksjonsdrift. Erfaringen fra en lokal PoC er et grunnlag å bygge videre på.

### Første tid – forstå domenet og arbeidsformen

Jeg vil først forstå hvilke kilder teamet bruker, hva dataene betyr, hvem som konsumerer dem og hvilke kvalitetskrav som følger av bruken. Jeg vil følge et eksisterende dataprodukt gjennom arkitektur, eierskap, tester og drift sammen med en erfaren kollega.

En god start er en avgrenset endring: forstå behovet, avtale forventet resultat, gjennomføre endringen og følge den helt ut til konsumenten. Slik kan jeg lære teamets arbeidsform og se hvordan kodegjennomgang, dokumentasjon og hendelseshåndtering fungerer i praksis.

Jeg vil bygge mer dybde i **SQL og Python**, og lære **dbt, Azure, Databricks og Airflow** gjennom konkrete oppgaver. Dette er læringsmål, ikke verktøy jeg fremstiller meg som ekspert på i dag. Retningen samsvarer med [NVEs satsing på data og plattform](https://www.nve.no/om-nve/jobb-i-nve/bli-en-del-av-nves-satsing-paa-data-plattform-og-gis/). Teamets faktiske arkitektur og behov vil styre hva jeg lærer først.

### Gradvis mer ansvar – hele dataproduktets livsløp

**Kilde → innhenting → transformasjon → modellering → datakvalitet → tilgjengeliggjøring → konsument → drift og overvåking.**

Etter hvert vil jeg kunne ta større leveranser gjennom denne kjeden, med faglige avklaringer og review underveis. Jeg vil bidra til robuste dataflyter, forståelige modeller og dokumenterte kontrakter, og bruke integrasjonsbakgrunnen min når eksterne kilder eller API-er inngår.

For eksempel ville jeg ved en ny datakilde avklart hva en rad eller hendelse betyr, hvordan oppdateringer håndteres, og hva konsumenten forventer. Deretter ville jeg gjort transformasjoner og kvalitetsregler testbare, dokumentert avvik og fulgt med på om dataene kommer frem som forventet. Dette er hvordan jeg ønsker å arbeide, ikke en påstand om en bestemt NVE-løsning.

Jeg vil også bidra til automatisert testing og CI/CD, og til **observability** som gjør det mulig å oppdage forsinkelser, manglende data og feil. Målet er at teamet kan forstå og rette problemer, og at konsumentene vet når et datagrunnlag har begrensninger.

### Etter 2–3 år – selvstendig med helhetsforståelse

Målet mitt er å være en selvstendig dataingeniør som kan ta ansvar for større deler av et dataprodukt fra behov til drift, samtidig som jeg vet når jeg bør involvere domeneeksperter og plattformkolleger.

Jeg ønsker å ha bidratt med dataflyter som er enklere å vedlikeholde, bedre modeller og kvalitetskontroller, og dokumentasjon som andre faktisk kan bruke. Faglig vil jeg ha utviklet dybde i plattformverktøyene, datamodellering og drift, samtidig som jeg beholder styrkene fra software engineering: systemgrenser, testing, feilsøking og integrasjon.

For meg innebærer selvstendighet også å delta i arkitekturdiskusjoner, begrunne avveininger og dele kunnskap. Jeg vil gjøre det lettere for neste kollega å forstå løsningen, ikke bare levere min egen oppgave.

### Team og samfunnsoppdrag

NVE arbeider med blant annet energi, vassdrag og naturfare. Jeg vil forstå hvordan data brukes i disse fagområdene og hvem som er avhengig av dem. [NVEs samfunnsoppdrag](https://www.nve.no/om-nve/dette-er-nve/) gir en konkret grunn til å være opptatt av datakvalitet og tydelige begrensninger.

Det motiverer meg å bygge løsninger der teknisk arbeid gir andre et mer pålitelig grunnlag for å gjøre jobben sin. Etter 2–3 år ønsker jeg å kunne koble domeneforståelse og teknisk gjennomføring: forstå behovet, levere data som kan brukes, og ta ansvar for at flyten fungerer over tid.
