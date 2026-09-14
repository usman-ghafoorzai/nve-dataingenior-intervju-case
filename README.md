# NVE – Casepresentasjon

**2. gangsintervju · Usman Ghafoorzai**

## Case 1 – Strukturert datautveksling i to retninger

Jeg tar utgangspunkt i **én interoperabilitetsløsning med to komplementære dataflyter** fra bachelorprosjektet: treningsdata inn til strukturert lagring og klinisk kontekst ut til konsumenten.

Vi var to studenter med felles ansvar for framdrift og kvalitet, og arbeidsformen var lagt opp slik at begge bidro til teknisk utvikling, dokumentasjon og kvalitetssikring gjennom prosjektet. Jeg arbeidet på tvers av analyse, design, implementasjon, testing/verifikasjon og rapportering.

> **Ramme:** Lokal PoC, simulert EPJ-miljø og syntetiske data. Produksjonsklar autentisering og autorisasjon, samt full synkroniserings- og konflikthåndtering, inngikk ikke i den implementerte PoC-en. Produksjonsintegrasjon og klinisk validering inngikk ikke.

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

### Implementert løsning og teknologier

![Implementert løsning: push via integrasjonsklient, HAPI FHIR og Subscription til bridge- og mappinglag og EHRbase; pull mellom klient, bridge og EHRbase. Begge repository-tjenestene bruker PostgreSQL.](docs/diagrammer/04-arkitektur.svg)

| Komponent / rolle | Teknologi og ansvar |
|---|---|
| Integrasjonsklient | **NestJS / TypeScript:** API-/DTO-grense, koordinering og tilpasning til konsumentformat. |
| Utveksling | **FHIR:** utvekslingsrepresentasjon. **HAPI FHIR:** ressurslagring og Subscription for push. |
| Bridge- og mappinglag | **Java / Spring:** transformasjon, EHR-oppslag og koordinering av lagring/uthenting. |
| Klinisk representasjon | **openEHR og template:** avgrenser forventet klinisk struktur for persistens. |
| Repository og persistens | **EHRbase:** openEHR-tjeneste. **PostgreSQL:** underliggende lagring for EHRbase og HAPI FHIR. |

Push brukte HAPI FHIR før bridge-laget. Pull brukte en separat uthentingsvei mellom integrasjonsklienten og bridge-laget. Applikasjonslogikken brukte tjenestegrensesnitt; PostgreSQL var underliggende persistens.

### Push – fra treningsdata til persistens

![Push-swimlane: input valideres i klienten og mappes til FHIR. HAPI FHIR lagrer og varsler bridge-laget, som bygger openEHR-struktur og lagrer gjennom EHRbase. Verifikasjon skjer separat.](docs/diagrammer/05-push.svg)

En syntetisk pasient var opprettet før innsending. Klienten validerte input, koordinerte flyten og mappet treningsdata til FHIR før videresending. HAPI FHIR lagret ressursen, og en konfigurert Subscription videresendte relevante nye ressurser til bridge-laget.

Bridge-laget fordelte mottaket til riktig behandling, hentet ut innholdet og bygde en openEHR composition mot forventet template-struktur. Riktig EHR ble funnet eller opprettet for den syntetiske pasienten før lagring gjennom EHRbase. Vi kontrollerte FHIR-resultatet og faktisk persistens separat fra kvitteringen ved inngangen.

### Pull – fra klinisk kontekst til konsument

![Pull-swimlane: validert forespørsel til bridge-laget; EHR-oppslag og tidsfiltrert AQL-uthenting fra EHRbase; parsing og mapping til FHIR før klienten lager konsumentrespons.](docs/diagrammer/06-pull.svg)

Konsumenten ba om oppdateringer for en pasient og et tidspunkt. Klienten validerte forespørselen; bridge-laget koordinerte EHR-oppslag og tidsfiltrert uthenting med **AQL** fra EHRbase.

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

- **API → FHIR:** DTO-validering kontrollerte input. Enhetstester med **Jest** kontrollerte mapping og logikk; API-kontroller undersøkte FHIR-resultatet.
- **FHIR → openEHR:** openEHR-templaten definerte forventet målstruktur. Tester av mappinglogikken og inspeksjon i **EHRbase** verifiserte transformasjonen og den faktiske persistensen. En template alene garanterer ikke datakvalitet eller klinisk riktighet.
- **openEHR → konsument:** AQL-verifikasjon, lokale E2E-tester og API-kontroller undersøkte uthenting, transformasjon, tidsfiltrering og tom respons. **Swagger/OpenAPI** støttet dokumentasjon og manuell kontroll.

Identifikatorer, responser og lagret/hentet innhold gjorde testdataene sporbare. **200 OK ved inngangen betyr ikke at hele dataflyten er korrekt.** Kontrollene gjaldt utvalgte tekniske scenarioer med syntetiske data.

### Ansvar, dataopprinnelse og kontrakter

Kildeapplikasjonen produserte treningsdataene; EPJ-miljøet var kilden til klinisk kontekst. Integrasjonsklienten validerte, transformerte og formidlet. Den var ingen autoritativ klinisk datakilde eller permanent klinisk lagring.

Vi hadde tydelige komponentansvar og tekniske grensesnittkontrakter gjennom **DTO/API-, FHIR- og openEHR-grensene**. Formaliserte datakontrakter, dataeierskap, SLA-er og driftsansvar var ikke etablert som i et produksjonsdataprodukt. I produksjon ville jeg formalisert eiere, versjonering, kvalitetskrav og ansvar ved feil og endringer.

