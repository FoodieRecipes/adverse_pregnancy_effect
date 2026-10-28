# Standardized Clinical & Field Research Questionnaire
**Research Title:** *A Predictive Model of Adverse Pregnancy Outcomes Among Malaria-Infected Pregnant Women in Resource-Constrained Settings using Explainable Boosting Machine (EBM)*  
**Researcher:** Akpan Divine Eteyen (AK22/PHS/CSC/002) — Department of Computer Science, Akwa Ibom State University  
**Dataset Mapping:** 1-to-1 aligned with `merged_malaria_pregnancy_outcomes_dataset.csv` (281 columns covering Clinical & Maternal Records, Maternal Health & Malaria Survey, Household & Vector Control Roster, Household Environmental & Food Security Survey, Pediatric & Neonatal Clinical Records, and Engineered EBM Features/Targets).

> **Instructions for Clinical / Field Enumerators & Software Developers:**  
> Every question below includes the **Field Code** (e.g., `v012`, `m49a`) and the **Descriptive Feature Name** (e.g., `maternal_age_years`, `malaria_iptp_sp_fansidar_during_pregnancy`) in brackets, followed by the exact numerical codes used in `merged_malaria_pregnancy_outcomes_dataset.csv`. Responses entered using these codes can be fed directly into the trained Explainable Boosting Machine (EBM) model without recoding.

---

## SECTION A: IDENTIFICATION, GEOGRAPHIC LOCATION & SURVEY METADATA

| Q# | Variable (`feature_name`) | Question / Field Prompt | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **A1** | `caseid` (`woman_case_id`) | Respondent / Patient Unique Identification Code | Alphanumeric ID (e.g., `AK22-0001`) |
| **A2** | `pidx` (`pregnancy_column_index`) | Pregnancy Episode Index (for this respondent) | Integer (`1` = Most recent pregnancy, `2` = Prior pregnancy, etc.) |
| **A3** | `pidxb` (`index_to_birth_history`) | Live Birth History Index (`0` if pregnancy ended in non-live termination) | `0` = Termination (stillbirth/miscarriage/abortion); `1, 2, ...` = Birth index |
| **A4** | `v001` (`cluster_number`) | Community / Health Facility Cluster Number | Integer (`1` to `1400`) |
| **A5** | `v002` (`household_number`) | Household Number within Cluster | Integer (`1` to `500`) |
| **A6** | `v003` (`respondent_line_number`) | Woman's Line Number in Household Roster | Integer (`1` to `50`) |
| **A7** | `p16` (`child_line_number_in_household`) | Child's Line Number in Household Roster (if live-born and living in household) | `0` = Not in household / deceased; `1..50` = Line number |
| **A8** | `v005` (`womens_sample_weight`) | Survey Sample Weight (6 decimals; set `1000000` for unweighted clinical data) | Integer (e.g., `1000000`) |
| **A9** | `v006` (`interview_month`) | Month of Interview / Clinical Assessment | `1`=Jan, `2`=Feb, `3`=Mar, `4`=Apr, `5`=May, `6`=Jun, `7`=Jul, `8`=Aug, `9`=Sep, `10`=Oct, `11`=Nov, `12`=Dec |
| **A10** | `v007` (`interview_year`) | Year of Interview / Clinical Assessment | Integer (e.g., `2024`, `2026`) |
| **A11** | `v008` (`interview_date_cmc`) | Century Month Code (CMC) of Interview: `(Year - 1900) * 12 + Month` | Integer (e.g., `1488` for Dec 2023) |
| **A12** | `v024` (`geopolitical_zone`) | In which geopolitical zone of Nigeria does the respondent reside? | `1` = North Central<br>`2` = North East<br>`3` = North West<br>`4` = South East<br>`5` = South South *(Study Focus Zone)*<br>`6` = South West |
| **A13** | `sstate` (`state_code`) | State of Residence in Nigeria | `1`=Sokoto, `2`=Zamfara, `3`=Katsina, `4`=Jigawa, `5`=Yobe, `6`=Borno, `7`=Adamawa, `8`=Gombe, `9`=Bauchi, `10`=Kano, `11`=Kaduna, `12`=Kebbi, `13`=Niger, `14`=FCT Abuja, `15`=Nasarawa, `16`=Plateau, `17`=Taraba, `18`=Benue, `19`=Kogi, `20`=Kwara, `21`=Oyo, `22`=Osun, `23`=Ekiti, `24`=Ondo, `25`=Edo, `26`=Anambra, `27`=Enugu, `28`=Ebonyi, `29`=Cross River, **`30`=Akwa Ibom**, `31`=Abia, `32`=Imo, `33`=Rivers, `34`=Bayelsa, `35`=Delta, `36`=Lagos, `37`=Ogun |
| **A14** | `v025` (`residence_urban_rural`) | Type of place of residence | `1` = Urban<br>`2` = Rural |
| **A15** | `v040` (`cluster_altitude_meters`) | Community / Cluster Altitude (in meters above sea level) | Numerical in meters (e.g., `15` to `1300`) |
| **A16** | `is_south_south_zone` *(Engineered)* | Auto-derived from `v024`: Is respondent in South-South Zone? | `1` = Yes (`v024 == 5`)<br>`0` = No |
| **A17** | `is_akwa_ibom_state` *(Engineered)* | Auto-derived from `sstate`: Is respondent in Akwa Ibom State? | `1` = Yes (`sstate == 30`)<br>`0` = No |

---

## SECTION B: MATERNAL SOCIO-DEMOGRAPHIC CHARACTERISTICS

