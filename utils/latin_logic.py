from typing import List, Dict, Optional
import json

class LatinMorphology:
    @staticmethod
    def normalize_latin(text: str) -> str:
        """
        Removes macrons from Latin text to allow for accent-insensitive comparison.
        """
        replacements = {
            'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u', 'ȳ': 'y',
            'Ā': 'A', 'Ē': 'E', 'Ī': 'I', 'Ō': 'O', 'Ū': 'U', 'Ȳ': 'Y'
        }
        normalized = text
        for char, replacement in replacements.items():
            normalized = normalized.replace(char, replacement)
        return normalized

    @staticmethod
    def decline_noun(word: str, declension: str, gender: str, genitive: str, irregular_forms: Optional[str] = None) -> Dict[str, str]:
        """
        Generates full declension table for a noun.
        Returns a dict with keys like 'nom_sg', 'gen_pl', etc.
        """
        forms = {}
        stem = ""
        
        # Simplified stem extraction logic
        if declension == "1":
            stem = word[:-1] if word.endswith("a") else word
            endings = {
                "nom_sg": "a", "voc_sg": "a", "gen_sg": "ae", "dat_sg": "ae", "acc_sg": "am", "abl_sg": "ā",
                "nom_pl": "ae", "voc_pl": "ae", "gen_pl": "ārum", "dat_pl": "īs", "acc_pl": "ās", "abl_pl": "īs"
            }
        elif declension == "2":
            if word.endswith("us"):
                stem = word[:-2]
                endings = {
                    "nom_sg": "us", "voc_sg": "e", "gen_sg": "ī", "dat_sg": "ō", "acc_sg": "um", "abl_sg": "ō",
                    "nom_pl": "ī", "voc_pl": "ī", "gen_pl": "ōrum", "dat_pl": "īs", "acc_pl": "ōs", "abl_pl": "īs"
                }
            elif word.endswith("um"): # Neuter
                stem = word[:-2]
                endings = {
                    "nom_sg": "um", "voc_sg": "um", "gen_sg": "ī", "dat_sg": "ō", "acc_sg": "um", "abl_sg": "ō",
                    "nom_pl": "a", "voc_pl": "a", "gen_pl": "ōrum", "dat_pl": "īs", "acc_pl": "a", "abl_pl": "īs"
                }
            elif word.endswith("r"): # puer, ager
                stem = genitive[:-1] # pueri -> puer
                endings = {
                    "nom_sg": "", "voc_sg": "", "gen_sg": "ī", "dat_sg": "ō", "acc_sg": "um", "abl_sg": "ō",
                    "nom_pl": "ī", "voc_pl": "ī", "gen_pl": "ōrum", "dat_pl": "īs", "acc_pl": "ōs", "abl_pl": "īs"
                }
            else:
                 # Fallback
                stem = word
                endings = {}

        elif declension == "3":
            stem = genitive[:-2] # rex, regis -> reg
            is_neuter = gender == 'n'
            
            if is_neuter:
                endings = {
                    "nom_sg": "", "voc_sg": "", "gen_sg": "is", "dat_sg": "ī", "acc_sg": "", "abl_sg": "e",
                    "nom_pl": "a", "voc_pl": "a", "gen_pl": "um", "dat_pl": "ibus", "acc_pl": "a", "abl_pl": "ibus"
                }
            else:
                endings = {
                    "nom_sg": "", "voc_sg": "", "gen_sg": "is", "dat_sg": "ī", "acc_sg": "em", "abl_sg": "e",
                    "nom_pl": "ēs", "voc_pl": "ēs", "gen_pl": "um", "dat_pl": "ibus", "acc_pl": "ēs", "abl_pl": "ibus"
                }
                
        elif declension == "4":
            stem = word[:-2]
            if gender == 'n': # cornu
                 endings = {
                    "nom_sg": "ū", "voc_sg": "ū", "gen_sg": "ūs", "dat_sg": "ū", "acc_sg": "ū", "abl_sg": "ū",
                    "nom_pl": "ua", "voc_pl": "ua", "gen_pl": "uum", "dat_pl": "ibus", "acc_pl": "ua", "abl_pl": "ibus"
                }
            else:
                endings = {
                    "nom_sg": "us", "voc_sg": "us", "gen_sg": "ūs", "dat_sg": "uī", "acc_sg": "um", "abl_sg": "ū",
                    "nom_pl": "ūs", "voc_pl": "ūs", "gen_pl": "uum", "dat_pl": "ibus", "acc_pl": "ūs", "abl_pl": "ibus"
                }

        elif declension == "5":
            stem = word[:-2]
            endings = {
                "nom_sg": "ēs", "voc_sg": "ēs", "gen_sg": "eī", "dat_sg": "eī", "acc_sg": "em", "abl_sg": "ē",
                "nom_pl": "ēs", "voc_pl": "ēs", "gen_pl": "ērum", "dat_pl": "ēbus", "acc_pl": "ēs", "abl_pl": "ēbus"
            }
        else:
            return {}

        for case, ending in endings.items():
            if case.startswith("nom_sg") and declension in ["2", "3"] and ending == "":
                forms[case] = word # Special handling for nom_sg where it's the base
            elif case.startswith("acc_sg") and declension == "3" and gender == 'n':
                 forms[case] = word
            else:
                forms[case] = stem + ending
                
        # Apply irregular forms overrides if present
        if irregular_forms:
            try:
                overrides = json.loads(irregular_forms)
                for key, value in overrides.items():
                    if key in forms:
                        forms[key] = value
            except json.JSONDecodeError:
                pass # Ignore invalid JSON

        return forms

    @staticmethod
    def decline_pronoun(pronoun: str) -> Dict[str, str]:
        """
        Generates declension for personal pronouns (ego, tū, nōs, vōs).
        These have completely irregular paradigms.
        """
        forms = {}
        
        pronoun_lower = pronoun.lower()
        
        if pronoun_lower == "ego":
            forms = {
                "nom_sg": "ego",
                "gen_sg": "meī",
                "dat_sg": "mihi",
                "acc_sg": "mē",
                "abl_sg": "mē",
                "nom_pl": "nōs",
                "gen_pl": "nostrum/nostrī",
                "dat_pl": "nōbīs",
                "acc_pl": "nōs",
                "abl_pl": "nōbīs"
            }
        elif pronoun_lower == "tū":
            forms = {
                "nom_sg": "tū",
                "gen_sg": "tuī",
                "dat_sg": "tibi",
                "acc_sg": "tē",
                "abl_sg": "tē",
                "nom_pl": "vōs",
                "gen_pl": "vestrum/vestrī",
                "dat_pl": "vōbīs",
                "acc_pl": "vōs",
                "abl_pl": "vōbīs"
            }
        elif pronoun_lower in ["nōs", "nos"]:
            forms = {
                "nom_sg": "—",
                "gen_sg": "—",
                "dat_sg": "—",
                "acc_sg": "—",
                "abl_sg": "—",
                "nom_pl": "nōs",
                "gen_pl": "nostrum/nostrī",
                "dat_pl": "nōbīs",
                "acc_pl": "nōs",
                "abl_pl": "nōbīs"
            }
        elif pronoun_lower in ["vōs", "vos"]:
            forms = {
                "nom_sg": "—",
                "gen_sg": "—",
                "dat_sg": "—",
                "acc_sg": "—",
                "abl_sg": "—",
                "nom_pl": "vōs",
                "gen_pl": "vestrum/vestrī",
                "dat_pl": "vōbīs",
                "acc_pl": "vōs",
                "abl_pl": "vōbīs"
            }
        
        # Demonstrative Pronouns (3 genders)
        elif pronoun_lower == "is":
            # is, ea, id - "that, he, she, it"
            forms = {
                "nom_sg_m": "is", "nom_sg_f": "ea", "nom_sg_n": "id",
                "gen_sg_m": "eius", "gen_sg_f": "eius", "gen_sg_n": "eius",
                "dat_sg_m": "eī", "dat_sg_f": "eī", "dat_sg_n": "eī",
                "acc_sg_m": "eum", "acc_sg_f": "eam", "acc_sg_n": "id",
                "abl_sg_m": "eō", "abl_sg_f": "eā", "abl_sg_n": "eō",
                "nom_pl_m": "eī/iī", "nom_pl_f": "eae", "nom_pl_n": "ea",
                "gen_pl_m": "eōrum", "gen_pl_f": "eārum", "gen_pl_n": "eōrum",
                "dat_pl_m": "eīs/iīs", "dat_pl_f": "eīs/iīs", "dat_pl_n": "eīs/iīs",
                "acc_pl_m": "eōs", "acc_pl_f": "eās", "acc_pl_n": "ea",
                "abl_pl_m": "eīs/iīs", "abl_pl_f": "eīs/iīs", "abl_pl_n": "eīs/iīs"
            }
        elif pronoun_lower == "hic":
            # hic, haec, hoc - "this"
            forms = {
                "nom_sg_m": "hic", "nom_sg_f": "haec", "nom_sg_n": "hoc",
                "gen_sg_m": "huius", "gen_sg_f": "huius", "gen_sg_n": "huius",
                "dat_sg_m": "huic", "dat_sg_f": "huic", "dat_sg_n": "huic",
                "acc_sg_m": "hunc", "acc_sg_f": "hanc", "acc_sg_n": "hoc",
                "abl_sg_m": "hōc", "abl_sg_f": "hāc", "abl_sg_n": "hōc",
                "nom_pl_m": "hī", "nom_pl_f": "hae", "nom_pl_n": "haec",
                "gen_pl_m": "hōrum", "gen_pl_f": "hārum", "gen_pl_n": "hōrum",
                "dat_pl_m": "hīs", "dat_pl_f": "hīs", "dat_pl_n": "hīs",
                "acc_pl_m": "hōs", "acc_pl_f": "hās", "acc_pl_n": "haec",
                "abl_pl_m": "hīs", "abl_pl_f": "hīs", "abl_pl_n": "hīs"
            }
        elif pronoun_lower == "ille":
            # ille, illa, illud - "that, that (over there)"
            forms = {
                "nom_sg_m": "ille", "nom_sg_f": "illa", "nom_sg_n": "illud",
                "gen_sg_m": "illīus", "gen_sg_f": "illīus", "gen_sg_n": "illīus",
                "dat_sg_m": "illī", "dat_sg_f": "illī", "dat_sg_n": "illī",
                "acc_sg_m": "illum", "acc_sg_f": "illam", "acc_sg_n": "illud",
                "abl_sg_m": "illō", "abl_sg_f": "illā", "abl_sg_n": "illō",
                "nom_pl_m": "illī", "nom_pl_f": "illae", "nom_pl_n": "illa",
                "gen_pl_m": "illōrum", "gen_pl_f": "illārum", "gen_pl_n": "illōrum",
                "dat_pl_m": "illīs", "dat_pl_f": "illīs", "dat_pl_n": "illīs",
                "acc_pl_m": "illōs", "acc_pl_f": "illās", "acc_pl_n": "illa",
                "abl_pl_m": "illīs", "abl_pl_f": "illīs", "abl_pl_n": "illīs"
            }
        elif pronoun_lower == "iste":
            # iste, ista, istud - "that (of yours)"
            forms = {
                "nom_sg_m": "iste", "nom_sg_f": "ista", "nom_sg_n": "istud",
                "gen_sg_m": "istīus", "gen_sg_f": "istīus", "gen_sg_n": "istīus",
                "dat_sg_m": "istī", "dat_sg_f": "istī", "dat_sg_n": "istī",
                "acc_sg_m": "istum", "acc_sg_f": "istam", "acc_sg_n": "istud",
                "abl_sg_m": "istō", "abl_sg_f": "istā", "abl_sg_n": "istō",
                "nom_pl_m": "istī", "nom_pl_f": "istae", "nom_pl_n": "ista",
                "gen_pl_m": "istōrum", "gen_pl_f": "istārum", "gen_pl_n": "istōrum",
                "dat_pl_m": "istīs", "dat_pl_f": "istīs", "dat_pl_n": "istīs",
                "acc_pl_m": "istōs", "acc_pl_f": "istās", "acc_pl_n": "ista",
                "abl_pl_m": "istīs", "abl_pl_f": "istīs", "abl_pl_n": "istīs"
            }
        
        return forms


    @staticmethod
    def conjugate_verb(word: str, conjugation: str, principal_parts: str, irregular_forms: Optional[str] = None) -> Dict[str, str]:
        """
        Generates basic conjugation table (Present, Imperfect, Perfect - Active Indicative).
        """
        forms = {}
        parts = principal_parts.split(", ")
        if len(parts) < 3:
            return {} # Cannot conjugate without parts
            
        # 1: amo, amare, amavi, amatum
        # 2: moneo, monere, monui, monitum
        # 3: rego, regere, rexi, rectum
        # 3io: capio, capere, cepi, captum
        # 4: audio, audire, audivi, auditum
        
        pres_stem = parts[1][:-3] # amar -> am (1), moner -> mon (2), reger -> reg (3), audir -> aud (4)
        if conjugation == "1":
            pres_stem = parts[1][:-3] # ama
        elif conjugation == "2":
            pres_stem = parts[1][:-3] # mone
        elif conjugation == "3":
            pres_stem = parts[1][:-3] # reg
        elif conjugation == "4":
            pres_stem = parts[1][:-3] # audi
            
        perf_stem = parts[2][:-1] # amavi -> amav
        
        # Present Indicative Active
        if conjugation == "1": # a-stem
            forms["pres_1sg"] = parts[0] # amo
            forms["pres_2sg"] = pres_stem + "ās"
            forms["pres_3sg"] = pres_stem + "at"
            forms["pres_1pl"] = pres_stem + "āmus"
            forms["pres_2pl"] = pres_stem + "ātis"
            forms["pres_3pl"] = pres_stem + "ant"
        elif conjugation == "2": # e-stem
            forms["pres_1sg"] = parts[0] # moneo
            forms["pres_2sg"] = pres_stem + "ēs"
            forms["pres_3sg"] = pres_stem + "et"
            forms["pres_1pl"] = pres_stem + "ēmus"
            forms["pres_2pl"] = pres_stem + "ētis"
            forms["pres_3pl"] = pres_stem + "ent"
        elif conjugation == "3": # consonant stem
            forms["pres_1sg"] = parts[0] # rego
            forms["pres_2sg"] = pres_stem + "is"
            forms["pres_3sg"] = pres_stem + "it"
            forms["pres_1pl"] = pres_stem + "imus"
            forms["pres_2pl"] = pres_stem + "itis"
            forms["pres_3pl"] = pres_stem + "unt"
        elif conjugation == "4": # i-stem
            forms["pres_1sg"] = parts[0] # audio
            forms["pres_2sg"] = pres_stem + "īs"
            forms["pres_3sg"] = pres_stem + "it"
            forms["pres_1pl"] = pres_stem + "īmus"
            forms["pres_2pl"] = pres_stem + "ītis"
            forms["pres_3pl"] = pres_stem + "iunt"

        # Imperfect Indicative Active
        if conjugation in ["1", "2"]:
            ba_stem = pres_stem + "ba" if conjugation == "1" else pres_stem + "bā" # ama-ba, mone-ba -> actually moneba
            # Correction: 1st: amā-ba, 2nd: monē-ba
            imp_stem = parts[1][:-2] + "ba" # amare -> amaba, monere -> moneba
        elif conjugation == "3":
            imp_stem = pres_stem + "ēba" # reg-eba
        elif conjugation == "4":
            imp_stem = pres_stem + "iēba" # audi-eba
        else:
            # Fallback for unexpected conjugation values
            imp_stem = pres_stem + "ba"
            
        forms["imp_1sg"] = imp_stem + "m"
        forms["imp_2sg"] = imp_stem + "s"
        forms["imp_3sg"] = imp_stem + "t"
        forms["imp_1pl"] = imp_stem + "mus"
        forms["imp_2pl"] = imp_stem + "tis"
        forms["imp_3pl"] = imp_stem + "nt"

        # Perfect Indicative Active
        forms["perf_1sg"] = perf_stem + "ī"
        forms["perf_2sg"] = perf_stem + "istī"
        forms["perf_3sg"] = perf_stem + "it"
        forms["perf_1pl"] = perf_stem + "imus"
        forms["perf_2pl"] = perf_stem + "istis"
        forms["perf_3pl"] = perf_stem + "ērunt"
        
        # ===== PASSIVE VOICE =====
        
        # Present Indicative Passive
        if conjugation == "1":
            forms["pres_pass_1sg"] = pres_stem + "or"
            forms["pres_pass_2sg"] = pres_stem + "āris"
            forms["pres_pass_3sg"] = pres_stem + "ātur"
            forms["pres_pass_1pl"] = pres_stem + "āmur"
            forms["pres_pass_2pl"] = pres_stem + "āminī"
            forms["pres_pass_3pl"] = pres_stem + "antur"
        elif conjugation == "2":
            forms["pres_pass_1sg"] = pres_stem + "or"
            forms["pres_pass_2sg"] = pres_stem + "ēris"
            forms["pres_pass_3sg"] = pres_stem + "ētur"
            forms["pres_pass_1pl"] = pres_stem + "ēmur"
            forms["pres_pass_2pl"] = pres_stem + "ēminī"
            forms["pres_pass_3pl"] = pres_stem + "entur"
        elif conjugation == "3":
            forms["pres_pass_1sg"] = pres_stem + "or"
            forms["pres_pass_2sg"] = pres_stem + "eris"
            forms["pres_pass_3sg"] = pres_stem + "itur"
            forms["pres_pass_1pl"] = pres_stem + "imur"
            forms["pres_pass_2pl"] = pres_stem + "iminī"
            forms["pres_pass_3pl"] = pres_stem + "untur"
        elif conjugation == "4":
            forms["pres_pass_1sg"] = pres_stem + "or"
            forms["pres_pass_2sg"] = pres_stem + "īris"
            forms["pres_pass_3sg"] = pres_stem + "ītur"
            forms["pres_pass_1pl"] = pres_stem + "īmur"
            forms["pres_pass_2pl"] = pres_stem + "īminī"
            forms["pres_pass_3pl"] = pres_stem + "iuntur"
        
        # Imperfect Indicative Passive
        # Use same stem as active imperfect
        forms["imp_pass_1sg"] = imp_stem + "r"
        forms["imp_pass_2sg"] = imp_stem + "ris"
        forms["imp_pass_3sg"] = imp_stem + "tur"
        forms["imp_pass_1pl"] = imp_stem + "mur"
        forms["imp_pass_2pl"] = imp_stem + "minī"
        forms["imp_pass_3pl"] = imp_stem + "ntur"
        
        # Perfect Indicative Passive (Periphrastic: PPP + sum)
        # Extract perfect passive participle from 4th principal part
        if len(parts) >= 4 and parts[3]:
            ppp = parts[3]  # e.g., "amatum", "monitum", "rectum"
            # PPP agrees with subject, using neuter singular for base form
            forms["perf_pass_1sg"] = ppp + " sum"
            forms["perf_pass_2sg"] = ppp + " es"
            forms["perf_pass_3sg"] = ppp + " est"
            forms["perf_pass_1pl"] = ppp.replace("um", "a") + " sumus"  # amata sumus (neuter plural)
            forms["perf_pass_2pl"] = ppp.replace("um", "a") + " estis"
            forms["perf_pass_3pl"] = ppp.replace("um", "a") + " sunt"
        
        # ===== SUBJUNCTIVE MOOD =====
        
        # Present Subjunctive Active
        # Rule: Use opposite vowel (1st conj uses 'e', others use 'ā')
        if conjugation == "1":
            forms["pres_subj_1sg"] = pres_stem + "em"
            forms["pres_subj_2sg"] = pres_stem + "ēs"
            forms["pres_subj_3sg"] = pres_stem + "et"
            forms["pres_subj_1pl"] = pres_stem + "ēmus"
            forms["pres_subj_2pl"] = pres_stem + "ētis"
            forms["pres_subj_3pl"] = pres_stem + "ent"
        elif conjugation == "2":
            forms["pres_subj_1sg"] = pres_stem + "eam"
            forms["pres_subj_2sg"] = pres_stem + "eās"
            forms["pres_subj_3sg"] = pres_stem + "eat"
            forms["pres_subj_1pl"] = pres_stem + "eāmus"
            forms["pres_subj_2pl"] = pres_stem + "eātis"
            forms["pres_subj_3pl"] = pres_stem + "eant"
        elif conjugation == "3":
            forms["pres_subj_1sg"] = pres_stem + "am"
            forms["pres_subj_2sg"] = pres_stem + "ās"
            forms["pres_subj_3sg"] = pres_stem + "at"
            forms["pres_subj_1pl"] = pres_stem + "āmus"
            forms["pres_subj_2pl"] = pres_stem + "ātis"
            forms["pres_subj_3pl"] = pres_stem + "ant"
        elif conjugation == "4":
            forms["pres_subj_1sg"] = pres_stem + "am"
            forms["pres_subj_2sg"] = pres_stem + "ās"
            forms["pres_subj_3sg"] = pres_stem + "at"
            forms["pres_subj_1pl"] = pres_stem + "āmus"
            forms["pres_subj_2pl"] = pres_stem + "ātis"
            forms["pres_subj_3pl"] = pres_stem + "ant"
        
        # Imperfect Subjunctive Active
        # Rule: present infinitive + personal endings (m, s, t, mus, tis, nt)
        inf_stem = parts[1]  # Full infinitive (amare, monere, regere, audire)
        forms["imp_subj_1sg"] = inf_stem + "m"
        forms["imp_subj_2sg"] = inf_stem + "s"
        forms["imp_subj_3sg"] = inf_stem + "t"
        forms["imp_subj_1pl"] = inf_stem + "mus"
        forms["imp_subj_2pl"] = inf_stem + "tis"
        forms["imp_subj_3pl"] = inf_stem + "nt"
        
        # Present Subjunctive Passive
        if conjugation == "1":
            forms["pres_subj_pass_1sg"] = pres_stem + "er"
            forms["pres_subj_pass_2sg"] = pres_stem + "ēris"
            forms["pres_subj_pass_3sg"] = pres_stem + "ētur"
            forms["pres_subj_pass_1pl"] = pres_stem + "ēmur"
            forms["pres_subj_pass_2pl"] = pres_stem + "ēminī"
            forms["pres_subj_pass_3pl"] = pres_stem + "entur"
        elif conjugation == "2":
            forms["pres_subj_pass_1sg"] = pres_stem + "ear"
            forms["pres_subj_pass_2sg"] = pres_stem + "eāris"
            forms["pres_subj_pass_3sg"] = pres_stem + "eātur"
            forms["pres_subj_pass_1pl"] = pres_stem + "eāmur"
            forms["pres_subj_pass_2pl"] = pres_stem + "eāminī"
            forms["pres_subj_pass_3pl"] = pres_stem + "eantur"
        elif conjugation == "3":
            forms["pres_subj_pass_1sg"] = pres_stem + "ar"
            forms["pres_subj_pass_2sg"] = pres_stem + "āris"
            forms["pres_subj_pass_3sg"] = pres_stem + "ātur"
            forms["pres_subj_pass_1pl"] = pres_stem + "āmur"
            forms["pres_subj_pass_2pl"] = pres_stem + "āminī"
            forms["pres_subj_pass_3pl"] = pres_stem + "antur"
        elif conjugation == "4":
            forms["pres_subj_pass_1sg"] = pres_stem + "ar"
            forms["pres_subj_pass_2sg"] = pres_stem + "āris"
            forms["pres_subj_pass_3sg"] = pres_stem + "ātur"
            forms["pres_subj_pass_1pl"] = pres_stem + "āmur"
            forms["pres_subj_pass_2pl"] = pres_stem + "āminī"
            forms["pres_subj_pass_3pl"] = pres_stem + "antur"
        
        # Imperfect Subjunctive Passive
        # Rule: present infinitive + passive endings (r, ris, tur, mur, mini, ntur)
        forms["imp_subj_pass_1sg"] = inf_stem + "r"
        forms["imp_subj_pass_2sg"] = inf_stem + "ris"
        forms["imp_subj_pass_3sg"] = inf_stem + "tur"
        forms["imp_subj_pass_1pl"] = inf_stem + "mur"
        forms["imp_subj_pass_2pl"] = inf_stem + "minī"
        forms["imp_subj_pass_3pl"] = inf_stem + "ntur"

        # ===== IMPERATIVE MOOD =====
        
        # Present Imperative Active (only 2nd person)
        # Singular: stem (no ending), Plural: add -te
        if conjugation == "1":
            forms["imv_2sg"] = pres_stem + "ā"  # amā
            forms["imv_2pl"] = pres_stem + "āte"  # amāte
        elif conjugation == "2":
            forms["imv_2sg"] = pres_stem + "ē"  # monē
            forms["imv_2pl"] = pres_stem + "ēte"  # monēte
        elif conjugation == "3":
            forms["imv_2sg"] = pres_stem + "e"  # rege
            forms["imv_2pl"] = pres_stem + "ite"  # regite
        elif conjugation == "4":
            forms["imv_2sg"] = pres_stem + "ī"  # audī
            forms["imv_2pl"] = pres_stem + "īte"  # audīte
        
        # Present Imperative Passive (only 2nd person)
        # Singular: add -re, Plural: add -minī
        if conjugation == "1":
            forms["imv_pass_2sg"] = pres_stem + "āre"  # amāre
            forms["imv_pass_2pl"] = pres_stem + "āminī"  # amāminī
        elif conjugation == "2":
            forms["imv_pass_2sg"] = pres_stem + "ēre"  # monēre
            forms["imv_pass_2pl"] = pres_stem + "ēminī"  # monēminī
        elif conjugation == "3":
            forms["imv_pass_2sg"] = pres_stem + "ere"  # regere
            forms["imv_pass_2pl"] = pres_stem + "iminī"  # regiminī
        elif conjugation == "4":
            forms["imv_pass_2sg"] = pres_stem + "īre"  # audīre
            forms["imv_pass_2pl"] = pres_stem + "īminī"  # audīminī

        # Apply irregular forms overrides if present
        if irregular_forms:
            try:
                overrides = json.loads(irregular_forms)
                for key, value in overrides.items():
                    forms[key] = value
            except json.JSONDecodeError:
                pass # Ignore invalid JSON

        return forms

