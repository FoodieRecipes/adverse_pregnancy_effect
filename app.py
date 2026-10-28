"""
Streamlit Prototype Predictive System & Result Explanation Interface for:
"A Predictive Model of Adverse Pregnancy Outcomes Among Malaria-Infected Pregnant Women
in Resource-Constrained Settings using Explainable Boosting Machine (EBM)"

Author: Akpan Divine Eteyen (AK22/PHS/CSC/002)
Department of Computer Science, Akwa Ibom State University

Run with:
    streamlit run app.py
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    roc_curve,
    precision_recall_curve,
)
from sklearn.calibration import calibration_curve

from ebm_core import (
    DOMAIN_FEATURES,
    FEATURE_TO_DOMAIN,
    ALL_CANDIDATE_FEATURES,
    ComponentWiseGradientBoostingSelector,
    ExplainableBoostingMachineClassifier,
)

st.set_page_config(
    page_title="Malaria in Pregnancy APO Predictive System (EBM)",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "research_datasets")
DATA_PATH = os.path.join(DATA_DIR, "merged_malaria_pregnancy_outcomes_dataset.csv")
DICT_PATH = os.path.join(DATA_DIR, "merged_malaria_pregnancy_outcomes_dictionary.csv")
TOP20_DATA_PATH = os.path.join(DATA_DIR, "top_20_important_features_dataset.csv")
TOP20_DICT_PATH = os.path.join(DATA_DIR, "top_20_important_features_dictionary.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
BUNDLE_PATH = os.path.join(MODELS_DIR, "ebm_malaria_pregnancy_bundle.joblib")
ARCH_IMG_CANDIDATES = [
    os.path.join(BASE_DIR, "proposed_system_architecture.png"),
    r"C:\Users\USER\.gemini\antigravity\brain\7c9a6d2e-7c24-4d83-9d9e-d82a858088d2\.user_uploaded\media_1793025780732_a0e907b4.png",
]

os.makedirs(MODELS_DIR, exist_ok=True)


@st.cache_data(show_spinner=False)
def load_dataset_and_dictionary():
    df = pd.read_csv(DATA_PATH, low_memory=False)
    df_dict = pd.read_csv(DICT_PATH)
    label_map = dict(zip(df_dict["feature_name"], df_dict["feature_description"]))
    return df, df_dict, label_map


def _build_and_save_bundle(df: pd.DataFrame):
    candidate_cols = [c for c in ALL_CANDIDATE_FEATURES if c in df.columns]
    primary_target = "target_any_adverse_pregnancy_outcome"

    X_all = df[candidate_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    y_all = df[primary_target].astype(int).to_numpy()

    X_train, X_temp, y_train, y_temp, idx_train, idx_temp = train_test_split(
        X_all, y_all, df.index.to_numpy(), test_size=0.30, random_state=42, stratify=y_all
    )
    X_val, X_test, y_val, y_test, idx_val, idx_test = train_test_split(
        X_temp, y_temp, idx_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    cwgb_selector = ComponentWiseGradientBoostingSelector(
        n_estimators=180,
        learning_rate=0.12,
        n_select=20,
        n_bins=12,
        l2_reg=5.0,
    )
    cwgb_selector.fit(X_train, y_train, domain_map=FEATURE_TO_DOMAIN)
    selected_features = cwgb_selector.selected_features_
    df_cwgb_rank = cwgb_selector.ranking_df_
    df_cwgb_trace = pd.DataFrame(cwgb_selector.selection_trace_)

    X_train_sel = cwgb_selector.transform(X_train)
    X_val_sel = cwgb_selector.transform(X_val)
    X_test_sel = cwgb_selector.transform(X_test)

    scaler_sel = StandardScaler()
    X_train_sel_scaled = scaler_sel.fit_transform(X_train_sel)
    X_val_sel_scaled = scaler_sel.transform(X_val_sel)
    X_test_sel_scaled = scaler_sel.transform(X_test_sel)

    ebm_model = ExplainableBoostingMachineClassifier(
        n_cycles=95,
        learning_rate=0.035,
        n_bags=8,
        subsample=0.82,
        max_bins=24,
        n_interactions=8,
        interaction_rounds=45,
        interaction_bins=6,
        l2_reg=8.0,
        random_state=42,
    )
    ebm_model.fit(X_train_sel, y_train)

    lr_model = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    lr_model.fit(X_train_sel_scaled, y_train)

    rf_model = RandomForestClassifier(
        n_estimators=200, max_depth=10, min_samples_leaf=10, random_state=42, n_jobs=-1
    )
    rf_model.fit(X_train_sel, y_train)

    gb_model = GradientBoostingClassifier(
        n_estimators=150, learning_rate=0.06, max_depth=3, random_state=42
    )
    gb_model.fit(X_train_sel, y_train)

    endpoint_targets = {
        "Composite APO or Maternal Anemia": "target_any_apo_or_maternal_anemia",
        "Maternal Anemia": "target_maternal_anemia",
        "Pregnancy Loss / Stillbirth": "target_pregnancy_loss",
        "Preterm Birth (<9 Months)": "target_preterm_birth",
        "Low Birth Weight (<2.5kg) / Small Size": "target_low_birth_weight_or_small_size",
        "Neonatal Mortality (0-30 Days)": "target_neonatal_death",
    }
    endpoint_ebm_models = {}
    for ep_label, ep_col in endpoint_targets.items():
        y_ep_train = df.loc[idx_train, ep_col].astype(int).to_numpy()
        ep_ebm = ExplainableBoostingMachineClassifier(
            n_cycles=75, learning_rate=0.035, n_bags=6, n_interactions=4, random_state=42
        )
        ep_ebm.fit(X_train_sel, y_ep_train)
        endpoint_ebm_models[ep_label] = ep_ebm

    val_probs_ebm = ebm_model.predict_proba(X_val_sel)[:, 1]
    thresholds = np.linspace(0.20, 0.55, 36)
    best_thresh = float(thresholds[np.argmax([f1_score(y_val, (val_probs_ebm >= t).astype(int)) for t in thresholds])])

    model_probs_test = {
        "Explainable Boosting Machine (EBM)": ebm_model.predict_proba(X_test_sel)[:, 1],
        "Gradient Boosting (GBDT)": gb_model.predict_proba(X_test_sel)[:, 1],
        "Random Forest": rf_model.predict_proba(X_test_sel)[:, 1],
        "Logistic Regression": lr_model.predict_proba(X_test_sel_scaled)[:, 1],
    }

    eval_rows = []
    for m_name, probs in model_probs_test.items():
        y_pred = (probs >= best_thresh).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        eval_rows.append({
            "Model": m_name,
            "Accuracy": round(accuracy_score(y_test, y_pred), 4),
            "Precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
            "Sensitivity (Recall)": round(recall_score(y_test, y_pred, zero_division=0), 4),
            "Specificity": round(tn / (tn + fp) if (tn + fp) > 0 else 0.0, 4),
            "F1-Score": round(f1_score(y_test, y_pred, zero_division=0), 4),
            "ROC-AUC": round(roc_auc_score(y_test, probs), 4),
            "PR-AUC": round(average_precision_score(y_test, probs), 4),
            "Brier Score": round(brier_score_loss(y_test, probs), 4),
        })
    df_eval = pd.DataFrame(eval_rows)

    df_test_meta = df.loc[idx_test].copy()
    df_test_meta["ebm_prob"] = model_probs_test["Explainable Boosting Machine (EBM)"]
    zone_names = {
        1: "North Central", 2: "North East", 3: "North West",
        4: "South East", 5: "South South (Study Focus)", 6: "South West",
    }
    slice_rows = []
    for z_code, z_label in zone_names.items():
        sub = df_test_meta[df_test_meta["geopolitical_zone"] == z_code]
        if len(sub) > 10 and sub[primary_target].nunique() == 2:
            slice_rows.append({
                "Subpopulation Slice": f"Zone: {z_label}",
                "Test Sample Size (n)": len(sub),
                "Observed APO Rate (%)": round(sub[primary_target].mean() * 100, 2),
                "Mean Predicted Risk (%)": round(sub["ebm_prob"].mean() * 100, 2),
                "ROC-AUC": round(roc_auc_score(sub[primary_target], sub["ebm_prob"]), 4),
                "PR-AUC": round(average_precision_score(sub[primary_target], sub["ebm_prob"]), 4),
                "Brier Score": round(brier_score_loss(sub[primary_target], sub["ebm_prob"]), 4),
            })
    for res_code, res_label in [(1, "Residence: Urban"), (2, "Residence: Rural")]:
        sub = df_test_meta[df_test_meta["residence_urban_rural"] == res_code]
        slice_rows.append({
            "Subpopulation Slice": res_label,
            "Test Sample Size (n)": len(sub),
            "Observed APO Rate (%)": round(sub[primary_target].mean() * 100, 2),
            "Mean Predicted Risk (%)": round(sub["ebm_prob"].mean() * 100, 2),
            "ROC-AUC": round(roc_auc_score(sub[primary_target], sub["ebm_prob"]), 4),
            "PR-AUC": round(average_precision_score(sub[primary_target], sub["ebm_prob"]), 4),
            "Brier Score": round(brier_score_loss(sub[primary_target], sub["ebm_prob"]), 4),
        })
    df_slices = pd.DataFrame(slice_rows)

    df_global_imp = pd.DataFrame({
        "term": ebm_model.term_names_,
        "importance_mean_abs_log_odds": ebm_model.term_importances_,
        "type": ["Pairwise Interaction" if " x " in t else "Main Effect" for t in ebm_model.term_names_],
    }).sort_values("importance_mean_abs_log_odds", ascending=False).reset_index(drop=True)

    feature_defaults = {col: float(X_train_sel[col].median()) for col in selected_features}
    feature_ranges = {col: (float(X_train_sel[col].min()), float(X_train_sel[col].max())) for col in selected_features}

    bundle = {
        "ebm_model": ebm_model,
        "lr_model": lr_model,
        "rf_model": rf_model,
        "gb_model": gb_model,
        "endpoint_ebm_models": endpoint_ebm_models,
        "cwgb_selector": cwgb_selector,
        "scaler_sel": scaler_sel,
        "selected_features": selected_features,
        "feature_defaults": feature_defaults,
        "feature_ranges": feature_ranges,
        "best_threshold": best_thresh,
        "df_eval": df_eval,
        "df_slices": df_slices,
        "df_global_imp": df_global_imp,
        "df_cwgb_rank": df_cwgb_rank,
        "df_cwgb_trace": df_cwgb_trace,
    }
    joblib.dump(bundle, BUNDLE_PATH)
    return bundle


@st.cache_resource(show_spinner="Loading / Training 20-Feature Explainable Boosting Machine (EBM) Pipeline...")
def get_model_bundle():
    df, _, _ = load_dataset_and_dictionary()
    if os.path.exists(BUNDLE_PATH):
        try:
            loaded = joblib.load(BUNDLE_PATH)
            if len(loaded.get("selected_features", [])) == 20:
                return loaded
        except Exception:
            pass
    return _build_and_save_bundle(df)


def generate_clinical_recommendations(patient_series: pd.Series, risk_prob: float) -> list:
    recs = []
    if patient_series.get("malaria_iptp_doses", 3) < 3 or patient_series.get("malaria_iptp_optimal_3plus", 1) == 0:
        recs.append(
            "💊 **Initiate / Complete WHO-Recommended IPTp-SP Regimen**: Patient has received fewer than 3 doses of Sulfadoxine-Pyrimethamine (SP/Fansidar). Administer directly observed IPTp-SP at monthly antenatal contacts starting in the 2nd trimester to clear placental parasitemia."
        )
    if patient_series.get("malaria_itn_slept_last_night", 1) == 0 and patient_series.get("malaria_llin_slept_last_night", 1) == 0:
        recs.append(
            "🦟 **Immediate Vector Control (LLIN / ITN Provision)**: Patient is not sleeping under an Insecticide-Treated Net (ITN/LLIN). Issue a Long-Lasting Insecticidal Net at ANC booking and counsel on nightly usage, especially during the rainy transmission season."
        )
    if patient_series.get("maternal_hemoglobin_g_dl", 11.5) < 11.0:
        hb = patient_series.get("maternal_hemoglobin_g_dl", 10.0)
        recs.append(
            f"🩸 **Anemia & Hematinic Management (Hb = {hb:.1f} g/dL)**: Maternal hemoglobin is below normal pregnancy threshold (< 11.0 g/dL). Prescribe therapeutic oral iron + folic acid supplementation, screen for peripheral malaria parasitemia (RDT/microscopy), and administer antihelminthic deworming."
        )
    if patient_series.get("number_of_anc_visits", 4) < 4:
        recs.append(
            "🏥 **Intensified Antenatal Care Surveillance**: Patient has fewer than 4 ANC visits. Schedule bi-weekly/monthly skilled antenatal contacts (WHO 8-contact model) with fetal heart rate monitoring, blood pressure checks, and urine protein screening."
        )
    if patient_series.get("is_primigravida", 0) == 1:
        recs.append(
            "🤰 **Primigravida Placental Malaria Vigilance**: First-time pregnancies lack parity-specific antibodies against *Plasmodium falciparum* VAR2CSA-mediated placental sequestration. Prioritize rapid malaria testing at every ANC contact."
        )
    if patient_series.get("maternal_bmi_kg_m2", 22.0) < 18.5:
        recs.append(
            "🥗 **Maternal Nutritional Supplementation**: Maternal BMI indicates clinical underweight (< 18.5 kg/m²), elevating intrauterine growth restriction (IUGR) and low birth weight risk. Provide balanced protein-energy and micronutrient counseling."
        )
    if not recs:
        recs.append(
            "✅ **Maintain Standard Preventive Antenatal Care**: Continue nightly LLIN bed net usage, scheduled IPTp-SP dosing, and routine hematinic supplementation through delivery."
        )
    return recs


# ==============================================================================
# MAIN STREAMLIT INTERFACE
# ==============================================================================
df, df_dict, label_map = load_dataset_and_dictionary()
bundle = get_model_bundle()

ebm_model: ExplainableBoostingMachineClassifier = bundle["ebm_model"]
endpoint_models: dict = bundle["endpoint_ebm_models"]
selected_features: list = bundle["selected_features"]
feature_defaults: dict = bundle["feature_defaults"]
feature_ranges: dict = bundle["feature_ranges"]
best_threshold: float = bundle["best_threshold"]

# Sidebar Header
with st.sidebar:
    st.markdown("## 🩺 Malaria-in-Pregnancy EBM System")
    st.caption(
        "**Research Title:** *A Predictive Model of Adverse Pregnancy Outcomes Among Malaria-Infected Pregnant Women in Resource-Constrained Settings using Explainable Boosting Machine*\n\n"
        "**Researcher:** Akpan Divine Eteyen (`AK22/PHS/CSC/002`)  \n"
        "**Institution:** Department of Computer Science, Akwa Ibom State University"
    )
    st.divider()
    st.metric("Total Pregnancy Records", f"{len(df):,}")
    st.metric("Total Dataset Features", f"{df.shape[1]}")
    st.metric("CWGB Selected Features", f"{len(selected_features)}")
    st.metric("EBM Pairwise Interactions", f"{len(ebm_model.interactions_)}")
    st.divider()
    st.info(
        "Use the tabs on the right to explore the **Proposed System Architecture**, **CWGB Feature Selection**, **EBM Global Shape Functions**, **Model Evaluation**, and the **Patient Risk Calculator & Local Explanation**."
    )

st.title("🩺 Explainable Boosting Machine (EBM) Predictive System for Adverse Pregnancy Outcomes")
st.markdown(
    "**Clinical Decision Support & Explainable AI Prototype for Malaria-Exposed Pregnant Women in Resource-Constrained Settings**"
)

tabs = st.tabs([
    "1️⃣ Prototype Predictive System & Local Explanation",
    "2️⃣ EBM Global Explainability (Shape Functions)",
    "3️⃣ CWGB Feature Selection & Preprocessing",
    "4️⃣ Model Evaluation & Subgroup Benchmarks",
    "5️⃣ System Architecture & Dataset Explorer",
    "6️⃣ Batch CSV Prediction (Questionnaire Upload)",
])

# ==============================================================================
# TAB 1: PROTOTYPE PREDICTIVE SYSTEM & LOCAL RESULT EXPLANATION
# ==============================================================================
with tabs[0]:
    st.subheader("Prototype Predictive System & Patient-Level Result Explanation")
    st.markdown(
        "Enter clinical, demographic, laboratory, and malaria prevention parameters across the **4 Architecture Domains**, or load a clinical preset below to compute the patient's **Adverse Pregnancy Outcome (APO) Risk** and **Exact Additive EBM Explanation**."
    )

    preset_col1, preset_col2 = st.columns([2, 2])
    with preset_col1:
        preset_choice = st.selectbox(
            "Select Clinical Patient Profile Preset:",
            [
                "Custom / Manual Clinical Entry",
                "High-Risk Profile: Unprotected Primigravida with Anemia in Rural Setting (0 IPTp-SP, No ITN)",
                "Protected Profile: Multigravida with Dual Protection (3+ IPTp-SP Doses + LLIN + 6 ANC Visits)",
                "Moderate-Risk Profile: Adolescent Mother with Late First ANC & 1 IPTp-SP Dose",
            ],
        )

    preset_vals = dict(feature_defaults)
    if "High-Risk Profile" in preset_choice:
        preset_vals.update({
            "maternal_age_years": 19.0,
            "is_primigravida": 1.0,
            "pregnancy_order_number": 1.0,
            "ever_had_terminated_pregnancy": 1.0,
            "number_of_pregnancy_losses": 1.0,
            "number_of_anc_visits": 1.0,
            "anc_4plus_visits": 0.0,
            "anc_8plus_visits": 0.0,
            "timing_first_anc_visit_months": 7.0,
            "anc_first_trimester": 0.0,
            "anc_any_skilled_provider": 0.0,
            "malaria_iptp_sp_fansidar_during_pregnancy": 0.0,
            "malaria_iptp_sp_taken": 0.0,
            "malaria_iptp_doses": 0.0,
            "malaria_iptp_optimal_3plus": 0.0,
            "number_of_times_took_fansidar_iptp": 0.0,
            "maternal_slept_under_mosquito_net": 0.0,
            "malaria_itn_slept_last_night": 0.0,
            "malaria_llin_slept_last_night": 0.0,
            "person_slept_under_llin_net": 0.0,
            "malaria_unprotected_in_pregnancy": 1.0,
            "pregnancy_outcome_rainy_season": 1.0,
            "maternal_hemoglobin_g_dl": 8.6,
            "maternal_hemoglobin_altitude_smoking_adj": 86.0,
            "maternal_hemoglobin_g_dl_1dec": 86.0,
            "maternal_bmi_kg_m2": 17.8,
            "maternal_underweight_bmi_under_18_5": 1.0,
            "residence_urban_rural": 2.0,
            "wealth_index_quintile": 1.0,
            "geopolitical_zone": 5.0,
            "state_code": 30.0,
            "is_south_south_zone": 1.0,
            "is_akwa_ibom_state": 1.0,
        })
    elif "Protected Profile" in preset_choice:
        preset_vals.update({
            "maternal_age_years": 28.0,
            "is_primigravida": 0.0,
            "pregnancy_order_number": 2.0,
            "ever_had_terminated_pregnancy": 0.0,
            "number_of_pregnancy_losses": 0.0,
            "preceding_pregnancy_interval_months": 36.0,
            "short_pregnancy_interval_under_24m": 0.0,
            "number_of_anc_visits": 6.0,
            "anc_4plus_visits": 1.0,
            "timing_first_anc_visit_months": 2.0,
            "anc_first_trimester": 1.0,
            "anc_any_skilled_provider": 1.0,
            "malaria_iptp_sp_fansidar_during_pregnancy": 1.0,
            "malaria_iptp_sp_taken": 1.0,
            "malaria_iptp_doses": 4.0,
            "malaria_iptp_optimal_3plus": 1.0,
            "number_of_times_took_fansidar_iptp": 4.0,
            "maternal_slept_under_mosquito_net": 1.0,
            "malaria_itn_slept_last_night": 1.0,
            "malaria_llin_slept_last_night": 1.0,
            "person_slept_under_llin_net": 1.0,
            "malaria_unprotected_in_pregnancy": 0.0,
            "maternal_hemoglobin_g_dl": 12.4,
            "maternal_hemoglobin_altitude_smoking_adj": 124.0,
            "maternal_hemoglobin_g_dl_1dec": 124.0,
            "maternal_bmi_kg_m2": 23.5,
            "maternal_underweight_bmi_under_18_5": 0.0,
            "residence_urban_rural": 1.0,
            "wealth_index_quintile": 4.0,
        })
    elif "Moderate-Risk Profile" in preset_choice:
        preset_vals.update({
            "maternal_age_years": 18.0,
            "is_primigravida": 1.0,
            "pregnancy_order_number": 1.0,
            "number_of_anc_visits": 2.0,
            "anc_4plus_visits": 0.0,
            "timing_first_anc_visit_months": 6.0,
            "malaria_iptp_sp_fansidar_during_pregnancy": 1.0,
            "malaria_iptp_sp_taken": 1.0,
            "malaria_iptp_doses": 1.0,
            "malaria_iptp_optimal_3plus": 0.0,
            "number_of_times_took_fansidar_iptp": 1.0,
            "malaria_itn_slept_last_night": 0.0,
            "malaria_unprotected_in_pregnancy": 1.0,
            "maternal_hemoglobin_g_dl": 10.2,
            "maternal_hemoglobin_altitude_smoking_adj": 102.0,
            "maternal_hemoglobin_g_dl_1dec": 102.0,
            "maternal_bmi_kg_m2": 19.4,
        })

    # Group selected features by the 4 Architecture Domains
    dom_cols = st.columns(4)
    domain_order = ["Malaria Data", "Clinical/Maternal Data", "Lab Data", "Demographic Data"]
    user_input = {}

    for d_idx, dom_name in enumerate(domain_order):
        with dom_cols[d_idx]:
            st.markdown(f"#### {dom_name}")
            feats_in_dom = [f for f in selected_features if FEATURE_TO_DOMAIN.get(f) == dom_name]
            for fname in feats_in_dom:
                fmin, fmax = feature_ranges.get(fname, (0.0, 100.0))
                default_v = float(preset_vals.get(fname, feature_defaults.get(fname, 0.0)))
                desc_lbl = label_map.get(fname, fname)
                if fmin == 0.0 and fmax == 1.0:
                    val_sel = st.selectbox(
                        f"{fname}",
                        options=[0, 1],
                        index=1 if int(round(default_v)) == 1 else 0,
                        format_func=lambda x: "1 = Yes" if x == 1 else "0 = No",
                        help=desc_lbl,
                        key=f"inp_{preset_choice}_{fname}",
                    )
                    user_input[fname] = float(val_sel)
                else:
                    step_v = 0.1 if ("bmi" in fname or "g_dl" in fname and "1dec" not in fname) else 1.0
                    val_num = st.number_input(
                        f"{fname}",
                        min_value=float(min(fmin, default_v)),
                        max_value=float(max(fmax, default_v, 1.0)),
                        value=float(default_v),
                        step=step_v,
                        help=desc_lbl,
                        key=f"inp_{preset_choice}_{fname}",
                    )
                    user_input[fname] = float(val_num)

    patient_series = pd.Series(user_input)[selected_features]
    local_exp = ebm_model.explain_local(patient_series)
    apo_prob = local_exp["predicted_probability"]

    st.divider()
    res_col1, res_col2 = st.columns([1.15, 1.85])

    with res_col1:
        st.markdown("### 🎯 Predicted Pregnancy Risk Assessment")
        if apo_prob >= best_threshold + 0.12:
            tier_label = "🔴 HIGH / CRITICAL ADVERSE OUTCOME RISK"
            st.error(f"**{tier_label}**  \nPredicted Composite APO Probability: **{apo_prob*100:.1f}%** (Clinical Action Threshold: {best_threshold*100:.1f}%)")
        elif apo_prob >= best_threshold - 0.05:
            tier_label = "🟠 MODERATE ADVERSE OUTCOME RISK"
            st.warning(f"**{tier_label}**  \nPredicted Composite APO Probability: **{apo_prob*100:.1f}%** (Clinical Action Threshold: {best_threshold*100:.1f}%)")
        else:
            tier_label = "🟢 LOW ADVERSE OUTCOME RISK"
            st.success(f"**{tier_label}**  \nPredicted Composite APO Probability: **{apo_prob*100:.1f}%** (Clinical Action Threshold: {best_threshold*100:.1f}%)")

        st.markdown("#### Multi-Endpoint Clinical Risk Breakdown")
        ep_rows = []
        for ep_name, ep_model in endpoint_models.items():
            ep_p = float(ep_model.predict_proba(patient_series.to_frame().T)[0, 1])
            ep_rows.append({"Clinical Endpoint": ep_name, "Predicted Risk (%)": f"{ep_p*100:.1f}%", "_raw": ep_p})
        df_ep_risk = pd.DataFrame(ep_rows)
        st.dataframe(df_ep_risk[["Clinical Endpoint", "Predicted Risk (%)"]], use_container_width=True, hide_index=True)

        st.markdown("#### 🩺 Personalized Clinical Recommendations")
        for rec_text in generate_clinical_recommendations(patient_series, apo_prob):
            st.markdown(f"- {rec_text}")

    with res_col2:
        st.markdown("### 🔍 Local EBM Result Explanation (Exact Additive Log-Odds Breakdown)")
        top_contrib = local_exp["contributions_df"].head(14).iloc[::-1]
        fig_loc, ax_loc = plt.subplots(figsize=(9.5, 5.6))
        colors_loc = ["#dc2626" if v > 0 else "#16a34a" for v in top_contrib["log_odds_contribution"]]
        labels_loc = [f"{r['term']} ({r['patient_value']})" for _, r in top_contrib.iterrows()]
        ax_loc.barh(labels_loc, top_contrib["log_odds_contribution"], color=colors_loc, edgecolor="#1e293b", alpha=0.9)
        ax_loc.axvline(0.0, color="#0f172a", linewidth=1.2)
        ax_loc.set_xlabel("Additive Log-Odds Contribution (Red = Increases Risk | Green = Protective)")
        ax_loc.set_title(
            f"Patient-Specific EBM Feature Contributions (Intercept = {local_exp['intercept_log_odds']:.2f}, Total Log-Odds = {local_exp['total_log_odds']:.2f})",
            fontweight="bold",
            fontsize=10,
        )
        ax_loc.grid(axis="x", alpha=0.25)
        plt.tight_layout()
        st.pyplot(fig_loc)
        plt.close(fig_loc)

        with st.expander("View Full Patient Additive Contribution Table (All 20 Selected Features + Pairwise Interactions)"):
            st.dataframe(local_exp["contributions_df"], use_container_width=True, hide_index=True)


# ==============================================================================
# TAB 2: EBM GLOBAL EXPLAINABILITY (SHAPE FUNCTIONS & 2D INTERACTIONS)
# ==============================================================================
with tabs[1]:
    st.subheader("Explainable Boosting Machine (EBM) Global Glass-Box Explainability")
    st.markdown(
        "An EBM is a Generalized Additive Model with Pairwise Interactions: "
        r"$g(E[y]) = \beta_0 + \sum_j f_j(x_j) + \sum_{(i,j)} f_{ij}(x_i, x_j)$. "
        "Inspect the global feature rankings, non-linear 1D shape functions $f_j(x_j)$, and 2D interaction surfaces $f_{ij}(x_i, x_j)$."
    )

    g_col1, g_col2 = st.columns([1.15, 1.35])
    with g_col1:
        st.markdown("#### Global EBM Term Importances ($\text{mean}|f(x)|$)")
        df_gimp = bundle["df_global_imp"]
        fig_g, ax_g = plt.subplots(figsize=(7.5, 6.2))
        top_g = df_gimp.head(20).iloc[::-1]
        c_g = ["#d97706" if t == "Pairwise Interaction" else "#0f766e" for t in top_g["type"]]
        ax_g.barh(top_g["term"], top_g["importance_mean_abs_log_odds"], color=c_g, edgecolor="#1e293b")
        ax_g.set_xlabel("Mean |Log-Odds Contribution|")
        ax_g.set_title("Top 20 EBM Main Effects & Pairwise Interactions", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig_g)
        plt.close(fig_g)

    with g_col2:
        st.markdown("#### Interactive 1D EBM Shape Function Explorer $f_j(x_j)$")
        chosen_feat = st.selectbox(
            "Select a Feature to Inspect its Learned EBM Shape Function:",
            selected_features,
            index=0,
        )
        st.caption(f"**Description:** {label_map.get(chosen_feat, chosen_feat)} | **Domain:** `{FEATURE_TO_DOMAIN.get(chosen_feat, 'Clinical')}`")
        sdf = ebm_model.get_shape_function_df(chosen_feat)

        fig_s, (ax_top, ax_bot) = plt.subplots(
            2, 1, figsize=(8.2, 5.5), gridspec_kw={"height_ratios": [2.4, 1]}, sharex=True
        )
        ax_top.axhline(0.0, color="#64748b", linestyle="--", linewidth=1.0)
        ax_top.step(sdf["feature_value"], sdf["log_odds_score"], where="mid", color="#0f766e", linewidth=2.5, label="Shape Function f_j(x_j)")
        ax_top.fill_between(
            sdf["feature_value"], sdf["lower_bound"], sdf["upper_bound"],
            step="mid", color="#0f766e", alpha=0.22, label="±1 SD (Outer Bags)"
        )
        ax_top.set_ylabel("Log-Odds Risk Contribution")
        ax_top.set_title(f"Non-Linear EBM Shape Function: {chosen_feat}", fontweight="bold")
        ax_top.legend(loc="best")
        ax_top.grid(alpha=0.25)

        ax_bot.bar(
            sdf["feature_value"], sdf["sample_count"],
            width=max((sdf["feature_value"].max() - sdf["feature_value"].min()) / max(len(sdf) * 1.5, 4), 0.15),
            color="#0284c7", alpha=0.75, edgecolor="#1e293b"
        )
        ax_bot.set_xlabel(chosen_feat)
        ax_bot.set_ylabel("Train Count")
        ax_bot.grid(alpha=0.25)
        plt.tight_layout()
        st.pyplot(fig_s)
        plt.close(fig_s)

    st.divider()
    st.markdown("#### Interactive 2D Pairwise Interaction Heatmap Explorer $f_{ij}(x_i, x_j)$")
    inter_labels = [
        f"{ebm_model.feature_names_in_[i]}  ×  {ebm_model.feature_names_in_[j]}"
        for (i, j) in ebm_model.interactions_
    ]
    if inter_labels:
        sel_inter_idx = st.selectbox("Select Pairwise Clinical Interaction:", range(len(inter_labels)), format_func=lambda k: inter_labels[k])
        i_f, j_f = ebm_model.interactions_[sel_inter_idx]
        fname_i = ebm_model.feature_names_in_[i_f]
        fname_j = ebm_model.feature_names_in_[j_f]
        surf_2d = ebm_model.interaction_tables_[sel_inter_idx]

        fig_2d, ax_2d = plt.subplots(figsize=(8.5, 4.8))
        im2d = ax_2d.imshow(surf_2d, cmap="coolwarm", aspect="auto", origin="lower")
        ax_2d.set_xticks(range(len(ebm_model.inter_bin_centers_[j_f])))
        ax_2d.set_xticklabels([f"{v:.1f}" for v in ebm_model.inter_bin_centers_[j_f]], rotation=25)
        ax_2d.set_yticks(range(len(ebm_model.inter_bin_centers_[i_f])))
        ax_2d.set_yticklabels([f"{v:.1f}" for v in ebm_model.inter_bin_centers_[i_f]])
        ax_2d.set_xlabel(fname_j)
        ax_2d.set_ylabel(fname_i)
        ax_2d.set_title(f"2D Interaction Log-Odds Surface: {fname_i} × {fname_j}", fontweight="bold")
        plt.colorbar(im2d, ax=ax_2d, label="Interaction Log-Odds f_ij(x_i, x_j)")
        plt.tight_layout()
        st.pyplot(fig_2d)
        plt.close(fig_2d)


# ==============================================================================
# TAB 3: CWGB FEATURE SELECTION & DATA PREPROCESSING
# ==============================================================================
with tabs[2]:
    st.subheader("Data Preprocessing & Component-Wise Gradient Boosting (CWGB) Feature Selection")
    st.markdown(
        "As shown in the **Proposed System Architecture**, after Data Cleaning, Missing Value Imputation, Encoding, and Normalization, **Component-Wise Gradient Boosting** iteratively fits univariate base learners to pseudo-residuals $u_i = y_i - \sigma(F_{m-1}(x_i))$ to select the most informative predictors across all four domains."
    )
    cw_col1, cw_col2 = st.columns([1, 1.3])
    with cw_col1:
        df_trace = bundle["df_cwgb_trace"]
        fig_tr, ax_tr = plt.subplots(figsize=(6.8, 4.8))
        ax_tr.plot(df_trace["iteration"], df_trace["log_loss"], color="#0f766e", linewidth=2.2)
        ax_tr.set_xlabel("Boosting Iteration (m)")
        ax_tr.set_ylabel("Training Binomial Log-Loss")
        ax_tr.set_title("CWGB Loss Convergence Across 180 Iterations", fontweight="bold")
        ax_tr.grid(alpha=0.25)
        plt.tight_layout()
        st.pyplot(fig_tr)
        plt.close(fig_tr)

    with cw_col2:
        df_rank = bundle["df_cwgb_rank"]
        st.markdown("##### Top 20 Features Selected by Feature Importance (CWGB)")
        st.dataframe(
            df_rank[df_rank["selected_for_ebm"]][
                ["rank", "feature_name", "domain", "selection_frequency", "cumulative_rss_gain", "relative_importance_pct"]
            ],
            use_container_width=True,
            hide_index=True,
        )


# ==============================================================================
# TAB 4: MODEL EVALUATION & SUBGROUP BENCHMARKS
# ==============================================================================
with tabs[3]:
    st.subheader("Model Evaluation & Regional Subgroup Benchmarking")
    st.markdown("#### Comparative Performance on Held-Out Test Set (`n = 2,698` Pregnancies)")
    st.dataframe(bundle["df_eval"], use_container_width=True, hide_index=True)

    st.markdown("#### Slice-Based Subgroup Analysis (Geopolitical Zones, South-South Focus Zone & Urban/Rural)")
    st.dataframe(bundle["df_slices"], use_container_width=True, hide_index=True)


# ==============================================================================
# TAB 5: SYSTEM ARCHITECTURE & DATASET EXPLORER
# ==============================================================================
with tabs[4]:
    st.subheader("Proposed System Architecture & Dataset Explorer")
    for img_path in ARCH_IMG_CANDIDATES:
        if os.path.exists(img_path):
            st.image(img_path, caption="Proposed System Architecture: Data Collection → Data Preprocessing → CWGB Feature Selection → Explainable Boosting Machine → Prototype Predictive System & Result Explanation", use_container_width=True)
            break

    st.markdown("#### Extracted Top-20 Important Features Dataset")
    if os.path.exists(TOP20_DATA_PATH):
        df_top20 = pd.read_csv(TOP20_DATA_PATH)
        st.caption(f"`top_20_important_features_dataset.csv`: {df_top20.shape[0]:,} rows x {df_top20.shape[1]} columns (20 predictors + outcome targets)")
        st.dataframe(df_top20.head(50), use_container_width=True)
        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            st.download_button(
                "Download Top-20 Features Dataset (CSV)",
                data=df_top20.to_csv(index=False).encode("utf-8"),
                file_name="top_20_important_features_dataset.csv",
                mime="text/csv",
            )
        if os.path.exists(TOP20_DICT_PATH):
            df_top20_dict = pd.read_csv(TOP20_DICT_PATH)
            with dl_col2:
                st.download_button(
                    "Download Top-20 Features Dictionary (CSV)",
                    data=df_top20_dict.to_csv(index=False).encode("utf-8"),
                    file_name="top_20_important_features_dictionary.csv",
                    mime="text/csv",
                )
            with st.expander("View Top-20 Features Dictionary"):
                st.dataframe(df_top20_dict, use_container_width=True, hide_index=True)

    st.markdown(f"#### Full Dataset Feature Dictionary (`{df.shape[1]} Features`)")
    search_q = st.text_input("Filter Dictionary by Feature Name, Field Code, Description, or Category:", "")
    if search_q.strip():
        mask = (
            df_dict["feature_name"].str.contains(search_q, case=False, na=False)
            | df_dict["field_code"].astype(str).str.contains(search_q, case=False, na=False)
            | df_dict["feature_description"].astype(str).str.contains(search_q, case=False, na=False)
            | df_dict["research_category"].astype(str).str.contains(search_q, case=False, na=False)
        )
        st.dataframe(df_dict[mask], use_container_width=True, hide_index=True)
    else:
        st.dataframe(df_dict, use_container_width=True, hide_index=True)

    st.markdown("#### Sample Records from `merged_malaria_pregnancy_outcomes_dataset.csv`")
    st.dataframe(df.head(50), use_container_width=True)


# ==============================================================================
# TAB 6: BATCH CSV PREDICTION (QUESTIONNAIRE UPLOAD)
# ==============================================================================
with tabs[5]:
    st.subheader("Batch Prediction & Local Explanation from Questionnaire CSV")
    st.markdown(
        "Upload a CSV file collected via the **Research Data Collection Questionnaire / Google Form** (or any subset of `merged_malaria_pregnancy_outcomes_dataset.csv`) to generate batch EBM risk predictions and top patient-specific risk drivers."
    )
    uploaded_csv = st.file_uploader("Upload Patient / Questionnaire CSV File", type=["csv"])
    if uploaded_csv is not None:
        df_up = pd.read_csv(uploaded_csv)
        for col in selected_features:
            if col not in df_up.columns:
                df_up[col] = feature_defaults.get(col, 0.0)
        X_up = df_up[selected_features].apply(pd.to_numeric, errors="coerce").fillna(pd.Series(feature_defaults))
        probs_up = ebm_model.predict_proba(X_up)[:, 1]
        df_up["predicted_apo_probability"] = np.round(probs_up, 4)
        df_up["predicted_apo_class"] = (probs_up >= best_threshold).astype(int)
        df_up["risk_tier"] = np.where(
            probs_up >= best_threshold + 0.12, "High Risk",
            np.where(probs_up >= best_threshold - 0.05, "Moderate Risk", "Low Risk")
        )
        st.success(f"Processed {len(df_up):,} records! High-Risk Cases Flagged: {int((df_up['predicted_apo_class'] == 1).sum()):,}")
        st.dataframe(
            df_up[["predicted_apo_probability", "predicted_apo_class", "risk_tier"] + selected_features[:10]].head(50),
            use_container_width=True,
        )
        csv_bytes = df_up.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Scored Batch Predictions CSV",
            data=csv_bytes,
            file_name="ebm_scored_pregnancy_outcomes.csv",
            mime="text/csv",
        )
