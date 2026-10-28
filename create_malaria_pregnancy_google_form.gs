/**
 * ============================================================================
 * GOOGLE FORMS AUTO-GENERATOR FOR MALARIA IN PREGNANCY & APO EBM RESEARCH
 * ============================================================================
 * Research Title: A Predictive Model of Adverse Pregnancy Outcomes Among
 *                 Malaria-Infected Pregnant Women in Resource-Constrained
 *                 Settings using Explainable Boosting Machine (EBM)
 * Researcher:     Akpan Divine Eteyen (AK22/PHS/CSC/002)
 *                 Department of Computer Science, Akwa Ibom State University
 *
 * HOW TO GENERATE YOUR LIVE GOOGLE FORM LINK IN 60 SECONDS:
 * 1. Go to https://script.google.com and sign in with your Google Account.
 * 2. Click "New project" (top-left).
 * 3. Delete any default code in the editor and paste this ENTIRE file.
 * 4. Click "Save" (Ctrl+S), ensure `createMalariaPregnancyGoogleForm` is
 *    selected in the top toolbar dropdown, and click "Run".
 * 5. Grant permissions when prompted ("Review permissions" -> "Advanced" ->
 *    "Go to Untitled project (unsafe)" -> "Allow").
 * 6. Wait ~45-60 seconds. Your live Google Form Link (short link + full link),
 *    Edit Link, and Linked Google Sheet Link will be printed in the
 *    Execution Log at the bottom of the screen!
 * ============================================================================
 */