| Q# | Variable (`feature_name`) | Question / Field Prompt | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **B1** | `v012` (`maternal_age_years`) | How old are you in completed years? | Integer (`15` to `49` years) |
| **B2** | `v013` (`maternal_age_group_5yr`) | Maternal Age Group (5-year intervals, derived from `v012`) | `1` = 15–19<br>`2` = 20–24<br>`3` = 25–29<br>`4` = 30–34<br>`5` = 35–39<br>`6` = 40–44<br>`7` = 45–49 |
| **B3** | `v106` (`maternal_education_level`) | What is the highest level of school you attended? | `0` = No education<br>`1` = Primary<br>`2` = Secondary<br>`3` = Higher (Tertiary) |
| **B4** | `v133` (`maternal_education_years`) | Total number of years of formal education completed | Integer (`0` to `25` years) |
| **B5** | `v155` (`maternal_literacy`) | Can you read a whole sentence or part of a sentence? | `0` = Cannot read at all<br>`1` = Able to read only parts of sentence<br>`2` = Able to read whole sentence<br>`3` = No card with required language<br>`4` = Blind/visually impaired |
| **B6** | `v130` (`religion`) | What is your religion? | `1` = Catholic<br>`2` = Other Christian<br>`3` = Islam<br>`4` = Traditionalist<br>`96` = Other |
| **B7** | `v131` (`ethnicity`) | What is your ethnic group? | Country-specific code (e.g., `1`–`370`, including Ibibio/Annang/Oron/Efik, Hausa, Yoruba, Igbo, Ijaw, etc.) |
| **B8** | `v501` (`marital_status_detailed`) | What is your current marital status? | `0` = Never in union<br>`1` = Married<br>`2` = Living with partner<br>`3` = Widowed<br>`4` = Divorced<br>`5` = No longer living together / separated |
| **B9** | `v502` (`marital_union_status`) | Grouped marital union status | `0` = Never in union<br>`1` = Currently in union/living with a man<br>`2` = Formerly in union/living with a man |
| **B10** | `v511` (`age_at_first_cohabitation`) | How old were you when you first started living with your (first) husband/partner? | Integer (`10` to `49` years; leave blank if never in union) |
| **B11** | `hv219` (`sex_of_head_of_household`) | What is the sex of the head of your household? | `1` = Male<br>`2` = Female |
| **B12** | `hv220` (`age_of_head_of_household`) | How old is the head of your household? | Integer (`15` to `95`+ years; `98` = Don't know) |

---

## SECTION C: SOCIOECONOMIC STATUS, AUTONOMY, MEDIA EXPOSURE & FOOD SECURITY

| Q# | Variable (`feature_name`) | Question / Field Prompt | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **C1** | `v190` (`wealth_index_quintile`) | Household Wealth Index Quintile | `1` = Poorest<br>`2` = Poorer<br>`3` = Middle<br>`4` = Richer<br>`5` = Richest |
| **C2** | `v191` (`wealth_index_factor_score`) | Household Wealth Index Factor Score (5 decimals) | Continuous integer score (e.g., `-250000` to `+250000`) |
| **C3** | `v190a` (`wealth_index_urban_rural_quintile`) | Urban/Rural-Specific Wealth Index Quintile | `1` = Poorest, `2` = Poorer, `3` = Middle, `4` = Richer, `5` = Richest |
| **C4** | `v714` (`maternal_currently_working`) | Aside from your own housework, have you done any work in the last 7 days? | `0` = No<br>`1` = Yes |
| **C5** | `v717` (`maternal_occupation_group`) | What is your occupation (what kind of work do you mainly do)? | `0` = Not working<br>`1` = Professional / technical / managerial<br>`2` = Clerical<br>`3` = Sales<br>`4` = Agricultural - self employed<br>`5` = Agricultural - employee<br>`6` = Household and domestic<br>`7` = Services<br>`8` = Skilled manual<br>`9` = Unskilled manual<br>`96` = Other |
| **C6** | `v701` (`partner_education_level`) | What is your husband/partner's highest level of education? | `0` = No education<br>`1` = Primary<br>`2` = Secondary<br>`3` = Higher<br>`8` = Don't know |
| **C7** | `v715` (`partner_education_years`) | Husband/partner's total number of years of education | Integer (`0` to `25`; `98` = Don't know) |
| **C8** | `v705` (`partner_occupation_group`) | Husband/partner's occupation group | Same codes as `v717` (`0` to `9`, `96`, `98` = Don't know) |
| **C9** | `v730` (`partner_age_years`) | How old is your husband/partner? | Integer (`15` to `95` years; `98` = Don't know) |
| **C10** | `v743a` (`decision_maker_maternal_healthcare`) | Who usually makes decisions about health care for yourself? | `1` = Respondent alone<br>`2` = Respondent and husband/partner jointly<br>`3` = Husband/partner alone<br>`4` = Someone else<br>`5` = Other |
| **C11** | `v157` (`media_newspaper_frequency`) | How often do you read a newspaper or magazine? | `0` = Not at all<br>`1` = Less than once a week<br>`2` = At least once a week |
| **C12** | `v158` (`media_radio_frequency`) | How often do you listen to the radio? | `0` = Not at all<br>`1` = Less than once a week<br>`2` = At least once a week |
| **C13** | `v159` (`media_tv_frequency`) | How often do you watch television? | `0` = Not at all<br>`1` = Less than once a week<br>`2` = At least once a week |
| **C14** | `v169a` (`owns_mobile_phone`) | Do you own a mobile phone? | `0` = No<br>`1` = Yes |
| **C15** | `v171a` (`use_of_internet`) | Have you ever used the internet? | `0` = Never<br>`1` = Yes, last 12 months<br>`2` = Yes, before last 12 months |
| **C16** | `hfs1` (`fies_worried_not_enough_food`) | *(Past 12 months)* Were you worried you would not have enough food to eat because of a lack of money or other resources? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **C17** | `hfs2` (`fies_unable_to_eat_healthy_nutritious_food`) | *(Past 12 months)* Were you unable to eat healthy and nutritious food because of a lack of money? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **C18** | `hfs3` (`fies_ate_only_a_few_kinds_of_foods`) | *(Past 12 months)* Did you eat only a few kinds of foods because of a lack of money? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **C19** | `hfs4` (`fies_had_to_skip_a_meal`) | *(Past 12 months)* Did you have to skip a meal because there was not enough money or resources to get food? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **C20** | `hfs5` (`fies_ate_less_than_thought_should`) | *(Past 12 months)* Did you eat less than you thought you should because of a lack of money? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **C21** | `hfs6` (`fies_household_ran_out_of_food`) | *(Past 12 months)* Did your household run out of food because of a lack of money? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **C22** | `hfs7` (`fies_hungry_but_did_not_eat`) | *(Past 12 months)* Were you hungry but did not eat because there was not enough money for food? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **C23** | `hfs8` (`fies_went_without_eating_for_whole_day`) | *(Past 12 months)* Did you go without eating for a whole day because of a lack of money? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **C24** | `hfs_mod` (`household_moderate_or_severe_food_insecurity_prob`) | Household Probability of Moderate or Severe Food Insecurity (FIES scaled 0–100) | Integer (`0` to `100`) |
| **C25** | `hfs_sev` (`household_severe_food_insecurity_prob`) | Household Probability of Severe Food Insecurity (FIES scaled 0–100) | Integer (`0` to `100`) |

---

## SECTION D: HOUSEHOLD & ENVIRONMENTAL RISK FACTORS (MOSQUITO BREEDING & HOUSING QUALITY)

| Q# | Variable (`feature_name`) | Question / Field Prompt | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **D1** | `v113` (`drinking_water_source`) | What is the main source of drinking water for members of your household? | `11`=Piped into dwelling, `12`=Piped to yard/plot, `13`=Piped to neighbor, `14`=Public tap/standpipe, `21`=Tube well or borehole, `31`=Protected well, `32`=Unprotected well, `41`=Protected spring, `42`=Unprotected spring, `43`=River/dam/lake/ponds/stream/canal, `51`=Rainwater, `61`=Tanker truck, `62`=Cart with small tank, `71`=Bottled water, `72`=Sachet water ("pure water"), `96`=Other |
| **D2** | `v115` (`time_to_water_source_mins`) | How long does it take to go to your water source, get water, and come back? | Minutes (`0` to `900`), `996` = On premises, `998` = Don't know |
| **D3** | `hv237` (`anything_done_to_water_to_make_safe_to_drink`) | Do you do anything to your water to make it safer to drink? | `0` = No, `1` = Yes, `8` = Don't know |
| **D4** | `v116` (`toilet_facility_type`) | What kind of toilet facility do members of your household usually use? | `11`=Flush to piped sewer, `12`=Flush to septic tank, `13`=Flush to pit latrine, `14`=Flush to somewhere else, `21`=Ventilated Improved Pit (VIP) latrine, `22`=Pit latrine with slab, `23`=Pit latrine without slab / open pit, `31`=No facility / bush / field, `41`=Composting toilet, `42`=Bucket toilet, `43`=Hanging toilet/latrine, `96`=Other |
| **D5** | `v160` (`toilet_shared_with_other_households`) | Do you share this toilet facility with other households? | `0` = No, `1` = Yes |
| **D6** | `v119` (`household_has_electricity`) | Does your household have electricity? | `0` = No, `1` = Yes |
| **D7** | `v127` (`main_floor_material`) | Main material of the dwelling floor | `11`=Earth/sand, `12`=Dung, `21`=Wood planks, `22`=Palm/bamboo, `31`=Parquet/polished wood, `32`=Vinyl/asphalt strips, `33`=Ceramic tiles, `34`=Cement, `35`=Carpet, `96`=Other |
| **D8** | `v128` (`main_wall_material`) | Main material of the exterior walls | `11`=No walls, `12`=Cane/palm/trunks, `13`=Dirt/mud, `21`=Bamboo with mud, `22`=Stone with mud, `23`=Uncovered adobe, `24`=Plywood, `25`=Cardboard, `26`=Reused wood, `31`=Cement, `32`=Stone with lime/cement, `33`=Bricks, `34`=Cement blocks, `35`=Covered adobe, `36`=Wood planks/shingles, `96`=Other |
| **D9** | `v129` (`main_roof_material`) | Main material of the roof | `11`=No roof, `12`=Thatch/palm leaf, `21`=Rustic mat, `22`=Palm/bamboo, `23`=Wood planks, `24`=Cardboard, `31`=Metal / Zinc / Corrugated iron, `32`=Wood, `33`=Calamine/cement fiber, `34`=Ceramic tiles, `35`=Cement, `36`=Roofing shingles, `96`=Other |
| **D10** | `v161` (`type_of_cooking_fuel`) | What type of fuel does your household mainly use for cooking? | `1`=Electricity, `2`=LPG/cooking gas, `3`=Natural gas, `4`=Biogas, `5`=Kerosene, `6`=Coal/lignite, `7`=Charcoal, `8`=Wood/firewood, `9`=Straw/shrubs/grass, `10`=Agricultural crop, `11`=Animal dung, `95`=No food cooked in household, `96`=Other |
| **D11** | `hv241` (`food_cooked_in_house_separate_building_outdoors`) | Is the cooking usually done in the house, in a separate building, or outdoors? | `1` = In the house<br>`2` = In a separate building<br>`3` = Outdoors<br>`6` = Other |
| **D12** | `v136` (`total_household_members`) | Total number of people living in the household | Integer (`1` to `50`) |
| **D13** | `v137` (`children_under_5_in_household`) | Number of children aged 5 and under in the household | Integer (`0` to `20`) |
| **D14** | `hv216` (`number_of_rooms_used_for_sleeping`) | How many rooms in this household are used for sleeping? | Integer (`1` to `25`) |
| **D15** | `hv230a` (`place_where_household_members_wash_hands`) | Place where household members most often wash their hands | `1`=Observed fixed place, `2`=Observed mobile place, `3`=Not observed: not in dwelling, `4`=Not observed: no permission, `5`=Not observed: other reason |
| **D16** | `hv230b` (`presence_of_water_at_handwashing_place`) | Presence of water at handwashing place | `0` = Water not available<br>`1` = Water is available |
| **D17** | `hv232` (`items_present_soap_or_detergent`) | Is soap or detergent present at the handwashing place? | `0` = No<br>`1` = Yes |
| **D18** | `hv246` (`household_owns_livestock_herds_or_farm_animals`) | Does this household own any livestock, herds, other farm animals, or poultry? | `0` = No<br>`1` = Yes |
| **D19** | `hv252` (`frequency_household_members_smoke_inside_house`) | How often does anyone smoke inside your house? | `0` = Never<br>`1` = Daily<br>`2` = Weekly<br>`3` = Monthly<br>`4` = Less than once a month |

---

## SECTION E: OBSTETRIC & PREGNANCY HISTORY

| Q# | Variable (`feature_name`) | Question / Field Prompt | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **E1** | `pord` (`pregnancy_order_number`) | What is the order number of this pregnancy (gravidity order)? | Integer (`1` = First pregnancy, `2` = Second, etc.) |
| **E2** | `is_primigravida` *(Engineered)* | Auto-derived from `pord`: Is this the woman's first pregnancy (Primigravida)? | `1` = Primigravida (`pord == 1`)<br>`0` = Multigravida (`pord > 1`) |
| **E3** | `v201` (`parity_total_children_ever_born`) | Total number of live-born children ever born to the woman | Integer (`0` to `20`) |
| **E4** | `v218` (`number_of_living_children`) | Total number of living children the woman currently has | Integer (`0` to `20`) |
| **E5** | `v212` (`age_at_first_birth`) | How old were you when you gave birth to your very first child? | Integer (`10` to `49` years) |
| **E6** | `v224` (`total_birth_history_entries`) | Total entries in live birth history | Integer (`0` to `20`) |
| **E7** | `v246` (`total_pregnancy_history_entries`) | Total number of pregnancies ever experienced (gravidity) | Integer (`1` to `25`) |
| **E8** | `v228` (`ever_had_terminated_pregnancy`) | Have you ever had a pregnancy that miscarried, was aborted, or ended in a stillbirth? | `0` = No<br>`1` = Yes |
| **E9** | `v245` (`number_of_pregnancy_losses`) | How many pregnancies in total have ended in miscarriage, abortion, or stillbirth? | Integer (`0` to `15`) |
| **E10** | `p0` (`multiple_or_twin_pregnancy`) | Was this pregnancy a single or multiple (twin/triplet) pregnancy? | `0` = Single pregnancy<br>`1` = 1st of multiple<br>`2` = 2nd of multiple<br>`3` = 3rd of multiple |
| **E11** | `p11` (`preceding_pregnancy_interval_months`) | How many months elapsed between the end of the previous pregnancy and the outcome of this pregnancy? | Integer in months (`2` to `300`; leave blank if 1st pregnancy) |
| **E12** | `p12` (`succeeding_pregnancy_interval_months`) | Months to next pregnancy (if any subsequent pregnancy occurred) | Integer in months (`2` to `300`; blank if most recent) |
| **E13** | `short_pregnancy_interval_under_24m` *(Engineered)* | Auto-derived from `p11` & `pord`: Was the preceding pregnancy interval `< 24` months? | `1` = Yes (`p11 < 24`)<br>`0` = No (`>= 24` months or 1st pregnancy) |
| **E14** | `m10` (`pregnancy_wantedness`) | When you got pregnant with this pregnancy, did you want to get pregnant then, later, or not at all? | `1` = Wanted then<br>`2` = Wanted later<br>`3` = Wanted no more |
| **E15** | `v213` (`currently_pregnant`) | Are you currently pregnant at the time of interview? | `0` = No or unsure<br>`1` = Yes |
| **E16** | `v214` (`current_pregnancy_duration_months`) | If currently pregnant, how many months pregnant are you? | Integer (`1` to `10` months) |
| **E17** | `v401` (`last_birth_caesarean_section`) | Was your most recent birth delivered by caesarean section (C-section)? | `0` = No<br>`1` = Yes |
| **E18** | `m17` (`delivery_by_caesarean_section`) | Was THIS specific pregnancy delivered by caesarean section? | `0` = No<br>`1` = Yes |
| **E19** | `p1` (`month_of_pregnancy_outcome`) | In which calendar month did this pregnancy end? | `1`=Jan, `2`=Feb, `3`=Mar, `4`=Apr, `5`=May, `6`=Jun, `7`=Jul, `8`=Aug, `9`=Sep, `10`=Oct, `11`=Nov, `12`=Dec |
| **E20** | `p2` (`year_of_pregnancy_outcome`) | In which calendar year did this pregnancy end? | Integer (e.g., `2021` to `2026`) |
| **E21** | `p3` (`date_of_pregnancy_outcome_cmc`) | Century Month Code (CMC) of end of pregnancy: `(p2 - 1900) * 12 + p1` | Integer |
| **E22** | `p19` (`months_since_pregnancy_outcome`) | Months elapsed since the end of this pregnancy | Integer (`0` to `35` months) |
| **E23** | `p21` (`pregnancy_duration_coded`) | Reported duration of pregnancy (coded in weeks/months) | Integer (`100+` weeks or `201–210` months) |
| **E24** | `p4` (`sex_of_child`) | Sex of the baby (for live births) | `1` = Male<br>`2` = Female |
| **E25** | `p8` (`current_age_of_child_years`) | Current age of child in completed years (if alive) | Integer (`0` to `3` years) |
| **E26** | `pregnancy_outcome_rainy_season` *(Engineered)* | Auto-derived from `p1`: Did pregnancy end during the Nigerian rainy/peak malaria transmission season (April–October)? | `1` = Rainy season (`4 <= p1 <= 10`)<br>`0` = Dry season (`p1` in `1,2,3,11,12`) |

---

## SECTION F: ANTENATAL CARE (ANC) UTILIZATION, DELIVERY & HEALTHCARE ACCESS

| Q# | Variable (`feature_name`) | Question / Field Prompt | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **F1** | `m14` (`number_of_anc_visits`) | How many times did you receive antenatal care (ANC) during this pregnancy? | `0` = No ANC visits<br>`1` to `20` = Number of visits<br>`98` = Don't know |
| **F2** | `anc_4plus_visits` *(Engineered)* | Auto-derived from `m14`: Did the woman attend 4 or more ANC visits? | `1` = Yes (`4 <= m14 <= 90`)<br>`0` = No (`< 4` visits) |
| **F3** | `anc_8plus_visits` *(Engineered)* | Auto-derived from `m14`: Did the woman attend WHO-recommended 8 or more ANC contacts? | `1` = Yes (`8 <= m14 <= 90`)<br>`0` = No (`< 8` visits) |
| **F4** | `m13` (`timing_first_anc_visit_months`) | How many months pregnant were you when you first received antenatal care for this pregnancy? | Integer (`1` to `9` months; `98` = Don't know) |
| **F5** | `anc_first_trimester` *(Engineered)* | Auto-derived from `m13`: Was the first ANC check in the 1st trimester (`<= 3` months)? | `1` = Yes (`1 <= m13 <= 3`)<br>`0` = No (`> 3` months or no ANC) |
| **F6** | `m2a` (`anc_provider_doctor`) | Did you see a **Doctor** for antenatal care during this pregnancy? | `0` = No<br>`1` = Yes |
| **F7** | `m2b` (`anc_provider_nurse_midwife`) | Did you see a **Nurse or Midwife** for antenatal care? | `0` = No<br>`1` = Yes |
| **F8** | `m2c` (`anc_provider_chew`) | Did you see a **Community Health Extension Worker (CHEW)** for ANC? | `0` = No<br>`1` = Yes |
| **F9** | `m2g` (`anc_provider_traditional_birth_attendant`) | Did you see a **Traditional Birth Attendant (TBA)** for ANC? | `0` = No<br>`1` = Yes |
| **F10** | `m2h` (`anc_provider_auxiliary_midwife`) | Did you see an **Auxiliary Midwife** for ANC? | `0` = No<br>`1` = Yes |
| **F11** | `m2n` (`anc_provider_no_one`) | Did you receive antenatal care from **No One**? | `0` = Received some care<br>`1` = Yes, no care |
| **F12** | `anc_any_skilled_provider` *(Engineered)* | Auto-derived: Received ANC from a skilled provider (`m2a==1` or `m2b==1` or `m2h==1`)? | `1` = Yes<br>`0` = No |
| **F13** | `m1` (`tetanus_injections_before_birth`) | During this pregnancy, how many times did you get a tetanus injection? | `0` = None, `1`–`7` = Number of injections, `8` = Don't know |
| **F14** | `m1a` (`tetanus_injections_before_pregnancy`) | Prior to this pregnancy, how many times did you receive a tetanus injection? | `0` = None, `1`–`7` = Number of injections, `8` = Don't know |
| **F15** | `m45` (`iron_tablets_or_syrup_taken`) | During this pregnancy, were you given or did you buy any iron tablets or iron syrup? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **F16** | `m46` (`days_iron_tablets_or_syrup_taken`) | During the whole pregnancy, for how many days did you take the iron tablets or syrup? | `0` to `300` days; `998` = Don't know |
| **F17** | `m60` (`intestinal_parasite_drugs_during_pregnancy`) | During this pregnancy, did you take any drug for intestinal worms/parasites? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **F18** | `m42g` (`anc_counseled_on_nutrition`) | During ANC, did a healthcare provider talk to you about nutritious foods to eat? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **F19** | `m15` (`place_of_delivery`) | Where did you give birth / deliver this pregnancy? | `11`=Her home, `12`=Other home, `21`=Teaching hospital, `22`=Federal medical center, `23`=General hospital, `24`=Primary health care center (PHC), `25`=Primary health clinic, `26`=Health post, `27`=Other public sector, `31`=Private hospital, `32`=Private clinic, `33`=Pharmacy, `34`=PPMV (chemist), `35`=Private doctor, `36`=Mobile clinic, `37`=Maternity center, `41`=Faith-based hospital, `42`=Faith-based clinic, `96`=Other |
| **F20** | `m3a` (`delivery_assistance_doctor`) | Did a **Doctor** assist with the delivery? | `0` = No, `1` = Yes |
| **F21** | `m3b` (`delivery_assistance_nurse_midwife`) | Did a **Nurse/Midwife** assist with the delivery? | `0` = No, `1` = Yes |
| **F22** | `m3c` (`delivery_assistance_chew`) | Did a **Community Health Extension Worker (CHEW)** assist with the delivery? | `0` = No, `1` = Yes |
| **F23** | `m3g` (`delivery_assistance_tba`) | Did a **Traditional Birth Attendant (TBA)** assist with the delivery? | `0` = No, `1` = Yes |
| **F24** | `m3n` (`delivery_assistance_no_one`) | Did **No One** assist with the delivery? | `0` = Some assistance, `1` = No one assisted |
| **F25** | `v481` (`covered_by_health_insurance`) | Are you covered by any health insurance (e.g., NHIA/state health insurance)? | `0` = No<br>`1` = Yes |
| **F26** | `v483a` (`minutes_to_nearest_healthcare_facility`) | How many minutes does it take to reach the nearest healthcare facility from your home? | Integer in minutes (`0` to `600`) |
| **F27** | `v483b` (`mode_of_transport_to_healthcare_facility`) | What mode of transport do you use to reach the nearest health facility? | `11`=Car/truck, `12`=Public bus, `13`=Motorcycle/scooter (Okada), `14`=Boat with motor, `15`=Keke NAPEP (tricycle), `21`=Animal-drawn cart, `22`=Bicycle, `23`=Boat without motor, `31`=Walking, `96`=Other |
| **F28** | `v467b` (`barrier_getting_permission_to_go`) | When you are sick, is **getting permission to go** to the doctor a big problem? | `1` = Big problem<br>`2` = Not a big problem |
| **F29** | `v467c` (`barrier_getting_money_for_treatment`) | Is **getting money needed for advice or treatment** a big problem? | `1` = Big problem<br>`2` = Not a big problem |
| **F30** | `v467d` (`barrier_distance_to_health_facility`) | Is the **distance to the health facility** a big problem? | `1` = Big problem<br>`2` = Not a big problem |
| **F31** | `v467f` (`barrier_not_wanting_to_go_alone`) | Is **not wanting to go alone** a big problem? | `1` = Big problem<br>`2` = Not a big problem |

---

## SECTION G: MALARIA PROPHYLAXIS (IPTp-SP), VECTOR CONTROL (ITN/LLIN), EXPOSURE & FEVER/MALARIA DIAGNOSIS

| Q# | Variable (`feature_name`) | Question / Field Prompt | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **G1** | `m49a` (`malaria_iptp_sp_fansidar_during_pregnancy`) | During this pregnancy, did you take **SP / Fansidar** to keep you from getting malaria? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **G2** | `ml1` (`number_of_times_took_fansidar_iptp`) | How many times (doses) did you take SP / Fansidar during this pregnancy? | Integer (`0` to `90` doses; `98` = Don't know) |
| **G3** | `ml2` (`source_of_antimalarial_during_pregnancy`) | Where did you get the SP / Fansidar during pregnancy? | `1` = Antenatal (ANC) visit<br>`2` = Another health facility visit<br>`3` = Community Health Extension Worker (CHEW)<br>`6` = Other source (e.g., pharmacy/PPMV) |
| **G4** | `malaria_iptp_sp_taken` *(Engineered)* | Auto-derived binary indicator of SP/Fansidar prophylaxis (`m49a`) | `1` = Yes<br>`0` = No |
| **G5** | `malaria_iptp_doses` *(Engineered)* | Auto-derived IPTp-SP dose count (`0` if `m49a == 0`, else `ml1`) | Integer (`0` to `90`) |
| **G6** | `malaria_iptp_optimal_3plus` *(Engineered)* | Auto-derived: Did the woman take the WHO-recommended `>= 3` doses of IPTp-SP? | `1` = Yes (`>= 3` doses)<br>`0` = No (`< 3` doses) |
| **G7** | `v459` (`household_has_mosquito_bed_net`) | Does your household have any mosquito nets that can be used while sleeping? | `0` = No<br>`1` = Yes |
| **G8** | `hml1` (`number_of_mosquito_bed_nets_in_hh`) | How many mosquito bed nets does your household own? | Integer (`0` to `25`) |
| **G9** | `v461` (`maternal_slept_under_mosquito_net`) | Did you (the mother) sleep under a mosquito bed net last night? | `0` = No<br>`1` = Yes |
| **G10** | `ml101` (`maternal_type_of_mosquito_bed_net`) | What type of mosquito bed net did you sleep under last night? | `0` = No net<br>`1` = Only insecticide-treated nets (ITN)<br>`2` = Both treated and untreated nets<br>`3` = Only untreated nets |
| **G11** | `hml10` (`net_used_was_insecticide_treated_itn`) | Was the specific mosquito net used an Insecticide-Treated Net (ITN)? | `0` = No / Don't know<br>`1` = Yes (ITN) |
| **G12** | `hml11` (`number_of_persons_who_slept_under_this_net`) | How many people slept under this mosquito net last night? | Integer (`1` to `8`) |
| **G13** | `hml12` (`person_type_of_mosquito_bed_net_slept_under`) | Household Roster Member Net Type | `0` = Did not sleep under a net<br>`1` = Only treated (ITN) nets<br>`2` = Both treated and untreated<br>`3` = Only untreated nets |
| **G14** | `hml19` (`person_slept_under_ever_treated_net`) | Slept under an ever-treated net | `0` = No<br>`1` = Yes |
| **G15** | `hml20` (`person_slept_under_llin_net`) | Did you sleep under a **Long-Lasting Insecticidal Net (LLIN)** last night? | `0` = No<br>`1` = Yes |
| **G16** | `malaria_itn_slept_last_night` *(Engineered)* | Auto-derived: Did the woman sleep under an ITN (`ml101 in (1,2)` or `hml12 in (1,2)`)? | `1` = Yes (ITN)<br>`0` = No |
| **G17** | `malaria_llin_slept_last_night` *(Engineered)* | Auto-derived: Did the woman sleep under an LLIN (`hml20 == 1`)? | `1` = Yes (LLIN)<br>`0` = No |
| **G18** | `malaria_unprotected_in_pregnancy` *(Engineered)* | Auto-derived: Was the woman unprotected against malaria (neither optimal 3+ IPTp-SP nor ITN)? | `1` = Unprotected (`malaria_iptp_optimal_3plus==0` & `malaria_itn_slept_last_night==0`)<br>`0` = Protected |
| **G19** | `v460` (`children_under_5_slept_under_bed_net`) | Did children under age 5 in the household sleep under a mosquito net last night? | `0` = No<br>`1` = All children<br>`2` = Some children<br>`3` = No net in household |
| **G20** | `ml0` (`child_slept_under_mosquito_net_type`) | Type of mosquito net THIS child slept under last night | `0` = No net, `1` = Only treated nets, `2` = Both, `3` = Only untreated nets |
| **G21** | `ml501` (`seen_or_heard_malaria_messages_last_6m`) | In the past 6 months, have you seen or heard any messages about malaria? | `0` = No<br>`1` = Yes |
| **G22** | `ml501a`–`ml501i` (`malaria_msg_source_*`) | Where did you hear or see malaria messages? *(Check each source: `0` = No, `1` = Yes)* | `ml501a` = Radio<br>`ml501b` = Television<br>`ml501c` = Poster / Billboard<br>`ml501f` = Healthcare Provider<br>`ml501g` = Community Health Worker<br>`ml501h` = Social Media<br>`ml501i` = Family / Friends / Neighbors |
| **G23** | `ml503` (`knows_ways_to_avoid_getting_malaria`) | Are there ways to avoid getting malaria? | `0` = No<br>`1` = Yes |
| **G24** | `ml503a`–`ml503h` (`prevent_malaria_*`) | What are the ways to prevent malaria? *(Check each: `0` = No, `1` = Yes, `8` = Don't know)* | `ml503a` = Sleep under a mosquito net<br>`ml503b` = Sleep under an insecticide-treated net (ITN)<br>`ml503c` = Use mosquito repellent<br>`ml503d` = Take preventive medications<br>`ml503e` = Spray house with insecticide<br>`ml503f` = Fill in stagnant waters<br>`ml503g` = Keep surroundings clean<br>`ml503h` = Put mosquito screen on windows |
| **G25** | `ml505` (`community_gets_malaria_in_rainy_season_perception`) | Do you agree or disagree: *"Almost every week during the rainy season, people in this community get malaria"*? | `0` = Disagree<br>`1` = Agree<br>`8` = Don't know / Uncertain |
| **G26** | `ml506` (`worries_child_fever_is_malaria`) | Agree/disagree: *"When a child has a fever, you almost always worry it might be malaria"*? | `0` = Disagree, `1` = Agree, `8` = Don't know |
| **G27** | `ml507` (`believes_malaria_not_problem_as_treatable`) | Agree/disagree: *"Getting malaria is not a problem because it can be easily treated"*? | `0` = Disagree, `1` = Agree, `8` = Don't know |
| **G28** | `ml508` (`believes_only_weak_children_die_from_malaria`) | Agree/disagree: *"Only weak children can die from malaria"*? | `0` = Disagree, `1` = Agree, `8` = Don't know |
| **G29** | `ml509` (`sleeps_under_net_when_lots_of_mosquitoes`) | Agree/disagree: *"You only sleep under a net when there are lots of mosquitoes"*? | `0` = Disagree, `1` = Agree, `8` = Don't know |
| **G30** | `ml510` (`sleeps_under_net_when_few_mosquitoes`) | Agree/disagree: *"You still sleep under a net even when there are few mosquitoes"*? | `0` = Disagree, `1` = Agree, `8` = Don't know |
| **G31** | `ml511` (`dislikes_sleeping_in_net_when_too_warm`) | Agree/disagree: *"You do not like sleeping under a mosquito net when the weather is too warm"*? | `0` = Disagree, `1` = Agree, `8` = Don't know |
| **G32** | `ml512` (`gives_home_medicine_first_when_child_has_fever`) | Agree/disagree: *"When a child has a fever, it is best to start by giving any medicine you have at home"*? | `0` = Disagree, `1` = Agree, `8` = Don't know |
| **G33** | `ml513` (`community_takes_febrile_child_same_day`) | In your community, do most people take children with fever to a health provider on the same or next day? | `0` = Disagree / Less than half<br>`1` = Agree / More than half<br>`8` = Don't know |
| **G34** | `ml514` (`community_sleeps_under_nets_every_night`) | In your community, do most people who have nets sleep under them every night? | `0` = Disagree / Less than half<br>`1` = Agree / More than half<br>`8` = Don't know |
| **G35** | `h22` (`child_fever_last_2_weeks`) | Has the child had an illness with a **fever** at any time in the last 2 weeks? | `0` = No, `1` = Yes, `8` = Don't know |
| **G36** | `h32z` (`child_fever_cough_medical_treatment`) | Was advice or treatment sought from a medical facility/provider for the fever? | `0` = No, `1` = Yes |
| **G37** | `h47` (`child_blood_taken_from_finger_heel_for_testing`) | At any time during the illness, did the child have **blood taken from a finger or heel** for malaria testing (RDT/microscopy)? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **G38** | `h71` (`told_child_had_malaria_diagnosis`) | Were you told by a healthcare provider that the **child had malaria**? | `0` = No<br>`1` = Yes<br>`8` = Don't know |
| **G39** | `h37a`–`h37h` (`child_took_*_for_fever`) | Which antimalarial drug was given for the fever/malaria? *(Code each: `0` = No, `1` = Yes, `8` = Don't know)* | `h37a` = SP / Fansidar<br>`h37b` = Chloroquine<br>`h37c` = Amodiaquine<br>`h37d` = Quinine (pills)<br>`h37da` = Quinine (injection / IV)<br>`h37e` = **Artemisinin-based Combination Therapy (ACT)**<br>`h37f` = Artesunate (rectal)<br>`h37g` = Artesunate (injection / IV)<br>`h37h` = Other antimalarial |

---

## SECTION H: CLINICAL SCREENING, ANTHROPOMETRY, BIOMARKERS & COMORBIDITIES

| Q# | Variable (`feature_name`) | Question / Field Prompt | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **H1** | `m42c` (`anc_blood_pressure_taken`) | During ANC for this pregnancy, did a healthcare provider **measure your blood pressure**? | `0` = No, `1` = Yes, `8` = Don't know |
| **H2** | `m42d` (`anc_urine_sample_taken`) | During ANC, did a healthcare provider **take a urine sample**? | `0` = No, `1` = Yes, `8` = Don't know |
| **H3** | `m42e` (`anc_blood_sample_taken`) | During ANC, did a healthcare provider **take a blood sample** (for malaria/Hb/screening)? | `0` = No, `1` = Yes, `8` = Don't know |
| **H4** | `m42f` (`anc_listened_to_baby_heartbeat`) | During ANC, did a healthcare provider **listen to the baby's heartbeat**? | `0` = No, `1` = Yes, `8` = Don't know |
| **H5** | `m42i` (`anc_asked_about_vaginal_bleeding`) | During ANC, did a healthcare provider **ask if you had vaginal bleeding**? | `0` = No, `1` = Yes, `8` = Don't know |
| **H6** | `v176` (`self_reported_health_status`) | In general, how would you rate your own health status? | `1` = Very good<br>`2` = Good<br>`3` = Moderate<br>`4` = Bad<br>`5` = Very bad |
| **H7** | `v437` (`maternal_weight_kg_1dec`) | Maternal Weight in kilograms (1 decimal implied, e.g., `62.5 kg` entered as `625`) | Integer (`300` to `1800`) |
| **H8** | `v438` (`maternal_height_cm_1dec`) | Maternal Height in centimeters (1 decimal implied, e.g., `160.5 cm` entered as `1605`) | Integer (`1200` to `2000`) |
| **H9** | `v445` / `ha40` (`maternal_bmi_2dec`) | Maternal Body Mass Index (2 decimals implied, e.g., `22.45` entered as `2245`) | Integer (`1200` to `6000`) |
| **H10** | `maternal_bmi_kg_m2` *(Engineered)* | Maternal BMI in standard `kg/m2` (`v445 / 100.0`) | Decimal (e.g., `22.45`) |
| **H11** | `maternal_underweight_bmi_under_18_5` *(Engineered)* | Is the mother clinically underweight (`BMI < 18.5 kg/m2`)? | `1` = Underweight (`< 18.5`)<br>`0` = Normal/Overweight (`>= 18.5`) |
| **H12** | `v453` / `ha53` (`maternal_hemoglobin_g_dl_1dec`) | Unadjusted Maternal Hemoglobin level (`g/dL`, 1 decimal implied, e.g., `10.8 g/dL` -> `108`) | Integer (`30` to `200`) |
| **H13** | `v455` (`result_of_hemoglobin_measurement`) | Hemoglobin measurement completion status | `0` = Measured, `3` = Not present, `4` = Refused, `6` = Other |
| **H14** | `v456` / `v456a` / `ha56` (`maternal_hemoglobin_altitude_smoking_adj`) | Altitude & smoking-adjusted Maternal Hemoglobin (`g/dL` x 10, e.g., `10.5` -> `105`) | Integer (`30` to `200`) |
| **H15** | `maternal_hemoglobin_g_dl` *(Engineered)* | Maternal Hemoglobin in standard `g/dL` (`v456 / 10.0`) | Decimal (e.g., `10.5`) |
| **H16** | `v463a` (`maternal_smokes_cigarettes`) | Do you currently smoke cigarettes? | `0` = No, `1` = Yes |
| **H17** | `v463z` (`maternal_does_not_use_tobacco`) | Do you abstain from all tobacco products? | `0` = Uses tobacco, `1` = Yes, smokes/uses nothing |
| **H18** | `chd01` (`ever_had_blood_pressure_measured`) | Have you ever had your blood pressure measured by a doctor or healthcare worker? | `0` = No, `1` = Yes, `8` = Don't know |
| **H19** | `chd02` (`ever_told_has_high_blood_pressure_hypertension`) | Have you ever been told by a doctor/health worker that you have **high blood pressure or hypertension**? | `0` = No<br>`1` = Yes |
| **H20** | `chd03` (`told_high_bp_in_last_12_months`) | In the past 12 months, were you told you have high blood pressure/hypertension? | `0` = No, `1` = Yes |
| **H21** | `chd04` (`prescribed_medication_for_high_bp`) | Have you been prescribed medication to control high blood pressure? | `0` = No, `1` = Yes |
| **H22** | `chd05` (`currently_taking_medication_for_high_bp`) | Are you currently taking medication to control your blood pressure? | `0` = No, `1` = Yes |
| **H23** | `chd06` (`ever_had_blood_sugar_measured`) | Have you ever had your blood sugar measured by a doctor or healthcare worker? | `0` = No, `1` = Yes, `8` = Don't know |
| **H24** | `chd07` (`ever_told_has_high_blood_sugar_diabetes`) | Have you ever been told by a doctor/health worker that you have **high blood sugar or diabetes**? | `0` = No<br>`1` = Yes |
| **H25** | `chd08` (`told_high_blood_sugar_in_last_12_months`) | In the past 12 months, were you told you have high blood sugar or diabetes? | `0` = No, `1` = Yes |
| **H26** | `chd09` (`prescribed_medication_for_diabetes`) | Have you been prescribed medication to control high blood sugar / diabetes? | `0` = No, `1` = Yes |
| **H27** | `chd10` (`currently_taking_medication_for_diabetes`) | Are you currently taking medication to control your blood sugar / diabetes? | `0` = No, `1` = Yes |
| **H28** | `s1112ga` (`tested_for_hepatitis_b_during_anc`) | During ANC for this pregnancy, were you tested for **Hepatitis B**? | `0` = No, `1` = Yes, `8` = Don't know |
| **H29** | `s1112ha` (`hepatitis_b_test_result_anc`) | What was the result of your ANC **Hepatitis B** test? | `0` = Negative, `1` = Positive, `5` = Not tested, `8` = Don't know |
| **H30** | `s1112gb` (`tested_for_hepatitis_c_during_anc`) | During ANC for this pregnancy, were you tested for **Hepatitis C**? | `0` = No, `1` = Yes, `8` = Don't know |
| **H31** | `s1112hb` (`hepatitis_c_test_result_anc`) | What was the result of your ANC **Hepatitis C** test? | `0` = Negative, `1` = Positive, `5` = Not tested, `8` = Don't know |
| **H32** | `s1112b` / `s1112c` (`ever_tested_for_hepatitis_b` / `result_of_hepatitis_b_test`) | Lifetime Hepatitis B testing (`0`=No, `1`=Yes) and result (`0`=Negative, `1`=Positive, `8`=DK) | Binary / Categorical |
| **H33** | `s1112eb` / `s1112ec` (`tested_for_hepatitis_c_last_12m` / `result_of_hepatitis_c_test`) | Past 12m Hepatitis C testing (`0`=No, `1`=Yes) and result (`0`=Negative, `1`=Positive, `8`=DK) | Binary / Categorical |
| **H34** | `v781` (`ever_been_tested_for_hiv`) | Have you ever been tested for **HIV**? | `0` = No, `1` = Yes |
| **H35** | `v840` (`tested_for_hiv_as_part_of_anc_visit`) | Were you tested for HIV as part of an antenatal care visit? | `0` = No, `1` = Yes |
| **H36** | `v840a` (`tested_for_hiv_prior_to_delivery`) | Were you tested for HIV between going for delivery and before the baby was born? | `0` = No, `1` = Yes |
| **H37** | `v841` (`got_results_of_hiv_test_at_anc`) | Did you get the results of your ANC HIV test? | `0` = No, `1` = Yes |
| **H38** | `v861` (`result_of_last_hiv_test`) | What was the result of your most recent HIV test? | `1` = Positive<br>`2` = Negative<br>`3` = Indeterminate<br>`4` = Declined to answer<br>`5` = Did not receive result |
| **H39** | `v863` (`currently_taking_arv_daily`) | If HIV-positive, are you currently taking antiretroviral (ARV) medicines daily? | `0` = No, `1` = Yes, `8` = Don't know |
| **H40** | `fi1` / `fi2` (`currently_experiences_obstetric_fistula_leakage` / `ever_experienced_obstetric_fistula_leakage`) | Experience of constant leakage of urine or stool from vagina (Obstetric Fistula) | `0` = No, `1` = Yes |
| **H41** | `s473aa` / `s473ab` (`postpartum_feeling_nervous_anxious` / `postpartum_feeling_depressed_hopeless`) | During first 2 days after delivery, felt nervous/anxious (`s473aa`) or depressed/hopeless (`s473ab`)? | `0` = No, `1` = Yes, `8` = Don't know |
| **H42** | `d104` / `d106` / `d107` / `d108` (`experienced_any_*_violence`) | History of intimate partner violence: Emotional (`d104`), Less severe physical (`d106`), Severe physical (`d107`), Sexual (`d108`) | `0` = No, `1` = Yes |
| **H43** | `d118y` (`did_not_experience_physical_violence_during_pregnancy`) | Did anyone hit, slap, kick, or physically hurt you **while you were pregnant**? | `0` = Yes (Someone hurt respondent during pregnancy)<br>`1` = No (No one hurt respondent during pregnancy) |
| **H44** | `h31` / `h11` (`child_cough_last_2_weeks` / `child_diarrhea_last_2_weeks`) | Child had cough (`h31`) or diarrhea (`h11`) in last 2 weeks | `0` = No, `1`/`2` = Yes, `8` = Don't know |
| **H45** | `hw53` / `hw56` (`child_hemoglobin_*`) | Child Hemoglobin (`g/dL` x 10, unadjusted `hw53` and altitude-adjusted `hw56`) | Integer (`25` to `180`) |
| **H46** | `hw70` / `hw71` / `hw72` (`child_*_zscore_who`) | Child WHO Growth Z-scores x 100: Height-for-Age (`hw70`), Weight-for-Age (`hw71`), Weight-for-Height (`hw72`) | Integer (`-600` to `+600`) |

---

## SECTION I: PREGNANCY & MATERNAL OUTCOMES (TARGET VARIABLES FOR EBM MODELING)

| Q# | Variable (`feature_name`) | Outcome Question / Clinical Endpoint | Response Options & Exact Dataset Codes |
| :--- | :--- | :--- | :--- |
| **I1** | `p30` (`pregnancy_outcome_declared`) | Pregnancy outcome declared by respondent | `1` = Born alive<br>`2` = Born dead (Stillbirth)<br>`3` = Miscarriage<br>`4` = Induced abortion |
| **I2** | `p31` (`baby_cried_moved_or_breathed`) | If declared born dead (`p30 == 2`), did the baby cry, move, or breathe at birth? | `0` = No (Confirmed stillbirth)<br>`1` = Yes (Reclassified to live birth) |
| **I3** | `p32` (`pregnancy_outcome_reclassified`) | **Final Reclassified Pregnancy Outcome** | `1` = Born alive (Live birth)<br>`2` = Born dead (Stillbirth, `>= 7` months)<br>`3` = Miscarriage (`< 7` months spontaneous loss)<br>`4` = Abortion |
| **I4** | `m80` (`pregnancy_outcome_section_status`) | Pregnancy outcome status for ANC/Maternal Health module | `1` = Most recent live birth<br>`2` = Prior live birth<br>`3` = Most recent stillbirth<br>`4` = Prior stillbirth<br>`5` = Miscarriage / abortion |
| **I5** | `p20` (`pregnancy_duration_months`) | **Duration of Pregnancy (Gestational Age at Outcome in Months)** | Integer (`1` to `10` months; `< 9` months = Preterm / Early Termination) |
| **I6** | `m19` (`birth_weight_grams_3dec`) | **Infant Birth Weight in Grams** (e.g., `2.400 kg` entered as `2400`) | `500` to `6500` grams (`< 2500` = Low Birth Weight)<br>`9996` = Not weighed at birth<br>`9998` = Don't know |
| **I7** | `birth_weight_kg` *(Engineered)* | Infant Birth Weight in Kilograms (`m19 / 1000.0`) | Decimal in kg (e.g., `2.400`; `< 2.500` = LBW) |
| **I8** | `m19a` (`birth_weight_source_card_or_recall`) | Source of birth weight record | `0` = Not weighed<br>`1` = From written health card<br>`2` = From mother's recall<br>`8` = Don't know |
| **I9** | `m18` (`child_size_at_birth`) | When the child was born, was he/she very large, larger than average, average, smaller than average, or very small? | `1` = Very large<br>`2` = Larger than average<br>`3` = Average<br>`4` = **Smaller than average**<br>`5` = **Very small**<br>`8` = Don't know |
| **I10** | `p5` (`child_is_alive`) | Is the child currently alive? | `0` = No (Deceased)<br>`1` = Yes (Alive) |
| **I11** | `p6` (`child_age_at_death_coded`) | If deceased (`p5 == 0`), how old was the child when he/she died? | `100` = Died on day of birth (Day 0)<br>`101`–`130` = Died at `1`–`30` days (**Neonatal Death**)<br>`201`–`223` = Died at `1`–`23` months<br>`301`+ = Died in years |
| **I12** | `p7` (`child_age_at_death_months_imputed`) | Imputed age at death in completed months | Integer (`0` to `35` months) |
| **I13** | `v457` / `v457a` / `ha57` (`maternal_anemia_level`) | **Maternal Anemia Severity Level** | `1` = **Severe anemia**<br>`2` = **Moderate anemia**<br>`3` = **Mild anemia**<br>`4` = Not anemic |
| **I14** | `hw57` / `hw57a` (`child_anemia_level`) | **Child Anemia Severity Level** | `1` = Severe, `2` = Moderate, `3` = Mild, `4` = Not anemic |
| **I15** | `target_stillbirth` *(Target 1)* | **Binary Target: Stillbirth** (`p32 == 2`) | `1` = Stillbirth, `0` = Otherwise |
| **I16** | `target_pregnancy_loss` *(Target 2)* | **Binary Target: Any Pregnancy Loss** (`p32 in (2, 3, 4)`) | `1` = Pregnancy loss (Stillbirth/Miscarriage/Abortion), `0` = Live birth |
| **I17** | `target_preterm_birth` *(Target 3)* | **Binary Target: Preterm Birth / Early Termination** (`p20 < 9` months) | `1` = Preterm (`< 9` months), `0` = Full term (`>= 9` months) |
| **I18** | `target_preterm_delivery` *(Target 4)* | **Binary Target: Preterm Delivery** (`p32 in (1, 2)` and `p20 < 9`) | `1` = Preterm delivery, `0` = Term delivery |
| **I19** | `target_lbw_measured` *(Target 5)* | **Binary Target: Measured Low Birth Weight** (`m19 < 2500`g among weighed babies) | `1` = LBW (`< 2500`g), `0` = Normal weight (`>= 2500`g) |
| **I20** | `target_low_birth_weight_or_small_size` *(Target 6)* | **Binary Target: Low Birth Weight or Small Size at Birth** (`m19 < 2500`g OR `m18 in (4, 5)`) | `1` = LBW or Small/Very small size, `0` = Normal/Large |
| **I21** | `target_neonatal_death` *(Target 7)* | **Binary Target: Neonatal Mortality** (`p32 == 1`, `p5 == 0`, `100 <= p6 <= 130`) | `1` = Neonatal death (`0–30` days), `0` = Survived neonatal period |
| **I22** | `target_perinatal_mortality` *(Target 8)* | **Binary Target: Perinatal Mortality** (`p32 == 2` OR early neonatal death `100 <= p6 <= 107`) | `1` = Perinatal death, `0` = Survived perinatal period |
| **I23** | `target_maternal_anemia` *(Target 9)* | **Binary Target: Maternal Anemia** (`v457 in (1, 2, 3)`) | `1` = Anemic (Mild/Moderate/Severe), `0` = Not anemic (`v457 == 4`) |
| **I24** | `target_maternal_moderate_severe_anemia` *(Target 10)* | **Binary Target: Moderate or Severe Maternal Anemia** (`v457 in (1, 2)`) | `1` = Moderate/Severe anemia, `0` = Mild or Not anemic |
| **I25** | `target_any_adverse_pregnancy_outcome` *(Primary Composite Target)* | **Primary Composite Target: Any Fetal/Neonatal Adverse Pregnancy Outcome** (Pregnancy loss/Stillbirth, Preterm `<9m`, LBW `<2500g`/Small size, or Neonatal death) | `1` = Adverse Pregnancy Outcome occurred<br>`0` = Healthy full-term normal-weight surviving birth |
| **I26** | `target_any_apo_or_maternal_anemia` *(Extended Composite Target)* | **Extended Composite Target: Any Fetal/Neonatal Adverse Outcome OR Maternal Anemia** | `1` = Any APO or Maternal Anemia<br>`0` = No APO & Not Anemic |
