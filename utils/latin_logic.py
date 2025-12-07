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
    def decline_noun(word: str, declension: str, gender: str, genitive: str, irregular_forms: Optional[str] = None, parisyllabic: Optional[bool] = None, is_plurale_tantum: bool = False, is_singulare_tantum: bool = False) -> Dict[str, str]:
        """
        Generates full declension table for a noun.
        Returns a dict with keys like 'nom_sg', 'gen_pl', etc.
        
        Args:
            is_plurale_tantum: If True, word only exists in plural (e.g., castra, arma)
            is_singulare_tantum: If True, word only exists in singular
        """
        # Clean up homonym markers (digits) from word and genitive
        clean_word = ''.join([c for c in word if not c.isdigit()])
        clean_genitive = ''.join([c for c in genitive if not c.isdigit()])
        
        forms = {}
        stem = ""
        
        # Simplified stem extraction logic
        if declension == "1":
            stem = clean_word[:-1] if clean_word.endswith("a") else clean_word
            endings = {
                "nom_sg": "a", "voc_sg": "a", "gen_sg": "ae", "dat_sg": "ae", "acc_sg": "am", "abl_sg": "ā",
                "nom_pl": "ae", "voc_pl": "ae", "gen_pl": "ārum", "dat_pl": "īs", "acc_pl": "ās", "abl_pl": "īs"
            }
        elif declension == "2":
            if clean_word.endswith("us"):
                stem = clean_word[:-2]
                endings = {
                    "nom_sg": "us", "voc_sg": "e", "gen_sg": "ī", "dat_sg": "ō", "acc_sg": "um", "abl_sg": "ō",
                    "nom_pl": "ī", "voc_pl": "ī", "gen_pl": "ōrum", "dat_pl": "īs", "acc_pl": "ōs", "abl_pl": "īs"
                }
            elif clean_word.endswith("um"): # Neuter
                stem = clean_word[:-2]
                endings = {
                    "nom_sg": "um", "voc_sg": "um", "gen_sg": "ī", "dat_sg": "ō", "acc_sg": "um", "abl_sg": "ō",
                    "nom_pl": "a", "voc_pl": "a", "gen_pl": "ōrum", "dat_pl": "īs", "acc_pl": "a", "abl_pl": "īs"
                }
            elif clean_word.endswith("r"): # puer, ager
                stem = clean_genitive[:-1] # pueri -> puer
                endings = {
                    "nom_sg": "", "voc_sg": "", "gen_sg": "ī", "dat_sg": "ō", "acc_sg": "um", "abl_sg": "ō",
                    "nom_pl": "ī", "voc_pl": "ī", "gen_pl": "ōrum", "dat_pl": "īs", "acc_pl": "ōs", "abl_pl": "īs"
                }
            else:
                 # Fallback
                stem = clean_word
                endings = {}

        elif declension == "3":
            stem = clean_genitive[:-2] # rex, regis -> reg
            is_neuter = gender == 'n'
            is_parisyllabic = parisyllabic if parisyllabic is not None else False
            
            if is_neuter:
                if is_parisyllabic:  # e.g., mare, maris
                    endings = {
                        "nom_sg": "", "voc_sg": "", "gen_sg": "is", "dat_sg": "ī", "acc_sg": "", "abl_sg": "ī",
                        "nom_pl": "ia", "voc_pl": "ia", "gen_pl": "ium", "dat_pl": "ibus", "acc_pl": "ia", "abl_pl": "ibus"
                    }
                else:  # e.g., corpus, corporis (imparisyllabic)
                    endings = {
                        "nom_sg": "", "voc_sg": "", "gen_sg": "is", "dat_sg": "ī", "acc_sg": "", "abl_sg": "e",
                        "nom_pl": "a", "voc_pl": "a", "gen_pl": "um", "dat_pl": "ibus", "acc_pl": "a", "abl_pl": "ibus"
                    }
            else:  # Masculine/Feminine
                if is_parisyllabic:  # e.g., civis, civis
                    endings = {
                        "nom_sg": "", "voc_sg": "", "gen_sg": "is", "dat_sg": "ī", "acc_sg": "em", "abl_sg": "ī",
                        "nom_pl": "ēs", "voc_pl": "ēs", "gen_pl": "ium", "dat_pl": "ibus", "acc_pl": "ēs", "abl_pl": "ibus"
                    }
                else:  # e.g., rex, regis (imparisyllabic)
                    endings = {
                        "nom_sg": "", "voc_sg": "", "gen_sg": "is", "dat_sg": "ī", "acc_sg": "em", "abl_sg": "e",
                        "nom_pl": "ēs", "voc_pl": "ēs", "gen_pl": "um", "dat_pl": "ibus", "acc_pl": "ēs", "abl_pl": "ibus"
                    }
                
        elif declension == "4":
            stem = clean_word[:-2]
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
                forms[case] = clean_word # Special handling for nom_sg where it's the base
            elif case.startswith("acc_sg") and declension == "3" and gender == 'n':
                 forms[case] = clean_word
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

        # Handle pluralia tantum (only plural forms exist)
        if is_plurale_tantum:
            for key in list(forms.keys()):
                if '_sg' in key:
                    forms[key] = "—"
        
        # Handle singularia tantum (only singular forms exist)
        if is_singulare_tantum:
            for key in list(forms.keys()):
                if '_pl' in key:
                    forms[key] = "—"

        return forms
    @staticmethod
    def decline_adjective(word: str, declension: str, gender: str, genitive: str) -> Dict[str, str]:
        """
        Generates declension for adjectives.
        Handles 2-1-2 (bonus, bona, bonum) and 3rd declension (tristis, forte).
        """
        forms = {}
        
        # 1st/2nd Declension (2-1-2)
        if declension == "1/2":
            # word is masculine form: bonus
            stem = word[:-2] if word.endswith("us") else (word[:-2] + "r" if word.endswith("er") else word)
            # Correction for 'er' adjectives (pulcher -> pulchr)
            if word.endswith("er") and genitive:
                stem = genitive[:-1] # pulchri -> pulchr
            
            # Masculine (2nd Declension)
            forms.update({f"{k}_m": v for k, v in LatinMorphology.decline_noun(word, "2", "m", genitive).items()})
            
            # Feminine (1st Declension)
            fem_base = stem + "a"
            forms.update({f"{k}_f": v for k, v in LatinMorphology.decline_noun(fem_base, "1", "f", stem + "ae").items()})
            
            # Neuter (2nd Declension Neuter)
            neut_base = stem + "um"
            forms.update({f"{k}_n": v for k, v in LatinMorphology.decline_noun(neut_base, "2", "n", stem + "i").items()})

        # 3rd Declension
        elif declension == "3":
            # Handles: tristis (m/f), triste (n); audax (m/f/n); acer (m), acris (f), acre (n)
            # Simplified approach using noun logic for now
            # Assume entry is masculine/common form
            stem = genitive[:-2] # tristis -> trist
            
            # Masculine/Feminine
            forms.update({f"{k}_m": v for k, v in LatinMorphology.decline_noun(word, "3", "m", genitive, parisyllabic=True).items()})
            forms.update({f"{k}_f": v for k, v in LatinMorphology.decline_noun(word, "3", "f", genitive, parisyllabic=True).items()})
            
            # Neuter
            # If word is 'tristis', neuter is 'triste'
            if word.endswith("is"):
                neut_base = word[:-2] + "e"
                forms.update({f"{k}_n": v for k, v in LatinMorphology.decline_noun(neut_base, "3", "n", genitive, parisyllabic=True).items()})
            else:
                 # Fallback
                forms.update({f"{k}_n": v for k, v in LatinMorphology.decline_noun(word, "3", "n", genitive, parisyllabic=True).items()})
                
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
        
        elif pronoun_lower == "qui":
            # qui, quae, quod - "who, which"
            forms = {
                "nom_sg_m": "quī", "nom_sg_f": "quae", "nom_sg_n": "quod",
                "gen_sg_m": "cuius", "gen_sg_f": "cuius", "gen_sg_n": "cuius",
                "dat_sg_m": "cui", "dat_sg_f": "cui", "dat_sg_n": "cui",
                "acc_sg_m": "quem", "acc_sg_f": "quam", "acc_sg_n": "quod",
                "abl_sg_m": "quō", "abl_sg_f": "quā", "abl_sg_n": "quō",
                "nom_pl_m": "quī", "nom_pl_f": "quae", "nom_pl_n": "quae",
                "gen_pl_m": "quōrum", "gen_pl_f": "quārum", "gen_pl_n": "quōrum",
                "dat_pl_m": "quibus", "dat_pl_f": "quibus", "dat_pl_n": "quibus",
                "acc_pl_m": "quōs", "acc_pl_f": "quās", "acc_pl_n": "quae",
                "abl_pl_m": "quibus", "abl_pl_f": "quibus", "abl_pl_n": "quibus"
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

        # Future Indicative Active
        if conjugation == "1":
            # 1st: -ābō, -ābis, -ābit...
            forms["fut_1sg"] = pres_stem + "ābō"
            forms["fut_2sg"] = pres_stem + "ābis"
            forms["fut_3sg"] = pres_stem + "ābit"
            forms["fut_1pl"] = pres_stem + "ābimus"
            forms["fut_2pl"] = pres_stem + "ābitis"
            forms["fut_3pl"] = pres_stem + "ābunt"
        elif conjugation == "2":
            # 2nd: -ēbō, -ēbis, -ēbit...
            forms["fut_1sg"] = pres_stem + "ēbō"
            forms["fut_2sg"] = pres_stem + "ēbis"
            forms["fut_3sg"] = pres_stem + "ēbit"
            forms["fut_1pl"] = pres_stem + "ēbimus"
            forms["fut_2pl"] = pres_stem + "ēbitis"
            forms["fut_3pl"] = pres_stem + "ēbunt"
        elif conjugation == "3":
            # 3rd: -am, -ēs, -et...
            # pres_stem: reg
            forms["fut_1sg"] = pres_stem + "am"
            forms["fut_2sg"] = pres_stem + "ēs"
            forms["fut_3sg"] = pres_stem + "et"
            forms["fut_1pl"] = pres_stem + "ēmus"
            forms["fut_2pl"] = pres_stem + "ētis"
            forms["fut_3pl"] = pres_stem + "ent"
        elif conjugation == "4":
            # 4th: -iam, -iēs, -iet...
            # pres_stem: audi (actually aud)
            forms["fut_1sg"] = pres_stem + "iam"
            forms["fut_2sg"] = pres_stem + "iēs"
            forms["fut_3sg"] = pres_stem + "iet"
            forms["fut_1pl"] = pres_stem + "iēmus"
            forms["fut_2pl"] = pres_stem + "iētis"
            forms["fut_3pl"] = pres_stem + "ient"

        # Pluperfect Indicative Active
        # perf_stem + eram
        forms["plup_1sg"] = perf_stem + "eram"
        forms["plup_2sg"] = perf_stem + "erās"
        forms["plup_3sg"] = perf_stem + "erat"
        forms["plup_1pl"] = perf_stem + "erāmus"
        forms["plup_2pl"] = perf_stem + "erātis"
        forms["plup_3pl"] = perf_stem + "erant"

        # Future Perfect Indicative Active
        # perf_stem + ero
        forms["futperf_1sg"] = perf_stem + "erō"
        forms["futperf_2sg"] = perf_stem + "eris"
        forms["futperf_3sg"] = perf_stem + "erit"
        forms["futperf_1pl"] = perf_stem + "erimus"
        forms["futperf_2pl"] = perf_stem + "eritis"
        forms["futperf_3pl"] = perf_stem + "erint"
        
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
            forms["pres_pass_1sg"] = parts[0][:-1] + "or" # regor
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
        
        # Future Indicative Passive
        if conjugation == "1":
            # 1st: -ābor, -āberis, -ābitur...
            forms["fut_pass_1sg"] = pres_stem + "ābor"
            forms["fut_pass_2sg"] = pres_stem + "āberis"
            forms["fut_pass_3sg"] = pres_stem + "ābitur"
            forms["fut_pass_1pl"] = pres_stem + "ābimur"
            forms["fut_pass_2pl"] = pres_stem + "ābiminī"
            forms["fut_pass_3pl"] = pres_stem + "ābuntur"
        elif conjugation == "2":
            # 2nd: -ēbor, -ēberis, -ēbitur...
            forms["fut_pass_1sg"] = pres_stem + "ēbor"
            forms["fut_pass_2sg"] = pres_stem + "ēberis"
            forms["fut_pass_3sg"] = pres_stem + "ēbitur"
            forms["fut_pass_1pl"] = pres_stem + "ēbimur"
            forms["fut_pass_2pl"] = pres_stem + "ēbiminī"
            forms["fut_pass_3pl"] = pres_stem + "ēbuntur"
        elif conjugation == "3":
            # 3rd: -ar, -ēris, -ētur...
            # pres_stem: reg
            forms["fut_pass_1sg"] = pres_stem + "ar"
            forms["fut_pass_2sg"] = pres_stem + "ēris"
            forms["fut_pass_3sg"] = pres_stem + "ētur"
            forms["fut_pass_1pl"] = pres_stem + "ēmur"
            forms["fut_pass_2pl"] = pres_stem + "ēminī"
            forms["fut_pass_3pl"] = pres_stem + "entur"
        elif conjugation == "4":
            # 4th: -iar, -iēris, -iētur...
            # pres_stem: audi
            forms["fut_pass_1sg"] = pres_stem + "iar"
            forms["fut_pass_2sg"] = pres_stem + "iēris"
            forms["fut_pass_3sg"] = pres_stem + "iētur"
            forms["fut_pass_1pl"] = pres_stem + "iēmur"
            forms["fut_pass_2pl"] = pres_stem + "iēminī"
            forms["fut_pass_3pl"] = pres_stem + "ientur"

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
            
            # Pluperfect Indicative Passive (PPP + eram)
            forms["plup_pass_1sg"] = ppp + " eram"
            forms["plup_pass_2sg"] = ppp + " erās"
            forms["plup_pass_3sg"] = ppp + " erat"
            forms["plup_pass_1pl"] = ppp.replace("um", "a") + " erāmus"
            forms["plup_pass_2pl"] = ppp.replace("um", "a") + " erātis"
            forms["plup_pass_3pl"] = ppp.replace("um", "a") + " erant"
            
            # Future Perfect Indicative Passive (PPP + ero)
            forms["futperf_pass_1sg"] = ppp + " erō"
            forms["futperf_pass_2sg"] = ppp + " eris"
            forms["futperf_pass_3sg"] = ppp + " erit"
            forms["futperf_pass_1pl"] = ppp.replace("um", "a") + " erimus"
            forms["futperf_pass_2pl"] = ppp.replace("um", "a") + " eritis"
            forms["futperf_pass_3pl"] = ppp.replace("um", "a") + " erunt"
            
            # Perfect Subjunctive Passive (PPP + sim)
            forms["perf_subj_pass_1sg"] = ppp + " sim"
            forms["perf_subj_pass_2sg"] = ppp + " sīs"
            forms["perf_subj_pass_3sg"] = ppp + " sit"
            forms["perf_subj_pass_1pl"] = ppp.replace("um", "a") + " sīmus"
            forms["perf_subj_pass_2pl"] = ppp.replace("um", "a") + " sītis"
            forms["perf_subj_pass_3pl"] = ppp.replace("um", "a") + " sint"
            
            # Pluperfect Subjunctive Passive (PPP + essem)
            forms["plup_subj_pass_1sg"] = ppp + " essem"
            forms["plup_subj_pass_2sg"] = ppp + " essēs"
            forms["plup_subj_pass_3sg"] = ppp + " esset"
            forms["plup_subj_pass_1pl"] = ppp.replace("um", "a") + " essēmus"
            forms["plup_subj_pass_2pl"] = ppp.replace("um", "a") + " essētis"
            forms["plup_subj_pass_3pl"] = ppp.replace("um", "a") + " essent"
        
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
        
        # Perfect Subjunctive Active
        # perf_stem + erim
        forms["perf_subj_1sg"] = perf_stem + "erim"
        forms["perf_subj_2sg"] = perf_stem + "eris"
        forms["perf_subj_3sg"] = perf_stem + "erit"
        forms["perf_subj_1pl"] = perf_stem + "erimus"
        forms["perf_subj_2pl"] = perf_stem + "eritis"
        forms["perf_subj_3pl"] = perf_stem + "erint"
        
        # Pluperfect Subjunctive Active
        # perf_stem + issem
        forms["plup_subj_1sg"] = perf_stem + "issem"
        forms["plup_subj_2sg"] = perf_stem + "issēs"
        forms["plup_subj_3sg"] = perf_stem + "isset"
        forms["plup_subj_1pl"] = perf_stem + "issēmus"
        forms["plup_subj_2pl"] = perf_stem + "issētis"
        forms["plup_subj_3pl"] = perf_stem + "issent"
        
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

    @staticmethod
    def get_participles(word: str, conjugation: str, principal_parts: str) -> Dict[str, str]:
        """
        Generates participles for a verb.
        Returns a dict with keys: 'pres_act', 'perf_pass', 'fut_act', 'fut_pass'
        """
        forms = {}
        parts = principal_parts.split(", ")
        if len(parts) < 3:
            return {}

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

        # Present Active Participle (ns, ntis)
        if conjugation == "1":
            forms["pres_act"] = pres_stem + "ns, " + pres_stem + "ntis"
        elif conjugation == "2":
            forms["pres_act"] = pres_stem + "ns, " + pres_stem + "ntis"
        elif conjugation == "3":
            forms["pres_act"] = pres_stem + "ēns, " + pres_stem + "entis"
        elif conjugation == "4":
            forms["pres_act"] = pres_stem + "iēns, " + pres_stem + "ientis"

        # Perfect Passive Participle (us, a, um) - from 4th principal part (supine)
        if len(parts) >= 4 and parts[3]:
            ppp = parts[3] # amatum
            if ppp.endswith("um"):
                base = ppp[:-2] # amat
                forms["perf_pass"] = f"{base}us, -a, -um"
            else:
                forms["perf_pass"] = ppp # Fallback

        # Future Active Participle (urus, a, um) - from 4th principal part
        if len(parts) >= 4 and parts[3]:
            ppp = parts[3]
            if ppp.endswith("um"):
                base = ppp[:-2]
                forms["fut_act"] = f"{base}ūrus, -a, -um"
            else:
                 forms["fut_act"] = "-"

        # Future Passive Participle (Gerundive) - (ndus, a, um)
        if conjugation == "1":
            forms["fut_pass"] = pres_stem + "ndus, -a, -um"
        elif conjugation == "2":
            forms["fut_pass"] = pres_stem + "ndus, -a, -um"
        elif conjugation == "3":
            forms["fut_pass"] = pres_stem + "endus, -a, -um"
        elif conjugation == "4":
            forms["fut_pass"] = pres_stem + "iendus, -a, -um"

        return forms


# =============================================================================
# FUNCIONES WRAPPER PARA COMPATIBILIDAD CON IMPORTS LEGACY
# =============================================================================
# Las páginas antiguas importan funciones standalone que no existían.
# Estas wrappers mantienen compatibilidad sin cambiar todas las páginas.

_morphology = LatinMorphology()

def get_declension_forms(word: str, declension: str, gender: str, genitive: str, **kwargs):
    """
    Wrapper para LatinMorphology.decline_noun()
    
    Usado por: Declinatio.py, Analysis.py
    """
    return _morphology.decline_noun(word, declension, gender, genitive, **kwargs)


def get_conjugation_forms(word: str, conjugation: str, principal_parts: str, **kwargs):
    """
    Wrapper para LatinMorphology.conjugate_verb()
    
    Usado por: Conjugatio.py, Analysis.py
    """
    return _morphology.conjugate_verb(word, conjugation, principal_parts, **kwargs)


def get_pronoun_forms(pronoun: str):
    """
    Wrapper para LatinMorphology.decline_pronoun()
    
    Usado por: Declinatio.py
    """
    return _morphology.decline_pronoun(pronoun)


def get_demonstrative_genders():
    """
    Retorna lista de géneros para demostrativos.
    
    Usado por: Declinatio.py
    """
    return ["m", "f", "n"]

