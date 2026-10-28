"""
Core Machine Learning & Explainable AI Module for:
"A Predictive Model of Adverse Pregnancy Outcomes Among Malaria-Infected Pregnant Women
in Resource-Constrained Settings using Explainable Boosting Machine"
Author: Akpan Divine Eteyen (AK22/PHS/CSC/002)

Implements the exact Proposed System Architecture:
1. Data Collection Organization (Clinical/Maternal, Demographic, Lab, Malaria Data)
2. Data Preprocessing (Data Cleaning, Missing Value Imputation, Data Encoding, Normalization)
3. Component-Wise Gradient Boosting (CWGB) for Feature Selection (Top 20 Features by Importance)
4. Explainable Boosting Machine (EBM / GA2M: Cyclic Boosted Generalized Additive Model
   with Pairwise Interactions, Global Shape Functions, and Local Explanations)
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import StandardScaler


# ==============================================================================
# 1. CANDIDATE PREDICTOR FEATURES ORGANIZED BY THE 4 ARCHITECTURE DOMAINS
# ==============================================================================
# Non-redundant pre-outcome predictors across the 4 domains (excluding post-outcome
# target-leakage variables and duplicate rescaled copies).

DOMAIN_FEATURES = {
    "Clinical/Maternal Data": [
        "pregnancy_order_number",
        "is_primigravida",
        "parity_total_children_ever_born",
        "number_of_living_children",
        "age_at_first_birth",
        "ever_had_terminated_pregnancy",
        "number_of_pregnancy_losses",
        "total_pregnancy_history_entries",
        "multiple_or_twin_pregnancy",
        "preceding_pregnancy_interval_months",
        "short_pregnancy_interval_under_24m",
        "pregnancy_wantedness",
        "number_of_anc_visits",
        "anc_4plus_visits",
        "anc_8plus_visits",
        "timing_first_anc_visit_months",
        "anc_first_trimester",
        "anc_any_skilled_provider",
        "anc_provider_doctor",
        "anc_provider_nurse_midwife",
        "anc_provider_chew",
        "anc_provider_traditional_birth_attendant",
        "anc_provider_no_one",
        "tetanus_injections_before_birth",
        "iron_tablets_or_syrup_taken",
        "days_iron_tablets_or_syrup_taken",
        "intestinal_parasite_drugs_during_pregnancy",
        "anc_counseled_on_nutrition",
        "anc_blood_pressure_taken",
        "anc_asked_about_vaginal_bleeding",
        "maternal_bmi_kg_m2",
        "maternal_underweight_bmi_under_18_5",
        "self_reported_health_status",
        "ever_told_has_high_blood_pressure_hypertension",
        "currently_taking_medication_for_high_bp",
        "ever_told_has_high_blood_sugar_diabetes",
        "did_not_experience_physical_violence_during_pregnancy",
        "experienced_any_emotional_violence",
        "experienced_any_less_severe_physical_violence",
        "experienced_any_severe_physical_violence",
        "covered_by_health_insurance",
        "minutes_to_nearest_healthcare_facility",
        "mode_of_transport_to_healthcare_facility",
        "barrier_getting_permission_to_go",
        "barrier_getting_money_for_treatment",
        "barrier_distance_to_health_facility",
        "barrier_not_wanting_to_go_alone",
    ],
    "Demographic Data": [
        "maternal_age_years",
        "geopolitical_zone",
        "state_code",
        "is_south_south_zone",
        "is_akwa_ibom_state",
        "residence_urban_rural",
        "cluster_altitude_meters",
        "maternal_education_level",
        "maternal_education_years",
        "maternal_literacy",
        "religion",
        "marital_status_detailed",
        "marital_union_status",
        "age_at_first_cohabitation",
        "wealth_index_quintile",
        "maternal_currently_working",
        "maternal_occupation_group",
        "partner_education_level",
        "partner_education_years",
        "partner_age_years",
        "decision_maker_maternal_healthcare",
        "media_radio_frequency",
        "media_tv_frequency",
        "owns_mobile_phone",
        "use_of_internet",
        "drinking_water_source",
        "time_to_water_source_mins",
        "anything_done_to_water_to_make_safe_to_drink",
        "toilet_facility_type",
        "toilet_shared_with_other_households",
        "household_has_electricity",
        "main_floor_material",
        "main_wall_material",
        "main_roof_material",
        "type_of_cooking_fuel",
        "total_household_members",
        "children_under_5_in_household",
        "number_of_rooms_used_for_sleeping",
        "sex_of_head_of_household",
        "age_of_head_of_household",
        "frequency_household_members_smoke_inside_house",
        "fies_worried_not_enough_food",
        "fies_unable_to_eat_healthy_nutritious_food",
        "fies_had_to_skip_a_meal",
        "fies_hungry_but_did_not_eat",
        "fies_went_without_eating_for_whole_day",
        "household_moderate_or_severe_food_insecurity_prob",
    ],
    "Lab Data": [
        "maternal_hemoglobin_g_dl",
        "result_of_hemoglobin_measurement",
        "anc_blood_sample_taken",
        "anc_urine_sample_taken",
        "tested_for_hepatitis_b_during_anc",
        "hepatitis_b_test_result_anc",
        "tested_for_hepatitis_c_during_anc",
        "hepatitis_c_test_result_anc",
        "ever_been_tested_for_hiv",
        "tested_for_hiv_as_part_of_anc_visit",
        "result_of_last_hiv_test",
    ],
    "Malaria Data": [
        "malaria_iptp_sp_taken",
        "malaria_iptp_doses",
        "malaria_iptp_optimal_3plus",
        "source_of_antimalarial_during_pregnancy",
        "household_has_mosquito_bed_net",
        "number_of_mosquito_bed_nets_in_hh",
        "maternal_slept_under_mosquito_net",
        "maternal_type_of_mosquito_bed_net",
        "net_used_was_insecticide_treated_itn",
        "number_of_persons_who_slept_under_this_net",
        "person_slept_under_llin_net",
        "malaria_itn_slept_last_night",
        "malaria_llin_slept_last_night",
        "malaria_unprotected_in_pregnancy",
        "pregnancy_outcome_rainy_season",
        "month_of_pregnancy_outcome",
        "seen_or_heard_malaria_messages_last_6m",
        "malaria_msg_source_radio",
        "malaria_msg_source_television",
        "malaria_msg_source_healthcare_provider",
        "malaria_msg_source_community_health_worker",
        "knows_ways_to_avoid_getting_malaria",
        "prevent_malaria_sleep_under_mosquito_net",
        "prevent_malaria_sleep_under_itn",
        "prevent_malaria_take_preventive_medications",
        "prevent_malaria_fill_in_stagnant_waters",
        "prevent_malaria_keep_surroundings_clean",
        "community_gets_malaria_in_rainy_season_perception",
        "worries_child_fever_is_malaria",
        "believes_malaria_not_problem_as_treatable",
        "sleeps_under_net_when_lots_of_mosquitoes",
        "sleeps_under_net_when_few_mosquitoes",
        "dislikes_sleeping_in_net_when_too_warm",
        "community_takes_febrile_child_same_day",
        "community_sleeps_under_nets_every_night",
        "child_fever_last_2_weeks",
        "child_blood_taken_from_finger_heel_for_testing",
        "told_child_had_malaria_diagnosis",
        "child_took_act_for_fever",
        "child_took_sp_fansidar_for_fever",
    ],
}

FEATURE_TO_DOMAIN = {}
ALL_CANDIDATE_FEATURES = []
for dom, feats in DOMAIN_FEATURES.items():
    for f in feats:
        if f not in FEATURE_TO_DOMAIN:
            FEATURE_TO_DOMAIN[f] = dom
            ALL_CANDIDATE_FEATURES.append(f)


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30.0, 30.0)))


# ==============================================================================
# 2. COMPONENT-WISE GRADIENT BOOSTING FOR FEATURE SELECTION (TOP 20 BY IMPORTANCE)
# ==============================================================================
class ComponentWiseGradientBoostingSelector:
    """
    Component-Wise Gradient Boosting (Bühlmann & Yu, 2003; Binder & Schumacher, 2008)
    for feature importance ranking and selecting the Top 20 features.

    At each boosting iteration m = 1..M:
      1. Computes negative binomial log-likelihood gradients (pseudo-residuals):
         u_i = y_i - sigmoid(F_{m-1}(x_i))
      2. Fits a separate univariate base learner to every candidate feature x_j.
      3. Selects the single best feature j* that maximizes the reduction in
         Residual Sum of Squares (RSS gain) on u.
      4. Updates F_m(x) = F_{m-1}(x) + nu * h_{j*}(x_{j*}).
      5. Ranks all features by feature importance (cumulative RSS gain) and selects
         strictly the top `n_select=20` most important features.
    """

    def __init__(
        self,
        n_estimators=180,
        learning_rate=0.12,
        n_select=20,
        n_bins=12,
        l2_reg=5.0,
    ):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.n_select = n_select
        self.n_bins = n_bins
        self.l2_reg = l2_reg

        self.feature_names_ = None
        self.selection_counts_ = None
        self.cumulative_gain_ = None
        self.Normalized_importance_ = None
        self.selected_features_ = None
        self.selection_trace_ = []
        self.ranking_df_ = None

    def _prebin_features(self, X_np):
        n_samples, n_features = X_np.shape
        binned = np.zeros((n_samples, n_features), dtype=np.int32)
        n_bins_list = []
        for j in range(n_features):
            col = X_np[:, j]
            uniq = np.unique(col)
            if len(uniq) <= self.n_bins:
                edges = uniq[:-1] + 0.5 * np.diff(uniq)
            else:
                qs = np.linspace(0, 100, self.n_bins + 1)[1:-1]
                edges = np.unique(np.percentile(col, qs))
            b = np.searchsorted(edges, col, side="right")
            binned[:, j] = b
            n_bins_list.append(len(edges) + 1)
        return binned, n_bins_list

    def fit(self, X_df: pd.DataFrame, y: np.ndarray, domain_map: dict = None):
        self.feature_names_ = list(X_df.columns)
        X_np = X_df.to_numpy(dtype=np.float64)
        y_np = np.asarray(y, dtype=np.float64)
        n_samples, n_features = X_np.shape

        pos_rate = np.clip(np.mean(y_np), 1e-4, 1.0 - 1e-4)
        F = np.full(n_samples, np.log(pos_rate / (1.0 - pos_rate)), dtype=np.float64)

        binned_X, n_bins_list = self._prebin_features(X_np)

        selection_counts = np.zeros(n_features, dtype=np.int32)
        cumulative_gain = np.zeros(n_features, dtype=np.float64)
        self.selection_trace_ = []

        for m in range(self.n_estimators):
            p = _sigmoid(F)
            residuals = y_np - p

            best_j = 0
            best_gain = -1.0
            best_pred = None

            for j in range(n_features):
                b = binned_X[:, j]
                nb = n_bins_list[j]
                sum_r = np.bincount(b, weights=residuals, minlength=nb)
                cnt = np.bincount(b, minlength=nb).astype(np.float64)
                bin_vals = sum_r / (cnt + self.l2_reg)
                raw_gain = float(np.sum(sum_r * bin_vals))
                effective_gain = raw_gain / (1.0 + 0.15 * selection_counts[j])
                if effective_gain > best_gain:
                    best_gain = effective_gain
                    best_j = j
                    best_pred = bin_vals[b]

            F += self.learning_rate * best_pred
            selection_counts[best_j] += 1
            cumulative_gain[best_j] += best_gain

            loss_val = float(
                -np.mean(
                    y_np * np.log(np.clip(_sigmoid(F), 1e-7, 1 - 1e-7))
                    + (1 - y_np) * np.log(np.clip(1 - _sigmoid(F), 1e-7, 1 - 1e-7))
                )
            )
            self.selection_trace_.append({
                "iteration": m + 1,
                "selected_feature": self.feature_names_[best_j],
                "rss_gain": round(best_gain, 4),
                "log_loss": round(loss_val, 5),
            })

        total_gain = float(np.sum(cumulative_gain)) or 1.0
        norm_imp = (cumulative_gain / total_gain) * 100.0

        self.selection_counts_ = selection_counts
        self.cumulative_gain_ = cumulative_gain
        self.Normalized_importance_ = norm_imp

        rows = []
        for j, fname in enumerate(self.feature_names_):
            dom = domain_map.get(fname, "Other") if domain_map else FEATURE_TO_DOMAIN.get(fname, "Other")
            rows.append({
                "feature_name": fname,
                "domain": dom,
                "selection_frequency": int(selection_counts[j]),
                "cumulative_rss_gain": round(float(cumulative_gain[j]), 4),
                "relative_importance_pct": round(float(norm_imp[j]), 3),
            })

        df_rank = pd.DataFrame(rows).sort_values(
            by=["relative_importance_pct", "cumulative_rss_gain", "selection_frequency"],
            ascending=False,
        ).reset_index(drop=True)
        df_rank["rank"] = np.arange(1, len(df_rank) + 1)

        # Select strictly the top `n_select` (20) features ranked by feature importance
        selected = df_rank.head(self.n_select)["feature_name"].tolist()
        df_rank["selected_for_ebm"] = df_rank["feature_name"].isin(selected)

        self.selected_features_ = selected
        self.ranking_df_ = df_rank
        return self

    def transform(self, X_df: pd.DataFrame) -> pd.DataFrame:
        return X_df[self.selected_features_].copy()


# ==============================================================================
# 3. EXPLAINABLE BOOSTING MACHINE (EBM / GA2M CLASSIFIER)
# ==============================================================================
class ExplainableBoostingMachineClassifier(BaseEstimator, ClassifierMixin):
    """
    Explainable Boosting Machine (EBM — Lou et al., 2012, 2013; Nori et al., 2019).
    Generalized Additive Model with Pairwise Interactions (GA2M):
        g(E[y]) = beta_0 + sum_{j=1}^{20} f_j(x_j) + sum_{(i,j)} f_{ij}(x_i, x_j)
    """

    def __init__(
        self,
        n_cycles=85,
        learning_rate=0.035,
        n_bags=8,
        subsample=0.82,
        max_bins=24,
        n_interactions=6,
        interaction_rounds=45,
        interaction_bins=6,
        l2_reg=8.0,
        random_state=42,
    ):
        self.n_cycles = n_cycles
        self.learning_rate = learning_rate
        self.n_bags = n_bags
        self.subsample = subsample
        self.max_bins = max_bins
        self.n_interactions = n_interactions
        self.interaction_rounds = interaction_rounds
        self.interaction_bins = interaction_bins
        self.l2_reg = l2_reg
        self.random_state = random_state

    def _fit_bin_edges(self, X_np, max_b):
        n_features = X_np.shape[1]
        edges_list = []
        bin_centers_list = []
        for j in range(n_features):
            col = X_np[:, j]
            uniq = np.unique(col)
            if len(uniq) <= max_b:
                edges = uniq[:-1] + 0.5 * np.diff(uniq)
                centers = uniq.astype(np.float64)
            else:
                qs = np.linspace(0, 100, max_b + 1)[1:-1]
                edges = np.unique(np.percentile(col, qs))
                b_idx = np.searchsorted(edges, col, side="right")
                nb = len(edges) + 1
                centers = np.zeros(nb, dtype=np.float64)
                for b in range(nb):
                    mask = b_idx == b
                    if np.any(mask):
                        centers[b] = float(np.median(col[mask]))
                    else:
                        centers[b] = float(edges[min(b, len(edges) - 1)])
            edges_list.append(edges)
            bin_centers_list.append(centers)
        return edges_list, bin_centers_list

    @staticmethod
    def _apply_bins(X_np, edges_list):
        n_samples, n_features = X_np.shape
        binned = np.zeros((n_samples, n_features), dtype=np.int32)
        for j in range(n_features):
            binned[:, j] = np.searchsorted(edges_list[j], X_np[:, j], side="right")
        return binned

    def fit(self, X, y):
        if isinstance(X, pd.DataFrame):
            self.feature_names_in_ = list(X.columns)
            X_np = X.to_numpy(dtype=np.float64)
        else:
            X_np = np.asarray(X, dtype=np.float64)
            self.feature_names_in_ = [f"feature_{i}" for i in range(X_np.shape[1])]

        y_np = np.asarray(y, dtype=np.float64)
        self.classes_ = np.array([0, 1])
        n_samples, n_features = X_np.shape

        self.bin_edges_, self.bin_centers_ = self._fit_bin_edges(X_np, self.max_bins)
        binned_X = self._apply_bins(X_np, self.bin_edges_)
        self.n_bins_per_feature_ = [len(e) + 1 for e in self.bin_edges_]
        self.bin_counts_ = [
            np.bincount(binned_X[:, j], minlength=self.n_bins_per_feature_[j]).tolist()
            for j in range(n_features)
        ]

        pos_rate = np.clip(np.mean(y_np), 1e-4, 1.0 - 1e-4)
        base_log_odds = float(np.log(pos_rate / (1.0 - pos_rate)))

        rng = np.random.RandomState(self.random_state)
        bag_tables = [[np.zeros(nb, dtype=np.float64) for nb in self.n_bins_per_feature_] for _ in range(self.n_bags)]
        bag_intercepts = np.full(self.n_bags, base_log_odds, dtype=np.float64)

        for b_idx in range(self.n_bags):
            sub_n = int(round(self.subsample * n_samples))
            sample_idx = rng.choice(n_samples, size=sub_n, replace=False)
            X_b = binned_X[sample_idx]
            y_b = y_np[sample_idx]

            F_b = np.full(sub_n, bag_intercepts[b_idx], dtype=np.float64)
            tables_b = bag_tables[b_idx]

            for _ in range(self.n_cycles):
                for j in range(n_features):
                    p_b = _sigmoid(F_b)
                    grad = y_b - p_b
                    hess = p_b * (1.0 - p_b)

                    nb = self.n_bins_per_feature_[j]
                    col_b = X_b[:, j]
                    sum_g = np.bincount(col_b, weights=grad, minlength=nb)
                    sum_h = np.bincount(col_b, weights=hess, minlength=nb)

                    step = self.learning_rate * (sum_g / (sum_h + self.l2_reg))
                    if nb > 6:
                        step_smooth = step.copy()
                        step_smooth[1:-1] = 0.15 * step[:-2] + 0.70 * step[1:-1] + 0.15 * step[2:]
                        step = step_smooth

                    tables_b[j] += step
                    F_b += step[col_b]

            for j in range(n_features):
                col_full = binned_X[:, j]
                mean_shift = float(np.mean(tables_b[j][col_full]))
                tables_b[j] -= mean_shift
                bag_intercepts[b_idx] += mean_shift

        self.intercept_ = float(np.mean(bag_intercepts))
        self.shape_functions_ = []
        self.shape_stds_ = []
        for j in range(n_features):
            stacked = np.vstack([bag_tables[b_idx][j] for b_idx in range(self.n_bags)])
            self.shape_functions_.append(np.mean(stacked, axis=0))
            self.shape_stds_.append(np.std(stacked, axis=0))

        # FAST Pairwise Interaction Detection & 2D Additive Surface Boosting
        F_main = np.full(n_samples, self.intercept_, dtype=np.float64)
        for j in range(n_features):
            F_main += self.shape_functions_[j][binned_X[:, j]]

        self.inter_bin_edges_, self.inter_bin_centers_ = self._fit_bin_edges(X_np, self.interaction_bins)
        binned_inter_X = self._apply_bins(X_np, self.inter_bin_edges_)
        self.n_inter_bins_ = [len(e) + 1 for e in self.inter_bin_edges_]

        main_importances = [
            float(np.mean(np.abs(self.shape_functions_[j][binned_X[:, j]])))
            for j in range(n_features)
        ]
        top_main_idx = np.argsort(main_importances)[::-1][:min(14, n_features)]

        residuals_main = y_np - _sigmoid(F_main)
        pair_scores = []
        for idx_a in range(len(top_main_idx)):
            for idx_b in range(idx_a + 1, len(top_main_idx)):
                i = int(top_main_idx[idx_a])
                j = int(top_main_idx[idx_b])
                nb_i = self.n_inter_bins_[i]
                nb_j = self.n_inter_bins_[j]
                flat_idx = binned_inter_X[:, i] * nb_j + binned_inter_X[:, j]
                sum_r = np.bincount(flat_idx, weights=residuals_main, minlength=nb_i * nb_j)
                cnt = np.bincount(flat_idx, minlength=nb_i * nb_j).astype(np.float64)
                gain = float(np.sum((sum_r ** 2) / (cnt + self.l2_reg * 2.0)))
                pair_scores.append((gain, i, j))

        pair_scores.sort(reverse=True, key=lambda x: x[0])
        self.interactions_ = [(i, j) for _, i, j in pair_scores[:self.n_interactions]]
        self.interaction_tables_ = [
            np.zeros((self.n_inter_bins_[i], self.n_inter_bins_[j]), dtype=np.float64)
            for (i, j) in self.interactions_
        ]

        if self.interactions_:
            F_total = F_main.copy()
            for _ in range(self.interaction_rounds):
                for k, (i, j) in enumerate(self.interactions_):
                    p_cur = _sigmoid(F_total)
                    grad = y_np - p_cur
                    hess = p_cur * (1.0 - p_cur)
                    nb_i = self.n_inter_bins_[i]
                    nb_j = self.n_inter_bins_[j]
                    bi = binned_inter_X[:, i]
                    bj = binned_inter_X[:, j]
                    flat_idx = bi * nb_j + bj
                    sum_g = np.bincount(flat_idx, weights=grad, minlength=nb_i * nb_j).reshape(nb_i, nb_j)
                    sum_h = np.bincount(flat_idx, weights=hess, minlength=nb_i * nb_j).reshape(nb_i, nb_j)
                    step_2d = (self.learning_rate * 0.6) * (sum_g / (sum_h + self.l2_reg * 2.5))
                    step_2d -= np.mean(step_2d[bi, bj])
                    self.interaction_tables_[k] += step_2d
                    F_total += step_2d[bi, bj]

        self.term_names_ = list(self.feature_names_in_) + [
            f"{self.feature_names_in_[i]} x {self.feature_names_in_[j]}"
            for (i, j) in self.interactions_
        ]
        term_imps = []
        for j in range(n_features):
            term_imps.append(float(np.mean(np.abs(self.shape_functions_[j][binned_X[:, j]]))))
        for k, (i, j) in enumerate(self.interactions_):
            bi = binned_inter_X[:, i]
            bj = binned_inter_X[:, j]
            term_imps.append(float(np.mean(np.abs(self.interaction_tables_[k][bi, bj]))))

        self.term_importances_ = np.array(term_imps, dtype=np.float64)
        self.main_importances_ = self.term_importances_[:n_features]
        return self

    def decision_function(self, X):
        if isinstance(X, pd.DataFrame):
            X_np = X[self.feature_names_in_].to_numpy(dtype=np.float64)
        else:
            X_np = np.asarray(X, dtype=np.float64)

        n_samples, n_features = X_np.shape
        binned_X = self._apply_bins(X_np, self.bin_edges_)
        F = np.full(n_samples, self.intercept_, dtype=np.float64)
        for j in range(n_features):
            F += self.shape_functions_[j][binned_X[:, j]]

        if self.interactions_:
            binned_inter_X = self._apply_bins(X_np, self.inter_bin_edges_)
            for k, (i, j) in enumerate(self.interactions_):
                F += self.interaction_tables_[k][binned_inter_X[:, i], binned_inter_X[:, j]]
        return F

    def predict_proba(self, X):
        log_odds = self.decision_function(X)
        prob_pos = _sigmoid(log_odds)
        return np.column_stack([1.0 - prob_pos, prob_pos])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    def get_shape_function_df(self, feature_name: str) -> pd.DataFrame:
        j = self.feature_names_in_.index(feature_name)
        centers = self.bin_centers_[j]
        scores = self.shape_functions_[j]
        stds = self.shape_stds_[j]
        counts = self.bin_counts_[j]
        return pd.DataFrame({
            "bin_index": np.arange(len(centers)),
            "feature_value": centers,
            "log_odds_score": scores,
            "upper_bound": scores + stds,
            "lower_bound": scores - stds,
            "sample_count": counts,
        })

    def explain_local(self, x_row) -> dict:
        if isinstance(x_row, pd.Series):
            x_vals = np.array([float(x_row[f]) for f in self.feature_names_in_], dtype=np.float64)
        elif isinstance(x_row, pd.DataFrame):
            x_vals = x_row[self.feature_names_in_].iloc[0].to_numpy(dtype=np.float64)
        else:
            x_vals = np.asarray(x_row, dtype=np.float64).ravel()

        X_2d = x_vals.reshape(1, -1)
        binned_X = self._apply_bins(X_2d, self.bin_edges_)[0]
        binned_inter_X = self._apply_bins(X_2d, self.inter_bin_edges_)[0]

        contributions = []
        total_log_odds = self.intercept_

        for j, fname in enumerate(self.feature_names_in_):
            b = binned_X[j]
            score = float(self.shape_functions_[j][b])
            total_log_odds += score
            contributions.append({
                "term": fname,
                "type": "Main Effect",
                "domain": FEATURE_TO_DOMAIN.get(fname, "Clinical"),
                "patient_value": float(x_vals[j]),
                "log_odds_contribution": score,
            })

        for k, (i, j) in enumerate(self.interactions_):
            bi = binned_inter_X[i]
            bj = binned_inter_X[j]
            score = float(self.interaction_tables_[k][bi, bj])
            total_log_odds += score
            contributions.append({
                "term": f"{self.feature_names_in_[i]} x {self.feature_names_in_[j]}",
                "type": "Pairwise Interaction",
                "domain": "Interaction",
                "patient_value": f"{x_vals[i]:.1f} & {x_vals[j]:.1f}",
                "log_odds_contribution": score,
            })

        prob = float(_sigmoid(total_log_odds))
        df_contrib = pd.DataFrame(contributions)
        df_contrib["abs_contribution"] = df_contrib["log_odds_contribution"].abs()
        df_contrib = df_contrib.sort_values("abs_contribution", ascending=False).reset_index(drop=True)

        return {
            "intercept_log_odds": self.intercept_,
            "total_log_odds": float(total_log_odds),
            "predicted_probability": prob,
            "contributions_df": df_contrib,
        }
