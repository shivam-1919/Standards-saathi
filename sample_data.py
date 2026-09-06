"""
Sample BIS (Bureau of Indian Standards) Data and Indian Standards (IS Codes).
Enriched with detailed metadata: filename, page numbers, section clauses,
BIS purchase/view URLs, and related standards.
"""

SAMPLE_STANDARDS = [
    {
        "id": "IS-2720-P1",
        "standard_number": "IS 2720 (Part 1):1983",
        "title": "Methods of Test for Soils — Part 1: Preparation of Dry Soil Samples for Various Tests (Second Revision, Reaffirmed 2020)",
        "category": "Civil & Geotechnical Engineering",
        "department": "Civil Engineering Department (CED 23: Soil Engineering and Rock Mechanics)",
        "status": "National Standard for Soil Mechanics & Foundation Testing",
        "filename": "IS_2720_Part_1_1983.pdf",
        "purchase_url": "https://www.standardsbis.in/gemini/detail/IS_2720_Part_1",
        "related_standards": ["IS 2720 (Part 2):1973", "IS 2720 (Part 4):1985", "IS 2720 (Part 5):1985", "IS 2720 (Part 7):1980", "IS 2720 (Part 16):1987", "IS 460 (Part 1):1978"],
        "summary": "Covers the standard method of preparation of dry soil samples from the bulk soil sample received from the field for various laboratory tests including grain size analysis, liquid/plastic limits, compaction, specific gravity, CBR, direct shear, and chemical tests.",
        "clauses": [
            {
                "clause_id": "Clause 2 / Apparatus",
                "clause_title": "Apparatus for Soil Sample Preparation (Mallet, Pulverizer, Sieves, Oven)",
                "page_number": 4,
                "section_number": "Section 2.0",
                "content": (
                    "Essential apparatus for soil sample preparation under IS 2720 (Part 1):\n"
                    "1. Wooden Mallet: For breaking up soil clods without crushing individual mineral grains.\n"
                    "2. Trays: For air drying of soil, made of non-rusting material.\n"
                    "3. Pulverizing Apparatus: Mortar with rubber-covered pestle or mechanical power-driven rubber-covered pestle (or soft wood mortar/pestle) to break aggregations without reducing grain sizes.\n"
                    "4. Sampler: Riffle sampler or sample splitter for quartering/representative sub-sampling (conforming to IS 1607).\n"
                    "5. Standard Test Sieves (IS 460 Part 1): 75-mm, 63-mm, 37.5-mm, 19-mm, 13.2-mm, 9.50-mm, 6.7-mm, 4.75-mm, 2.00-mm, and 425-micron.\n"
                    "6. Drying Oven: Thermostatically controlled with non-corroding interior maintaining temperature between 105°C and 110°C.\n"
                    "7. Balances: 10 kg capacity (sensitivity 100 g), 1 kg capacity (sensitivity 1 g), and 250 g capacity (sensitivity 0.01 g)."
                ),
                "keywords": ["soil testing apparatus", "wooden mallet", "pulverizing mortar", "riffle sampler", "sieves", "drying oven", "IS 2720", "soil preparation"]
            },
            {
                "clause_id": "Clause 3 / Drying",
                "clause_title": "Drying and Pulverization of Soil Sample (Temperature Limits & Organic Matter)",
                "page_number": 4,
                "section_number": "Section 3.1 & 3.2",
                "content": (
                    "Standard sample preparation and drying procedures:\n"
                    "1. General Drying: Soil sample received from the field shall be dried in air or sun. In wet weather, a drying apparatus may be used where temperature shall NOT exceed 60°C.\n"
                    "2. Organic / Calcareous Soils: Soils containing organic matter or calcareous matter shall NOT be dried at temperatures above 60°C.\n"
                    "3. Debris Removal: Organic matter like tree roots, bark pieces, and shells must be separated, noted, and their percentage recorded. For estimation of organic/lime content, total unseparated sample is used.\n"
                    "4. Pulverization: Break large clods with a wooden mallet and mortar/rubber pestle until soil passes the specified test sieve. Care must be taken not to crush individual soil grains.\n"
                    "5. Sub-sampling: Smaller samples must be extracted by quartering or riffling (for coarse gravels, mix thoroughly on flat surface and divide into 4 quadrants; cone quartering is prohibited)."
                ),
                "keywords": ["soil drying temperature", "60 degrees", "air drying", "pulverization", "quartering", "calcareous soil", "organic soil", "IS 2720 Part 1"]
            },
            {
                "clause_id": "Table 1 / Clause 4.1",
                "clause_title": "Quantity of Soil Sample Required for Various Laboratory Tests",
                "page_number": 5,
                "section_number": "Section 4.1",
                "content": (
                    "Summary of required soil sample quantities and sieve sizes under IS 2720:\n"
                    "- Water Content (Part 2): Oven dry 24 h at 105–110°C; 25 g (<425µm) up to 1000 g (<37.5mm).\n"
                    "- Specific Gravity (Part 3): 50 g (fine-grained passing 2 mm) or 400 g (medium/coarse-grained).\n"
                    "- Grain Size Analysis (Part 4): Air-dried sample, 0.4 kg (<4.75mm) up to 60 kg (75mm).\n"
                    "- Liquid Limit & Plastic Limit (Part 5): 270 g and 60 g respectively, passing 425-micron IS sieve.\n"
                    "- Shrinkage Factors (Part 6): 100 g passing 425-micron sieve.\n"
                    "- Compaction Tests (Part 7 Light & Part 8 Heavy): 6 kg (or 15 kg if crushing occurs) passing 19-mm sieve.\n"
                    "- CBR (California Bearing Ratio - Part 16): 6 kg passing 19-mm sieve (air-dried).\n"
                    "- Direct Shear Test (Part 13): 1 kg passing 4.75-mm sieve.\n"
                    "- Permeability (Part 17): 2.5 kg for 100 mm dia mold / 5 kg for 200 mm dia mold (passing 9.5-mm sieve).\n"
                    "- Free Swell Index (Part 40): 20 g oven-dried soil passing 425-micron sieve.\n"
                    "- Swelling Pressure (Part 41): 2 kg passing 2-mm sieve."
                ),
                "keywords": ["soil sample quantity", "liquid limit sample", "CBR sample", "compaction sample", "grain size quantity", "free swell", "IS 2720 Table 1"]
            }
        ]
    },
    {
        "id": "IS-10262",
        "standard_number": "IS 10262:2019",
        "title": "Concrete Mix Proportioning — Guidelines (Second Revision)",
        "category": "Civil & Structural Engineering",
        "department": "Civil Engineering Department (CED 2: Cement and Concrete)",
        "status": "National Standard for Concrete Mix Design",
        "filename": "IS_10262_2019.pdf",
        "purchase_url": "https://www.standardsbis.in/gemini/detail/IS_10262_2019",
        "related_standards": ["IS 456:2000", "IS 383:2016", "IS 9103:1999", "IS 1199 (Part 6):2018", "IS 3812 (Part 1):2013", "IS 16714:2018", "IS 15388:2003"],
        "summary": "Comprehensive guidelines for proportioning concrete mixes for Ordinary (M10–M20), Standard (M25–M60), High Strength (M65–M100), Self-Compacting Concrete (SCC), and Mass Concrete. Covers target mean strength calculation, w/c ratio selection, aggregate volume fractions, and illustrative trial mix designs.",
        "clauses": [
            {
                "clause_id": "Clause 4.2 / Table 1 & 2",
                "clause_title": "Target Mean Compressive Strength Formula & Standard Deviation",
                "page_number": 2,
                "section_number": "Section 4.2",
                "content": (
                    "Target mean compressive strength at 28 days (f'ck) is calculated by:\n"
                    "f'ck = fck + 1.65 S  OR  f'ck = fck + X (whichever is HIGHER)\n"
                    "Where:\n"
                    "- fck = Characteristic compressive strength at 28 days in N/mm²\n"
                    "- S = Standard deviation in N/mm² (calculated from >=30 test results or assumed from Table 2: 3.5 for M10-M15; 4.0 for M20-M25; 5.0 for M30-M60; 6.0 for M65-M80)\n"
                    "- X = Factor based on grade of concrete (Table 1: 5.0 for M10-M15; 5.5 for M20-M25; 6.5 for M30-M60; 8.0 for M65 and above).\n"
                    "Example for M40: f'ck = 40 + 1.65(5) = 48.25 N/mm² vs 40 + 6.5 = 46.5 N/mm² -> Target is 48.25 N/mm²."
                ),
                "keywords": ["target strength", "f'ck", "standard deviation", "Table 1 factor X", "M40 mix design", "concrete mix proportioning", "IS 10262", "fck + 1.65S"]
            },
            {
                "clause_id": "Clause 5.3 / Table 4 & 5",
                "clause_title": "Water Content and Coarse Aggregate Proportioning (Normal & Standard Concrete)",
                "page_number": 4,
                "section_number": "Section 5.3 & 5.5",
                "content": (
                    "1. Water Content (Table 4 for 50 mm slump with crushed angular aggregate):\n"
                    "   - 10 mm aggregate: 208 kg/m³\n"
                    "   - 20 mm aggregate: 186 kg/m³\n"
                    "   - 40 mm aggregate: 165 kg/m³\n"
                    "   - Adjustments: +/- 3% water for every +/- 25 mm slump variation. Reduce by 10 kg for sub-angular, 15 kg for gravel, 20 kg for rounded gravel. Superplasticizers reduce water by 20% to 30%+.\n"
                    "2. Coarse Aggregate Volume (Table 5 for w/c = 0.50):\n"
                    "   - For 20 mm aggregate: Zone I sand = 0.60, Zone II = 0.62, Zone III = 0.64, Zone IV = 0.66.\n"
                    "   - Correction: Increase coarse aggregate by 0.01 for every 0.05 decrease in w/c ratio (and vice versa).\n"
                    "   - Pumpable concrete: Coarse aggregate proportion may be reduced by up to 10%."
                ),
                "keywords": ["water content", "Table 4", "Table 5", "coarse aggregate volume", "slump adjustment", "superplasticizer", "IS 10262", "20mm aggregate"]
            },
            {
                "clause_id": "Section 3 / Table 8 & 9",
                "clause_title": "High Strength Concrete (Grade M65 to M100)",
                "page_number": 7,
                "section_number": "Section 3.0",
                "content": (
                    "High Strength Concrete (HSC >= M65 N/mm²):\n"
                    "1. Low w/cm ratio (0.24 to 0.36 per Table 8) achieved using PCE (Polycarboxylate Ether) superplasticizers with >= 30% water reduction.\n"
                    "2. Maximum aggregate size restricted to 20 mm (10–12.5 mm preferred for M80 and above; flakiness/elongation index <= 30%, crushing value <= 22%).\n"
                    "3. Mineral Admixtures (Table 9): Fly ash (15–30%), GGBS (25–50%), Metakaolin (5–15%), Silica fume (5–10%).\n"
                    "4. Entrapped air (Table 6): 0.5% for 20 mm aggregate, 0.8% for 12.5 mm, 1.0% for 10 mm."
                ),
                "keywords": ["high strength concrete", "M65", "M70", "M80", "M100", "silica fume", "PCE superplasticizer", "Table 8", "Table 9", "IS 10262"]
            },
            {
                "clause_id": "Section 4 / Section 4.0",
                "clause_title": "Self-Compacting Concrete (SCC) Mix Proportioning",
                "page_number": 10,
                "section_number": "Section 4.0",
                "content": (
                    "Self-Compacting Concrete (SCC) flows under its own weight without segregation or mechanical vibration:\n"
                    "1. Fresh Properties (IS 1199 Part 6):\n"
                    "   - Slump Flow: SF1 (550–650 mm), SF2 (660–750 mm), SF3 (760–850 mm).\n"
                    "   - Passing Ability (L-Box): Ratio h2/h1 >= 0.8 (1.0 for ideal water-like flow).\n"
                    "   - Viscosity (V-Funnel): Class V1 (<= 8 s), Class V2 (8 to 25 s).\n"
                    "   - Sieve Segregation Resistance: SR1 (15–20%), SR2 (< 15%).\n"
                    "2. Mix Proportioning:\n"
                    "   - Total powder content (< 0.125 mm): 400 to 600 kg/m³ (includes cement, fly ash, micro-fines).\n"
                    "   - Water/powder ratio: 0.85 to 1.10 by volume.\n"
                    "   - Sand content: 48% to 60% of total aggregate; use of PCE HRWRA and Viscosity Modifying Admixtures (VMA)."
                ),
                "keywords": ["self compacting concrete", "SCC", "slump flow", "SF1", "SF2", "SF3", "L-box", "V-funnel", "VMA", "powder content", "IS 10262 Section 4"]
            },
            {
                "clause_id": "Section 5 / Section 5.0",
                "clause_title": "Mass Concrete Mix Proportioning (Dams, Rafts, 40/80/150 mm Aggregates)",
                "page_number": 12,
                "section_number": "Section 5.0",
                "content": (
                    "Proportioning for massive structures (dams, bridge piers, thick raft foundations):\n"
                    "1. Objective: Minimize heat of hydration and thermal cracking while ensuring durability.\n"
                    "2. Aggregate Sizes: Uses 40 mm, 80 mm, and 150 mm maximum nominal size of aggregate (msa).\n"
                    "3. Target Strength Wet-Sieving Correction: Target strength calculated is increased by 20% for 80 mm msa and by 25% for 150 mm msa for 150 mm cube testing.\n"
                    "4. Water Content (Table 12 for 50 mm slump): 165 kg (40 mm), 145 kg (80 mm), 125 kg (150 mm). Reduced by 10–20 kg for rounded gravels.\n"
                    "5. Air Entrainment: 3% to 4% for 150 mm msa and 3.5% to 4.5% for 80 mm msa to enhance freeze-thaw durability and reduce bleeding."
                ),
                "keywords": ["mass concrete", "dams", "150mm aggregate", "80mm aggregate", "heat of hydration", "wet sieving", "air entrainment", "Table 12", "IS 10262 Section 5"]
            }
        ]
    },
    {
        "id": "IS-456",
        "standard_number": "IS 456:2000 (with Amendments 1–5)",
        "title": "Plain and Reinforced Concrete — Code of Practice (Fourth Revision, with Amendments 1 to 5 up to 2019)",
        "category": "Civil & Structural Engineering",
        "department": "Civil Engineering Department (CED 2: Cement and Concrete)",
        "status": "National Standard & Mandatory Structural Code of India",
        "filename": "IS_456_2000_Amend_1_5.pdf",
        "purchase_url": "https://www.standardsbis.in/gemini/detail/IS_456_2000",
        "related_standards": ["IS 10262:2019", "IS 1786:2008", "IS 383:2016", "IS 13920:2016", "IS 16172:2014"],
        "summary": "The premier code of practice for design and construction of plain and reinforced concrete structures in India. Governs materials (cements, mineral admixtures, water, aggregates), concrete grades (M10–M100), durability & exposure criteria (Table 5), formwork stripping periods (Table 11.3.1), reinforcement detailing, development length, and limit state design.",
        "clauses": [
            {
                "clause_id": "Clause 5 & Table 1",
                "clause_title": "Materials: Cements, Mineral Admixtures, and Water Permissible Limits",
                "page_number": 13,
                "section_number": "Section 2.0 (Cl 5.1 - 5.4)",
                "content": (
                    "Materials requirements per IS 456 (incorporating Amendments 1–5):\n"
                    "1. Cement Types: OPC 33/43/53 (IS 269), PSC (IS 455), PPC fly ash/clay based (IS 1489), Sulphate Resisting (IS 12330).\n"
                    "2. Mineral Admixtures: Fly ash (IS 3812 Part 1 >= 25%), GGBS (IS 16714 >= 50%), Silica fume (IS 15388 5–10%), Metakaolin (IS 16354 5–15%). Fibres may be added per Cl 5.7.\n"
                    "3. Water Permissible Limits (Table 1):\n"
                    "   - pH value: Not less than 6.0.\n"
                    "   - Organic solids: Max 200 mg/L\n"
                    "   - Inorganic solids: Max 3000 mg/L\n"
                    "   - Sulphates (as SO4): Max 400 mg/L (SO3 = 0.833 SO4)\n"
                    "   - Chlorides (as Cl): Max 2000 mg/L for PCC; Max 500 mg/L for RCC.\n"
                    "   - Suspended matter: Max 2000 mg/L.\n"
                    "   - Sea Water: Strict prohibition — sea water shall NOT be used for mixing or curing RCC."
                ),
                "keywords": ["water permissible limits", "chloride in concrete", "sulphate limit", "pH of water", "mineral admixtures", "fly ash", "silica fume", "GGBS", "IS 456 Table 1"]
            },
            {
                "clause_id": "Table 2 / Clause 6.1",
                "clause_title": "Grades of Concrete (Ordinary, Standard, High Strength M10 to M100)",
                "page_number": 16,
                "section_number": "Section 6.1",
                "content": (
                    "Concrete grades designated by 28-day characteristic compressive strength of 150 mm cube (Table 2 as amended):\n"
                    "1. Ordinary Concrete: M10 (10 N/mm²), M15 (15 N/mm²), M20 (20 N/mm²).\n"
                    "2. Standard Concrete: M25, M30, M35, M40, M45, M50, M55, M60.\n"
                    "3. High Strength Concrete: M65, M70, M75, M80, M85, M90, M95, M100.\n"
                    "Mandatory minimum grade: M20 for Reinforced Concrete (RCC) in normal conditions; M30 for concrete in sea-water/coastal exposure; M15 for Plain Concrete (PCC)."
                ),
                "keywords": ["concrete grades", "M20", "M25", "M30", "M40", "M60", "M100", "minimum grade for RCC", "characteristic strength", "IS 456 Table 2"]
            },
            {
                "clause_id": "Table 5 / Clause 8.2",
                "clause_title": "Durability, Exposure Conditions, Minimum Cement & Maximum W/C Ratio",
                "page_number": 20,
                "section_number": "Section 8.2 (Table 5)",
                "content": (
                    "Durability & Exposure stipulations for Reinforced Concrete (20 mm aggregate):\n"
                    "- Mild (sheltered): Min cement 300 kg/m³, Max W/C 0.55, Min grade M20, Nominal cover 20 mm.\n"
                    "- Moderate (rain/sheltered salt air): Min cement 300 kg/m³, Max W/C 0.50, Min grade M25, Nominal cover 30 mm.\n"
                    "- Severe (coastal immersion, alternate wet/dry): Min cement 320 kg/m³, Max W/C 0.45, Min grade M30, Nominal cover 45 mm.\n"
                    "- Very Severe (sea water spray, corrosive fumes): Min cement 340 kg/m³, Max W/C 0.45, Min grade M35, Nominal cover 50 mm.\n"
                    "- Extreme (tidal zone, aggressive chemicals): Min cement 360 kg/m³, Max W/C 0.40, Min grade M40, Nominal cover 75 mm.\n"
                    "Maximum cement content (excluding mineral admixtures) = 450 kg/m³."
                ),
                "keywords": ["durability", "exposure conditions", "mild", "moderate", "severe", "very severe", "extreme", "Table 5", "minimum cement", "max w/c ratio", "IS 456"]
            },
            {
                "clause_id": "Clause 11.3 / Table 11.3.1",
                "clause_title": "Formwork Stripping Time (De-Shuttering Periods & Strength Criteria)",
                "page_number": 25,
                "section_number": "Section 11.3 (Amendment 5)",
                "content": (
                    "Minimum period before striking formwork (under normal temperature >= 15°C):\n"
                    "1. Vertical formwork to columns, walls, beams: 16–24 hours (for both OPC and Blended cement).\n"
                    "2. Soffit formwork to slabs (props refixed immediately): 3 days (OPC) / 7 days (Blended/Fly ash/Slag).\n"
                    "3. Soffit formwork to beams (props refixed immediately): 7 days (OPC) / 10 days (Blended/Fly ash/Slag).\n"
                    "4. Props to slabs:\n"
                    "   - Spanning up to 4.5 m: 7 days (OPC) / 10 days (Blended).\n"
                    "   - Spanning over 4.5 m: 14 days (for both).\n"
                    "5. Props to beams and arches:\n"
                    "   - Spanning up to 6 m: 14 days (for both).\n"
                    "   - Spanning over 6 m: 21 days (for both).\n"
                    "Early Stripping by Cube Testing (Cl 11.3.1.1): 3 days = 45% of specified strength, 7 days = 60%, 14 days = 85%."
                ),
                "keywords": ["stripping time", "de-shuttering period", "formwork removal", "props to slabs", "props to beams", "16-24 hours", "7 days", "14 days", "21 days", "IS 456 Cl 11.3"]
            },
            {
                "clause_id": "Clause 26 / Detailing",
                "clause_title": "Reinforcement Detailing: Beams, Slabs, Columns & Clear Cover",
                "page_number": 45,
                "section_number": "Section 26.0",
                "content": (
                    "Key reinforcement detailing rules per IS 456:\n"
                    "1. Beams:\n"
                    "   - Minimum tension steel: As / (b*d) = 0.85 / fy.\n"
                    "   - Maximum tension/compression steel: 0.04 b*D.\n"
                    "   - Side face reinforcement: 0.1% of web area (distributed equally on both faces, spacing <= 300 mm) when web depth D > 750 mm.\n"
                    "   - Shear stirrup spacing: <= 0.75 d or 300 mm (whichever is less).\n"
                    "2. Slabs:\n"
                    "   - Minimum reinforcement: 0.15% of gross area for Mild steel, 0.12% for HYSD (Fe 415/500/550).\n"
                    "   - Maximum bar diameter: <= 1/8 of total slab thickness (D/8).\n"
                    "   - Maximum bar spacing: Main bars <= 3d or 300 mm; Distribution bars <= 5d or 450 mm.\n"
                    "3. Columns:\n"
                    "   - Longitudinal steel: Min 0.8% and Max 6.0% (practical limit 4% to avoid congestion).\n"
                    "   - Minimum number of bars: 4 for rectangular columns, 6 for circular columns; minimum bar diameter = 12 mm.\n"
                    "   - Lateral ties pitch: <= least lateral dimension, <= 16 * smallest bar diameter, <= 300 mm. Tie diameter >= 1/4 largest bar dia (min 6 mm).\n"
                    "4. Development Length: Ld = (phi * sigma_s) / (4 * tau_bd). Design bond stress tau_bd is increased by 60% for deformed bars (IS 1786) and by 25% for compression bars."
                ),
                "keywords": ["reinforcement detailing", "minimum steel in beam", "slab reinforcement", "column steel", "lateral ties pitch", "development length", "Ld", "side face steel", "IS 456 Cl 26"]
            },
            {
                "clause_id": "Section 5 / Design",
                "clause_title": "Limit State Design Formulas: Flexure, Shear, Deflection & Crack Width",
                "page_number": 68,
                "section_number": "Section 5.0 (Cl 35 - 43)",
                "content": (
                    "Limit State Design fundamentals (IS 456 Section 5):\n"
                    "1. Modulus of Elasticity: Ec = 5000 * sqrt(fck) N/mm².\n"
                    "2. Flexural Tensile Strength (Modulus of Rupture): fcr = 0.7 * sqrt(fck) N/mm².\n"
                    "3. Maximum concrete compressive strain in bending = 0.0035; in axial compression = 0.002.\n"
                    "4. Partial Safety Factors: Concrete gamma_m = 1.5; Steel gamma_m = 1.15. Load factors: 1.5 (DL + IL) / 1.2 (DL + IL + WL/EL).\n"
                    "5. Limiting Neutral Axis Depth: xu,max/d = 0.53 for Fe 250; 0.48 for Fe 415; 0.46 for Fe 500.\n"
                    "6. Limiting Moment of Resistance (Singly Reinforced): Mu,lim = 0.36*(xu,max/d)*(1 - 0.42*xu,max/d)*b*d²*fck (0.138 fck b d² for Fe 415; 0.133 fck b d² for Fe 500).\n"
                    "7. Maximum Crack Width Limits: 0.3 mm (normal), 0.2 mm (moisture/soil contact), 0.1 mm (severe/extreme exposure).\n"
                    "8. Deflection Span/Depth basic ratios: Cantilever = 7, Simply supported = 20, Continuous = 26 (modified by tension/compression steel factors)."
                ),
                "keywords": ["limit state design", "Ec = 5000 sqrt(fck)", "flexural strength", "Mu,lim", "crack width limit", "deflection ratio", "xu,max", "IS 456 Section 5"]
            }
        ]
    },
    {
        "id": "IS-1417",
        "standard_number": "IS 1417:2016",
        "title": "Gold and Gold Alloys, Jewellery/Artefacts — Fineness and Marking — Specification (Fourth Revision)",
        "category": "Consumer Products & Precious Metals",
        "department": "Metallurgical Engineering Department (MTD 10: Precious Metals)",
        "status": "Mandatory Quality Control & Hallmarking Order",
        "filename": "IS_1417_2016.pdf",
        "purchase_url": "https://www.standardsbis.in/gemini/detail/IS_1417_2016",
        "related_standards": ["IS 15820:2009", "IS 1418:2009", "IS 3095:1999", "IS 2790:1999"],
        "summary": "Specifies purity grades of fine gold, standard gold, and gold alloys for bullion, coins, and jewellery/artefacts. Prescribes mandatory hallmarking symbols, chemical limits for cadmium and platinum group metals, and assay tolerances.",
        "clauses": [
            {
                "clause_id": "Clause 4 & Table 1",
                "clause_title": "Purity Grades, Caratage & Minimum Fineness (24K, 22K, 18K, 14K)",
                "page_number": 3,
                "section_number": "Section 4.1",
                "content": (
                    "Gold and gold alloys classification by fineness (parts per thousand / ppt) per IS 1417:2016:\n"
                    "1. Fine Gold: Minimum 999 ppt (used for bullion and minted coins).\n"
                    "2. Standard Gold: Minimum 995 ppt (used for market bullion bars and coins).\n"
                    "3. 22 Carat (22K): Minimum 916 ppt (916.6 ppt exact) - standard jewellery grade.\n"
                    "4. 18 Carat (18K): Minimum 750 ppt - stone-studded & diamond jewellery.\n"
                    "5. 14 Carat (14K): Minimum 585 ppt - lightweight and fashion jewellery.\n"
                    "Note on Consumer Welfare: Intermediate grades of 958 (23K), 875 (21K), 833 (20K), 791 (19K), 708 (17K), 666 (16K), and 375 (9K) have been DELETED to eliminate consumer confusion."
                ),
                "keywords": ["gold purity", "22K", "916", "18K", "750", "14K", "585", "fine gold 999", "standard gold 995", "caratage", "IS 1417"]
            },
            {
                "clause_id": "Clause 4.1.1 / Chemical Limits",
                "clause_title": "Toxic Element Limits (Cadmium <= 0.02%, PGM <= 0.05%) and Solders",
                "page_number": 3,
                "section_number": "Section 4.1.1",
                "content": (
                    "Safety and chemical composition restrictions for gold jewellery:\n"
                    "1. Cadmium Restriction: Maximum permissible limit of Cadmium in gold alloys and solders is 0.02% (200 ppm) to prevent toxic exposure.\n"
                    "2. Platinum Group Metals (PGM): Maximum permissible limit of each platinum group metal is 0.05%.\n"
                    "3. Detection: Presence of Ruthenium (Ru), Iridium (Ir), and Cadmium (Cd) shall be detected by X-ray Fluorescence (XRF) or fire assay.\n"
                    "4. Solders (IS 3095): Must have the exact same gold fineness as the jewellery itself."
                ),
                "keywords": ["cadmium limit 0.02%", "toxic elements", "solders", "XRF test", "ruthenium", "iridium", "IS 1417", "IS 3095"]
            },
            {
                "clause_id": "Clause 5 & 6 / Marking",
                "clause_title": "Mandatory Hallmarking Symbols, Retesting Tolerance (-2 ppt) and Small Articles",
                "page_number": 4,
                "section_number": "Section 5.0 & 6.0",
                "content": (
                    "Hallmarking requirements on gold jewellery/artefacts:\n"
                    "1. Mandatory Marks: (a) BIS Standard Mark, (b) Purity in carat and fineness (e.g. 22K916), (c) Assaying & Hallmarking Centre's mark/number, (d) Jeweller's identification mark/number (or laser HUID under current statutory order).\n"
                    "2. Retesting Tolerance: On retesting hallmarked jewellery by an enforcement officer or consumer, a maximum negative tolerance of 2 ppt is permitted.\n"
                    "3. Small Articles: Gold jewellery/artefacts weighing less than 2 g may also be hallmarked.\n"
                    "4. Hollow Articles: Any article with a hollow centre filled with base metal, cement, or lac is prohibited from hallmarking unless the exact gold weight is declared and laser-marked."
                ),
                "keywords": ["hallmarking marks", "retesting tolerance 2 ppt", "articles under 2g", "hollow gold", "BIS mark", "purity mark", "IS 1417"]
            }
        ]
    },
    {
        "id": "IS-1239",
        "standard_number": "IS 1239 (Part 1):2004",
        "title": "Steel Tubes, Tubulars and Other Wrought Steel Fittings — Specification (Part 1: Steel Tubes - Sixth Revision, Reaffirmed 2015)",
        "category": "Mechanical & Metallurgical Engineering",
        "department": "Metallurgical Engineering Department (MTD 19: Steel Tubes, Pipes and Fittings)",
        "status": "Mandatory Quality Control Order (QCO)",
        "filename": "IS_1239_Part_1_2004.pdf",
        "purchase_url": "https://www.standardsbis.in/gemini/detail/IS_1239_Part_1",
        "related_standards": ["IS 1239 (Part 2):1992", "IS 2062:2011", "IS 554:1999", "IS 4736:1986", "IS 2328:1983", "IS 2329:1985"],
        "summary": "Covers requirements for welded and seamless plain end or screwed and socketed steel tubes (6 mm to 150 mm nominal bore) intended for water, gas, air, and steam lines. Specifies Light, Medium, and Heavy classes, 5 MPa hydrostatic testing, cold bend/flattening tests, and color coding.",
        "clauses": [
            {
                "clause_id": "Clause 6 & Table 1 / 2",
                "clause_title": "Manufacturing Processes and Chemical Composition (Ladle & Product Analysis)",
                "page_number": 4,
                "section_number": "Section 6.0 & 7.0",
                "content": (
                    "Steel tube manufacturing specifications:\n"
                    "1. Manufacturing Processes: Hot Finished Seamless (HFS), Cold Finished Seamless (CDS), Hot Finished Welded (HFW), or Electric Resistance Welded / High Frequency Induction Welded (ERW/HFIW). Manual welding is prohibited.\n"
                    "2. Chemical Composition (Table 1 Ladle Analysis, Max %):\n"
                    "   - Carbon (C): 0.20% max (Permissible product variation +0.02%)\n"
                    "   - Manganese (Mn): 1.30% max (Permissible product variation +0.04%)\n"
                    "   - Sulphur (S): 0.040% max (Permissible product variation +0.005%)\n"
                    "   - Phosphorus (P): 0.040% max (Permissible product variation +0.005%)\n"
                    "3. Internal Weld Fin: Height shall not exceed 60% of specified wall thickness."
                ),
                "keywords": ["steel tube chemical composition", "ERW", "HFS", "seamless tube", "carbon 0.20%", "manganese 1.30%", "weld fin", "IS 1239"]
            },
            {
                "clause_id": "Clause 8 / Tables 3, 4, 5",
                "clause_title": "Classification, Dimensions & Mass (Light, Medium, Heavy Series)",
                "page_number": 5,
                "section_number": "Section 8.0 & 9.0",
                "content": (
                    "Dimensions and mass for steel tubes (6 mm to 150 mm nominal bore):\n"
                    "1. Light Class (Table 3 / Yellow Band): Wall thickness 1.8 mm (6 mm NB, 0.360 kg/m) to 3.6 mm (100 mm NB, 9.75 kg/m).\n"
                    "2. Medium Class (Table 4 / Blue Band): Wall thickness 2.0 mm (6 mm NB, 0.404 kg/m) to 4.8 mm (150 mm NB, 18.90 kg/m). Suitable for steam services.\n"
                    "3. Heavy Class (Table 5 / Red Band): Wall thickness 2.6 mm (6 mm NB, 0.487 kg/m) to 5.4 mm (150 mm NB, 21.30 kg/m). For high pressure steam and fire hydrants.\n"
                    "4. Manufacturing Tolerances (Clause 9):\n"
                    "   - Thickness: Welded Light (+not limited, -8%); Welded Medium/Heavy (+not limited, -10%); Seamless (+not limited, -12.5%).\n"
                    "   - Mass: Single tube Light (+10%, -8%); Medium/Heavy (+/- 10%); Bulk 10 tonne lot (+/- 7.5%)."
                ),
                "keywords": ["steel pipe dimensions", "light class", "medium class", "heavy class", "Table 3", "Table 4", "Table 5", "wall thickness tolerance", "IS 1239"]
            },
            {
                "clause_id": "Clause 13 & 14 / Tests",
                "clause_title": "Pressure Testing (5 MPa Hydrostatic / Eddy Current) and Mechanical Tests",
                "page_number": 9,
                "section_number": "Section 13.0 & 14.0",
                "content": (
                    "Mandatory physical and leak-tightness tests:\n"
                    "1. Hydrostatic Leak Test (Cl 13.1): Every tube tested at 5.0 MPa (50 bar) pressure maintained for >= 3 seconds without any leakage.\n"
                    "2. Eddy Current Test (Annex B): Permitted as an in-line non-destructive alternative calibrated with standard drill holes (1.2 mm to 3.7 mm).\n"
                    "3. Tensile Strength (Cl 14.1): Minimum 320 MPa (320 N/mm²); Min elongation = 20% for steam tubes, 12% for <=25 mm, 20% for >25 mm.\n"
                    "4. Bend Test (Cl 14.2, <=50 mm NB): Cold bend 180° around former (6x OD) for ungalvanized; 90° around former (8x OD) for galvanized.\n"
                    "5. Flattening Test (Cl 14.3, >50 mm NB): Cold flattened between parallel plates with weld at 90°; no weld opening until plates reach < 75% OD, no metal cracking until < 60% OD.\n"
                    "6. Marking (Cl 17): Yellow band (Light), Blue band (Medium), Red band (Heavy), White band (Steam)."
                ),
                "keywords": ["hydrostatic test 5 MPa", "50 bar", "eddy current test", "flattening test", "bend test", "tensile strength 320 MPa", "color bands", "IS 1239"]
            }
        ]
    },
    {
        "id": "IS-2062",
        "standard_number": "IS 2062:2011",
        "title": "Hot Rolled Medium and High Tensile Structural Steel — Specification (Seventh Revision, Reaffirmed 2021)",
        "category": "Civil & Metallurgical Engineering",
        "department": "Metallurgical Engineering Department (MTD 4: Wrought Steel Products)",
        "status": "Mandatory Quality Control Order (QCO)",
        "filename": "IS_2062_2011.pdf",
        "purchase_url": "https://www.standardsbis.in/gemini/detail/IS_2062_2011",
        "related_standards": ["IS 800:2007", "IS 1786:2008", "IS 1239:2004", "IS 1757:1988", "IS 10842:1984"],
        "summary": "Specifies 9 grades of hot-rolled structural steel (E250 to E650) with sub-qualities (A, BR, B0, C) based on deoxidation and Charpy V-notch impact toughness at room temperature, 0°C, and -20°C. Defines carbon equivalent (CE) limits, tensile strength, yield stress, and bend properties.",
        "clauses": [
            {
                "clause_id": "Clause 5 / Table 1 & 2",
                "clause_title": "9 Basic Grades (E250 to E650) and Sub-Qualities (A, BR, B0, C)",
                "page_number": 2,
                "section_number": "Section 5.0",
                "content": (
                    "Structural steel grades based on minimum yield strength for thickness <= 20 mm (Table 1 & 2):\n"
                    "1. Basic Grades: E250, E275, E300, E350, E410, E450, E550, E600, E650.\n"
                    "2. Sub-Qualities:\n"
                    "   - Quality A: Impact test not required; semi-killed/killed steel.\n"
                    "   - Quality BR: Impact test optional at room temperature (+27°C ± 2°C), min 27 Joules (20 J for E450, 15 J for E550-E650).\n"
                    "   - Quality B0: Impact test mandatory at 0°C, min 27 Joules (25 J for E410).\n"
                    "   - Quality C: Impact test mandatory at -20°C (killed steel), min 27 Joules (25 J for E410) - mandatory for cold regions and seismic bridges.\n"
                    "3. Mechanical Properties Summary:\n"
                    "   - E250: Yield >= 250 MPa, Tensile >= 410 MPa, Elongation >= 23%, Bend 2t (<=25mm) / 3t (>25mm).\n"
                    "   - E275: Yield >= 275 MPa, Tensile >= 430 MPa, Elongation >= 22%, Bend 2t / 3t.\n"
                    "   - E300: Yield >= 300 MPa, Tensile >= 440 MPa, Elongation >= 22%.\n"
                    "   - E350: Yield >= 350 MPa, Tensile >= 490 MPa, Elongation >= 22%.\n"
                    "   - E410: Yield >= 410 MPa, Tensile >= 540 MPa, Elongation >= 20%.\n"
                    "   - E450: Yield >= 450 MPa, Tensile >= 570 MPa, Elongation >= 20%."
                ),
                "keywords": ["E250", "E275", "E300", "E350", "E410", "E450", "Quality A", "Quality BR", "Quality B0", "Quality C", "yield stress", "IS 2062"]
            },
            {
                "clause_id": "Table 1 / Notes",
                "clause_title": "Chemical Composition, Carbon Equivalent (CE) Formula & Micro-Alloying",
                "page_number": 3,
                "section_number": "Section 8.0 (Table 1)",
                "content": (
                    "Chemical composition and weldability limits (Table 1):\n"
                    "1. Carbon Equivalent Formula (Ladle Analysis):\n"
                    "   CE = C + (Mn / 6) + ((Cr + Mo + V) / 5) + ((Ni + Cu) / 15)\n"
                    "2. Maximum CE limits: E250 (0.39-0.42), E275 (0.41-0.43), E300 (0.44), E350 (0.45-0.47), E410 (0.50), E450 (0.52), E550/E600 (0.54), E650 (0.55).\n"
                    "3. Micro-Alloying: Elements like Nb, V, and Ti singly or combined shall not exceed 0.25%.\n"
                    "4. Copper Bearing Steel (Suffix Cu): Cu content between 0.20% and 0.35% for corrosion resistance.\n"
                    "5. Nitrogen content shall not exceed 0.012%.\n"
                    "6. Steel Density: 7.85 g/cm³."
                ),
                "keywords": ["carbon equivalent formula", "CE max", "micro alloying", "niobium", "vanadium", "titanium", "copper bearing steel", "density 7.85", "IS 2062"]
            },
            {
                "clause_id": "Clause 12 & 13",
                "clause_title": "Charpy V-Notch Impact Test (IS 1757) and Y-Groove Crackability (IS 10842)",
                "page_number": 7,
                "section_number": "Section 12.0 & 13.0",
                "content": (
                    "Toughness and crackability testing:\n"
                    "1. Charpy V-Notch Impact Test (Cl 12.1 per IS 1757): Carried out on products with thickness >= 12 mm parallel to rolling direction. Minimum average of 3 test pieces >= 27 Joules (no single specimen < 70% of minimum).\n"
                    "2. Y-Groove Crackability Test (Cl 13 per IS 10842): Applicable for Grade E 250 C material with thickness >= 12 mm to evaluate heat-affected zone (HAZ) weld cracking susceptibility.\n"
                    "3. Re-testing (Cl 17): If a sample fails, 2 additional tests from the same cast must pass."
                ),
                "keywords": ["Charpy impact test", "27 Joules", "sub zero impact", "Y-groove crackability", "IS 10842", "IS 1757", "E 250 C", "IS 2062"]
            }
        ]
    },
    {
        "id": "IS-10500",
        "standard_number": "IS 10500:2012",
        "title": "Drinking Water — Specification (Second Revision)",
        "category": "Chemical & Water Quality",
        "department": "Chemical Department (CHD 13)",
        "status": "Mandatory Quality Control Order (QCO)",
        "filename": "IS_10500_2012.pdf",
        "purchase_url": "https://www.standardsbis.in/gemini/detail/IS_10500_2012",
        "related_standards": ["IS 3025:2014", "IS 13428:2005", "IS 14543:2004"],
        "summary": "Prescribes quality requirements, acceptable limits, permissible limits in absence of alternate source, and test methods for water intended for human consumption.",
        "clauses": [
            {
                "clause_id": "Table 1 / Clause 4.1",
                "clause_title": "Organoleptic and Physical Parameters (pH, TDS, Turbidity, Color)",
                "page_number": 2,
                "section_number": "Section 4.1",
                "content": (
                    "Table 1 defines essential physical parameters for drinking water:\n"
                    "- Color: Acceptable limit 5 Hazen units (Max 15 Hazen units in absence of alternate source). Test method IS 3025 (Part 4).\n"
                    "- Odour: Agreeable (must be agreeable in both limits).\n"
                    "- pH value: Acceptable limit 6.5 to 8.5 (No relaxation; strictly 6.5 - 8.5). Test method IS 3025 (Part 11).\n"
                    "- Taste: Agreeable.\n"
                    "- Turbidity: Acceptable limit 1 NTU (Max 5 NTU in absence of alternate source). Test method IS 3025 (Part 10).\n"
                    "- Total Dissolved Solids (TDS): Acceptable limit 500 mg/L (Max 2000 mg/L in absence of alternate source). Test method IS 3025 (Part 16)."
                ),
                "keywords": ["pH", "TDS", "turbidity", "color", "odour", "physical parameters", "drinking water", "IS 10500", "total dissolved solids"]
            },
            {
                "clause_id": "Table 3 / Clause 4.3",
                "clause_title": "Toxic Substances & Heavy Metals Limits (Lead, Arsenic, Mercury)",
                "page_number": 3,
                "section_number": "Section 4.3",
                "content": (
                    "Table 3 specifies strict threshold limits for toxic heavy metals and toxic substances:\n"
                    "- Lead (as Pb): Acceptable limit 0.01 mg/L (No relaxation).\n"
                    "- Arsenic (as As): Acceptable limit 0.01 mg/L (Max 0.05 mg/L in absence of alternate source).\n"
                    "- Mercury (as Hg): Acceptable limit 0.001 mg/L (No relaxation).\n"
                    "- Cadmium (as Cd): Acceptable limit 0.003 mg/L (No relaxation).\n"
                    "- Total Chromium (as Cr): Acceptable limit 0.05 mg/L (No relaxation).\n"
                    "- Copper (as Cu): Acceptable limit 0.05 mg/L (Max 1.5 mg/L).\n"
                    "- Iron (as Fe): Acceptable limit 1.0 mg/L (No relaxation in 2012 amendment)."
                ),
                "keywords": ["lead", "arsenic", "mercury", "cadmium", "chromium", "heavy metals", "toxic substances", "IS 10500"]
            },
            {
                "clause_id": "Table 6 / Clause 5.1",
                "clause_title": "Bacteriological Quality & Safety (E. coli, Coliforms)",
                "page_number": 4,
                "section_number": "Section 5.1",
                "content": (
                    "Bacteriological requirements for all water intended for drinking:\n"
                    "1. All water samples entering distribution system must be free from coliform organisms.\n"
                    "2. E. coli or thermotolerant coliform bacteria: Shall NOT be detectable in any 100 mL sample (0 CFU / 100 mL).\n"
                    "3. Total coliform bacteria: Shall not be detectable in any 100 mL sample in treated water.\n"
                    "4. If coliforms are detected, immediate re-sampling and disinfection audit is mandatory."
                ),
                "keywords": ["bacteria", "e coli", "coliform", "bacteriological", "biological contamination", "IS 10500", "disinfection"]
            }
        ]
    },
    {
        "id": "IS-1786",
        "standard_number": "IS 1786:2008",
        "title": "High Strength Deformed Steel Bars and Wires for Concrete Reinforcement (Fourth Revision)",
        "category": "Civil & Metallurgical Engineering",
        "department": "Metallurgical Engineering Department (MTD 4)",
        "status": "Mandatory Quality Control Order (QCO)",
        "filename": "IS_1786_2008.pdf",
        "purchase_url": "https://www.bis.gov.in/bis-care/product/IS_1786_2008",
        "related_standards": ["IS 456:2000", "IS 13920:2016", "IS 2062:2011"],
        "summary": "Covers requirements for high strength deformed steel rebar (TMT bars) used for reinforced concrete structures. Defines Fe 415, Fe 500, Fe 500D, Fe 550, Fe 550D, and Fe 600 grades.",
        "clauses": [
            {
                "clause_id": "Clause 4 / Table 3",
                "clause_title": "Mechanical Properties & Strength Grades (Fe 415, Fe 500, Fe 500D, Fe 550D, Fe 600)",
                "page_number": 5,
                "section_number": "Section 4.1",
                "content": (
                    "Table 3 specifies yield stress / 0.2% proof stress, tensile strength, and elongation:\n"
                    "- Fe 415: Min 0.2% proof stress = 415 N/mm², Min Tensile Strength (TS) = 485 N/mm² (TS/YS >= 1.10), Min Elongation = 14.5%.\n"
                    "- Fe 500: Min 0.2% proof stress = 500 N/mm², Min TS = 545 N/mm² (TS/YS >= 1.08), Min Elongation = 12.0%.\n"
                    "- Fe 500D (Ductile - Seismic zones): Min 0.2% proof stress = 500 N/mm², Min TS = 565 N/mm² (TS/YS >= 1.10), Min Elongation = 16.0% (Total Elongation at max force min 5%).\n"
                    "- Fe 550D: Min 0.2% proof stress = 550 N/mm², Min TS = 600 N/mm² (TS/YS >= 1.08), Min Elongation = 14.5%.\n"
                    "- Fe 600: Min 0.2% proof stress = 600 N/mm², Min TS = 660 N/mm² (TS/YS >= 1.06), Min Elongation = 10.0%."
                ),
                "keywords": ["TMT bar", "Fe 500", "Fe 500D", "Fe 415", "Fe 550D", "Fe 600", "rebar", "yield strength", "elongation", "IS 1786", "seismic rebar"]
            }
        ]
    },
    {
        "id": "IS-1293",
        "standard_number": "IS 1293:2019",
        "title": "Plugs and Socket-Outlets of Rated Voltage up to and Including 250 V and Rated Current up to 16 A",
        "category": "Electrotechnical & Appliances",
        "department": "Electrotechnical Department (ETD 14)",
        "status": "Mandatory Quality Control Order (QCO)",
        "filename": "IS_1293_2019.pdf",
        "purchase_url": "https://www.bis.gov.in/bis-care/product/IS_1293_2019",
        "related_standards": ["IS 732:2019", "IS 694:2010"],
        "summary": "Mandates dimensional, insulation, child-safety shutter, and temperature rise criteria for 6A and 16A domestic plugs, socket outlets, multi-plugs, and power strips in India.",
        "clauses": [
            {
                "clause_id": "Clause 13 / Safety",
                "clause_title": "Child Safety Shutters and Terminal Temperature Rise",
                "page_number": 8,
                "section_number": "Section 13.1",
                "content": (
                    "Key safety mandates under IS 1293:2019:\n"
                    "1. Safety Shutters: All household socket outlets must be provided with internal child safety shutters on live and neutral pins to prevent accidental electric shock.\n"
                    "2. Temperature Rise Test: Maximum temperature rise at terminal connections shall not exceed 45 K when loaded continuously at rated current (6A or 16A).\n"
                    "3. Resistance to Heat & Fire: Enclosure material must withstand 750°C glow wire flammability test.\n"
                    "4. Mandatory QCO: Sale of non-ISI marked plugs, extension boards, and socket-outlets is prohibited across India."
                ),
                "keywords": ["plugs", "sockets", "safety shutters", "6A", "16A", "temperature rise", "glow wire test", "IS 1293", "electric shock"]
            }
        ]
    },
    {
        "id": "IS-732",
        "standard_number": "IS 732:2019",
        "title": "Code of Practice for Electrical Wiring Installations (Fourth Revision)",
        "category": "Electrotechnical & Safety",
        "department": "Electrotechnical Department (ETD 20)",
        "status": "National Electrical Wiring Standard",
        "filename": "IS_732_2019.pdf",
        "purchase_url": "https://www.bis.gov.in/bis-care/product/IS_732_2019",
        "related_standards": ["IS 3043:2018", "IS 1293:2019", "IS 694:2010"],
        "summary": "Covers essential safety guidelines for low voltage electrical wiring installations in residential, commercial, and industrial premises. Specifies earthing, voltage drop limits, and RCD protection.",
        "clauses": [
            {
                "clause_id": "Clause 5 / Earthing & Voltage Drop",
                "clause_title": "Voltage Drop Limits, Earthing and 30mA RCD Protection",
                "page_number": 14,
                "section_number": "Section 5.2",
                "content": (
                    "Mandatory electrical installation rules under IS 732:\n"
                    "1. Voltage Drop Limits: Total voltage drop from the origin of the installation (meter board) to any socket/load point shall not exceed 3% for lighting circuits and 5% for power circuits.\n"
                    "2. Shock Protection (RCD): All socket outlet circuits <= 32A must be protected by a Residual Current Device (RCD / RCCB) with rated residual operating current not exceeding 30 mA.\n"
                    "3. Protective Earthing: Continuous copper or GI protective earthing conductor conforming to IS 3043 is mandatory for all metal enclosures and appliances."
                ),
                "keywords": ["electrical wiring", "voltage drop", "30mA RCD", "RCCB", "earthing", "IS 732", "lighting circuit", "power circuit"]
            }
        ]
    },
    {
        "id": "IS-15820",
        "standard_number": "IS 15820:2009",
        "title": "General Requirements for Competence of Assaying and Hallmarking Centres",
        "category": "Consumer Products & Hallmarking",
        "department": "Hallmarking Department (HM 1)",
        "status": "Mandatory Consumer Protection Scheme",
        "filename": "IS_15820_2009.pdf",
        "purchase_url": "https://www.bis.gov.in/bis-care/product/IS_15820_2009",
        "related_standards": ["IS 1417:2016", "IS 1418:2009", "IS 2112:2014"],
        "summary": "Regulates hallmarking of gold and silver jewellery. Defines 3 mandatory marks including the 6-digit alphanumeric Hallmark Unique Identification (HUID) code and purity standards (24K, 22K, 18K, 14K).",
        "clauses": [
            {
                "clause_id": "Clause 5 / HUID Rules",
                "clause_title": "3 Mandatory Hallmarks on Gold Jewellery and 6-Digit HUID Code",
                "page_number": 3,
                "section_number": "Section 5.1",
                "content": (
                    "Since April 1, 2023, every piece of hallmarked gold jewellery sold in India must bear exactly 3 marks:\n"
                    "1. BIS Standard Logo (Triangular logo with BIS emblem).\n"
                    "2. Purity / Fineness Grade (e.g., '22K916' or '18K750' or '14K585').\n"
                    "3. 6-digit Alphanumeric HUID (Hallmark Unique Identification number, e.g., 'AB1234') laser engraved on each article.\n"
                    "Note: Consumers can verify this 6-digit code on the BIS Care App."
                ),
                "keywords": ["HUID", "3 marks", "BIS logo", "hallmarking", "alphanumeric code", "gold jewelry", "verify HUID", "IS 15820"]
            }
        ]
    },
    {
        "id": "IS-2189",
        "standard_number": "IS 2189:2008",
        "title": "Selection, Installation and Maintenance of Automatic Fire Detection and Alarm System",
        "category": "Fire & Life Safety",
        "department": "Fire Fighting Sectional Committee (CED 22)",
        "status": "National Building Code Mandate",
        "filename": "IS_2189_2008.pdf",
        "purchase_url": "https://www.bis.gov.in/bis-care/product/IS_2189_2008",
        "related_standards": ["IS 2175:1988", "NBC 2016 (Part 4)"],
        "summary": "Prescribes requirements for design, spacing, layout, installation, and testing of automatic smoke, heat, and optical fire detectors, manual call points (MCP), and alarm sounders.",
        "clauses": [
            {
                "clause_id": "Clause 6 & 7 / Detector Spacing",
                "clause_title": "Smoke Detector Spacing, MCP Positioning and Sounder Output",
                "page_number": 11,
                "section_number": "Section 6.2",
                "content": (
                    "Fire alarm system layout rules under IS 2189:\n"
                    "1. Smoke Detectors: Maximum coverage area of 50 m² per point-type smoke detector; maximum distance between detectors shall not exceed 7.5 m (and 5.3 m from any wall/corner).\n"
                    "2. Heat Detectors: Maximum coverage area of 30 m²; maximum spacing 5.3 m.\n"
                    "3. Manual Call Points (MCP): Installed at 1.4 m height from floor level; travel distance from any point in the building to the nearest MCP shall not exceed 30 m.\n"
                    "4. Fire Sounders: Minimum sound level of 65 dBA or 5 dBA above ambient noise (75 dBA in sleeping areas) throughout the protected premises."
                ),
                "keywords": ["smoke detector spacing", "fire alarm", "MCP", "manual call point", "heat detector", "sounder level", "IS 2189", "fire safety"]
            }
        ]
    },
    {
        "id": "IS-16046",
        "standard_number": "IS 16046 (Part 1 & 2):2018 / IEC 62133",
        "title": "Secondary Cells and Batteries Containing Alkaline or Other Non-Acid Electrolytes — Safety Requirements",
        "category": "Electronics & Battery Safety",
        "department": "Electrotechnical Department (ETD 11)",
        "status": "Mandatory CRS Regulation (MeitY)",
        "filename": "IS_16046_2018.pdf",
        "purchase_url": "https://www.bis.gov.in/bis-care/product/IS_16046_2018",
        "related_standards": ["IS 16047:2014", "IS 16270:2014"],
        "summary": "Specifies safety requirements for portable sealed secondary lithium and nickel cells/batteries used in smartphones, laptops, power banks, and electric vehicles.",
        "clauses": [
            {
                "clause_id": "Clause 8 / Abuse Tests",
                "clause_title": "Thermal Abuse, Continuous Charging, External Short Circuit & Overcharge",
                "page_number": 9,
                "section_number": "Section 8.3",
                "content": (
                    "Mandatory safety tests for lithium-ion battery certification under IS 16046 (Part 2):\n"
                    "1. Thermal Abuse Test: Cells heated to 130°C ± 2°C for 10 minutes; shall show NO explosion or fire.\n"
                    "2. External Short Circuit: Cell short-circuited with external resistance < 0.1 ohm at 55°C; shall not explode or catch fire.\n"
                    "3. Overcharge Test: Fully discharged battery charged at 2x rated current for prescribed duration without thermal runaway.\n"
                    "4. Forced Internal Short Circuit Test: High-speed mechanical indent test on cell jelly roll.\n"
                    "5. Mandatory CRS Registration: Must bear BIS R-number and Standard Mark before import or sale."
                ),
                "keywords": ["lithium battery", "thermal abuse", "short circuit", "overcharge test", "battery explosion", "CRS", "R-number", "IS 16046"]
            }
        ]
    },
    {
        "id": "BIS-SERVICES",
        "standard_number": "BIS Act 2016 / Schemes",
        "title": "BIS Conformity Assessment Schemes, ISI Mark, CRS & Certification Guidelines",
        "category": "Conformity Assessment & BIS Services",
        "department": "Bureau of Indian Standards Central Administration",
        "status": "Statutory Authority under Ministry of Consumer Affairs, Food & Public Distribution",
        "filename": "BIS_Conformity_Scheme_2018.pdf",
        "purchase_url": "https://www.bis.gov.in/bis-care/product/BIS_Conformity_Scheme_2018",
        "related_standards": ["IS 10500:2012", "IS 2062:2011", "IS 1293:2019", "IS 456:2000", "IS 10262:2019", "IS 1417:2016"],
        "summary": "Overview of BIS certification schemes (ISI Mark Scheme-I, CRS for Electronics, FMCS for foreign manufacturers, Hallmarking, BIS Care App, Know Your Standards, e-BIS portal).",
        "clauses": [
            {
                "clause_id": "7-Step Certification Roadmap",
                "clause_title": "Comprehensive 7-Step BIS Certification, Licensing & MSME Concession Guide",
                "page_number": 3,
                "section_number": "Section 1.5",
                "content": (
                    "Complete 7-Step BIS Certification Process for Indian Manufacturers and MSMEs:\n"
                    "1. Step 1 (Identify Standard & Scheme): Identify applicable Indian Standard (IS code) and conformity scheme (Scheme-I ISI Mark for industrial/structural goods or Scheme-II CRS for electronics). Verify Quality Control Order (QCO) mandatory status.\n"
                    "2. Step 2 (In-House Laboratory Setup): Establish in-house testing facility conforming to the BIS Scheme of Inspection and Testing (SIT). Maintain calibrated test equipment and appoint qualified QC technical personnel.\n"
                    "3. Step 3 (Online Portal Submission): Submit Form-V on e-BIS Manakonline portal (www.manakonline.in). Upload factory layout, machinery list, test equipment list, and Udyam MSME certificate. Pay application fee (₹1,000; ₹200 for Micro MSMEs).\n"
                    "4. Step 4 (Factory Audit & Inspection): BIS technical officer visits the manufacturing premises to audit the production line, verify testing facility, check raw material sourcing, and assess QC competency (Audit fee ₹7,000/day).\n"
                    "5. Step 5 (Sample Drawing & Lab Testing): Counter-samples drawn during factory audit are sealed. One sample is tested in factory lab; second sealed sample is dispatched to a BIS-recognized/NABL-accredited laboratory for independent verification.\n"
                    "6. Step 6 (Grant of BIS License / CM/L): Upon successful laboratory test reports and audit clearance, BIS grants the Certificate of Conformity and a 7-to-8 digit CM/L number, granting legal authorization to affix the ISI mark.\n"
                    "7. Step 7 (Market Surveillance & Annual Renewal): Regular surveillance samples from factory and market are tested to ensure continuous quality. Pay annual marking fee and renew license every 1 to 2 years.\n\n"
                    "TIMELINE & COST ESTIMATES:\n"
                    "- Timeline: 30 to 60 Days (30 days fast-track under Simplified Scheme; 45-60 days normal procedure).\n"
                    "- Total Cost Estimate: ₹20,000 to ₹80,000 (depending on scale & product testing charges).\n"
                    "- MSME Fee Concessions: Micro enterprises get 80% discount on application & license fees (Net cost ~₹18k-₹25k) and 50% discount on BIS laboratory testing charges. Small enterprises get 50% discount.\n"
                    "- Essential Portals: Manakonline (www.manakonline.in), BIS Lab Directory (www.bis.gov.in/laboratories/laboratory-directory/), Fee Structure (www.bis.gov.in/conformity-assessment/fee-structure/), QCO Tracker (www.bis.gov.in/product-certification/qco-orders/)."
                ),
                "keywords": ["7-step certification", "BIS certification guide", "how to get BIS certified", "ISI license process", "timeline 30-60 days", "cost estimate", "manakonline", "lab directory", "MSME 80% discount", "SIT", "CM/L number"]
            },
            {
                "clause_id": "Scheme I Process",
                "clause_title": "How to Get BIS ISI Mark Certification (Product Certification)",
                "page_number": 5,
                "section_number": "Section 2.1",
                "content": (
                    "Step-by-step process to obtain a BIS ISI Mark License (Scheme-I):\n"
                    "1. Online Application: Submit application on the e-BIS Manakonline portal (www.manakonline.in) with factory details, manufacturing machinery list, and in-house testing lab equipment list conforming to relevant Indian Standard.\n"
                    "2. Preliminary Factory Audit: BIS Technical Officer visits the manufacturing premises to verify manufacturing infrastructure, quality control system, and in-house test capabilities.\n"
                    "3. Sample Drawing & Testing: Sample is drawn by BIS auditor, sealed, and sent to an independent BIS recognized laboratory for full testing.\n"
                    "4. Grant of License: Upon satisfactory test reports and audit clearance, a CM/L (Certification Marks License) 7-8 digit number is issued.\n"
                    "5. MSME Subsidy: Micro enterprises receive an 80% concession and small enterprises receive a 50% concession on application and annual license fees."
                ),
                "keywords": ["BIS certification", "ISI mark license", "how to get BIS", "CM/L number", "factory audit", "manakonline", "MSME concession"]
            },
            {
                "clause_id": "Scheme II / CRS",
                "clause_title": "Compulsory Registration Scheme (CRS) for Electronic & IT Goods",
                "page_number": 8,
                "section_number": "Section 3.2",
                "content": (
                    "1. Self-declaration of conformity based on testing in a BIS-recognized lab.\n"
                    "2. No preliminary factory audit required before registration grant.\n"
                    "3. Covers: Smartphones, laptops, LED lighting, smart TVs, adapters, lithium batteries, power banks (Granted R-number, e.g. R-41000000)."
                ),
                "keywords": ["CRS", "Compulsory Registration Scheme", "MeitY", "electronics", "R-number", "laptop", "mobile", "LED", "BIS"]
            }
        ]
    }
]


