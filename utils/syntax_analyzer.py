"""
Utilidad para análisis sintáctico automático de oraciones latinas usando LatinCy
"""
import json
from typing import Optional, List, Dict
from database.syntax_models import SentenceAnalysis

try:
    import spacy
    from spacy import displacy
    LATINCY_AVAILABLE = True
except ImportError:
    LATINCY_AVAILABLE = False
    print("WARNING: LatinCy not installed. Run: pip install latincy && python -m spacy download la_core_web_md")


class LatinSyntaxAnalyzer:
    """Analiza oraciones latinas y extrae funciones sintácticas usando LatinCy"""
    
    def __init__(self, model_name: str = "la_core_web_md"):
        """
        Inicializa el analizador con el modelo de LatinCy
        
        Args:
            model_name: Nombre del modelo spaCy (la_core_web_sm, la_core_web_md, o la_core_web_lg)
        """
        if not LATINCY_AVAILABLE:
            raise ImportError("LatinCy no está instalado. Ejecuta: pip install latincy")
        
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Modelo {model_name} no encontrado. Descargando...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)
            self.nlp = spacy.load(model_name)
    
    def analyze_sentence(
        self,
        latin_text: str,
        translation: str = "",
        source: str = "",
        level: int = 1,
        lesson_number: Optional[int] = None
    ) -> SentenceAnalysis:
        """
        Analiza una oración latina y retorna objeto SentenceAnalysis
        
        Args:
            latin_text: Texto latino a analizar
            translation: Traducción al español
            source: Fuente del texto (e.g., "familia_romana_cap1")
            level: Nivel de complejidad 1-10
            lesson_number: Número de lección/capítulo
            
        Returns:
            Objeto SentenceAnalysis con análisis completo
        """
        # Procesar con LatinCy
        doc = self.nlp(latin_text)
        
        # Extraer árbol de dependencias
        dependency_tree = self._extract_dependencies(doc)
        
        # Mapear a funciones sintácticas
        syntax_roles = self._extract_syntax_roles(doc)
        
        # Detectar construcciones especiales
        constructions = self._detect_constructions(doc)
        
        # Clasificar tipo de oración
        sentence_type = self._classify_sentence(doc)
        
        # Generar diagrama SVG
        tree_svg = self._generate_tree_diagram(doc)
        
        # Crear y retornar objeto
        return SentenceAnalysis(
            latin_text=latin_text,
            spanish_translation=translation,
            complexity_level=level,
            sentence_type=sentence_type,
            source=source,
            lesson_number=lesson_number,
            dependency_json=json.dumps(dependency_tree, ensure_ascii=False),
            syntax_roles=json.dumps(syntax_roles, ensure_ascii=False),
            constructions=json.dumps(constructions, ensure_ascii=False) if constructions else None,
            tree_diagram_svg=tree_svg
        )
    
    def _extract_dependencies(self, doc) -> List[Dict]:
        """Extrae árbol de dependencias completo"""
        dependencies = []
        for token in doc:
            dependencies.append({
                "id": token.i,
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "dep": token.dep_,
                "head": token.head.i,
                "morph": str(token.morph)
            })
        return dependencies
    
    def _extract_syntax_roles(self, doc) -> Dict[str, List[int]]:
        """Mapea dependencias de spaCy a funciones sintácticas tradicionales"""
        roles = {
            "subject": [],
            "predicate": [],
            "direct_object": [],
            "indirect_object": [],
            "complement": [],
            "attribute": [],
            "apposition": []
        }
        
        for token in doc:
            # Sujeto
            if token.dep_ in ["nsubj", "csubj"]:
                roles["subject"].append(token.i)
            
            # Predicado (verbo principal)
            elif token.dep_ == "ROOT":
                roles["predicate"].append(token.i)
            
            # Objeto directo
            elif token.dep_ == "obj":
                roles["direct_object"].append(token.i)
            
            # Objeto indirecto
            elif token.dep_ == "iobj":
                roles["indirect_object"].append(token.i)
            
            # Complementos circunstanciales
            elif token.dep_ in ["obl", "advmod", "advcl"]:
                roles["complement"].append(token.i)
            
            # Atributos/Adjetivos
            elif token.dep_ in ["amod", "det"]:
                roles["attribute"].append(token.i)
            
            # Aposición
            elif token.dep_ == "appos":
                roles["apposition"].append(token.i)
        
        return roles
    
    def _detect_constructions(self, doc) -> List[str]:
        """Detecta construcciones sintácticas especiales del latín"""
        constructions = []
        
        # Ablativo absoluto: ABL + participio
        for token in doc:
            if token.morph.get("Case") == ["Abl"]:
                # Buscar participio dependiente
                for child in token.children:
                    if child.pos_ == "VERB" and "Part" in child.morph.get("VerbForm", []):
                        constructions.append("ablative_absolute")
                        break
        
        # Acusativo + Infinitivo
        for token in doc:
            if token.pos_ == "VERB" and "Inf" in token.morph.get("VerbForm", []):
                # Buscar acusativo como sujeto del infinitivo
                for child in token.children:
                    if child.morph.get("Case") == ["Acc"] and child.dep_ in ["nsubj", "obj"]:
                        constructions.append("accusative_infinitive")
                        break
        
        # Genitivo objetivo/subjetivo
       # (más complejo, requiere análisis semántico)
        
        # Dativo de posesión
        for token in doc:
            if token.dep_ == "iobj" and token.morph.get("Case") == ["Dat"]:
                # Verificar si el verbo es "sum"
                if token.head.lemma_ in ["sum", "esse"]:
                    constructions.append("dative_possession")
        
        return list(set(constructions))  # Eliminar duplicados
    
    def _classify_sentence(self, doc) -> str:
        """Clasifica el tipo de oración"""
        # Contar cláusulas (ROOT = verbo principal)
        root_count = len([t for t in doc if t.dep_ == "ROOT"])
        
        # Detectar subordinadas
        has_subordinate = any(t.dep_ in ["csubj", "ccomp", "advcl", "acl", "relcl"] 
                             for t in doc)
        
        # Detectar coordinación
        has_coordination = any(t.dep_ == "conj" for t in doc)
        
        if root_count == 1 and not has_subordinate and not has_coordination:
            return "simple"
        elif has_subordinate:
            return "complex"
        elif has_coordination:
            return "compound"
        else:
            return "simple"
    
    def _generate_tree_diagram(self, doc) -> str:
        """Genera diagrama de árbol de dependencias en formato SVG"""
        try:
            svg = displacy.render(doc, style="dep", options={
                "compact": True,
                "distance": 120,
                "word_spacing": 30,
                "font": "Cardo"
            })
            return svg
        except Exception as e:
            print(f"Error generando diagrama: {e}")
            return ""
    
    def batch_analyze(
        self,
        sentences: List[tuple],  # [(latin, translation, source, level), ...]
    ) -> List[SentenceAnalysis]:
        """
        Analiza múltiples oraciones en batch
        
        Args:
            sentences: Lista de tuplas (latin_text, translation, source, level)
            
        Returns:
            Lista de objetos SentenceAnalysis
        """
        results = []
        for item in sentences:
            latin = item[0]
            translation = item[1] if len(item) > 1 else ""
            source = item[2] if len(item) > 2 else ""
            level = item[3] if len(item) > 3 else 1
            
            analysis = self.analyze_sentence(latin, translation, source, level)
            results.append(analysis)
        
        return results
