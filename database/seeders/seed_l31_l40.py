import sys
import os
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database import get_session, Word, LessonVocabulary, SentenceAnalysis

def seed_lessons_31_40(session: Session):
    print("🌱 Iniciando población de Lecciones 31-40 (Autores Clásicos y Periodos)...")

    # 1. Vocabulario (10 palabras por lección)
    lesson_vocab = [
        # L31: César (Guerra de las Galias)
        {"latin": "divido", "translation": "dividir", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 31},
        {"latin": "incolo", "translation": "habitar", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 31},
        {"latin": "lex", "translation": "ley", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 31},
        {"latin": "proelium", "translation": "batalla", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 31},
        {"latin": "flumen", "translation": "río", "part_of_speech": "noun", "declension": "3ª", "gender": "Neutro", "lesson": 31},
        {"latin": "mons", "translation": "monte, montaña", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 31},
        {"latin": "fines", "translation": "fronteras, territorio", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 31},
        {"latin": "copia", "translation": "abundancia (pl. tropas)", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 31},
        {"latin": "legatus", "translation": "legado, embajador", "part_of_speech": "noun", "declension": "2ª", "gender": "Masculino", "lesson": 31},
        {"latin": "imperium", "translation": "mando, poder, imperio", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 31},

        # L32: Cicerón (Catilinarias)
        {"latin": "abutor", "translation": "abusar", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 32},
        {"latin": "patientia", "translation": "paciencia", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 32},
        {"latin": "furor", "translation": "locura, furia", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 32},
        {"latin": "eludo", "translation": "burlar, esquivar", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 32},
        {"latin": "audacia", "translation": "audacia, osadía", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 32},
        {"latin": "senatus", "translation": "senado", "part_of_speech": "noun", "declension": "4ª", "gender": "Masculino", "lesson": 32},
        {"latin": "consul", "translation": "cónsul", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 32},
        {"latin": "res publica", "translation": "república, estado", "part_of_speech": "noun", "declension": "5ª", "gender": "Femenino", "lesson": 32},
        {"latin": "mos", "translation": "costumbre", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 32},
        {"latin": "tempus", "translation": "tiempo", "part_of_speech": "noun", "declension": "3ª", "gender": "Neutro", "lesson": 32},

        # L33: Salustio (Conjuración de Catilina)
        {"latin": "ingenium", "translation": "talento, carácter", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 33},
        {"latin": "pravus", "translation": "torcido, malvado", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 33},
        {"latin": "inedia", "translation": "ayuno, falta de comida", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 33},
        {"latin": "algor", "translation": "frío", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 33},
        {"latin": "vigilia", "translation": "vigilia, falta de sueño", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 33},
        {"latin": "corpus", "translation": "cuerpo", "part_of_speech": "noun", "declension": "3ª", "gender": "Neutro", "lesson": 33},
        {"latin": "animus", "translation": "espíritu, mente", "part_of_speech": "noun", "declension": "2ª", "gender": "Masculino", "lesson": 33},
        {"latin": "cupido", "translation": "deseo, pasión", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 33},
        {"latin": "coniuratio", "translation": "conjuración, conspiración", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 33},
        {"latin": "civitas", "translation": "ciudadanía, estado", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 33},

        # L34: Catulo (Carmina)
        {"latin": "odi", "translation": "odiar", "part_of_speech": "verb", "conjugation": "Defectivo", "lesson": 34},
        {"latin": "amo", "translation": "amar", "part_of_speech": "verb", "conjugation": "1ª", "lesson": 34},
        {"latin": "requiro", "translation": "buscar, preguntar", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 34},
        {"latin": "sentio", "translation": "sentir", "part_of_speech": "verb", "conjugation": "4ª", "lesson": 34},
        {"latin": "excrucior", "translation": "ser torturado", "part_of_speech": "verb", "conjugation": "1ª", "lesson": 34},
        {"latin": "passer", "translation": "gorrión", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 34},
        {"latin": "basium", "translation": "beso", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 34},
        {"latin": "vivamus", "translation": "vivamos (subjuntivo)", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 34},
        {"latin": "rumor", "translation": "rumor, habladuría", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 34},
        {"latin": "senex", "translation": "anciano", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 34},

        # L35: Virgilio (Eneida)
        {"latin": "cano", "translation": "cantar", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 35},
        {"latin": "ora", "translation": "costa, orilla", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 35},
        {"latin": "fatum", "translation": "destino", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 35},
        {"latin": "profugus", "translation": "prófugo, fugitivo", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 35},
        {"latin": "litus", "translation": "playa, costa", "part_of_speech": "noun", "declension": "3ª", "gender": "Neutro", "lesson": 35},
        {"latin": "arma", "translation": "armas", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 35},
        {"latin": "vir", "translation": "hombre, héroe", "part_of_speech": "noun", "declension": "2ª", "gender": "Masculino", "lesson": 35},
        {"latin": "altum", "translation": "alta mar, lo profundo", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 35},
        {"latin": "moenia", "translation": "murallas", "part_of_speech": "noun", "declension": "3ª", "gender": "Neutro", "lesson": 35},
        {"latin": "numen", "translation": "divinidad, voluntad divina", "part_of_speech": "noun", "declension": "3ª", "gender": "Neutro", "lesson": 35},

        # L36: Horacio (Odas)
        {"latin": "carpo", "translation": "arrancar, cosechar, aprovechar", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 36},
        {"latin": "credulus", "translation": "crédulo, confiado", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 36},
        {"latin": "posterus", "translation": "siguiente, futuro", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 36},
        {"latin": "aetas", "translation": "edad, tiempo, vida", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 36},
        {"latin": "fugio", "translation": "huir", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 36},
        {"latin": "vinum", "translation": "vino", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 36},
        {"latin": "hiems", "translation": "invierno", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 36},
        {"latin": "mare", "translation": "mar", "part_of_speech": "noun", "declension": "3ª", "gender": "Neutro", "lesson": 36},
        {"latin": "navis", "translation": "nave, barco", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 36},
        {"latin": "aureus", "translation": "dorado, de oro", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 36},

        # L37: Ovidio (Metamorfosis)
        {"latin": "amor", "translation": "amor", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 37},
        {"latin": "ira", "translation": "ira", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 37},
        {"latin": "saevus", "translation": "cruel, fiero", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 37},
        {"latin": "fors", "translation": "suerte, azar", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 37},
        {"latin": "ignarus", "translation": "ignorante", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 37},
        {"latin": "muto", "translation": "cambiar, transformar", "part_of_speech": "verb", "conjugation": "1ª", "lesson": 37},
        {"latin": "forma", "translation": "forma, belleza", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 37},
        {"latin": "novus", "translation": "nuevo", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 37},
        {"latin": "orbis", "translation": "círculo, mundo", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 37},
        {"latin": "phoebus", "translation": "Febo (Apolo)", "part_of_speech": "noun", "declension": "2ª", "gender": "Masculino", "lesson": 37},

        # L38: Latín Medieval
        {"latin": "universitas", "translation": "universidad, totalidad", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 38},
        {"latin": "scholasticus", "translation": "escolástico, de la escuela", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 38},
        {"latin": "trinitas", "translation": "trinidad", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 38},
        {"latin": "peccatum", "translation": "pecado", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 38},
        {"latin": "infernus", "translation": "infierno", "part_of_speech": "noun", "declension": "2ª", "gender": "Masculino", "lesson": 38},
        {"latin": "monasterium", "translation": "monasterio", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 38},
        {"latin": "abbas", "translation": "abad", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 38},
        {"latin": "oratio", "translation": "oración, rezo", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 38},
        {"latin": "missa", "translation": "misa", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 38},
        {"latin": "credo", "translation": "creer", "part_of_speech": "verb", "conjugation": "3ª", "lesson": 38},

        # L39: Latín Eclesiástico
        {"latin": "saeculum", "translation": "siglo, mundo", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 39},
        {"latin": "amen", "translation": "amén, así sea", "part_of_speech": "adverb", "lesson": 39},
        {"latin": "spiritus", "translation": "espíritu", "part_of_speech": "noun", "declension": "4ª", "gender": "Masculino", "lesson": 39},
        {"latin": "sanctus", "translation": "santo", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 39},
        {"latin": "pater", "translation": "padre", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 39},
        {"latin": "caelum", "translation": "cielo", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 39},
        {"latin": "panis", "translation": "pan", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 39},
        {"latin": "quotidianus", "translation": "cotidiano, diario", "part_of_speech": "adjective", "declension": "1ª/2ª", "lesson": 39},
        {"latin": "debitor", "translation": "deudor", "part_of_speech": "noun", "declension": "3ª", "gender": "Masculino", "lesson": 39},
        {"latin": "tentatio", "translation": "tentación", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 39},

        # L40: Latín Renacentista/Científico
        {"latin": "hypothesis", "translation": "hipótesis", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 40},
        {"latin": "experimentum", "translation": "experimento", "part_of_speech": "noun", "declension": "2ª", "gender": "Neutro", "lesson": 40},
        {"latin": "gravitas", "translation": "gravedad, peso", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 40},
        {"latin": "orbita", "translation": "órbita", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 40},
        {"latin": "calculus", "translation": "cálculo, piedra", "part_of_speech": "noun", "declension": "2ª", "gender": "Masculino", "lesson": 40},
        {"latin": "methodus", "translation": "método", "part_of_speech": "noun", "declension": "2ª", "gender": "Femenino", "lesson": 40},
        {"latin": "natura", "translation": "naturaleza", "part_of_speech": "noun", "declension": "1ª", "gender": "Femenino", "lesson": 40},
        {"latin": "motus", "translation": "movimiento", "part_of_speech": "noun", "declension": "4ª", "gender": "Masculino", "lesson": 40},
        {"latin": "observatio", "translation": "observación", "part_of_speech": "noun", "declension": "3ª", "gender": "Femenino", "lesson": 40},
        {"latin": "systema", "translation": "sistema", "part_of_speech": "noun", "declension": "3ª", "gender": "Neutro", "lesson": 40},
    ]

    # 2. Oraciones de Traducción (10 por lección)
    translation_sentences = [
        # L31: César
        {"latin": "Gallia est omnis divisa in partes tres.", "spanish": "Toda la Galia está dividida en tres partes.", "difficulty_level": 1, "lesson": 31},
        {"latin": "Belgae unam partem incolunt.", "spanish": "Los belgas habitan una parte.", "difficulty_level": 1, "lesson": 31},
        {"latin": "Aquitani aliam partem incolunt.", "spanish": "Los aquitanos habitan otra parte.", "difficulty_level": 1, "lesson": 31},
        {"latin": "Horum omnium fortissimi sunt Belgae.", "spanish": "De todos estos, los más fuertes son los belgas.", "difficulty_level": 2, "lesson": 31},
        {"latin": "Helvetii cum Germanis contendunt.", "spanish": "Los helvecios luchan con los germanos.", "difficulty_level": 2, "lesson": 31},
        {"latin": "Caesar legatos ad eum misit.", "spanish": "César envió embajadores a él.", "difficulty_level": 2, "lesson": 31},
        {"latin": "Flumen Rhenus agros dividit.", "spanish": "El río Rin divide los campos.", "difficulty_level": 1, "lesson": 31},
        {"latin": "Milites castra posuerunt.", "spanish": "Los soldados establecieron el campamento.", "difficulty_level": 2, "lesson": 31},
        {"latin": "Imperator copias eduxit.", "spanish": "El general sacó las tropas.", "difficulty_level": 2, "lesson": 31},
        {"latin": "Caesar in Galliam venit.", "spanish": "César vino a la Galia.", "difficulty_level": 1, "lesson": 31},

        # L32: Cicerón
        {"latin": "Quousque tandem abutere patientia nostra?", "spanish": "¿Hasta cuándo abusarás de nuestra paciencia?", "difficulty_level": 3, "lesson": 32},
        {"latin": "O tempora, o mores!", "spanish": "¡Oh tiempos, oh costumbres!", "difficulty_level": 1, "lesson": 32},
        {"latin": "Senatus haec intellegit.", "spanish": "El senado entiende estas cosas.", "difficulty_level": 1, "lesson": 32},
        {"latin": "Consul videt.", "spanish": "El cónsul (lo) ve.", "difficulty_level": 1, "lesson": 32},
        {"latin": "Hic tamen vivit.", "spanish": "Este, sin embargo, vive.", "difficulty_level": 1, "lesson": 32},
        {"latin": "Vivit? Immo vero etiam in senatum venit.", "spanish": "¿Vive? Más aún, incluso viene al senado.", "difficulty_level": 2, "lesson": 32},
        {"latin": "Nos autem viri fortes sumus.", "spanish": "Nosotros, en cambio, somos hombres fuertes.", "difficulty_level": 2, "lesson": 32},
        {"latin": "Catilina, nobiscum esse non potes.", "spanish": "Catilina, no puedes estar con nosotros.", "difficulty_level": 2, "lesson": 32},
        {"latin": "Egredere ex urbe, Catilina.", "spanish": "Sal de la ciudad, Catilina.", "difficulty_level": 2, "lesson": 32},
        {"latin": "Patria te odit ac metuit.", "spanish": "La patria te odia y te teme.", "difficulty_level": 2, "lesson": 32},

        # L33: Salustio
        {"latin": "Lucius Catilina nobili genere natus est.", "spanish": "Lucio Catilina nació de noble linaje.", "difficulty_level": 2, "lesson": 33},
        {"latin": "Fuit magna vi animi et corporis.", "spanish": "Fue de gran fuerza de espíritu y de cuerpo.", "difficulty_level": 2, "lesson": 33},
        {"latin": "Ingenio malo pravoque erat.", "spanish": "Era de carácter malo y depravado.", "difficulty_level": 2, "lesson": 33},
        {"latin": "Huic ab adulescentia bella intestina grata fuerunt.", "spanish": "A este, desde la adolescencia, le fueron gratas las guerras civiles.", "difficulty_level": 3, "lesson": 33},
        {"latin": "Corpus patiens inediae erat.", "spanish": "Su cuerpo era capaz de soportar el ayuno.", "difficulty_level": 2, "lesson": 33},
        {"latin": "Alieni appetens, sui profusus.", "spanish": "Deseoso de lo ajeno, derrochador de lo propio.", "difficulty_level": 3, "lesson": 33},
        {"latin": "Satis eloquentiae, sapientiae parum.", "spanish": "Suficiente elocuencia, poca sabiduría.", "difficulty_level": 2, "lesson": 33},
        {"latin": "Vastus animus immoderata cupiebat.", "spanish": "Su espíritu insaciable deseaba cosas desmesuradas.", "difficulty_level": 3, "lesson": 33},
        {"latin": "Civitas corrupta erat.", "spanish": "La ciudad estaba corrompida.", "difficulty_level": 1, "lesson": 33},
        {"latin": "Divitiae morum bonorum ruinam effecerunt.", "spanish": "Las riquezas causaron la ruina de las buenas costumbres.", "difficulty_level": 3, "lesson": 33},

        # L34: Catulo
        {"latin": "Odi et amo.", "spanish": "Odio y amo.", "difficulty_level": 1, "lesson": 34},
        {"latin": "Vivamus, mea Lesbia, atque amemus.", "spanish": "Vivamos, mi Lesbia, y amemos.", "difficulty_level": 2, "lesson": 34},
        {"latin": "Da mihi basia mille.", "spanish": "Dame mil besos.", "difficulty_level": 1, "lesson": 34},
        {"latin": "Soles occidere et redire possunt.", "spanish": "Los soles pueden ponerse y volver.", "difficulty_level": 2, "lesson": 34},
        {"latin": "Nobis una nox dormienda est.", "spanish": "Nosotros debemos dormir una sola noche.", "difficulty_level": 3, "lesson": 34},
        {"latin": "Lugete, o Veneres Cupidinesque.", "spanish": "Llorad, oh Venus y Cupidos.", "difficulty_level": 2, "lesson": 34},
        {"latin": "Passer mortuus est meae puellae.", "spanish": "El gorrión de mi niña ha muerto.", "difficulty_level": 2, "lesson": 34},
        {"latin": "Miser Catulle, desinas ineptire.", "spanish": "Miserable Catulo, deja de hacer tonterías.", "difficulty_level": 3, "lesson": 34},
        {"latin": "Nulli se dicit mulier mea nubere malle.", "spanish": "Mi mujer dice que prefiere no casarse con nadie.", "difficulty_level": 3, "lesson": 34},
        {"latin": "Sed mulier cupido quod dicit amanti...", "spanish": "Pero lo que la mujer dice a su amante deseoso...", "difficulty_level": 3, "lesson": 34},

        # L35: Virgilio
        {"latin": "Arma virumque cano.", "spanish": "Canto a las armas y al hombre.", "difficulty_level": 1, "lesson": 35},
        {"latin": "Troiae qui primus ab oris venit.", "spanish": "Quien vino primero desde las costas de Troya.", "difficulty_level": 2, "lesson": 35},
        {"latin": "Multum ille et terris iactatus et alto.", "spanish": "Él, muy sacudido tanto en tierra como en alta mar.", "difficulty_level": 3, "lesson": 35},
        {"latin": "Tantae molis erat Romanam condere gentem.", "spanish": "De tan gran esfuerzo era fundar la nación romana.", "difficulty_level": 3, "lesson": 35},
        {"latin": "O fortunati, quorum iam moenia surgunt!", "spanish": "¡Oh afortunados, cuyas murallas ya se levantan!", "difficulty_level": 2, "lesson": 35},
        {"latin": "Timeo Danaos et dona ferentes.", "spanish": "Temo a los griegos incluso cuando traen regalos.", "difficulty_level": 2, "lesson": 35},
        {"latin": "Dux femina facti.", "spanish": "Una mujer fue la líder de la hazaña.", "difficulty_level": 2, "lesson": 35},
        {"latin": "Amor omnibus idem.", "spanish": "El amor es el mismo para todos.", "difficulty_level": 1, "lesson": 35},
        {"latin": "Labor omnia vincit.", "spanish": "El trabajo lo vence todo.", "difficulty_level": 1, "lesson": 35},
        {"latin": "Fama, malum qua non aliud velocius ullum.", "spanish": "La Fama, mal del cual ningún otro es más veloz.", "difficulty_level": 3, "lesson": 35},

        # L36: Horacio
        {"latin": "Carpe diem.", "spanish": "Aprovecha el día.", "difficulty_level": 1, "lesson": 36},
        {"latin": "Nunc est bibendum.", "spanish": "Ahora hay que beber.", "difficulty_level": 2, "lesson": 36},
        {"latin": "Aurea mediocritas.", "spanish": "La dorada medianía.", "difficulty_level": 1, "lesson": 36},
        {"latin": "Eheu fugaces, Postume, labuntur anni.", "spanish": "Ay, Póstumo, los años fugaces se escapan.", "difficulty_level": 3, "lesson": 36},
        {"latin": "Dulce et decorum est pro patria mori.", "spanish": "Dulce y honorable es morir por la patria.", "difficulty_level": 2, "lesson": 36},
        {"latin": "Non omnis moriar.", "spanish": "No moriré del todo.", "difficulty_level": 1, "lesson": 36},
        {"latin": "Exegi monumentum aere perennius.", "spanish": "He levantado un monumento más duradero que el bronce.", "difficulty_level": 3, "lesson": 36},
        {"latin": "Beatus ille qui procul negotiis...", "spanish": "Dichoso aquel que lejos de los negocios...", "difficulty_level": 2, "lesson": 36},
        {"latin": "Odi profanum vulgus.", "spanish": "Odio al vulgo profano.", "difficulty_level": 2, "lesson": 36},
        {"latin": "Pulvis et umbra sumus.", "spanish": "Somos polvo y sombra.", "difficulty_level": 1, "lesson": 36},

        # L37: Ovidio
        {"latin": "In nova fert animus mutatas dicere formas.", "spanish": "Mi espíritu me lleva a hablar de formas transformadas en cuerpos nuevos.", "difficulty_level": 3, "lesson": 37},
        {"latin": "Primus amor Phoebi Daphne fuit.", "spanish": "El primer amor de Febo fue Dafne.", "difficulty_level": 1, "lesson": 37},
        {"latin": "Pater, fer opem!", "spanish": "¡Padre, trae ayuda!", "difficulty_level": 1, "lesson": 37},
        {"latin": "Vix prece finita, torpor occupat artus.", "spanish": "Apenas terminada la súplica, un torpor ocupa sus miembros.", "difficulty_level": 3, "lesson": 37},
        {"latin": "Omnia vincit Amor.", "spanish": "El Amor lo vence todo.", "difficulty_level": 1, "lesson": 37},
        {"latin": "Tempus edax rerum.", "spanish": "El tiempo, devorador de las cosas.", "difficulty_level": 1, "lesson": 37},
        {"latin": "Video meliora proboque, deteriora sequor.", "spanish": "Veo lo mejor y lo apruebo, pero sigo lo peor.", "difficulty_level": 3, "lesson": 37},
        {"latin": "Donec eris felix, multos numerabis amicos.", "spanish": "Mientras seas feliz, contarás muchos amigos.", "difficulty_level": 2, "lesson": 37},
        {"latin": "Gutta cavat lapidem.", "spanish": "La gota horada la piedra.", "difficulty_level": 1, "lesson": 37},
        {"latin": "Ars latet arte sua.", "spanish": "El arte se oculta con su propio arte.", "difficulty_level": 2, "lesson": 37},

        # L38: Latín Medieval
        {"latin": "Dies irae, dies illa.", "spanish": "Día de ira, aquel día.", "difficulty_level": 1, "lesson": 38},
        {"latin": "O Fortuna, velut luna statu variabilis.", "spanish": "Oh Fortuna, variable como la luna.", "difficulty_level": 2, "lesson": 38},
        {"latin": "Gaudeamus igitur, iuvenes dum sumus.", "spanish": "Alegrémonos pues, mientras somos jóvenes.", "difficulty_level": 2, "lesson": 38},
        {"latin": "Ubi sunt qui ante nos in mundo fuere?", "spanish": "¿Dónde están los que fueron antes de nosotros en el mundo?", "difficulty_level": 3, "lesson": 38},
        {"latin": "Stabat Mater dolorosa.", "spanish": "Estaba la Madre dolorosa.", "difficulty_level": 1, "lesson": 38},
        {"latin": "Veni, Creator Spiritus.", "spanish": "Ven, Espíritu Creador.", "difficulty_level": 1, "lesson": 38},
        {"latin": "Confiteor Deo omnipotenti.", "spanish": "Confieso a Dios todopoderoso.", "difficulty_level": 2, "lesson": 38},
        {"latin": "Requiem aeternam dona eis, Domine.", "spanish": "Dales, Señor, el descanso eterno.", "difficulty_level": 2, "lesson": 38},
        {"latin": "Te Deum laudamus.", "spanish": "A ti, Dios, te alabamos.", "difficulty_level": 1, "lesson": 38},
        {"latin": "Salve, Regina, mater misericordiae.", "spanish": "Salve, Reina, madre de misericordia.", "difficulty_level": 2, "lesson": 38},

        # L39: Latín Eclesiástico
        {"latin": "Pater noster, qui es in caelis.", "spanish": "Padre nuestro, que estás en los cielos.", "difficulty_level": 1, "lesson": 39},
        {"latin": "Sanctificetur nomen tuum.", "spanish": "Santificado sea tu nombre.", "difficulty_level": 2, "lesson": 39},
        {"latin": "Adveniat regnum tuum.", "spanish": "Venga tu reino.", "difficulty_level": 1, "lesson": 39},
        {"latin": "Fiat voluntas tua.", "spanish": "Hágase tu voluntad.", "difficulty_level": 2, "lesson": 39},
        {"latin": "Panem nostrum quotidianum da nobis hodie.", "spanish": "Danos hoy nuestro pan de cada día.", "difficulty_level": 2, "lesson": 39},
        {"latin": "Et dimitte nobis debita nostra.", "spanish": "Y perdónanos nuestras deudas.", "difficulty_level": 2, "lesson": 39},
        {"latin": "Sicut et nos dimittimus debitoribus nostris.", "spanish": "Así como nosotros perdonamos a nuestros deudores.", "difficulty_level": 3, "lesson": 39},
        {"latin": "Et ne nos inducas in tentationem.", "spanish": "Y no nos dejes caer en la tentación.", "difficulty_level": 2, "lesson": 39},
        {"latin": "Sed libera nos a malo.", "spanish": "Mas líbranos del mal.", "difficulty_level": 1, "lesson": 39},
        {"latin": "Gloria Patri et Filio et Spiritui Sancto.", "spanish": "Gloria al Padre y al Hijo y al Espíritu Santo.", "difficulty_level": 1, "lesson": 39},

        # L40: Latín Renacentista/Científico
        {"latin": "Cogito, ergo sum.", "spanish": "Pienso, luego existo.", "difficulty_level": 1, "lesson": 40},
        {"latin": "Hypotheses non fingo.", "spanish": "No invento hipótesis.", "difficulty_level": 2, "lesson": 40},
        {"latin": "Eppur si muove.", "spanish": "Y sin embargo se mueve.", "difficulty_level": 1, "lesson": 40},
        {"latin": "Natura abhorret a vacuo.", "spanish": "La naturaleza aborrece el vacío.", "difficulty_level": 2, "lesson": 40},
        {"latin": "Homo homini lupus.", "spanish": "El hombre es un lobo para el hombre.", "difficulty_level": 1, "lesson": 40},
        {"latin": "Scientia potentia est.", "spanish": "El conocimiento es poder.", "difficulty_level": 1, "lesson": 40},
        {"latin": "Tabula rasa.", "spanish": "Tabla rasa (hoja en blanco).", "difficulty_level": 1, "lesson": 40},
        {"latin": "Lex parsimoniae.", "spanish": "Ley de la parsimonia (Navaja de Ockham).", "difficulty_level": 2, "lesson": 40},
        {"latin": "Systema Naturae.", "spanish": "Sistema de la Naturaleza.", "difficulty_level": 1, "lesson": 40},
        {"latin": "Philosophiae Naturalis Principia Mathematica.", "spanish": "Principios Matemáticos de la Filosofía Natural.", "difficulty_level": 3, "lesson": 40},
    ]

    # 3. Oraciones de Análisis Sintáctico (1 por lección)
    syntax_sentences = [
        {
            "latin_text": "Gallia est omnis divisa in partes tres.",
            "spanish_translation": "Toda la Galia está dividida en tres partes.",
            "difficulty_level": 2,
            "lesson_number": 31,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Gallia", "role": "subject", "parent": 3},
                    {"id": 2, "label": "omnis", "role": "modifier", "parent": 1},
                    {"id": 3, "label": "est divisa", "role": "verb", "parent": 0},
                    {"id": 4, "label": "in partes", "role": "prepositional_phrase", "parent": 3},
                    {"id": 5, "label": "tres", "role": "modifier", "parent": 4}
                ]
            }
        },
        {
            "latin_text": "Quousque tandem abutere, Catilina, patientia nostra?",
            "spanish_translation": "¿Hasta cuándo abusarás, Catilina, de nuestra paciencia?",
            "difficulty_level": 3,
            "lesson_number": 32,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Quousque", "role": "adverb", "parent": 3},
                    {"id": 2, "label": "tandem", "role": "adverb", "parent": 1},
                    {"id": 3, "label": "abutere", "role": "verb", "parent": 0},
                    {"id": 4, "label": "Catilina", "role": "vocative", "parent": 3},
                    {"id": 5, "label": "patientia", "role": "object", "parent": 3},
                    {"id": 6, "label": "nostra", "role": "modifier", "parent": 5}
                ]
            }
        },
        {
            "latin_text": "Lucius Catilina, nobili genere natus, fuit magna vi animi.",
            "spanish_translation": "Lucio Catilina, nacido de noble linaje, fue de gran fuerza de espíritu.",
            "difficulty_level": 3,
            "lesson_number": 33,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Lucius Catilina", "role": "subject", "parent": 5},
                    {"id": 2, "label": "natus", "role": "participle", "parent": 1},
                    {"id": 3, "label": "nobili genere", "role": "ablative", "parent": 2},
                    {"id": 4, "label": "fuit", "role": "verb", "parent": 0},
                    {"id": 5, "label": "magna vi", "role": "ablative_quality", "parent": 1},
                    {"id": 6, "label": "animi", "role": "genitive", "parent": 5}
                ]
            }
        },
        {
            "latin_text": "Odi et amo.",
            "spanish_translation": "Odio y amo.",
            "difficulty_level": 1,
            "lesson_number": 34,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Odi", "role": "verb", "parent": 0},
                    {"id": 2, "label": "et", "role": "conjunction", "parent": 0},
                    {"id": 3, "label": "amo", "role": "verb", "parent": 0}
                ]
            }
        },
        {
            "latin_text": "Arma virumque cano, Troiae qui primus ab oris venit.",
            "spanish_translation": "Canto a las armas y al hombre que vino primero desde las costas de Troya.",
            "difficulty_level": 3,
            "lesson_number": 35,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "cano", "role": "verb", "parent": 0},
                    {"id": 2, "label": "Arma", "role": "object", "parent": 1},
                    {"id": 3, "label": "virumque", "role": "object", "parent": 1},
                    {"id": 4, "label": "qui", "role": "subject_relative", "parent": 3},
                    {"id": 5, "label": "venit", "role": "verb_relative", "parent": 4},
                    {"id": 6, "label": "primus", "role": "modifier", "parent": 4},
                    {"id": 7, "label": "ab oris", "role": "prepositional_phrase", "parent": 5}
                ]
            }
        },
        {
            "latin_text": "Carpe diem, quam minimum credula postero.",
            "spanish_translation": "Aprovecha el día, confiando lo menos posible en el mañana.",
            "difficulty_level": 2,
            "lesson_number": 36,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Carpe", "role": "verb", "parent": 0},
                    {"id": 2, "label": "diem", "role": "object", "parent": 1},
                    {"id": 3, "label": "credula", "role": "modifier", "parent": 1},
                    {"id": 4, "label": "minimum", "role": "adverb", "parent": 3},
                    {"id": 5, "label": "postero", "role": "object", "parent": 3}
                ]
            }
        },
        {
            "latin_text": "Primus amor Phoebi Daphne fuit.",
            "spanish_translation": "El primer amor de Febo fue Dafne.",
            "difficulty_level": 1,
            "lesson_number": 37,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Primus", "role": "modifier", "parent": 2},
                    {"id": 2, "label": "amor", "role": "subject", "parent": 4},
                    {"id": 3, "label": "Phoebi", "role": "genitive", "parent": 2},
                    {"id": 4, "label": "fuit", "role": "verb", "parent": 0},
                    {"id": 5, "label": "Daphne", "role": "predicate", "parent": 4}
                ]
            }
        },
        {
            "latin_text": "Dies irae, dies illa, solvet saeclum in favilla.",
            "spanish_translation": "Día de ira, aquel día, disolverá el mundo en cenizas.",
            "difficulty_level": 2,
            "lesson_number": 38,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Dies", "role": "subject", "parent": 4},
                    {"id": 2, "label": "irae", "role": "genitive", "parent": 1},
                    {"id": 3, "label": "illa", "role": "modifier", "parent": 1},
                    {"id": 4, "label": "solvet", "role": "verb", "parent": 0},
                    {"id": 5, "label": "saeclum", "role": "object", "parent": 4},
                    {"id": 6, "label": "in favilla", "role": "prepositional_phrase", "parent": 4}
                ]
            }
        },
        {
            "latin_text": "Pater noster, qui es in caelis.",
            "spanish_translation": "Padre nuestro, que estás en los cielos.",
            "difficulty_level": 1,
            "lesson_number": 39,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Pater", "role": "vocative", "parent": 0},
                    {"id": 2, "label": "noster", "role": "modifier", "parent": 1},
                    {"id": 3, "label": "qui", "role": "subject_relative", "parent": 1},
                    {"id": 4, "label": "es", "role": "verb_relative", "parent": 3},
                    {"id": 5, "label": "in caelis", "role": "prepositional_phrase", "parent": 4}
                ]
            }
        },
        {
            "latin_text": "Cogito, ergo sum.",
            "spanish_translation": "Pienso, luego existo.",
            "difficulty_level": 1,
            "lesson_number": 40,
            "analysis_json": {
                "nodes": [
                    {"id": 1, "label": "Cogito", "role": "verb", "parent": 0},
                    {"id": 2, "label": "ergo", "role": "conjunction", "parent": 0},
                    {"id": 3, "label": "sum", "role": "verb", "parent": 0}
                ]
            }
        }
    ]

    # Insert Vocabulary
    for vocab_data in lesson_vocab:
        # Check if word exists
        statement = select(Word).where(Word.latin == vocab_data["latin"])
        word = session.exec(statement).first()
        
        if not word:
            word = Word(
                latin=vocab_data["latin"],
                translation=vocab_data["translation"],
                part_of_speech=vocab_data["part_of_speech"],
                declension=vocab_data.get("declension"),
                conjugation=vocab_data.get("conjugation"),
                gender=vocab_data.get("gender")
            )
            session.add(word)
            session.commit()
            session.refresh(word)
            print(f"  + Agregada palabra: {word.latin}")
        
        # Link to lesson
        statement = select(LessonVocabulary).where(
            LessonVocabulary.word_id == word.id,
            LessonVocabulary.lesson_number == vocab_data["lesson"]
        )
        link = session.exec(statement).first()
        
        if not link:
            link = LessonVocabulary(
                word_id=word.id,
                lesson_number=vocab_data["lesson"],
                is_essential=True
            )
            session.add(link)
            print(f"    -> Vinculada a Lección {vocab_data['lesson']}")

    # Insert Translation Sentences
    for sent_data in translation_sentences:
        statement = select(SentenceAnalysis).where(
            SentenceAnalysis.latin_text == sent_data["latin"]
        )
        sentence = session.exec(statement).first()
        
        if not sentence:
            sentence = SentenceAnalysis(
                latin_text=sent_data["latin"],
                spanish_translation=sent_data["spanish"],
                difficulty_level=sent_data["difficulty_level"],
                lesson_number=sent_data["lesson"]
            )
            session.add(sentence)
            print(f"  + Agregada oración: {sentence.latin_text[:30]}...")

    # Insert Syntax Sentences
    for syntax_data in syntax_sentences:
        statement = select(SentenceAnalysis).where(
            SentenceAnalysis.latin_text == syntax_data["latin_text"]
        )
        sentence = session.exec(statement).first()
        
        if not sentence:
            sentence = SentenceAnalysis(
                latin_text=syntax_data["latin_text"],
                spanish_translation=syntax_data["spanish_translation"],
                difficulty_level=syntax_data["difficulty_level"],
                lesson_number=syntax_data["lesson_number"],
                analysis_json=syntax_data["analysis_json"]
            )
            session.add(sentence)
            print(f"  + Agregada análisis: {sentence.latin_text[:30]}...")

    session.commit()
    print("✅ Población de Lecciones 31-40 completada.")

if __name__ == "__main__":
    with get_session() as session:
        seed_lessons_31_40(session)
