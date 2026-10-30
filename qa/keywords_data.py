# Keyword table source data for the SEO deliverables.
#
# Honesty rules (see SEARCH_DEMAND_REPORT.md):
# - No search volume, difficulty or CPC is available. The data below contains NONE.
# - "origin": S = seed query given in the brief (section 5), G = intent seen as a gap in the
#   competitor research of 2026-10-30, H = expert hypothesis (a suggestion, not demand data).
# - "comp": 1 = result lists dominated by authority domains (law firms, government, big vendors);
#           2 = few or no service pages seen for the intent; 3 = mixed (directories, news, some service pages);
#           0 = not checked. All are observations in a US-located tool sample, not rankings.
# - CR (commercial relevance), SF (service fit), IP (probability that the searcher wants a
#   consultant service rather than free information) are 1-5 expert judgements.
# - GAP is 0-2: 2 = no service page seen in the sample, 1 = partial or fragmented, 0 = crowded.
#
# Row format: query | lang | geo | intent | origin | comp | CR | SF | IP | GAP | page | note
# intent: K commercial, T transactional, I informational, N navigational, R research
# geo: RU Russia, RS Serbia, BAL Balkans, INT international
# page: page key, "-" means no page (query not targeted)

ROWS = """
# ---- A. Serbia market entry ----
как выйти на рынок Сербии|RU|RU|I|S|3|4|5|3|1|A_ENTRY|
выход российского производителя на рынок Сербии|RU|RU|K|S|2|5|5|4|2|S_ENTRY|
продажи российских товаров в Сербии|RU|RU|K|S|3|4|4|3|1|S_ENTRY|
выход на рынок Сербии консультант|RU|RU|T|H|2|5|5|5|2|S_ENTRY|
выход на рынок Сербии|RU|RU|K|H|3|5|5|3|1|H|
Serbia market entry|EN|INT|K|S|1|5|5|3|0|H|
Serbia market entry consultant|EN|INT|T|S|1|5|5|5|0|S_ENTRY|
How to enter the Serbian market|EN|INT|I|S|1|4|5|2|0|A_ENTRY|
Business expansion to Serbia|EN|INT|K|S|1|3|4|3|0|S_ENTRY|
Go-to-market strategy Serbia|EN|INT|K|S|3|4|4|3|1|S_ENTRY|
FMCG market entry Serbia|EN|INT|K|H|3|5|5|4|1|S_ENTRY|
market entry strategy Serbia food|EN|INT|K|H|3|4|4|3|1|S_ENTRY|
Ulazak na tržište Srbije|SR|RS|K|S|3|4|5|3|1|S_ENTRY|
ulazak stranih kompanija na srpsko tržište|SR|RS|I|H|3|3|4|2|1|A_ENTRY|
# ---- B. Import and export ----
экспорт из России в Сербию|RU|RU|I|S|3|4|5|3|1|S_IMP|
импорт российских товаров в Сербию|RU|RU|K|S|3|4|5|3|1|S_IMP|
поставки товаров в Сербию|RU|RU|K|S|3|4|5|3|1|S_IMP|
экспорт продуктов питания в Сербию|RU|RU|K|S|3|5|5|3|1|A_IMP|
Russia Serbia trade consultant|EN|INT|T|S|2|5|5|5|2|S_IMP|
Import from Russia to Serbia|EN|INT|K|S|3|4|5|3|1|S_IMP|
Export to Serbia|EN|INT|K|S|1|3|4|2|0|S_IMP|
Uvoz robe iz Rusije|SR|RS|K|S|2|4|5|3|2|S_IMP|
Izvoz robe u Srbiju|SR|RS|K|S|2|3|4|3|1|S_IMP|
Izvoz iz Srbije u Rusiju|SR|RS|I|G|3|3|4|3|2|S_EXP|
export from Serbia to Russia|EN|INT|K|H|3|3|4|3|1|S_EXP|
экспорт из Сербии в Россию|RU|RS|K|H|3|3|3|3|1|S_EXP|
Russia Serbia free trade agreement|EN|INT|I|S|1|3|4|2|1|A_EAEU|
соглашение о свободной торговле Сербия ЕАЭС|RU|RU|I|H|3|3|4|2|2|A_EAEU|
зона свободной торговли Россия Сербия|RU|RU|I|H|3|3|4|2|2|A_EAEU|
сертификат происхождения СТ-2 Сербия|RU|RU|I|G|3|3|4|2|2|A_EAEU|
EAEU Serbia free trade agreement rules of origin|EN|INT|I|H|2|3|4|2|1|A_EAEU|
sporazum o slobodnoj trgovini Srbija EAEU|SR|RS|I|H|3|2|3|2|2|A_EAEU|
# ---- C. Distributors and buyers ----
найти дистрибьютора в Сербии|RU|RU|T|S|2|5|5|5|2|S_DIST|
дистрибьюторы продуктов питания Сербия|RU|RU|K|S|2|5|5|4|2|S_DIST|
оптовые покупатели Сербия|RU|RU|K|S|3|4|4|3|1|S_DIST|
поиск торговых партнеров в Белграде|RU|RS|K|S|2|4|5|4|2|S_DIST|
как найти дистрибьютора в Сербии|RU|RU|I|G|2|5|5|4|2|A_DIST|
Find distributors in Serbia|EN|INT|T|S|2|5|5|5|2|S_DIST|
Serbia FMCG distributors|EN|INT|K|S|3|5|5|4|1|S_DIST|
Food distributors Serbia|EN|INT|K|S|3|5|5|3|1|S_DIST|
Distributor sourcing Serbia|EN|INT|T|S|2|5|5|5|2|S_DIST|
Finding wholesale buyers in Serbia|EN|INT|K|S|3|4|4|3|1|S_DIST|
how to choose a distributor in Serbia|EN|INT|I|H|3|4|5|3|1|A_DIST|
distributor due diligence Serbia|EN|INT|I|G|3|3|3|2|1|A_DIST|
distribution agreement Serbia exclusive distributor|EN|INT|I|G|1|3|3|2|0|A_DIST|
договор дистрибуции Сербия|RU|RU|I|H|3|3|3|2|1|A_DIST|
Pronalaženje distributera u Srbiji|SR|RS|T|S|2|4|5|4|2|S_DIST|
ugovor o distribuciji Srbija|SR|RS|I|H|1|2|3|1|0|A_DIST|
distributer hrane Srbija|SR|RS|K|H|3|2|3|2|1|S_DIST|
# ---- D. FMCG and food ----
российские продукты в Сербии|RU|RS|K|S|3|2|3|2|1|S_IMP|mixed audience, includes consumers
российские сладости оптом Сербия|RU|RS|T|S|3|3|3|3|1|S_DIST|
кондитерские изделия экспорт Сербия|RU|RU|K|S|2|5|5|4|2|A_IMP|
поставки снеков в Сербию|RU|RU|K|S|2|5|5|4|2|A_IMP|
как экспортировать кондитерские изделия в Сербию|RU|RU|I|H|2|5|5|4|2|A_IMP|
FMCG market Serbia|EN|INT|R|S|3|4|4|2|1|S_RES|
Food distribution Serbia|EN|INT|K|S|3|5|5|3|1|S_DIST|
Confectionery distributors Serbia|EN|INT|K|S|3|4|5|4|1|S_DIST|
Healthy snacks Serbia distribution|EN|INT|K|S|2|4|5|4|2|S_DIST|
Serbian supermarket suppliers|EN|INT|K|S|3|3|4|2|1|A_RETAIL|
FMCG tržište Srbije|SR|RS|R|H|3|3|4|2|1|S_RES|
tržište hrane u Srbiji analiza|SR|RS|R|H|3|3|4|2|1|S_RES|
# ---- E. Retail chains ----
как стать поставщиком Maxi|RU|RU|T|S|2|4|4|4|2|A_RETAIL|chain named in query; the site makes no claim of agreements with chains
как попасть в торговые сети Сербии|RU|RU|I|S|2|5|5|4|2|A_RETAIL|
как предложить продукцию сербскому ритейлеру|RU|RU|I|S|2|5|5|4|2|A_RETAIL|
условия работы с торговыми сетями Сербии|RU|RU|I|G|2|4|5|3|2|A_RETAIL|
листинг в торговой сети Сербия|RU|RU|K|H|2|4|5|3|2|A_RETAIL|
крупнейшие торговые сети Сербии|RU|RU|R|H|3|3|4|2|1|A_RETAIL|
How to become a supermarket supplier in Serbia|EN|INT|I|S|2|5|5|4|2|A_RETAIL|
Retail listing Serbia|EN|INT|K|S|2|5|5|4|2|A_RETAIL|
Supplier requirements Serbian supermarkets|EN|INT|I|S|2|5|5|3|2|A_RETAIL|
Lidl Serbia supplier|EN|INT|N|S|2|3|3|3|2|A_RETAIL|chain named in query
listing fee Serbia retail|EN|INT|I|H|2|3|5|3|2|A_RETAIL|
Law on Trade Practices Serbia suppliers|EN|INT|I|G|2|3|4|2|1|A_RETAIL|
Serbia retail chains list|EN|INT|R|H|3|3|4|2|1|A_RETAIL|
kako postati dobavljač trgovinskog lanca u Srbiji|SR|RS|I|G|2|4|5|3|2|A_RETAIL|
zakon o trgovačkim praksama dobavljači|SR|RS|I|G|3|2|3|1|1|A_RETAIL|audience mostly Serbian suppliers
# ---- F. Commercial representative ----
представитель компании в Сербии|RU|RU|K|S|2|4|5|4|2|S_REP|
найти торгового представителя в Белграде|RU|RS|T|S|2|5|5|5|2|S_REP|
коммерческий агент Сербия|RU|RU|K|S|2|4|4|3|2|S_REP|
представительство российского производителя|RU|RU|K|S|2|4|4|3|2|A_REP|
филиал или представительство в Сербии|RU|RU|I|H|1|2|3|2|0|A_REP|
Local commercial representative Serbia|EN|INT|T|S|2|5|5|5|2|S_REP|
Sales agent Serbia|EN|INT|K|S|2|4|4|4|2|S_REP|
Business development representative Belgrade|EN|INT|T|S|2|4|4|4|2|S_REP|
Outsourced sales Serbia|EN|INT|K|S|2|4|4|4|2|S_REP|
agent vs distributor Serbia|EN|INT|I|H|3|4|5|3|1|A_REP|
commercial agency agreement Serbia|EN|INT|I|G|1|3|3|2|0|A_REP|
open representative office Serbia|EN|INT|I|H|1|2|3|2|0|A_REP|
komercijalni zastupnik Srbija|SR|RS|K|G|2|3|4|3|2|A_REP|
poslovni predstavnik stranog proizvođača Srbija|SR|RS|K|H|2|4|4|3|2|S_REP|
# ---- G. Research and analytics ----
анализ рынка Сербии|RU|RU|R|S|3|4|4|3|1|S_RES|
исследование FMCG рынка Сербии|RU|RU|R|S|2|5|5|4|2|S_RES|
цены на продукты в Сербии|RU|RS|R|S|3|2|3|2|1|A_RES|mixed audience, includes consumers and tourists
конкуренты на сербском рынке|RU|RU|R|S|3|3|4|3|1|S_RES|
расчет полной стоимости поставки в Сербию|RU|RU|I|G|2|4|5|3|2|A_RES|
ценообразование на сербском рынке|RU|RU|R|S|3|4|4|3|1|A_RES|
Serbia market research|EN|INT|R|S|1|5|5|4|0|S_RES|
Serbia retail market analysis|EN|INT|R|S|3|4|4|3|1|S_RES|
FMCG pricing Serbia|EN|INT|R|S|3|4|4|3|1|A_RES|
Competitive analysis Serbia|EN|INT|R|S|3|4|4|3|1|S_RES|
Market feasibility study Serbia|EN|INT|K|S|3|4|5|4|1|S_RES|
landed cost Serbia import|EN|INT|I|G|1|4|4|3|1|A_RES|
shelf price survey Serbia|EN|INT|R|H|2|4|5|3|2|A_RES|
cena na polici maloprodaja Srbija analiza|SR|RS|R|H|3|3|3|2|1|A_RES|
# ---- H. Customs, logistics, regulation ----
растаможка товаров в Сербии|RU|RU|I|S|3|2|2|1|1|A_IMP|searchers often look for a broker; service not offered
сертификация продуктов питания Сербия|RU|RU|I|S|3|3|3|2|1|A_IMP|
таможенные пошлины Россия Сербия|RU|RU|I|S|3|2|3|1|1|A_EAEU|
доставка товаров Россия Сербия|RU|RU|T|S|3|2|2|2|1|A_EAEU|freight is not offered
маркировка продуктов для Сербии|RU|RU|I|H|3|3|4|2|2|A_IMP|
НДС при импорте в Сербию|RU|RU|I|H|3|3|4|2|1|A_IMP|
ветеринарное свидетельство Сербия мясо|RU|RU|I|H|3|2|3|2|1|A_IMP|
Serbia food import regulations|EN|INT|I|S|1|3|4|2|0|A_IMP|
Serbia customs clearance|EN|INT|T|S|1|2|2|1|0|A_IMP|searchers often look for a broker; service not offered
Serbia food labeling requirements|EN|INT|I|S|2|3|4|2|1|A_IMP|
Serbia import VAT food|EN|INT|I|H|2|3|4|2|1|A_IMP|
importer of record Serbia|EN|INT|I|H|2|3|4|3|1|A_IMP|
uvoz hrane u Srbiju propisi|SR|RS|I|H|2|3|4|2|1|A_IMP|
deklarisanje hrane Srbija uvoznik|SR|RS|I|H|2|3|4|2|1|A_IMP|
таможенный брокер Сербия|RU|RU|T|H|3|1|1|1|1|-|not offered; Dmitry is not a licensed customs broker
customs broker Serbia|EN|INT|T|H|1|1|1|1|0|-|not offered; Dmitry is not a licensed customs broker
# ---- I. Direct search for a consultant ----
эксперт по экспорту в Сербию|RU|RU|T|S|2|5|5|5|2|H|
консультант по импорту Сербия|RU|RU|T|S|2|5|5|5|2|S_IMP|
бизнес-консультант Белград|RU|RS|T|S|3|4|4|4|1|H|
специалист по выходу на рынок Сербии|RU|RU|T|S|2|5|5|5|2|S_ENTRY|
Serbia business consultant|EN|INT|T|S|1|4|5|4|0|H|
Serbia trade consultant|EN|INT|T|S|2|5|5|5|1|H|
Market entry expert Belgrade|EN|INT|T|S|2|5|5|5|2|S_ENTRY|
FMCG consultant Serbia|EN|INT|T|S|2|5|5|5|2|S_ENTRY|
consultant for Russian companies in Serbia|EN|INT|T|H|2|4|5|4|2|H|
Russian-speaking business consultant Belgrade|EN|INT|T|H|2|4|4|4|2|ABOUT|
Konsultant za međunarodnu trgovinu Srbija|SR|RS|T|S|2|4|4|4|2|H|
konsultant za uvoz i izvoz Srbija|SR|RS|T|H|2|4|4|4|2|S_IMP|
# ---- J. Brand ----
Dmitry Astakhov|EN|INT|N|S|2|4|5|3|2|ABOUT|name shared with many unrelated people
Dmitry Astakhov Serbia|EN|INT|N|S|2|4|5|3|2|ABOUT|
Dmitry Astakhov Belgrade|EN|INT|N|S|2|4|5|3|2|ABOUT|
Dmitry Astakhov market entry|EN|INT|N|S|2|4|5|3|2|H|
Дмитрий Астахов Сербия|RU|RU|N|S|2|4|5|3|2|ABOUT|
Дмитрий Астахов Белград|RU|RS|N|S|2|4|5|3|2|ABOUT|
Дмитрий Астахов экспорт импорт|RU|RU|N|S|2|4|5|3|2|ABOUT|
Dmitrij Astahov Srbija|SR|RS|N|S|2|4|5|3|2|ABOUT|
Dmitrij Astahov Beograd|SR|RS|N|S|2|4|5|3|2|ABOUT|
# ---- K. Adjacent topics from section 6 of the brief ----
выбор бизнес-партнера в Сербии|RU|RU|I|S|3|3|3|2|1|A_DIST|
оптовая торговля Сербия|RU|RS|K|S|3|3|3|2|1|S_DIST|
международная дистрибуция|RU|INT|I|S|3|2|3|2|0|A_DIST|
импорт продуктов питания в Сербию|RU|RU|K|S|3|5|5|3|1|A_IMP|
Importing food products into Serbia|EN|INT|K|S|1|4|5|3|0|A_IMP|
развитие продаж в Сербии|RU|RS|K|S|3|4|4|3|1|S_ENTRY|
переговоры с сербскими партнерами|RU|RU|I|S|3|3|3|2|1|S_REP|
Brand representation Serbia|EN|INT|K|S|2|4|4|3|2|S_REP|
конкурентоспособность российских товаров в Сербии|RU|RU|R|S|3|3|4|2|1|S_RES|
сербский потребительский рынок|RU|RU|R|S|3|3|3|2|1|S_RES|
Serbian consumer market|EN|INT|R|S|3|2|3|2|0|S_RES|
автоматизация коммерческих процессов|RU|RU|K|S|3|3|3|3|0|S_AUTO|broad topic; Dmitry's second pillar
CRM и автоматизация отчетов для оптовой торговли|RU|RU|K|H|3|3|4|3|1|S_AUTO|
sales reporting automation for distributors|EN|INT|K|H|3|3|4|3|1|S_AUTO|
business process automation Belgrade|EN|RS|K|H|3|3|3|3|1|S_AUTO|
automatizacija poslovnih procesa Beograd|SR|RS|K|H|3|2|3|3|1|S_AUTO|
# ---- L. Balkans and other languages (hypotheses, no separate pages) ----
distribution consultant Balkans|EN|BAL|T|H|0|3|2|3|1|H|expertise outside Serbia not confirmed
export to Montenegro from Serbia|EN|BAL|K|H|0|2|2|2|1|-|only mentioned as a route in the CV; no page
Markteintritt Serbien Beratung|DE|INT|T|H|0|3|3|3|1|-|no German version; no demand data
Sırbistan pazarına giriş danışmanlık|TR|INT|T|H|0|3|3|3|1|-|no Turkish version; no demand data
进入塞尔维亚市场 咨询|ZH|INT|T|H|0|3|3|3|1|-|no Chinese version; no demand data
# ---- M. Deliberately excluded (high volume is possible, fit is low) ----
работа в Сербии|RU|RU|I|S|3|1|1|1|0|-|likely high volume, does not lead to service inquiries
jobs in Serbia|EN|INT|I|H|3|1|1|1|0|-|same reason
открытие бизнеса в Сербии|RU|RU|I|S|3|2|1|1|0|-|audience is relocation and company registration; service not offered
виза в Сербию для россиян|RU|RU|I|H|3|1|1|1|0|-|not related to services
"""

