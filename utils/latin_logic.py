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
        
        # Apply irregular forms overrides if present
        if irregular_forms:
            try:
                overrides = json.loads(irregular_forms)
                for key, value in overrides.items():
                    forms[key] = value
            except json.JSONDecodeError:
                pass # Ignore invalid JSON

        return forms