### Største utfordring og designvalg

**Problem:** Den opprinnelige arkitekturen la opp til HAPI FHIR i begge retninger. Det fungerte for hendelsesdrevet push, men Subscription-mekanismen løste ikke behovet for forespørselsstyrt uthenting i pull.

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

Hvis vi spoler 2–3 år fram, ser jeg for meg at jeg har utviklet en tydeligere dataingeniørprofil fra software- og integrasjonsbakgrunnen i Case 1. Tilbakeblikket nedenfor beskriver hva jeg håper å ha bidratt med og hvordan jeg har utviklet meg, ikke erfaring jeg allerede har.

![Min utviklingsreise i NVE: fra software- og integrasjonsbakgrunn via domene- og plattformlæring til selvstendig ansvar for større deler av dataprodukter.](docs/diagrammer/09-utviklingsreise-nve.svg)

### Utgangspunktet – software og integrasjon

Jeg har en software- og integrasjonsprofil med Java, TypeScript, SQL/databaser, API-er, modellering, testing og grunnlag i CI/CD. Bachelorprosjektet ga erfaring med systemdesign og med å følge data fra input til lagring og konsumentrespons.

Styrken jeg tar med er å dele en løsning i forståelige ansvar, undersøke feil og teste det mottakeren faktisk får. Jeg har samtidig mer å lære om dataplattformer, datamodellering for analyse og produksjonsdrift. Erfaringen fra en lokal PoC er et grunnlag å bygge videre på.

### Første tid – forstå domenet og arbeidsformen

Jeg ser for meg at den første tiden handlet om å forstå kildene, dataenes betydning, konsumentene og kvalitetskravene. Sammen med en erfaren kollega fulgte jeg et eksisterende dataprodukt gjennom arkitektur, eierskap, tester og drift.

Jeg startet med avgrensede endringer: forstå behovet, avtale forventet resultat, gjennomføre endringen og følge den helt ut til konsumenten. Slik lærte jeg teamets arbeidsform og hvordan kodegjennomgang, dokumentasjon og hendelseshåndtering fungerer i praksis.

Gjennom konkrete oppgaver har jeg bygget mer dybde i **SQL og Python** og lært å bruke **dbt, Azure, Databricks og Airflow**. Dette er utviklingen jeg ser for meg, ikke verktøy jeg fremstiller meg som ekspert på i dag. Retningen samsvarer med [NVEs satsing på data og plattform](https://www.nve.no/om-nve/jobb-i-nve/bli-en-del-av-nves-satsing-paa-data-plattform-og-gis/). Teamets arkitektur og behov har styrt rekkefølgen på læringen.

### Gradvis mer ansvar – hele dataproduktets livsløp

**Kilde → innhenting → transformasjon → modellering → datakvalitet → tilgjengeliggjøring → konsument → drift og overvåking.**

Etter hvert har jeg tatt ansvar for større deler av leveranser gjennom denne kjeden, med faglige avklaringer og kodegjennomgang underveis. Jeg har bidratt til robuste dataflyter, forståelige modeller og dokumenterte kontrakter og avhengigheter, og brukt integrasjonsbakgrunnen min når eksterne kilder eller API-er inngår.

Et eksempel i dette scenarioet er en ny datakilde: Jeg har avklart hva en rad eller hendelse betyr, hvordan oppdateringer håndteres, og hva konsumenten forventer. Deretter har jeg gjort transformasjoner og kvalitetsregler testbare, dokumentert avvik og fulgt med på om dataene kommer frem som forventet.

Jeg har også bidratt til automatisert testing, CI/CD og **observability** som gjør det mulig å oppdage forsinkelser, manglende data og feil. Dette har gjort det enklere for teamet å forstå og rette problemer, og for konsumentene å kjenne datagrunnlagets begrensninger.

### Etter 2–3 år – selvstendig med helhetsforståelse

Etter 2–3 år ser jeg for meg at jeg har blitt en selvstendig dataingeniør som tar ansvar for større deler av et dataprodukt fra behov til drift, og vet når domeneeksperter og plattformkolleger bør involveres.

Bidraget mitt har vært dataflyter som er enklere å vedlikeholde, tydeligere modeller og kvalitetskontroller, og dokumentasjon som andre kan bruke. Faglig har jeg utviklet dybde i plattformverktøyene, datamodellering og drift, samtidig som jeg har beholdt styrkene fra software engineering: systemgrenser, testing, feilsøking og integrasjon.

Jeg har deltatt i arkitekturdiskusjoner, begrunnet avveininger og delt kunnskap. Samarbeidet har gjort meg tryggere på egne vurderinger og hjulpet neste kollega med å forstå løsningene.

### Team og samfunnsoppdrag

NVE arbeider med blant annet energi, vassdrag og naturfare. I dette tilbakeblikket har jeg fått bedre forståelse for hvordan data brukes i fagområdene og hvem som er avhengig av dem. [NVEs samfunnsoppdrag](https://www.nve.no/om-nve/dette-er-nve/) gir en konkret grunn til å være opptatt av datakvalitet og tydelige begrensninger.

Det motiverer meg å bygge løsninger der teknisk arbeid gir andre et mer pålitelig grunnlag for å gjøre jobben sin. Etter 2–3 år ser jeg for meg at jeg har koblet domeneforståelse og teknisk gjennomføring: forstått behovet, levert data som kan brukes, og tatt ansvar for at flyten fungerer over tid.
