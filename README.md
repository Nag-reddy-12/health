# WoundSense AI — AI-Based Wound Analysis & Treatment Support System

An intelligent, safety-first clinical decision-support and triage system designed to analyze human wound imagery, estimate morphological characteristics and severity, provide structured first-aid guidance, and detect critical red-flag conditions mandating physician referral.

---

## 🌟 Key Features

1. **Dual-Mode AI/ML Inference (Online & 100% Offline)**
   - **Online Mode:** Multimodal cloud AI integration (Google Gemini Vision API / REST endpoints) for contextual visual reasoning.
   - **Offline Mode:** Self-contained Edge Computer Vision engine running on-device using morphological pixel color clustering, edge density, and calibrated clinical heuristics. Fully operational without internet connectivity.
   - **Automated Fallback:** Real-time connectivity watcher detects network drops or API timeouts and transitions seamlessly to the offline edge model.

2. **Wound Image Analysis & Objective Biomarkers**
   - **Wound Categorization:** Abrasions, lacerations, puncture wounds, superficial burns, deep thermal burns, surgical incisions, chronic ulcers (venous/diabetic/pressure), and contusions/hematomas.
   - **Visual Biomarker Extraction:**
     - **Erythema (Redness Index):** Normalized red-to-green differential ratio and spreading peripheral margin coverage.
     - **Swelling / Edema:** Texture gradient and peri-wound inflammatory edema indicator.
     - **Bleeding Status:** Differentiates between active arterial/venous hemorrhage, capillary oozing, and hemostasis.
     - **Exudate / Discharge:** Identifies cloudy purulent discharge (infection risk) versus serous weeping fluid.
     - **Tissue Composition Breakdown:** Quantifies granulation tissue (pink/red), slough (yellow fibrous), eschar (black/dark necrotic), and maceration (waterlogged white skin).
     - **Approximate Dimensions:** Surface area in cm² and aspect ratio dimensions.
   - **Confidence Score & Uncertainty Handling:** Calibrated confidence scoring with explicit uncertainty notices for ambiguous presentations.

3. **Medical Safety & Regulatory Guardrails**
   - **Strict No-Antibiotics Policy:** Automated software cannot and does not prescribe prescription antibiotics (such as amoxicillin, ciprofloxacin, cephalexin, etc.). Explicit warnings explain antibiotic stewardship and the need for clinical microbiological culturing.
   - **Approved OTC Guidance:** Evidence-based non-prescription supportive care (0.9% sterile saline wash, white petrolatum/hydrogel moist wound barriers, sterile non-adherent dressings, OTC analgesics).
   - **Precautions & Age Considerations:** Specific considerations for pediatric skin fragility and geriatric dermatoporosis/NSAID risks.

4. **Emergency Detection & Doctor Referral**
   - **Immediate Emergency Alerts:** Prominent red banner triggers automatically for uncontrolled hemorrhage, severe burns (> 25 cm²), gaping lacerations requiring immediate closure (within 6-8 hours), deep puncture wounds with tetanus risk, animal/human bites, or systemic infection signs (fever, red streaks).
   - **Clear Referral Pathways:** Distinguishes between Emergency Room (911/112), Urgent Care (within 4-8 hours), and Routine Outpatient follow-up.

5. **Image Quality Pre-Validation**
   - **Blur Detection:** Calculates Laplacian kernel variance on grayscale image arrays; rejects blurry or out-of-focus captures.
   - **Illumination Checks:** Rejects underexposed (< 30/255 mean brightness) or washed-out (> 235/255) images.
   - **Cutaneous Suitability:** Filters out non-wound images, blank pages, and non-biological items.

6. **Privacy-First Architecture**
   - Ephemeral in-memory image processing by default.
   - Optional local history stored solely on the user's device.
   - **1-Click Privacy Wipe:** Instantly purges all local records and permanently deletes uploaded image files.

---

## 🏛️ System Architecture

