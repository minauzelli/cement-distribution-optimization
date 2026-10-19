# Cement Distribution Network Optimization: A Capacity-Constrained Transportation Model (Turkey)

[Türkçe sürüm](README.md)

A linear programming model (Python, PuLP) that serves province-level demand at minimum transport effort for a Turkish cement producer's 10-plant network. As a screening step, it also answers: *where would a new plant reduce transport effort the most?*

> This is a **scenario-based case study built on public data**. No internal company data (actual shipments, costs, customers) was used. The tables below separate real data from assumptions.

## Problem

The company operates 7 integrated (clinker + cement) plants and 3 grinding plants. If 2025 demand is spread across Turkey's 81 provinces, which plant should serve which province, and what is the total transport work (ton-km)? Where is the biggest transport gap in the current network?

## Data sources and what is real vs. assumed

| Input | Source | Status |
|---|---|---|
| Plant locations and cement/clinker capacities | Company's public annual report (2025), KAP | Real |
| Province populations (2025, total 86,092,168) | TurkStat (TÜİK), Address-Based Population Registration System | Real |
| National cement production (77.19 Mt) and domestic sales (63.77 Mt), 2025 | TÜRKÇİMENTO, Monthly Economic Report (Dec 2025) | Real |
| Province and plant coordinates | City/district centers, approximate | Approximate |
| Province-level demand | Allocated in proportion to population | **Assumption** |
| Volume served by the company | Capacity × utilization (80%) × domestic-sales ratio (82.6%) | **Assumption** |
| Road distance | Straight-line × 1.3, 20 km floor | **Assumption** |

## Method

**Demand.** The company's domestic volume is `total capacity × utilization × (national domestic sales / national production)` (base case: 22.5 × 0.80 × 0.826 = 14.87 Mt/year), allocated to provinces by population share.

**Model.** `x[i,j]` is the quantity shipped from plant i to province j (Mt/year):

```
min  Σ x[i,j] · d[i,j]                  (total Mt·km)
s.t. Σ_i x[i,j] = demand[j]             every province's demand is met
     Σ_j x[i,j] ≤ 0.95 · capacity[i]    plant utilization cap
     x[i,j] ≥ 0
```

**New plant screening.** For each province, a hypothetical 1 Mt plant is added, the model is re-solved, and the reduction in transport work is ranked.

## Results (base case)

- Domestic volume served: **14.87 Mt/year** (66% of capacity)
- Total transport work: **2,435 million ton-km**, weighted average distance **164 km**
- Utilization by province: Ankara 95%, Kocaeli 95%, Denizli 94%, Mardin 82%, Zonguldak 65%, Hatay 49%, Ordu 40%, Bolu 39%, Adana 38%

**Sensitivity (utilization assumption):**

| Utilization | Volume (Mt) | Mt·km | Avg. distance (km) | Provinces with unchanged main supplier |
|---|---|---|---|---|
| 70% | 13.01 | 2,051 | 158 | 98.8% |
| 80% (base) | 14.87 | 2,435 | 164 | 100% |
| 90% | 16.73 | 2,857 | 171 | 93.8% |

Each province's main supplier is largely insensitive to the utilization assumption.

**New plant candidates** (1 Mt, reduction in transport work):

| Rank | Candidate province | Reduction (Mt·km) | Reduction (%) |
|---|---|---|---|
| 1 | İzmir | 219 | 9.0 |
| 2 | Manisa | 205 | 8.4 |
| 3 | Bursa | 202 | 8.3 |
| 4 | Tekirdağ | 199 | 8.2 |
| 5 | İstanbul | 195 | 8.0 |

The model shows a transport gap in the Marmara and Aegean regions, where population is dense but plants are sparse.

## Dashboard (Power BI)

The results are presented in a five-page Power BI dashboard. Data is loaded from the CSV files in the `powerbi/` folder. The dashboard itself is not published online; screenshots are shown below.

| Overview | Supply Network |
|---|---|
| ![Overview](images/sayfa1_genel_bakis.png) | ![Supply Network](images/sayfa2_tedarik_agi.png) |

| Sensitivity | New Plant |
|---|---|
| ![Sensitivity](images/sayfa3_duyarlilik.png) | ![New Plant](images/sayfa4_yeni_tesis.png) |

![Data and Assumptions](images/sayfa5_veri_varsayim.png)

## Limitations

- **This is a transport-based screening, not an investment recommendation.** Competitor plants, raw-material (limestone) locations, land and capital costs are not modeled.
- Demand is proportional to population and the company's share is assumed uniform across provinces; in reality cement demand follows construction activity and market share varies by region. The analysis can be repeated with building-permit data.
- The cost-minimizing solution pushes some plants to the 95% cap and leaves others at low utilization. Production costs and clinker flows are not modeled.
- Grinding plants (İskenderun, Ereğli) receive clinker from elsewhere; here they are treated as cement-producing plants.
- İskenderun I and II share the same coordinates, so the solver splits volume between them arbitrarily; read results at the province level.
- Distances are approximate road estimates; exports and overseas facilities are out of scope.

## How to run

```bash
pip install "pulp<4" pandas matplotlib jupyter
jupyter notebook dagitim_modeli.ipynb
```

PuLP 4.x has a different API, so install `pulp<4`. The notebook looks for the CSV files in the same folder (`VERI = "."`); update that variable if you move them into a subfolder.

## Files

| File | Contents |
|---|---|
| `dagitim_modeli.ipynb` | Model, results, sensitivity and new-plant analysis |
| `tesisler.csv` | 10 plants: province, district, coordinates, capacity |
| `iller_nufus_2025.csv` | 81 provinces, 2025 population and share |
| `il_koordinatlari.csv` | 81 province coordinates |
| `mesafe_tesis_il_km.csv`, `mesafe_il_il_km.csv` | Estimated road-distance matrices |
| `mesafe_hesapla.py` | Code that generates the distance matrices |
| `powerbi/` | Data files for the Power BI dashboard (5 CSVs) |
| `images/` | Dashboard screenshots |
| `README.md` | Turkish version |

## Possible extensions

- A second demand scenario using building-permit data
- Actual road distances and a TRY/ton-km freight cost
- Clinker flows (integrated plants to grinding plants) and a two-stage network