function createMalariaPregnancyGoogleForm() {
  Logger.log("Starting creation of the Malaria in Pregnancy & Adverse Pregnancy Outcomes (EBM) Google Form...");

  var formTitle = "Clinical & Field Questionnaire: Malaria in Pregnancy & Adverse Pregnancy Outcomes (EBM Study)";
  var formDescription =
    "Research Study: A Predictive Model of Adverse Pregnancy Outcomes Among Malaria-Infected Pregnant Women in Resource-Constrained Settings using Explainable Boosting Machine (EBM)\n" +
    "Researcher: Akpan Divine Eteyen (AK22/PHS/CSC/002) — Department of Computer Science, Akwa Ibom State University\n\n" +
    "INSTRUCTIONS: Every question is mapped 1-to-1 with the EBM training dataset (merged_malaria_pregnancy_outcomes_dataset.csv). " +
    "Each option begins with its exact numerical dataset code (e.g., '1 = Yes', '0 = No') so responses can be fed directly into the Explainable Boosting Machine model.";

  var form = FormApp.create(formTitle);
  form.setDescription(formDescription)
      .setConfirmationMessage("Thank you! Your clinical/field questionnaire response has been recorded for the Malaria in Pregnancy EBM Predictive Study.")
      .setAllowResponseEdits(true)
      .setCollectEmail(false)
      .setProgressBar(true);

  // Helper functions for fast item creation
  function addText(code, feature, prompt, helpText, required) {
    var item = form.addTextItem();
    item.setTitle("[" + code + "] " + prompt + " (" + feature + ")");
    if (helpText) item.setHelpText(helpText);
    item.setRequired(!!required);
  }

  function addNumber(code, feature, prompt, minVal, maxVal, helpText, required) {
    var item = form.addTextItem();
    item.setTitle("[" + code + "] " + prompt + " (" + feature + ")");
    if (helpText) item.setHelpText(helpText);
    item.setRequired(!!required);
    if (minVal !== null && maxVal !== null) {
      var validation = FormApp.createTextValidation()
        .setHelpText("Please enter a valid number between " + minVal + " and " + maxVal + ".")
        .requireNumberBetween(minVal, maxVal)
        .build();
      item.setValidation(validation);
    } else {
      var numValidation = FormApp.createTextValidation()
        .setHelpText("Please enter a numeric value.")
        .requireNumber()
        .build();
      item.setValidation(numValidation);
    }
  }

  function addMC(code, feature, prompt, choices, helpText, required) {
    var item = form.addMultipleChoiceItem();
    item.setTitle("[" + code + "] " + prompt + " (" + feature + ")");
    if (helpText) item.setHelpText(helpText);
    item.setChoiceValues(choices);
    item.setRequired(!!required);
  }

  function addDropdown(code, feature, prompt, choices, helpText, required) {
    var item = form.addListItem();
    item.setTitle("[" + code + "] " + prompt + " (" + feature + ")");
    if (helpText) item.setHelpText(helpText);
    item.setChoiceValues(choices);
    item.setRequired(!!required);
  }

  var YES_NO = ["0 = No", "1 = Yes"];
  var YES_NO_DK = ["0 = No", "1 = Yes", "8 = Don't know"];
  var AGREE_DISAGREE_DK = ["0 = Disagree", "1 = Agree", "8 = Don't know / Uncertain"];

  // ==========================================================================
  // SECTION A: IDENTIFICATION, GEOGRAPHIC LOCATION & SURVEY METADATA
  // ==========================================================================
  form.addSectionHeaderItem()
      .setTitle("SECTION A: Identification, Geographic Location & Survey Metadata")
      .setHelpText("Patient/Respondent ID, geopolitical zone, state of residence, and urban/rural classification.");

  addText("caseid", "woman_case_id", "A1. Respondent / Patient Unique Identification Code", "Alphanumeric ID (e.g., AK22-0001)", true);
  addNumber("pidx", "pregnancy_column_index", "A2. Pregnancy Episode Index (for this respondent)", 1, 15, "1 = Most recent pregnancy, 2 = Prior pregnancy, etc.", true);
  addNumber("pidxb", "index_to_birth_history", "A3. Live Birth History Index", 0, 20, "Enter 0 if pregnancy ended in non-live termination (stillbirth/miscarriage/abortion); 1, 2, ... for live birth index", false);
  addNumber("v001", "cluster_number", "A4. Community / Health Facility Cluster Number", 1, 9999, "Cluster or facility code (1 to 1400)", false);
  addNumber("v002", "household_number", "A5. Household Number within Cluster", 1, 9999, "Integer (1 to 500)", false);
  addNumber("v003", "respondent_line_number", "A6. Woman's Line Number in Household Roster", 1, 50, "Integer (1 to 50)", false);
  addNumber("p16", "child_line_number_in_household", "A7. Child's Line Number in Household Roster (if live-born and living in household)", 0, 50, "0 = Not in household / deceased; 1..50 = Line number", false);
  addDropdown("v006", "interview_month", "A9. Month of Interview / Clinical Assessment", [
    "1 = January", "2 = February", "3 = March", "4 = April", "5 = May", "6 = June",
    "7 = July", "8 = August", "9 = September", "10 = October", "11 = November", "12 = December"
  ], null, true);
  addNumber("v007", "interview_year", "A10. Year of Interview / Clinical Assessment", 2020, 2030, "e.g., 2024 or 2026", true);
  addDropdown("v024", "geopolitical_zone", "A12. In which geopolitical zone of Nigeria does the respondent reside?", [
    "1 = North Central",
    "2 = North East",
    "3 = North West",
    "4 = South East",
    "5 = South South (Study Focus Zone)",
    "6 = South West"
  ], null, true);
  addDropdown("sstate", "state_code", "A13. State of Residence in Nigeria", [
    "30 = Akwa Ibom (Study Focus State)",
    "29 = Cross River", "33 = Rivers", "34 = Bayelsa", "35 = Delta", "25 = Edo",
    "1 = Sokoto", "2 = Zamfara", "3 = Katsina", "4 = Jigawa", "5 = Yobe", "6 = Borno",
    "7 = Adamawa", "8 = Gombe", "9 = Bauchi", "10 = Kano", "11 = Kaduna", "12 = Kebbi",
    "13 = Niger", "14 = FCT Abuja", "15 = Nasarawa", "16 = Plateau", "17 = Taraba",
    "18 = Benue", "19 = Kogi", "20 = Kwara", "21 = Oyo", "22 = Osun", "23 = Ekiti",
    "24 = Ondo", "26 = Anambra", "27 = Enugu", "28 = Ebonyi", "31 = Abia", "32 = Imo",
    "36 = Lagos", "37 = Ogun"
  ], null, true);
  addMC("v025", "residence_urban_rural", "A14. Type of place of residence", ["1 = Urban", "2 = Rural"], null, true);
  addNumber("v040", "cluster_altitude_meters", "A15. Community / Cluster Altitude (in meters above sea level)", 0, 3000, "e.g., 15 to 1300 meters (leave blank if unknown)", false);

  Logger.log("Section A created.");

  // ==========================================================================
  // SECTION B: MATERNAL SOCIO-DEMOGRAPHIC CHARACTERISTICS
  // ==========================================================================
  form.addPageBreakItem()
      .setTitle("SECTION B: Maternal Socio-Demographic Characteristics")
      .setHelpText("Maternal age, education, literacy, religion, ethnicity, marital status, and household head demographics.");

  addNumber("v012", "maternal_age_years", "B1. How old are you in completed years?", 15, 49, "Enter age in years (15 to 49)", true);
  addDropdown("v013", "maternal_age_group_5yr", "B2. Maternal Age Group (5-year intervals)", [
    "1 = 15-19", "2 = 20-24", "3 = 25-29", "4 = 30-34", "5 = 35-39", "6 = 40-44", "7 = 45-49"
  ], null, true);
  addMC("v106", "maternal_education_level", "B3. What is the highest level of school you attended?", [
    "0 = No education", "1 = Primary", "2 = Secondary", "3 = Higher (Tertiary)"
  ], null, true);
  addNumber("v133", "maternal_education_years", "B4. Total number of years of formal education completed", 0, 25, "Enter 0 to 25 years", true);
  addDropdown("v155", "maternal_literacy", "B5. Can you read a whole sentence or part of a sentence?", [
    "0 = Cannot read at all",
    "1 = Able to read only parts of sentence",
    "2 = Able to read whole sentence",
    "3 = No card with required language",
    "4 = Blind/visually impaired"
  ], null, true);
  addDropdown("v130", "religion", "B6. What is your religion?", [
    "1 = Catholic", "2 = Other Christian", "3 = Islam", "4 = Traditionalist", "96 = Other"
  ], null, true);
  addText("v131", "ethnicity", "B7. What is your ethnic group code/name?", "Enter ethnic group code (1-370) or ethnic group (e.g., Ibibio, Annang, Oron, Efik, Igbo, Yoruba, Hausa)", false);
  addDropdown("v501", "marital_status_detailed", "B8. What is your current marital status?", [
    "0 = Never in union",
    "1 = Married",
    "2 = Living with partner",
    "3 = Widowed",
    "4 = Divorced",
    "5 = No longer living together / separated"
  ], null, true);
  addMC("v502", "marital_union_status", "B9. Grouped marital union status", [
    "0 = Never in union",
    "1 = Currently in union/living with a man",
    "2 = Formerly in union/living with a man"
  ], null, true);
  addNumber("v511", "age_at_first_cohabitation", "B10. How old were you when you first started living with your (first) husband/partner?", 10, 49, "Leave blank if never in union", false);
  addMC("hv219", "sex_of_head_of_household", "B11. What is the sex of the head of your household?", ["1 = Male", "2 = Female"], null, true);
  addNumber("hv220", "age_of_head_of_household", "B12. How old is the head of your household?", 15, 99, "Enter age in years (98 = Don't know)", false);

  Logger.log("Section B created.");

  // ==========================================================================
  // SECTION C: SOCIOECONOMIC STATUS, AUTONOMY, MEDIA EXPOSURE & FOOD SECURITY
  // ==========================================================================
  form.addPageBreakItem()
      .setTitle("SECTION C: Socioeconomic Status, Autonomy, Media Exposure & Food Security")
      .setHelpText("Household wealth index, occupation, partner education, healthcare autonomy, media access, and FIES food insecurity.");

  addMC("v190", "wealth_index_quintile", "C1. Household Wealth Index Quintile", [
    "1 = Poorest", "2 = Poorer", "3 = Middle", "4 = Richer", "5 = Richest"
  ], null, true);
  addNumber("v191", "wealth_index_factor_score", "C2. Household Wealth Index Factor Score (optional, 5 decimals)", null, null, "Leave blank if using quintile only", false);
  addDropdown("v190a", "wealth_index_urban_rural_quintile", "C3. Urban/Rural-Specific Wealth Index Quintile", [
    "1 = Poorest", "2 = Poorer", "3 = Middle", "4 = Richer", "5 = Richest"
  ], null, false);
  addMC("v714", "maternal_currently_working", "C4. Aside from your own housework, have you done any work in the last 7 days?", YES_NO, null, true);
  addDropdown("v717", "maternal_occupation_group", "C5. What is your occupation (what kind of work do you mainly do)?", [
    "0 = Not working",
    "1 = Professional / technical / managerial",
    "2 = Clerical",
    "3 = Sales",
    "4 = Agricultural - self employed",
    "5 = Agricultural - employee",
    "6 = Household and domestic",
    "7 = Services",
    "8 = Skilled manual",
    "9 = Unskilled manual",
    "96 = Other"
  ], null, true);
  addDropdown("v701", "partner_education_level", "C6. What is your husband/partner's highest level of education?", [
    "0 = No education", "1 = Primary", "2 = Secondary", "3 = Higher", "8 = Don't know"
  ], null, false);
  addNumber("v715", "partner_education_years", "C7. Husband/partner's total number of years of education", 0, 98, "0 to 25 years (98 = Don't know)", false);
  addDropdown("v705", "partner_occupation_group", "C8. Husband/partner's occupation group", [
    "0 = Not working",
    "1 = Professional / technical / managerial",
    "2 = Clerical",
    "3 = Sales",
    "4 = Agricultural - self employed",
    "5 = Agricultural - employee",
    "6 = Household and domestic",
    "7 = Services",
    "8 = Skilled manual",
    "9 = Unskilled manual",
    "96 = Other",
    "98 = Don't know"
  ], null, false);
  addNumber("v730", "partner_age_years", "C9. How old is your husband/partner?", 15, 98, "15 to 95 years (98 = Don't know)", false);
  addDropdown("v743a", "decision_maker_maternal_healthcare", "C10. Who usually makes decisions about health care for yourself?", [
    "1 = Respondent alone",
    "2 = Respondent and husband/partner jointly",
    "3 = Husband/partner alone",
    "4 = Someone else",
    "5 = Other"
  ], null, false);
  addMC("v157", "media_newspaper_frequency", "C11. How often do you read a newspaper or magazine?", [
    "0 = Not at all", "1 = Less than once a week", "2 = At least once a week"
  ], null, true);
  addMC("v158", "media_radio_frequency", "C12. How often do you listen to the radio?", [
    "0 = Not at all", "1 = Less than once a week", "2 = At least once a week"
  ], null, true);
  addMC("v159", "media_tv_frequency", "C13. How often do you watch television?", [
    "0 = Not at all", "1 = Less than once a week", "2 = At least once a week"
  ], null, true);
  addMC("v169a", "owns_mobile_phone", "C14. Do you own a mobile phone?", YES_NO, null, true);
  addMC("v171a", "use_of_internet", "C15. Have you ever used the internet?", [
    "0 = Never", "1 = Yes, last 12 months", "2 = Yes, before last 12 months"
  ], null, true);
  addMC("hfs1", "fies_worried_not_enough_food", "C16. (Past 12 months) Were you worried you would not have enough food to eat because of a lack of money or other resources?", YES_NO_DK, null, true);
  addMC("hfs2", "fies_unable_to_eat_healthy_nutritious_food", "C17. (Past 12 months) Were you unable to eat healthy and nutritious food because of a lack of money?", YES_NO_DK, null, true);
  addMC("hfs3", "fies_ate_only_a_few_kinds_of_foods", "C18. (Past 12 months) Did you eat only a few kinds of foods because of a lack of money?", YES_NO_DK, null, true);
  addMC("hfs4", "fies_had_to_skip_a_meal", "C19. (Past 12 months) Did you have to skip a meal because there was not enough money or resources to get food?", YES_NO_DK, null, true);
  addMC("hfs5", "fies_ate_less_than_thought_should", "C20. (Past 12 months) Did you eat less than you thought you should because of a lack of money?", YES_NO_DK, null, true);
  addMC("hfs6", "fies_household_ran_out_of_food", "C21. (Past 12 months) Did your household run out of food because of a lack of money?", YES_NO_DK, null, true);
  addMC("hfs7", "fies_hungry_but_did_not_eat", "C22. (Past 12 months) Were you hungry but did not eat because there was not enough money for food?", YES_NO_DK, null, true);
  addMC("hfs8", "fies_went_without_eating_for_whole_day", "C23. (Past 12 months) Did you go without eating for a whole day because of a lack of money?", YES_NO_DK, null, true);
  addNumber("hfs_mod", "household_moderate_or_severe_food_insecurity_prob", "C24. Household Probability of Moderate or Severe Food Insecurity (FIES scaled 0-100)", 0, 100, "Enter 0 to 100", false);
  addNumber("hfs_sev", "household_severe_food_insecurity_prob", "C25. Household Probability of Severe Food Insecurity (FIES scaled 0-100)", 0, 100, "Enter 0 to 100", false);

  Logger.log("Section C created.");

  // ==========================================================================
  // SECTION D: HOUSEHOLD & ENVIRONMENTAL RISK FACTORS
  // ==========================================================================
  form.addPageBreakItem()
      .setTitle("SECTION D: Household & Environmental Risk Factors (Mosquito Breeding & Housing Quality)")
      .setHelpText("Water source, sanitation, housing construction materials, cooking fuel, crowding, and hygiene.");

  addDropdown("v113", "drinking_water_source", "D1. What is the main source of drinking water for members of your household?", [
    "11 = Piped into dwelling", "12 = Piped to yard/plot", "13 = Piped to neighbor",
    "14 = Public tap/standpipe", "21 = Tube well or borehole", "31 = Protected well",
    "32 = Unprotected well", "41 = Protected spring", "42 = Unprotected spring",
    "43 = River/dam/lake/ponds/stream/canal", "51 = Rainwater", "61 = Tanker truck",
    "62 = Cart with small tank", "71 = Bottled water", "72 = Sachet water ('pure water')", "96 = Other"
  ], null, true);
  addNumber("v115", "time_to_water_source_mins", "D2. How long does it take to go to your water source, get water, and come back (in minutes)?", 0, 998, "Enter minutes (0-900), 996 = On premises, 998 = Don't know", true);
  addMC("hv237", "anything_done_to_water_to_make_safe_to_drink", "D3. Do you do anything to your water to make it safer to drink?", YES_NO_DK, null, true);
  addDropdown("v116", "toilet_facility_type", "D4. What kind of toilet facility do members of your household usually use?", [
    "11 = Flush to piped sewer", "12 = Flush to septic tank", "13 = Flush to pit latrine",
    "14 = Flush to somewhere else", "21 = Ventilated Improved Pit (VIP) latrine",
    "22 = Pit latrine with slab", "23 = Pit latrine without slab / open pit",
    "31 = No facility / bush / field", "41 = Composting toilet", "42 = Bucket toilet",
    "43 = Hanging toilet/latrine", "96 = Other"
  ], null, true);
  addMC("v160", "toilet_shared_with_other_households", "D5. Do you share this toilet facility with other households?", YES_NO, null, false);
  addMC("v119", "household_has_electricity", "D6. Does your household have electricity?", YES_NO, null, true);
  addDropdown("v127", "main_floor_material", "D7. Main material of the dwelling floor", [
    "11 = Earth/sand", "12 = Dung", "21 = Wood planks", "22 = Palm/bamboo",
    "31 = Parquet/polished wood", "32 = Vinyl/asphalt strips", "33 = Ceramic tiles",
    "34 = Cement", "35 = Carpet", "96 = Other"
  ], null, true);
  addDropdown("v128", "main_wall_material", "D8. Main material of the exterior walls", [
    "11 = No walls", "12 = Cane/palm/trunks", "13 = Dirt/mud", "21 = Bamboo with mud",
    "22 = Stone with mud", "23 = Uncovered adobe", "24 = Plywood", "25 = Cardboard",
    "26 = Reused wood", "31 = Cement", "32 = Stone with lime/cement", "33 = Bricks",
    "34 = Cement blocks", "35 = Covered adobe", "36 = Wood planks/shingles", "96 = Other"
  ], null, true);
  addDropdown("v129", "main_roof_material", "D9. Main material of the roof", [
    "11 = No roof", "12 = Thatch/palm leaf", "21 = Rustic mat", "22 = Palm/bamboo",
    "23 = Wood planks", "24 = Cardboard", "31 = Metal / Zinc / Corrugated iron",
    "32 = Wood", "33 = Calamine/cement fiber", "34 = Ceramic tiles", "35 = Cement",
    "36 = Roofing shingles", "96 = Other"
  ], null, true);
  addDropdown("v161", "type_of_cooking_fuel", "D10. What type of fuel does your household mainly use for cooking?", [
    "1 = Electricity", "2 = LPG/cooking gas", "3 = Natural gas", "4 = Biogas",
    "5 = Kerosene", "6 = Coal/lignite", "7 = Charcoal", "8 = Wood/firewood",
    "9 = Straw/shrubs/grass", "10 = Agricultural crop", "11 = Animal dung",
    "95 = No food cooked in household", "96 = Other"
  ], null, true);
  addMC("hv241", "food_cooked_in_house_separate_building_outdoors", "D11. Is the cooking usually done in the house, in a separate building, or outdoors?", [
    "1 = In the house", "2 = In a separate building", "3 = Outdoors", "6 = Other"
  ], null, false);
  addNumber("v136", "total_household_members", "D12. Total number of people living in the household", 1, 50, "Integer (1 to 50)", true);
  addNumber("v137", "children_under_5_in_household", "D13. Number of children aged 5 and under in the household", 0, 20, "Integer (0 to 20)", true);
  addNumber("hv216", "number_of_rooms_used_for_sleeping", "D14. How many rooms in this household are used for sleeping?", 1, 25, "Integer (1 to 25)", true);
  addDropdown("hv230a", "place_where_household_members_wash_hands", "D15. Place where household members most often wash their hands", [
    "1 = Observed fixed place", "2 = Observed mobile place",
    "3 = Not observed: not in dwelling", "4 = Not observed: no permission", "5 = Not observed: other reason"
  ], null, false);
  addMC("hv230b", "presence_of_water_at_handwashing_place", "D16. Presence of water at handwashing place", [
    "0 = Water not available", "1 = Water is available"
  ], null, false);
  addMC("hv232", "items_present_soap_or_detergent", "D17. Is soap or detergent present at the handwashing place?", YES_NO, null, false);
  addMC("hv246", "household_owns_livestock_herds_or_farm_animals", "D18. Does this household own any livestock, herds, other farm animals, or poultry?", YES_NO, null, true);
  addDropdown("hv252", "frequency_household_members_smoke_inside_house", "D19. How often does anyone smoke inside your house?", [
    "0 = Never", "1 = Daily", "2 = Weekly", "3 = Monthly", "4 = Less than once a month"
  ], null, true);

  Logger.log("Section D created.");

  // ==========================================================================
  // SECTION E: OBSTETRIC & PREGNANCY HISTORY
  // ==========================================================================
  form.addPageBreakItem()
      .setTitle("SECTION E: Obstetric & Pregnancy History")
      .setHelpText("Gravidity, parity, prior pregnancy losses, multiple pregnancy, birth intervals, C-section, and season of pregnancy outcome.");

  addNumber("pord", "pregnancy_order_number", "E1. What is the order number of this pregnancy (gravidity order)?", 1, 25, "1 = First pregnancy (Primigravida), 2 = Second pregnancy, etc.", true);
  addNumber("v201", "parity_total_children_ever_born", "E3. Total number of live-born children ever born to the woman", 0, 20, "Integer (0 to 20)", true);
  addNumber("v218", "number_of_living_children", "E4. Total number of living children the woman currently has", 0, 20, "Integer (0 to 20)", true);
  addNumber("v212", "age_at_first_birth", "E5. How old were you when you gave birth to your very first child?", 10, 49, "Leave blank if no prior live birth", false);
  addNumber("v224", "total_birth_history_entries", "E6. Total entries in live birth history", 0, 20, "Integer (0 to 20)", false);
  addNumber("v246", "total_pregnancy_history_entries", "E7. Total number of pregnancies ever experienced (gravidity)", 1, 25, "Integer (1 to 25)", true);
  addMC("v228", "ever_had_terminated_pregnancy", "E8. Have you ever had a pregnancy that miscarried, was aborted, or ended in a stillbirth?", YES_NO, null, true);
  addNumber("v245", "number_of_pregnancy_losses", "E9. How many pregnancies in total have ended in miscarriage, abortion, or stillbirth?", 0, 15, "Integer (0 to 15)", true);
  addMC("p0", "multiple_or_twin_pregnancy", "E10. Was this pregnancy a single or multiple (twin/triplet) pregnancy?", [
    "0 = Single pregnancy", "1 = 1st of multiple", "2 = 2nd of multiple", "3 = 3rd of multiple"
  ], null, true);
  addNumber("p11", "preceding_pregnancy_interval_months", "E11. How many months elapsed between the end of the previous pregnancy and the outcome of this pregnancy?", 2, 300, "Leave blank if 1st pregnancy", false);
  addNumber("p12", "succeeding_pregnancy_interval_months", "E12. Months to next pregnancy (if any subsequent pregnancy occurred)", 2, 300, "Leave blank if most recent pregnancy", false);
  addMC("m10", "pregnancy_wantedness", "E14. When you got pregnant with this pregnancy, did you want to get pregnant then, later, or not at all?", [
    "1 = Wanted then", "2 = Wanted later", "3 = Wanted no more"
  ], null, false);
  addMC("v213", "currently_pregnant", "E15. Are you currently pregnant at the time of interview?", [
    "0 = No or unsure", "1 = Yes"
  ], null, true);
  addNumber("v214", "current_pregnancy_duration_months", "E16. If currently pregnant, how many months pregnant are you?", 1, 10, "Leave blank if not currently pregnant", false);
  addMC("v401", "last_birth_caesarean_section", "E17. Was your most recent birth delivered by caesarean section (C-section)?", YES_NO, null, false);
  addMC("m17", "delivery_by_caesarean_section", "E18. Was THIS specific pregnancy delivered by caesarean section?", YES_NO, null, false);
  addDropdown("p1", "month_of_pregnancy_outcome", "E19. In which calendar month did this pregnancy end?", [
    "1 = January", "2 = February", "3 = March", "4 = April (Rainy)", "5 = May (Rainy)", "6 = June (Rainy)",
    "7 = July (Rainy)", "8 = August (Rainy)", "9 = September (Rainy)", "10 = October (Rainy)", "11 = November", "12 = December"
  ], null, true);
  addNumber("p2", "year_of_pregnancy_outcome", "E20. In which calendar year did this pregnancy end?", 2020, 2030, "e.g., 2023, 2024, 2026", true);
  addNumber("p19", "months_since_pregnancy_outcome", "E22. Months elapsed since the end of this pregnancy", 0, 60, "0 to 35 months", false);
  addNumber("p21", "pregnancy_duration_coded", "E23. Reported duration of pregnancy (coded: 100+ weeks or 201-210 months)", 100, 212, "e.g., 209 for 9 months", false);
  addMC("p4", "sex_of_child", "E24. Sex of the baby (for live births)", ["1 = Male", "2 = Female"], "Leave blank if non-live termination", false);
  addNumber("p8", "current_age_of_child_years", "E25. Current age of child in completed years (if alive)", 0, 5, "0 to 3 years", false);

  Logger.log("Section E created.");

  // ==========================================================================
  // SECTION F: ANTENATAL CARE (ANC) UTILIZATION, DELIVERY & HEALTHCARE ACCESS
  // ==========================================================================
  form.addPageBreakItem()
      .setTitle("SECTION F: Antenatal Care (ANC) Utilization, Delivery & Healthcare Access")
      .setHelpText("Number and timing of ANC visits, ANC providers, iron/folate supplementation, intestinal deworming, tetanus, delivery place, and healthcare barriers.");

  addNumber("m14", "number_of_anc_visits", "F1. How many times did you receive antenatal care (ANC) during this pregnancy?", 0, 98, "0 = No ANC visits, 1 to 20 = Number of visits, 98 = Don't know", true);
  addNumber("m13", "timing_first_anc_visit_months", "F4. How many months pregnant were you when you first received antenatal care for this pregnancy?", 1, 98, "1 to 9 months (98 = Don't know; leave blank if 0 ANC visits)", false);
  addMC("m2a", "anc_provider_doctor", "F6. Did you see a DOCTOR for antenatal care during this pregnancy?", YES_NO, null, true);
  addMC("m2b", "anc_provider_nurse_midwife", "F7. Did you see a NURSE or MIDWIFE for antenatal care?", YES_NO, null, true);
  addMC("m2c", "anc_provider_chew", "F8. Did you see a COMMUNITY HEALTH EXTENSION WORKER (CHEW) for ANC?", YES_NO, null, true);
  addMC("m2g", "anc_provider_traditional_birth_attendant", "F9. Did you see a TRADITIONAL BIRTH ATTENDANT (TBA) for ANC?", YES_NO, null, true);
  addMC("m2h", "anc_provider_auxiliary_midwife", "F10. Did you see an AUXILIARY MIDWIFE for ANC?", YES_NO, null, true);
  addMC("m2n", "anc_provider_no_one", "F11. Did you receive antenatal care from NO ONE?", ["0 = Received some care", "1 = Yes, no care"], null, true);
  addNumber("m1", "tetanus_injections_before_birth", "F13. During this pregnancy, how many times did you get a tetanus injection?", 0, 8, "0 = None, 1-7 = Injections, 8 = Don't know", false);
  addNumber("m1a", "tetanus_injections_before_pregnancy", "F14. Prior to this pregnancy, how many times did you receive a tetanus injection?", 0, 8, "0 = None, 1-7 = Injections, 8 = Don't know", false);
  addMC("m45", "iron_tablets_or_syrup_taken", "F15. During this pregnancy, were you given or did you buy any iron tablets or iron syrup?", YES_NO_DK, null, true);
  addNumber("m46", "days_iron_tablets_or_syrup_taken", "F16. During the whole pregnancy, for how many days did you take the iron tablets or syrup?", 0, 998, "0 to 300 days (998 = Don't know)", false);
  addMC("m60", "intestinal_parasite_drugs_during_pregnancy", "F17. During this pregnancy, did you take any drug for intestinal worms/parasites?", YES_NO_DK, null, true);
  addMC("m42g", "anc_counseled_on_nutrition", "F18. During ANC, did a healthcare provider talk to you about nutritious foods to eat?", YES_NO_DK, null, false);
  addDropdown("m15", "place_of_delivery", "F19. Where did you give birth / deliver this pregnancy?", [
    "11 = Her home", "12 = Other home", "21 = Teaching hospital", "22 = Federal medical center",
    "23 = General hospital", "24 = Primary health care center (PHC)", "25 = Primary health clinic",
    "26 = Health post", "27 = Other public sector", "31 = Private hospital", "32 = Private clinic",
    "33 = Pharmacy", "34 = PPMV (chemist)", "35 = Private doctor", "36 = Mobile clinic",
    "37 = Maternity center", "41 = Faith-based hospital", "42 = Faith-based clinic", "96 = Other"
  ], null, false);
  addMC("m3a", "delivery_assistance_doctor", "F20. Did a DOCTOR assist with the delivery?", YES_NO, null, false);
  addMC("m3b", "delivery_assistance_nurse_midwife", "F21. Did a NURSE/MIDWIFE assist with the delivery?", YES_NO, null, false);
  addMC("m3c", "delivery_assistance_chew", "F22. Did a COMMUNITY HEALTH EXTENSION WORKER (CHEW) assist with the delivery?", YES_NO, null, false);
  addMC("m3g", "delivery_assistance_tba", "F23. Did a TRADITIONAL BIRTH ATTENDANT (TBA) assist with the delivery?", YES_NO, null, false);
  addMC("m3n", "delivery_assistance_no_one", "F24. Did NO ONE assist with the delivery?", ["0 = Some assistance", "1 = No one assisted"], null, false);
  addMC("v481", "covered_by_health_insurance", "F25. Are you covered by any health insurance (e.g., NHIA / State Health Insurance)?", YES_NO, null, true);
  addNumber("v483a", "minutes_to_nearest_healthcare_facility", "F26. How many minutes does it take to reach the nearest healthcare facility from your home?", 0, 600, "Enter minutes (0 to 600)", true);
  addDropdown("v483b", "mode_of_transport_to_healthcare_facility", "F27. What mode of transport do you use to reach the nearest health facility?", [
    "11 = Car/truck", "12 = Public bus", "13 = Motorcycle/scooter (Okada)", "14 = Boat with motor",
    "15 = Keke NAPEP (tricycle)", "21 = Animal-drawn cart", "22 = Bicycle", "23 = Boat without motor",
    "31 = Walking", "96 = Other"
  ], null, true);
  addMC("v467b", "barrier_getting_permission_to_go", "F28. When you are sick, is getting PERMISSION to go to the doctor a big problem?", ["1 = Big problem", "2 = Not a big problem"], null, true);
  addMC("v467c", "barrier_getting_money_for_treatment", "F29. Is getting MONEY needed for advice or treatment a big problem?", ["1 = Big problem", "2 = Not a big problem"], null, true);
  addMC("v467d", "barrier_distance_to_health_facility", "F30. Is the DISTANCE to the health facility a big problem?", ["1 = Big problem", "2 = Not a big problem"], null, true);
  addMC("v467f", "barrier_not_wanting_to_go_alone", "F31. Is NOT WANTING TO GO ALONE a big problem?", ["1 = Big problem", "2 = Not a big problem"], null, true);

  Logger.log("Section F created.");

  // ==========================================================================
  // SECTION G: MALARIA PROPHYLAXIS (IPTp-SP), VECTOR CONTROL (ITN/LLIN) & DIAGNOSIS
  // ==========================================================================
  form.addPageBreakItem()
      .setTitle("SECTION G: Malaria Prophylaxis (IPTp-SP), Vector Control (ITN/LLIN), Exposure & Diagnosis")
      .setHelpText("Intermittent Preventive Treatment in pregnancy with SP/Fansidar, ITN/LLIN mosquito net ownership and usage, malaria SBC perceptions, and fever/malaria testing & ACT treatment.");

  addMC("m49a", "malaria_iptp_sp_fansidar_during_pregnancy", "G1. During this pregnancy, did you take SP / Fansidar to keep you from getting malaria?", YES_NO_DK, null, true);
  addNumber("ml1", "number_of_times_took_fansidar_iptp", "G2. How many times (doses) did you take SP / Fansidar during this pregnancy?", 0, 98, "Enter 0 if none; 1 to 20 doses (98 = Don't know)", true);
  addDropdown("ml2", "source_of_antimalarial_during_pregnancy", "G3. Where did you get the SP / Fansidar during pregnancy?", [
    "1 = Antenatal (ANC) visit",
    "2 = Another health facility visit",
    "3 = Community Health Extension Worker (CHEW)",
    "6 = Other source (e.g., pharmacy/PPMV)"
  ], "Leave blank if SP/Fansidar was not taken", false);
  addMC("v459", "household_has_mosquito_bed_net", "G7. Does your household have any mosquito nets that can be used while sleeping?", YES_NO, null, true);
  addNumber("hml1", "number_of_mosquito_bed_nets_in_hh", "G8. How many mosquito bed nets does your household own?", 0, 25, "Enter 0 to 25", true);
  addMC("v461", "maternal_slept_under_mosquito_net", "G9. Did you (the mother) sleep under a mosquito bed net last night?", YES_NO, null, true);
  addDropdown("ml101", "maternal_type_of_mosquito_bed_net", "G10. What type of mosquito bed net did you sleep under last night?", [
    "0 = No net",
    "1 = Only insecticide-treated nets (ITN)",
    "2 = Both treated and untreated nets",
    "3 = Only untreated nets"
  ], null, true);
  addMC("hml10", "net_used_was_insecticide_treated_itn", "G11. Was the specific mosquito net used an Insecticide-Treated Net (ITN)?", ["0 = No / Don't know", "1 = Yes (ITN)"], null, true);
  addNumber("hml11", "number_of_persons_who_slept_under_this_net", "G12. How many people slept under this mosquito net last night?", 0, 10, "Enter 0 if no net used", false);
  addDropdown("hml12", "person_type_of_mosquito_bed_net_slept_under", "G13. Household Roster Member Net Type", [
    "0 = Did not sleep under a net",
    "1 = Only treated (ITN) nets",
    "2 = Both treated and untreated",
    "3 = Only untreated nets"
  ], null, false);
  addMC("hml19", "person_slept_under_ever_treated_net", "G14. Did you sleep under an ever-treated net?", YES_NO, null, false);
  addMC("hml20", "person_slept_under_llin_net", "G15. Did you sleep under a Long-Lasting Insecticidal Net (LLIN) last night?", YES_NO, null, true);
  addDropdown("v460", "children_under_5_slept_under_bed_net", "G19. Did children under age 5 in the household sleep under a mosquito net last night?", [
    "0 = No", "1 = All children", "2 = Some children", "3 = No net in household"
  ], null, false);
  addDropdown("ml0", "child_slept_under_mosquito_net_type", "G20. Type of mosquito net THIS child slept under last night", [
    "0 = No net", "1 = Only treated nets", "2 = Both", "3 = Only untreated nets"
  ], null, false);
  addMC("ml501", "seen_or_heard_malaria_messages_last_6m", "G21. In the past 6 months, have you seen or heard any messages about malaria?", YES_NO, null, true);
  addMC("ml501a", "malaria_msg_source_radio", "G22a. Heard malaria message on RADIO?", YES_NO, null, false);
  addMC("ml501b", "malaria_msg_source_tv", "G22b. Saw malaria message on TELEVISION?", YES_NO, null, false);
  addMC("ml501c", "malaria_msg_source_poster_billboard", "G22c. Saw malaria message on POSTER / BILLBOARD?", YES_NO, null, false);
  addMC("ml501f", "malaria_msg_source_healthcare_provider", "G22d. Heard malaria message from HEALTHCARE PROVIDER?", YES_NO, null, false);
  addMC("ml501g", "malaria_msg_source_community_health_worker", "G22e. Heard malaria message from COMMUNITY HEALTH WORKER?", YES_NO, null, false);
  addMC("ml501h", "malaria_msg_source_social_media", "G22f. Saw malaria message on SOCIAL MEDIA?", YES_NO, null, false);
  addMC("ml501i", "malaria_msg_source_family_friends", "G22g. Heard malaria message from FAMILY / FRIENDS / NEIGHBORS?", YES_NO, null, false);
  addMC("ml503", "knows_ways_to_avoid_getting_malaria", "G23. Are there ways to avoid getting malaria?", YES_NO, null, true);
  addMC("ml503a", "prevent_malaria_sleep_under_mosquito_net", "G24a. Way to avoid malaria: Sleep under a mosquito net?", YES_NO_DK, null, false);
  addMC("ml503b", "prevent_malaria_sleep_under_itn", "G24b. Way to avoid malaria: Sleep under an insecticide-treated net (ITN)?", YES_NO_DK, null, false);
  addMC("ml503c", "prevent_malaria_use_mosquito_repellent", "G24c. Way to avoid malaria: Use mosquito repellent?", YES_NO_DK, null, false);
  addMC("ml503d", "prevent_malaria_take_preventive_medication", "G24d. Way to avoid malaria: Take preventive medications?", YES_NO_DK, null, false);
  addMC("ml503e", "prevent_malaria_spray_house_with_insecticide", "G24e. Way to avoid malaria: Spray house with insecticide?", YES_NO_DK, null, false);
  addMC("ml503f", "prevent_malaria_fill_in_stagnant_water", "G24f. Way to avoid malaria: Fill in stagnant waters?", YES_NO_DK, null, false);
  addMC("ml503g", "prevent_malaria_keep_surroundings_clean", "G24g. Way to avoid malaria: Keep surroundings clean?", YES_NO_DK, null, false);
  addMC("ml503h", "prevent_malaria_put_mosquito_screen_on_windows", "G24h. Way to avoid malaria: Put mosquito screen on windows?", YES_NO_DK, null, false);
  addMC("ml505", "community_gets_malaria_in_rainy_season_perception", "G25. Do you agree or disagree: 'Almost every week during the rainy season, people in this community get malaria'?", AGREE_DISAGREE_DK, null, true);
  addMC("ml506", "worries_child_fever_is_malaria", "G26. Agree/disagree: 'When a child has a fever, you almost always worry it might be malaria'?", AGREE_DISAGREE_DK, null, false);
  addMC("ml507", "believes_malaria_not_problem_as_treatable", "G27. Agree/disagree: 'Getting malaria is not a problem because it can be easily treated'?", AGREE_DISAGREE_DK, null, false);
  addMC("ml508", "believes_only_weak_children_die_from_malaria", "G28. Agree/disagree: 'Only weak children can die from malaria'?", AGREE_DISAGREE_DK, null, false);
  addMC("ml509", "sleeps_under_net_when_lots_of_mosquitoes", "G29. Agree/disagree: 'You only sleep under a net when there are lots of mosquitoes'?", AGREE_DISAGREE_DK, null, false);
  addMC("ml510", "sleeps_under_net_when_few_mosquitoes", "G30. Agree/disagree: 'You still sleep under a net even when there are few mosquitoes'?", AGREE_DISAGREE_DK, null, false);
  addMC("ml511", "dislikes_sleeping_in_net_when_too_warm", "G31. Agree/disagree: 'You do not like sleeping under a mosquito net when the weather is too warm'?", AGREE_DISAGREE_DK, null, false);
  addMC("ml512", "gives_home_medicine_first_when_child_has_fever", "G32. Agree/disagree: 'When a child has a fever, it is best to start by giving any medicine you have at home'?", AGREE_DISAGREE_DK, null, false);
  addMC("ml513", "community_takes_febrile_child_same_day", "G33. In your community, do most people take children with fever to a health provider on the same or next day?", AGREE_DISAGREE_DK, null, false);
  addMC("ml514", "community_sleeps_under_nets_every_night", "G34. In your community, do most people who have nets sleep under them every night?", AGREE_DISAGREE_DK, null, false);
  addMC("h22", "child_fever_last_2_weeks", "G35. Has the child had an illness with a FEVER at any time in the last 2 weeks?", YES_NO_DK, null, false);
  addMC("h32z", "child_fever_cough_medical_treatment", "G36. Was advice or treatment sought from a medical facility/provider for the fever?", YES_NO, null, false);
  addMC("h47", "child_blood_taken_from_finger_heel_for_testing", "G37. Did the child have blood taken from a finger or heel for malaria testing (RDT/microscopy)?", YES_NO_DK, null, false);
  addMC("h71", "told_child_had_malaria_diagnosis", "G38. Were you told by a healthcare provider that the child had malaria?", YES_NO_DK, null, false);
  addMC("h37a", "child_took_sp_fansidar_for_fever", "G39a. Antimalarial taken for fever: SP / Fansidar?", YES_NO_DK, null, false);
  addMC("h37b", "child_took_chloroquine_for_fever", "G39b. Antimalarial taken for fever: Chloroquine?", YES_NO_DK, null, false);
  addMC("h37c", "child_took_amodiaquine_for_fever", "G39c. Antimalarial taken for fever: Amodiaquine?", YES_NO_DK, null, false);
  addMC("h37d", "child_took_quinine_pills_for_fever", "G39d. Antimalarial taken for fever: Quinine (pills)?", YES_NO_DK, null, false);
  addMC("h37da", "child_took_quinine_injection_iv_for_fever", "G39e. Antimalarial taken for fever: Quinine (injection / IV)?", YES_NO_DK, null, false);
  addMC("h37e", "child_took_act_for_fever", "G39f. Antimalarial taken for fever: Artemisinin-based Combination Therapy (ACT)?", YES_NO_DK, null, false);
  addMC("h37f", "child_took_artesunate_rectal_for_fever", "G39g. Antimalarial taken for fever: Artesunate (rectal)?", YES_NO_DK, null, false);
  addMC("h37g", "child_took_artesunate_injection_iv_for_fever", "G39h. Antimalarial taken for fever: Artesunate (injection / IV)?", YES_NO_DK, null, false);
  addMC("h37h", "child_took_other_antimalarial_for_fever", "G39i. Antimalarial taken for fever: Other antimalarial?", YES_NO_DK, null, false);

  Logger.log("Section G created.");

  // ==========================================================================
  // SECTION H: CLINICAL SCREENING, ANTHROPOMETRY, BIOMARKERS & COMORBIDITIES
  // ==========================================================================
  form.addPageBreakItem()
      .setTitle("SECTION H: Clinical Screening, Anthropometry, Biomarkers & Comorbidities")
      .setHelpText("ANC clinical checks, maternal weight/height/BMI, hemoglobin levels, hypertension, diabetes, Hepatitis B/C, HIV status, and intimate partner violence during pregnancy.");

  addMC("m42c", "anc_blood_pressure_taken", "H1. During ANC for this pregnancy, did a healthcare provider measure your BLOOD PRESSURE?", YES_NO_DK, null, true);
  addMC("m42d", "anc_urine_sample_taken", "H2. During ANC, did a healthcare provider take a URINE SAMPLE?", YES_NO_DK, null, true);
  addMC("m42e", "anc_blood_sample_taken", "H3. During ANC, did a healthcare provider take a BLOOD SAMPLE (for malaria/Hb/screening)?", YES_NO_DK, null, true);
  addMC("m42f", "anc_listened_to_baby_heartbeat", "H4. During ANC, did a healthcare provider listen to the BABY'S HEARTBEAT?", YES_NO_DK, null, true);
  addMC("m42i", "anc_asked_about_vaginal_bleeding", "H5. During ANC, did a healthcare provider ask if you had VAGINAL BLEEDING?", YES_NO_DK, null, true);
  addMC("v176", "self_reported_health_status", "H6. In general, how would you rate your own health status?", [
    "1 = Very good", "2 = Good", "3 = Moderate", "4 = Bad", "5 = Very bad"
  ], null, true);
  addNumber("v437", "maternal_weight_kg_1dec", "H7. Maternal Weight in kg x 10 (1 decimal implied, e.g., 62.5 kg -> enter 625)", 300, 1800, "Enter 300 to 1800", false);
  addNumber("v438", "maternal_height_cm_1dec", "H8. Maternal Height in cm x 10 (1 decimal implied, e.g., 160.5 cm -> enter 1605)", 1200, 2000, "Enter 1200 to 2000", false);
  addNumber("v445", "maternal_bmi_2dec", "H9. Maternal Body Mass Index x 100 (2 decimals implied, e.g., 22.45 -> enter 2245)", 1200, 6000, "Enter 1200 to 6000", false);
  addNumber("v453", "maternal_hemoglobin_g_dl_1dec", "H12. Unadjusted Maternal Hemoglobin level (g/dL x 10, e.g., 10.8 g/dL -> enter 108)", 30, 200, "Enter 30 to 200", false);
  addDropdown("v455", "result_of_hemoglobin_measurement", "H13. Hemoglobin measurement completion status", [
    "0 = Measured", "3 = Not present", "4 = Refused", "6 = Other"
  ], null, false);
  addNumber("v456", "maternal_hemoglobin_altitude_smoking_adj", "H14. Altitude & smoking-adjusted Maternal Hemoglobin (g/dL x 10, e.g., 10.5 -> enter 105)", 30, 200, "Enter 30 to 200", false);
  addMC("v463a", "maternal_smokes_cigarettes", "H16. Do you currently smoke cigarettes?", YES_NO, null, true);
  addMC("v463z", "maternal_does_not_use_tobacco", "H17. Do you abstain from all tobacco products?", ["0 = Uses tobacco", "1 = Yes, smokes/uses nothing"], null, true);
  addMC("chd01", "ever_had_blood_pressure_measured", "H18. Have you ever had your blood pressure measured by a doctor or healthcare worker?", YES_NO_DK, null, true);
  addMC("chd02", "ever_told_has_high_blood_pressure_hypertension", "H19. Have you ever been told by a doctor/health worker that you have HIGH BLOOD PRESSURE or HYPERTENSION?", YES_NO, null, true);
  addMC("chd03", "told_high_bp_in_last_12_months", "H20. In the past 12 months, were you told you have high blood pressure/hypertension?", YES_NO, null, false);
  addMC("chd04", "prescribed_medication_for_high_bp", "H21. Have you been prescribed medication to control high blood pressure?", YES_NO, null, false);
  addMC("chd05", "currently_taking_medication_for_high_bp", "H22. Are you currently taking medication to control your blood pressure?", YES_NO, null, false);
  addMC("chd06", "ever_had_blood_sugar_measured", "H23. Have you ever had your blood sugar measured by a doctor or healthcare worker?", YES_NO_DK, null, true);
  addMC("chd07", "ever_told_has_high_blood_sugar_diabetes", "H24. Have you ever been told by a doctor/health worker that you have HIGH BLOOD SUGAR or DIABETES?", YES_NO, null, true);
  addMC("chd08", "told_high_blood_sugar_in_last_12_months", "H25. In the past 12 months, were you told you have high blood sugar or diabetes?", YES_NO, null, false);
  addMC("chd09", "prescribed_medication_for_diabetes", "H26. Have you been prescribed medication to control high blood sugar / diabetes?", YES_NO, null, false);
  addMC("chd10", "currently_taking_medication_for_diabetes", "H27. Are you currently taking medication to control your blood sugar / diabetes?", YES_NO, null, false);
  addMC("s1112ga", "tested_for_hepatitis_b_during_anc", "H28. During ANC for this pregnancy, were you tested for HEPATITIS B?", YES_NO_DK, null, true);
  addDropdown("s1112ha", "hepatitis_b_test_result_anc", "H29. What was the result of your ANC Hepatitis B test?", [
    "0 = Negative", "1 = Positive", "5 = Not tested", "8 = Don't know"
  ], null, false);
  addMC("s1112gb", "tested_for_hepatitis_c_during_anc", "H30. During ANC for this pregnancy, were you tested for HEPATITIS C?", YES_NO_DK, null, true);
  addDropdown("s1112hb", "hepatitis_c_test_result_anc", "H31. What was the result of your ANC Hepatitis C test?", [
    "0 = Negative", "1 = Positive", "5 = Not tested", "8 = Don't know"
  ], null, false);
  addMC("s1112b", "ever_tested_for_hepatitis_b", "H32a. Have you ever been tested for Hepatitis B?", YES_NO_DK, null, false);
  addDropdown("s1112c", "result_of_hepatitis_b_test", "H32b. Result of lifetime Hepatitis B test", ["0 = Negative", "1 = Positive", "8 = Don't know"], null, false);
  addMC("s1112eb", "tested_for_hepatitis_c_last_12m", "H33a. Tested for Hepatitis C in the last 12 months?", YES_NO_DK, null, false);
  addDropdown("s1112ec", "result_of_hepatitis_c_test", "H33b. Result of Hepatitis C test", ["0 = Negative", "1 = Positive", "8 = Don't know"], null, false);
  addMC("v781", "ever_been_tested_for_hiv", "H34. Have you ever been tested for HIV?", YES_NO, null, true);
  addMC("v840", "tested_for_hiv_as_part_of_anc_visit", "H35. Were you tested for HIV as part of an antenatal care visit?", YES_NO, null, false);
  addMC("v840a", "tested_for_hiv_prior_to_delivery", "H36. Were you tested for HIV between going for delivery and before the baby was born?", YES_NO, null, false);
  addMC("v841", "got_results_of_hiv_test_at_anc", "H37. Did you get the results of your ANC HIV test?", YES_NO, null, false);
  addDropdown("v861", "result_of_last_hiv_test", "H38. What was the result of your most recent HIV test?", [
    "1 = Positive", "2 = Negative", "3 = Indeterminate", "4 = Declined to answer", "5 = Did not receive result"
  ], null, false);
  addMC("v863", "currently_taking_arv_daily", "H39. If HIV-positive, are you currently taking antiretroviral (ARV) medicines daily?", YES_NO_DK, null, false);
  addMC("fi1", "currently_experiences_obstetric_fistula_leakage", "H40a. Currently experiences constant leakage of urine or stool from vagina (Obstetric Fistula)?", YES_NO, null, false);
  addMC("fi2", "ever_experienced_obstetric_fistula_leakage", "H40b. Ever experienced obstetric fistula leakage?", YES_NO, null, false);
  addMC("s473aa", "postpartum_feeling_nervous_anxious", "H41a. During first 2 days after delivery, felt nervous or anxious?", YES_NO_DK, null, false);
  addMC("s473ab", "postpartum_feeling_depressed_hopeless", "H41b. During first 2 days after delivery, felt depressed or hopeless?", YES_NO_DK, null, false);
  addMC("d104", "experienced_any_emotional_violence", "H42a. Ever experienced any emotional partner violence?", YES_NO, null, false);
  addMC("d106", "experienced_any_less_severe_physical_violence", "H42b. Ever experienced any less severe physical partner violence?", YES_NO, null, false);
  addMC("d107", "experienced_any_severe_physical_violence", "H42c. Ever experienced any severe physical partner violence?", YES_NO, null, false);
  addMC("d108", "experienced_any_sexual_violence", "H42d. Ever experienced any sexual partner violence?", YES_NO, null, false);
  addMC("d118y", "did_not_experience_physical_violence_during_pregnancy", "H43. Did anyone hit, slap, kick, or physically hurt you WHILE YOU WERE PREGNANT?", [
    "0 = Yes (Someone physically hurt respondent during pregnancy)",
    "1 = No (Did not experience physical violence during pregnancy)"
  ], null, false);
  addMC("h31", "child_cough_last_2_weeks", "H44a. Child had cough in last 2 weeks?", YES_NO_DK, null, false);
  addMC("h11", "child_diarrhea_last_2_weeks", "H44b. Child had diarrhea in last 2 weeks?", YES_NO_DK, null, false);
  addNumber("hw53", "child_hemoglobin_g_dl_1dec", "H45a. Child unadjusted Hemoglobin (g/dL x 10)", 25, 180, "Leave blank if not measured", false);
  addNumber("hw56", "child_hemoglobin_altitude_adj", "H45b. Child altitude-adjusted Hemoglobin (g/dL x 10)", 25, 180, "Leave blank if not measured", false);
  addNumber("hw70", "child_height_for_age_zscore_who", "H46a. Child WHO Height-for-Age Z-score x 100", -600, 600, "Leave blank if not measured", false);
  addNumber("hw71", "child_weight_for_age_zscore_who", "H46b. Child WHO Weight-for-Age Z-score x 100", -600, 600, "Leave blank if not measured", false);
  addNumber("hw72", "child_weight_for_height_zscore_who", "H46c. Child WHO Weight-for-Height Z-score x 100", -600, 600, "Leave blank if not measured", false);

  Logger.log("Section H created.");

  // ==========================================================================
  // SECTION I: PREGNANCY & MATERNAL OUTCOMES (TARGET VARIABLES FOR EBM)
  // ==========================================================================
  form.addPageBreakItem()
      .setTitle("SECTION I: Pregnancy & Maternal Outcomes (EBM Target Variables)")
      .setHelpText("Clinical pregnancy outcomes, gestational duration, infant birth weight, neonatal survival, and maternal anemia endpoints.");

  addMC("p30", "pregnancy_outcome_declared", "I1. Pregnancy outcome declared by respondent", [
    "1 = Born alive",
    "2 = Born dead (Stillbirth)",
    "3 = Miscarriage",
    "4 = Induced abortion"
  ], null, true);
  addMC("p31", "baby_cried_moved_or_breathed", "I2. If declared born dead (p30 = 2), did the baby cry, move, or breathe at birth?", [
    "0 = No (Confirmed stillbirth)",
    "1 = Yes (Reclassified to live birth)"
  ], "Leave blank if born alive, miscarriage, or abortion", false);
  addMC("p32", "pregnancy_outcome_reclassified", "I3. Final Reclassified Pregnancy Outcome", [
    "1 = Born alive (Live birth)",
    "2 = Born dead (Stillbirth, >= 7 months)",
    "3 = Miscarriage (< 7 months spontaneous loss)",
    "4 = Abortion"
  ], null, true);
  addDropdown("m80", "pregnancy_outcome_section_status", "I4. Pregnancy outcome status for ANC/Maternal Health module", [
    "1 = Most recent live birth",
    "2 = Prior live birth",
    "3 = Most recent stillbirth",
    "4 = Prior stillbirth",
    "5 = Miscarriage / abortion"
  ], null, false);
  addNumber("p20", "pregnancy_duration_months", "I5. Duration of Pregnancy (Gestational Age at Outcome in Completed Months)", 1, 10, "1 to 10 months (< 9 months = Preterm / Early Termination)", true);
  addNumber("m19", "birth_weight_grams_3dec", "I6. Infant Birth Weight in Grams (e.g., 2.400 kg -> enter 2400)", 400, 9998, "500 to 6500 grams (< 2500 = Low Birth Weight); 9996 = Not weighed; 9998 = Don't know", false);
  addDropdown("m19a", "birth_weight_source_card_or_recall", "I8. Source of birth weight record", [
    "0 = Not weighed",
    "1 = From written health card",
    "2 = From mother's recall",
    "8 = Don't know"
  ], null, false);
  addDropdown("m18", "child_size_at_birth", "I9. When the child was born, how was his/her size at birth?", [
    "1 = Very large",
    "2 = Larger than average",
    "3 = Average",
    "4 = Smaller than average (LBW proxy)",
    "5 = Very small (LBW proxy)",
    "8 = Don't know"
  ], null, false);
  addMC("p5", "child_is_alive", "I10. Is the child currently alive?", [
    "0 = No (Deceased)",
    "1 = Yes (Alive)"
  ], "Leave blank if pregnancy ended in stillbirth, miscarriage, or abortion", false);
  addNumber("p6", "child_age_at_death_coded", "I11. If deceased (p5 = 0), how old was the child when he/she died (coded)?", 100, 399, "100 = Died on day of birth (Day 0); 101-130 = Died at 1-30 days (Neonatal Death); 201-223 = Died at 1-23 months", false);
  addDropdown("v457", "maternal_anemia_level", "I13. Maternal Anemia Severity Level", [
    "1 = Severe anemia",
    "2 = Moderate anemia",
    "3 = Mild anemia",
    "4 = Not anemic"
  ], null, false);
  addDropdown("hw57", "child_anemia_level", "I14. Child Anemia Severity Level", [
    "1 = Severe anemia",
    "2 = Moderate anemia",
    "3 = Mild anemia",
    "4 = Not anemic"
  ], null, false);

  // Create and link a Google Sheet for responses automatically
  var ss = SpreadsheetApp.create("Malaria_Pregnancy_EBM_Questionnaire_Responses");
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  var publishedUrl = form.getPublishedUrl();
  var shortUrl = form.shortenFormUrl(publishedUrl);
  var editUrl = form.getEditUrl();
  var sheetUrl = ss.getUrl();

  Logger.log("====================================================================");
  Logger.log("SUCCESS! GOOGLE FORM & LINKED RESPONSE SHEET CREATED:");
  Logger.log("1. LIVE GOOGLE FORM LINK (SHORT): " + shortUrl);
  Logger.log("2. LIVE GOOGLE FORM LINK (FULL):  " + publishedUrl);
  Logger.log("3. FORM EDITOR LINK:              " + editUrl);
  Logger.log("4. LINKED GOOGLE SHEET (CSV):     " + sheetUrl);
  Logger.log("====================================================================");
}