# Page registry: key -> (page id used by lib/pages.ts, English label)
PAGES = {
    'H': 'home',
    'ABOUT': 'about',
    'SVCS': 'services',
    'S_ENTRY': 'svc:serbia-market-entry',
    'S_DIST': 'svc:find-distributors-in-serbia',
    'S_IMP': 'svc:import-to-serbia',
    'S_EXP': 'svc:export-from-serbia',
    'S_REP': 'svc:local-commercial-representation',
    'S_RES': 'svc:serbia-market-research',
    'S_AUTO': 'svc:business-automation',
    'A_ENTRY': 'art:how-to-enter-the-serbian-market',
    'A_DIST': 'art:finding-distributors-in-serbia',
    'A_IMP': 'art:importing-food-products-into-serbia',
    'A_RETAIL': 'art:selling-to-serbian-retail-chains',
    'A_RES': 'art:serbia-market-research-before-you-ship',
    'A_REP': 'art:local-commercial-representation-in-serbia',
    'A_EAEU': 'art:russia-serbia-trade-agreements-for-exporters',
    'CONTACT': 'contact',
}

CLUSTERS = {
    'A': 'A. Выход на рынок Сербии',
    'B': 'B. Импорт и экспорт',
    'C': 'C. Дистрибьюторы и покупатели',
    'D': 'D. FMCG и продукты питания',
    'E': 'E. Торговые сети',
    'F': 'F. Коммерческий представитель',
    'G': 'G. Исследования и аналитика',
    'H': 'H. Таможня, логистика и регулирование',
    'I': 'I. Прямой поиск консультанта',
    'J': 'J. Брендовые запросы',
    'K': 'K. Смежные темы (раздел 6 ТЗ)',
    'L': 'L. Балканы и другие языки (гипотезы)',
    'M': 'M. Исключенные запросы',
}