def get_all_standards():
    """Returns the list of all available Indian Standards."""
    return SAMPLE_STANDARDS


def get_flattened_chunks():
    """
    Transforms the structured standards into individual search chunks
    suitable for dense vector embedding and retrieval with enriched citation metadata.
    """
    chunks = []
    for std in SAMPLE_STANDARDS:
        std_id = std["id"]
        std_num = std["standard_number"]
        std_title = std["title"]
        category = std["category"]
        status = std.get("status", "")
        filename = std.get("filename", f"{std_num.replace(':', '_').replace(' ', '_')}.pdf")
        purchase_url = std.get("purchase_url", "https://www.standardsbis.in/gemini/home")
        related_stds = std.get("related_standards", [])
        
        # Summary chunk
        chunks.append({
            "chunk_id": f"{std_id}-SUMMARY",
            "standard_id": std_id,
            "standard_number": std_num,
            "title": std_title,
            "category": category,
            "status": status,
            "clause_id": "Scope & Overview",
            "clause_title": std_title,
            "page_number": 1,
            "section_number": "Section 1.0",
            "filename": filename,
            "purchase_url": purchase_url,
            "related_standards": related_stds,
            "text": f"Indian Standard: {std_num} - {std_title}.\nCategory: {category}.\nStatus: {status}.\nSummary: {std['summary']}",
            "full_content": std["summary"],
            "keywords": [std_num, std_title, category, status]
        })
        
        # Clause chunks
        for idx, clause in enumerate(std["clauses"]):
            clause_id = clause["clause_id"]
            clause_title = clause["clause_title"]
            content = clause["content"]
            keywords = clause.get("keywords", [])
            page_num = clause.get("page_number", idx + 2)
            section_num = clause.get("section_number", f"Section {idx+1}.1")
            
            chunk_text = (
                f"Indian Standard: {std_num} - {std_title}\n"
                f"Category: {category} | Status: {status}\n"
                f"Clause/Section: {clause_id} ({section_num}) - {clause_title}\n"
                f"Requirements & Content:\n{content}"
            )
            
            chunks.append({
                "chunk_id": f"{std_id}-C{idx+1}",
                "standard_id": std_id,
                "standard_number": std_num,
                "title": std_title,
                "category": category,
                "status": status,
                "clause_id": clause_id,
                "clause_title": clause_title,
                "page_number": page_num,
                "section_number": section_num,
                "filename": filename,
                "purchase_url": purchase_url,
                "related_standards": related_stds,
                "text": chunk_text,
                "full_content": content,
                "keywords": keywords
            })
            
    return chunks
