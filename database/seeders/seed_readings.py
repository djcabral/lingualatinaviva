"""
Seeder: Readings (Text table)

Populates the Text table with progressive Latin readings for lessons 1-30.
L1-L10: Simple constructed sentences (LLPSI-style)
L11-L20: Adapted classical passages
L21-L30: Original excerpts with minor simplification
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database.connection import get_session
from database import Text

def seed_readings():
    """Seed reading texts for all 30 lessons"""
    
    readings = [
        # === L1-L5: Basic Morphology ===
        {
            "title": "Roma et Italia",
            "content": "Rōma in Italiā est. Italia in Eurōpā est. Rōma magna urbs est. Incolae Rōmae Rōmānī sunt. Rōmānī Latīnē loquuntur.",
            "difficulty": 1,
            "grammar_focus": '["nominative", "esse"]'
        },
        {
            "title": "Familia Rōmāna",
            "content": "Iūlius pater est. Aemilia māter est. Mārcus et Quīntus fīliī sunt. Iūlia fīlia est. Familia Iūliī magna est. Iūlius fīliōs et fīliam amat.",
            "difficulty": 2,
            "grammar_focus": '["nominative", "genitive", "accusative"]'
        },
        {
            "title": "Schola Latīna",
            "content": "Discipulī in scholā sunt. Magister discipulōs docet. Discipulī magistrum audiunt. Magister fābulam nārrat. Discipulī fābulam audiunt et gaudent.",
            "difficulty": 3,
            "grammar_focus": '["accusative", "present_tense"]'
        },
        {
            "title": "In Forō",
            "content": "Forum Rōmānum magnum est. Mercātōrēs in forō sunt. Cīvēs mercātōribus pecūniam dant. Mercātōrēs cīvibus mercem vendunt. Forum semper plēnum est.",
            "difficulty": 4,
            "grammar_focus": '["dative", "ablative"]'
        },
        {
            "title": "Dē Deīs Rōmānīs",
            "content": "Iuppiter rēx deōrum est. Iūnō rēgīna deōrum est. Mārs deus bellī est. Venus dea amōris est. Rōmānī multōs deōs colunt.",
            "difficulty": 5,
            "grammar_focus": '["genitive", "ablative"]'
        },
        
        # === L6-L10: Verbs & Cases ===
        {
            "title": "Cēna Rōmāna",
            "content": "Iūlius cēnam parat. Servī cibum afferunt. Familia in triclīniō cēnat. Aemilia vīnum miscet. Post cēnam Iūlius fābulam nārrat.",
            "difficulty": 6,
            "grammar_focus": '["present_active", "accusative"]'
        },
        {
            "title": "Iter ad Urbem",
            "content": "Mārcus cum patre Rōmam it. Via longa est. In viā multōs viātōrēs vident. Tandem ad portam urbis perveniunt. Mārcus laetus est.",
            "difficulty": 7,
            "grammar_focus": '["motion_verbs", "prepositions"]'
        },
        {
            "title": "Dē Temporibus Annī",
            "content": "Annus quattuor tempora habet: vēr, aestās, autumnus, hiems. Vēre flōrēs florent. Aestāte sol calidus est. Autumnō frūctūs mātūrēscunt. Hieme nix cadit.",
            "difficulty": 8,
            "grammar_focus": '["ablative_time", "seasons"]'
        },
        {
            "title": "Mīles Rōmānus",
            "content": "Mīlitēs Rōmānī fortēs sunt. Gladiōs et scūta portant. Imperātor mīlitēs dūcit. Mīlitēs imperātōrī pārent. Legiō Rōmāna invicta est.",
            "difficulty": 9,
            "grammar_focus": '["third_declension", "military_vocab"]'
        },
        {
            "title": "Epistula ad Amīcum",
            "content": "Mārcus Gāiō amīcō suō salūtem dīcit. Valēsne? Ego valeō. Hodiē in hortō lūsī. Crās ad tē veniam. Valē, amīce!",
            "difficulty": 10,
            "grammar_focus": '["epistolary_formulas", "future_tense"]'
        },
        
        # === L11-L15: Adapted Classical ===
        {
            "title": "Rōmulus et Remus",
            "content": "Rōmulus et Remus gemīnī erant. Lupa eōs nūtrīvit. Posteā Rōmulus urbem condidit. Urbs Rōma vocāta est. Rōmulus prīmus rēx Rōmānōrum fuit.",
            "difficulty": 11,
            "grammar_focus": '["perfect_tense", "passive_voice"]'
        },
        {
            "title": "Dē Bellō Pūnicō",
            "content": "Hannibal dux Carthāginiēnsium fuit. Cum elephantīs Alpēs trānsiit. Rōmānōs multīs proeliīs superāvit. Tamen Rōmam capere nōn potuit.",
            "difficulty": 12,
            "grammar_focus": '["perfect_tense", "cum_ablative"]'
        },
        {
            "title": "Vōx Populī",
            "content": "In forō cīvēs conveniēbant. Ōrātor verba faciēbat. Populus ōrātōrem audīvit. Aliquī laudāvērunt, aliquī vituperāvērunt. Sīc erat lībertās Rōmāna.",
            "difficulty": 13,
            "grammar_focus": '["imperfect_vs_perfect", "public_speaking"]'
        },
        {
            "title": "Aenēās ad Ītaliam",
            "content": "Aenēās Trōiā fūgit. Per maria multa errāvit. Tandem ad Ītaliam pervēnit. Ibi novam patriam invēnit. Rōmānī ab Aenēā oriundī sunt.",
            "difficulty": 14,
            "grammar_focus": '["perfect_passive", "ablative_separation"]'
        },
        {
            "title": "Caesar in Galliā",
            "content": "Gallia omnis in partēs trēs dīvīsa est. Ūnam partem Belgae incolunt, aliam Aquītānī, tertiam Celtae. Hī omnēs linguā et lēgibus differunt.",
            "difficulty": 15,
            "grammar_focus": '["passive_voice", "partitive_genitive"]'
        },
        
        # === L16-L20: Intermediate ===
        {
            "title": "Cicerō dē Amīcitiā",
            "content": "Amīcitia nihil aliud est nisi omnium dīvīnārum hūmānārumque rērum cum benevolentiā et cāritāte cōnsēnsiō. Sine amīcitiā vīta nūlla est.",
            "difficulty": 16,
            "grammar_focus": '["subjunctive_intro", "abstract_nouns"]'
        },
        {
            "title": "Horātius in Ponte",
            "content": "Porsenna rēx urbem oppugnābat. Horātius sōlus in ponte stetit. Hostēs sustinuit dum pōns ā tergō solvitur. Deinde in flūmen dēsiluit.",
            "difficulty": 17,
            "grammar_focus": '["temporal_clauses", "dum"]'
        },
        {
            "title": "Catilīnae Coniūrātiō",
            "content": "Catilīna rem pūblicam dēlēre voluit. Cicerō coniūrātiōnem dētēxit. In senātū ōrātiōnem habuit: 'Quōusque tandem abūtēre, Catilīna, patientiā nostrā?'",
            "difficulty": 18,
            "grammar_focus": '["future_participle", "rhetorical_questions"]'
        },
        {
            "title": "Ōvidius dē Amōre",
            "content": "Mīlitat omnis amāns, et habet sua castra Cupīdō. Quae bellō est habilis, Vēnerī quoque convenit aetās. Turpe senex mīles, turpe senīlis amor.",
            "difficulty": 19,
            "grammar_focus": '["poetry_intro", "dative_purpose"]'
        },
        {
            "title": "Seneca ad Lūcīlium",
            "content": "Nōn quī parum habet, sed quī plūs cupit, pauper est. Dīvitiās nōn quī habet, sed quī cupit, carēre potuit.",
            "difficulty": 20,
            "grammar_focus": '["relative_clauses", "comparative"]'
        },
        
        # === L21-L25: Advanced Syntax ===
        {
            "title": "Bellum Gallicum (Adaptātum)",
            "content": "Hīs rēbus cognitīs, Caesar exercitum trāns Rhēnum dūxit. Germānī, adventū Caesaris cognitō, in silvās fūgērunt. Caesar pontem rescindit.",
            "difficulty": 21,
            "grammar_focus": '["ablative_absolute", "participles"]'
        },
        {
            "title": "Ab Urbe Conditā",
            "content": "Rōmulō rēgnante, urbs crēscēbat. Multī hominēs Rōmam veniēbant. Rōmulus, senātōribus convocātīs, lēgēs tulit. Populus lēgēs accēpit.",
            "difficulty": 22,
            "grammar_focus": '["ablative_absolute", "participle_uses"]'
        },
        {
            "title": "Dē Officiīs",
            "content": "Officium est id quod faciendum est. Sunt autem officiā gerenda cum dignitāte. Nēmō enim est quī officiīs sē exsolvere possit.",
            "difficulty": 23,
            "grammar_focus": '["gerund", "gerundive"]'
        },
        {
            "title": "Perīphrasis",
            "content": "Hannibal Alpēs trānsitūrus erat. Mīlitēs sequendī erant. Rōma dēfendenda erat. Victōria adipīscenda erat cīvibus.",
            "difficulty": 24,
            "grammar_focus": '["periphrastic_conjugations", "obligation"]'
        },
        {
            "title": "Cum Historicum",
            "content": "Cum Caesar Galliam petīvisset, Helvētiī dē fīnibus suīs exīre cōnstituērunt. Cum profectī essent, Caesar eōs secūtus est.",
            "difficulty": 25,
            "grammar_focus": '["cum_clauses", "sequence_of_tenses"]'
        },
        
        # === L26-L30: Complex Syntax ===
        {
            "title": "Ōrātiō Oblīqua",
            "content": "Lēgātī dīxērunt sē pācem petere. Negāvērunt sē bellum velle. Affirmāvērunt rēgem suum amīcum populī Rōmānī esse.",
            "difficulty": 26,
            "grammar_focus": '["indirect_statement", "accusative_infinitive"]'
        },
        {
            "title": "Condiciōnēs",
            "content": "Sī hoc fēcerīs, laetus erō. Sī hoc facerēs, laetus essem. Sī hoc fēcissēs, laetus fuissem. Condiciōnēs dīversae sunt.",
            "difficulty": 27,
            "grammar_focus": '["conditionals", "subjunctive_moods"]'
        },
        {
            "title": "Relātīvae",
            "content": "Is quī sapit, felix est. Quod faciendum est, faciāmus. Quae vēra sunt, dīcenda sunt. Quōrum virtūs clāra est, laudandī sunt.",
            "difficulty": 28,
            "grammar_focus": '["relative_clauses", "subjunctive_attraction"]'
        },
        {
            "title": "Stīlus Indīrectus",
            "content": "Caesar in commentāriīs scrīpsit Gallōs fortēs esse. Dīxit sē eōs victūrum esse. Narrāvit Germānōs trans Rhēnum habitāre.",
            "difficulty": 29,
            "grammar_focus": '["oratio_obliqua", "sequence_of_tenses"]'
        },
        {
            "title": "Vergilius: Arma virumque canō",
            "content": "Arma virumque canō, Trōiae quī prīmus ab ōrīs Ītaliam fātō profugus Lāvīniaque vēnit lītora. Multum ille et terrīs iactātus et altō.",
            "difficulty": 30,
            "grammar_focus": '["poetry", "epic_style", "synthesis"]'
        },
    ]
    
    with get_session() as session:
        # Check if already seeded
        existing = session.query(Text).count()
        if existing > 0:
            print(f"⚠️  Ya existen {existing} textos. Saltando seed.")
            return
        
        for reading in readings:
            text = Text(**reading)
            session.add(text)
        
        session.commit()
        print(f"✅ Se insertaron {len(readings)} lecturas exitosamente.")

if __name__ == "__main__":
    seed_readings()