```
promt of health/
├── app/
│   ├── config.py                 # Application settings, thresholds & model versions
│   ├── main.py                   # FastAPI application server and REST endpoints
│   ├── database/
│   │   ├── medical_knowledge.json# Curated clinical database (types, severities, OTCs)
│   │   ├── db_manager.py         # Versioned DB manager with schema validation
│   │   └── history_store.py      # Privacy-centric local record manager with 1-click purge
│   ├── ml/
│   │   ├── preprocessor.py       # Quality assessment: Laplacian blur & illumination
│   │   ├── vision_analyzer.py    # Computer vision feature extractor (erythema, tissues, size)
│   │   ├── offline_model.py      # Standalone edge ML classifier and heuristics
│   │   ├── online_model.py       # Cloud vision API integration with timeout recovery
│   │   └── inference_engine.py   # Hybrid router with automatic online/offline fallback
│   ├── services/
│   │   ├── safety_guard.py       # Emergency trigger evaluation & antibiotic blocker
│   │   └── triage_service.py     # Synthesis of vision metrics + patient history
│   ├── samples/                  # Legally compliant synthetic wound fixtures
│   │   ├── sample_abrasion.png
│   │   ├── sample_laceration.png
│   │   ├── sample_burn.png
│   │   ├── sample_blurry.png
│   │   ├── sample_dark.png
│   │   └── sample_non_wound.png
│   └── static/                   # Modern responsive Web UI
│       ├── index.html            # SPA interface (Desktop & Mobile optimized)
│       ├── css/style.css         # Healthcare aesthetic styling & dark/light elements
│       └── js/
│           ├── app.js            # Frontend orchestrator, offline listener, DOM renderer
│           └── camera.js         # MediaDevices camera controller with camera switching
├── tests/                        # Comprehensive automated test suite (21 unit & E2E tests)
├── requirements.txt              # Production dependencies
├── run.py                        # Server startup launcher
└── README.md                     # Documentation
```

---

## 🚀 Installation & Quick Start

### 1. Prerequisites
- **Python 3.10+** (Python 3.12 verified).

### 2. Install Dependencies
```bash
py -m pip install -r requirements.txt
```

### 3. (Optional) Configure Cloud Multimodal AI
If you wish to enable Cloud Multimodal AI (Google Gemini Vision), set your environment variable:
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```
*(If no key is provided, the system automatically runs the high-performance local Edge CV engine).*

### 4. Start the Application
```bash
py run.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 🧪 Running the Automated Test Suite

A complete test suite covering blur detection, dark image rejection, offline classification, emergency triggers, antibiotic restrictions, and end-to-end REST endpoints is included:

```bash
py -m pytest -v
```

**Results:**
- `tests/test_preprocessor.py` — Quality, blur, and lighting filters
- `tests/test_medical_db.py` — Database schema integrity and antibiotic rules
- `tests/test_safety_guard.py` — Bleeding, infection, and emergency flags
- `tests/test_inference.py` — Edge CV classification and hybrid fallback
- `tests/test_api.py` — Full REST API endpoints

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | System health, loaded model versions, and cloud availability |
| `GET` | `/api/database/metadata` | Medical database version, categories, and disclaimer |
| `GET` | `/api/database/wounds` | All wound categories and first-aid protocols |
| `GET` | `/api/database/wounds/{cat}` | Detailed guidelines for a specific category |
| `POST` | `/api/validate-image` | Instant blur, lighting, and dimension validation |
| `POST` | `/api/analyze` | Full triage analysis: image + symptoms + emergency check |
| `GET` | `/api/history` | List of local assessments (summary only) |
| `DELETE` | `/api/history/{id}` | Permanently delete a record and its image |
| `POST` | `/api/history/clear` | 1-click purge of all records and image files |
| `GET` | `/api/samples` | List available synthetic test fixtures |

---

## ⚖️ Clinical Safety & Legal Disclaimer

> **IMPORTANT:** WoundSense AI is an **educational and clinical decision-support tool**, NOT a medical device, and does NOT provide definitive medical diagnoses or prescribe prescription drugs. An image alone cannot identify underlying bacterial organisms, systemic conditions, or vascular depth. In any critical situation (e.g. continuous bleeding, deep tissue involvement, signs of spreading infection, severe burns, or animal bites), seek **immediate emergency medical evaluation**.
