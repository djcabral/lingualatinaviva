#!/usr/bin/env python3
"""
Script de Población - Etapa 3: Oraciones de Traducción
Genera oraciones de práctica de traducción para las Lecciones 1-5.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_session
from database import SentenceAnalysis
from sqlmodel import select

def seed_translation_sentences():
    print("🌱 Generando oraciones de traducción para Lecciones 1-10...")
    
    # Oraciones organizadas por lección y tema gramatical
    sentences = [
        # LECCIÓN 1: Nominativo y Acusativo (1ª y 2ª Declinación)
        {
            "lesson": 1,
            "sentences": [
                ("Rosa est pulchra.", "La rosa es hermosa."),
                ("Puella rosam amat.", "La niña ama la rosa."),
                ("Dominus servum vocat.", "El señor llama al esclavo."),
                ("Puellae rosas amant.", "Las niñas aman las rosas."),
                ("Servus dominum laudat.", "El esclavo alaba al señor."),
                ("Templum est magnum.", "El templo es grande."),
                ("Pueri templa vident.", "Los niños ven los templos."),
                ("Femina puellam vocat.", "La mujer llama a la niña."),
                ("Nautae navem portant.", "Los marineros llevan la nave."),
                ("Poeta carmina scribit.", "El poeta escribe poemas."),
            ]
        },
        
        # LECCIÓN 2: Genitivo y Dativo
        {
            "lesson": 2,
            "sentences": [
                ("Rosa puellae est pulchra.", "La rosa de la niña es hermosa."),
                ("Dominus servo donum dat.", "El señor da un regalo al esclavo."),
                ("Liber poetae est bonus.", "El libro del poeta es bueno."),
                ("Femina puellae rosam dat.", "La mujer da una rosa a la niña."),
                ("Filia domini est laeta.", "La hija del señor está alegre."),
                ("Nauta nautis pecuniam dat.", "El marinero da dinero a los marineros."),
                ("Templum deorum est magnum.", "El templo de los dioses es grande."),
                ("Puer puero librum dat.", "El niño da un libro al niño."),
                ("Servi dominorum laborant.", "Los esclavos de los señores trabajan."),
                ("Feminae feminis dona dant.", "Las mujeres dan regalos a las mujeres."),
            ]
        },
        
        # LECCIÓN 3: Ablativo y Vocativo
        {
            "lesson": 3,
            "sentences": [
                ("Puella cum amica ambulat.", "La niña camina con la amiga."),
                ("Serve, veni ad dominum!", "¡Esclavo, ven al señor!"),
                ("Poeta carmina magna voce cantat.", "El poeta canta poemas en voz alta."),
                ("Domine, servus te vocat.", "Señor, el esclavo te llama."),
                ("Femina cum pueris venit.", "La mujer viene con los niños."),
                ("Nauta in nave laborat.", "El marinero trabaja en la nave."),
                ("Puellae, rosae sunt pulchrae!", "¡Niñas, las rosas son hermosas!"),
                ("Puer gladio pugnat.", "El niño lucha con la espada."),
                ("Amice, librum mihi da!", "¡Amigo, dame el libro!"),
                ("Servi in agris laborant.", "Los esclavos trabajan en los campos."),
            ]
        },
        
        # LECCIÓN 4: Presente de Indicativo (1ª y 2ª Conjugación)
        {
            "lesson": 4,
            "sentences": [
                ("Amo rosas pulchras.", "Amo las rosas hermosas."),
                ("Puella cantat et laudat.", "La niña canta y alaba."),
                ("Servi laborant in agris.", "Los esclavos trabajan en los campos."),
                ("Moneo puerum de periculo.", "Advierto al niño del peligro."),
                ("Habemus multos amicos.", "Tenemos muchos amigos."),
                ("Nautae navigant in mari.", "Los marineros navegan en el mar."),
                ("Video stellas in caelo.", "Veo las estrellas en el cielo."),
                ("Puellae rosas portant.", "Las niñas llevan rosas."),
                ("Dominus servos vocat.", "El señor llama a los esclavos."),
                ("Timemus hostes fortes.", "Tememos a los enemigos fuertes."),
            ]
        },
        
        # LECCIÓN 5: 3ª Declinación
        {
            "lesson": 5,
            "sentences": [
                ("Rex milites ducit.", "El rey conduce a los soldados."),
                ("Miles gladio pugnat.", "El soldado lucha con la espada."),
                ("Urbs est magna et pulchra.", "La ciudad es grande y hermosa."),
                ("Corpus militis est forte.", "El cuerpo del soldado es fuerte."),
                ("Reges urbium conveniunt.", "Los reyes de las ciudades se reúnen."),
                ("Milites regis pugnant.", "Los soldados del rey luchan."),
                ("In urbe sunt multa templa.", "En la ciudad hay muchos templos."),
                ("Rex urbem regit.", "El rey gobierna la ciudad."),
                ("Corpora militum sunt fortia.", "Los cuerpos de los soldados son fuertes."),
                ("Urbes regum sunt magnae.", "Las ciudades de los reyes son grandes."),
            ]
        },
        
        # LECCIÓN 6: Consolidación y Adjetivos
        {
            "lesson": 6,
            "sentences": [
                ("Puella bona est.", "La niña es buena."),
                ("Magnus rex regnum regit.", "El gran rey gobierna el reino."),
                ("Victoria gloriosa est.", "La victoria es gloriosa."),
                ("Memoria bonorum est pulchra.", "La memoria de los buenos es hermosa."),
                ("Liberi pueri ludunt.", "Los niños libres juegan."),
                ("Fortuna magna nos iuvat.", "La gran fortuna nos ayuda."),
                ("Pulchrae rosae in horto sunt.", "Las rosas hermosas están en el jardín."),
                ("Bonus dominus servos curat.", "El buen señor cuida a los esclavos."),
                ("Credimus in victoriam.", "Creemos en la victoria."),
                ("Magna gloria militum parat.", "La gran gloria prepara a los soldados."),
            ]
        },
        
        # LECCIÓN 7: 3ª Declinación y Dativo
        {
            "lesson": 7,
            "sentences": [
                ("Dux militibus pacem dat.", "El líder da paz a los soldados."),
                ("Lex urbis est dura.", "La ley de la ciudad es dura."),
                ("Pax hominibus grata est.", "La paz es grata a los hombres."),
                ("Nox obscura lux clarior.", "Después de la noche oscura, la luz es más clara."),
                ("Dico veritatem amicis.", "Digo la verdad a mis amigos."),
                ("Facio opus magnum.", "Hago una gran obra."),
                ("Dux agit cum sapientia.", "El líder actúa con sabiduría."),
                ("Capio multas praedas.", "Tomo muchos botínes."),
                ("Lux pacis in nocte fulget.", "La luz de la paz brilla en la noche."),
                ("Leges populorum sunt variae.", "Las leyes de los pueblos son variadas."),
            ]
        },
        
        # LECCIÓN 8: 4ª Declinación y Pasado
        {
            "lesson": 8,
            "sentences": [
                ("Dominus servum liberavit.", "El señor liberó al esclavo."),
                ("Manus exercitus fortes fuerunt.", "Las manos del ejército fueron fuertes."),
                ("In domu magna habitavi.", "Habité en una gran casa."),
                ("Exercitus hostes vicit.", "El ejército venció a los enemigos."),
                ("Fructus arboris bonus fuit.", "El fruto del árbol fue bueno."),
                ("Fui in urbe Romana.", "Estuve en la ciudad romana."),
                ("Multos libros habui.", "Tuve muchos libros."),
                ("Ad domum veni celeriter.", "Vine a casa rápidamente."),
                ("Manus militis gladium tenuit.", "La mano del soldado sostuvo la espada."),
                ("Exercitus Romanus pugnavít fortiter.", "El ejército romano luchó valientemente."),
            ]
        },
        
        # LECCIÓN 9: 5ª Declinación y Futuro
        {
            "lesson": 9,
            "sentences": [
                ("Rex urbem reget.", "El rey gobernará la ciudad."),
                ("Dies clara erit.", "El día será claro."),
                ("Res publica florebit.", "La república florecerá."),
                ("Spes victoriae nos sustinet.", "La esperanza de victoria nos sostiene."),
                ("Fides populi firma erit.", "La fe del pueblo será firme."),
                ("Ero fortis in bello.", "Seré fuerte en la guerra."),
                ("Habebimus pacem post victoriam.", "Tendremos paz después de la victoria."),
                ("Veniam ad te cras.", "Vendré a ti mañana."),
                ("Dies meliores venient.", "Vendrán días mejores."),
                ("Magna spes in corde manebit.", "Una gran esperanza permanecerá en el corazón."),
            ]
        },
        
        # LECCIÓN 10: Adjetivos de 2ª Clase
        {
            "lesson": 10,
            "sentences": [
                ("Miles fortis pugnat.", "El soldado valiente lucha."),
                ("Brevis vita est.", "La vida es breve."),
                ("Tristis historia nos movet.", "La historia triste nos conmueve."),
                ("Acer vir in proelio stat.", "El hombre ardiente permanece en la batalla."),
                ("Facilis via ducit ad urbem.", "El camino fácil conduce a la ciudad."),
                ("Fortes milites vincunt.", "Los soldados valientes vencen."),
                ("Breves dies fugaces sunt.", "Los días breves son fugaces."),
                ("Tristis nuntius venit.", "Llega una noticia triste."),
                ("Viri acres non cedunt.", "Los hombres ardientes no ceden."),
                ("Faciles artes discimus.", "Aprendemos las artes fáciles."),
            ]
        },
    ]
    
    with get_session() as session:
        added = 0
        
        for lesson_data in sentences:
            lesson_num = lesson_data["lesson"]
            
            for latin, spanish in lesson_data["sentences"]:
                # Check if sentence already exists
                existing = session.exec(
                    select(SentenceAnalysis).where(
                        SentenceAnalysis.latin_text == latin
                    )
                ).first()
                
                if not existing:
                    sentence = SentenceAnalysis(
                        latin_text=latin,
                        spanish_translation=spanish,
                        lesson_number=lesson_num,
                        complexity_level=lesson_num,  # Complexity increases with lesson
                        sentence_type="simple",
                        source=f"lesson_{lesson_num}_exercises",
                        usage_type="translation_exercise",  # NEW FIELD
                        verified=True
                    )
                    session.add(sentence)
                    added += 1
        
        session.commit()
        
        print(f"✅ Oraciones de traducción creadas: {added}")
        
        # Summary
        print("\n📊 Resumen por Lección:")
        for lesson_data in sentences:
            lesson_num = lesson_data["lesson"]
            count = len(lesson_data["sentences"])
            print(f"   Lección {lesson_num}: {count} oraciones")

if __name__ == "__main__":
    seed_translation_sentences()
