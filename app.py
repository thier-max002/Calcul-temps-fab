import streamlit as st
import os
from fpdf import FPDF
import base64

st.set_page_config(page_title="Calculateur Menuiserie", layout="centered")

# Code pour masquer le menu GitHub et le pied de page
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.set_page_config(page_title="Calculateur Menuiserie - PDF Edition", layout="centered")

# --- 1. BASE DE DONNÉES COMPLÈTE ---
DATABASE = {
    "SCHÜCO": {
        "Fenêtre AWS 60 /BD": {
            "types": {"Oscillo-battant 1 vantail": 2.0, "Oscillo-battant 2 vantaux": 3.0, "Fixe": 0.75, "Française 1 vantail": 1.5, "Française 2 vantaux": 2.5},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Grilles Air Frais": 0.33, "Mise en place profil en T pour composé": 0.25, "Fixation de composé": 0.5, "Fabrication et vitrage ouvrant parcloses par vtl": 0.25, "TH3 sur coulissant": 0.5, "Vitrage ouvrant caché": 0.16}
        },
        "Porte ADS 60": {
            "types": {"Porte 1 vantail": 4.0, "Porte 2 vantaux": 7.5, "Coulissant 2 vantaux": 2.0, "Coulissant 3 vantaux": 2.5, "Coulissant 4 vantaux": 3.0, "Galandage 1 vantail": 3.5, "Galandage 2 vantaux sur 1 côté": 4.0, "Galandage 2 vantaux sur 2 côté": 4.5},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Bandeau serrure dans ouvrant caché": 2.0, "Ferme porte": 0.33, "Bâton maréchal": 0.5, "Verrouillage semi fixe": 0.5, "Seuil PMR ou seuil plat frappé": 0.5, "Serrure 3 points": 0.5}
        },
        "Porte fenêtre": {
            "types": {"1 vantail": 2.0},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Grilles Air Frais": 0.33, "Bandeau serrure dans ouvrant caché": 2.0, "Ferme porte": 0.33, "Bâton maréchal": 0.5, "Verrouillage semi fixe": 0.5, "Seuil PMR ou seuil plat frappé": 0.5, "Seuil sur coulissant": 1.0, "Serrure 3 points": 0.5, "Bandeau ventouse 1 vantail ": 0.33, "Bandeau ventouse 2 vantail": 0.75}
        },
        "ASS 39 SC": {
            "types": {"Coulissant 1 vantail": 1.50, "Coulissant 2 vantaux": 3.0},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Grilles Air Frais": 0.33, "Bandeau serrure dans ouvrant caché": 2.0, "Ferme porte": 0.33, "Bâton maréchal": 0.5, "Verrouillage semi fixe": 0.5, "Seuil PMR ou seuil plat frappé": 0.5, "Seuil sur coulissant": 1.0, "Serrure 3 points": 0.5, "Bandeau ventouse 1 vantail ": 0.33, "Bandeau ventouse 2 vantail": 0.75}
        },
        "ASS 41 SC": {
            "types": {"Coulissant 2 vantaux": 2.0, "Coulissant 4 vantaux": 3.0, "Coulissant 6 vantaux":4.0 },
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Grilles Air Frais": 0.33, "Bandeau serrure dans ouvrant caché": 2.0, "Ferme porte": 0.33, "Bâton maréchal": 0.5, "Verrouillage semi fixe": 0.5, "Seuil PMR ou seuil plat frappé": 0.5, "Seuil sur coulissant": 1.0, "Serrure 3 points": 0.5, "Bandeau ventouse 1 vantail ": 0.33, "Bandeau ventouse 2 vantail": 0.75}
        }
    },
    "PAAL 52": {
        "Fenêtre": {
            "types": {"Séparation":0.5, "Fixe": 0.75, "Française 1 vantail": 1.5, "Française 2 vantaux": 2.5, "Oscillo-battant 1 vantail": 2.0, "Oscillo-battant 2 vantaux": 3.0},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Grilles Air Frais": 0.33, "Mise en place profil en T pour composé": 0.25, "Fixation de composé": 0.5, "Vitrage ouvrant portefeuille": 0.25, "1 Traverse": 0.15, "2 Traverses": 0.3, "3 Traverses": 0.45, "1 Montant": 0.15, "2 Montants": 0.3, "3 Montants": 0.45}
        },
        "Porte": {
            "types": {"Porte 1 vantail": 4.0, "Porte 2 vantaux": 6.0, "Coulissant 2 vantaux": 2.0, "Coulissant 3 vantaux": 2.5, "Coulissant 4 vantaux": 3.0, "Galandage 1 vantail": 3.5, "Galandage 2 vantaux sur 1 côté": 4.0, "Galandage 2 vantaux sur 2 côtés": 4.5},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Bandeau ventouse 1 vtl": 0.33, "Bandeau ventouse 2 vantaux": 0.75, "Ferme porte": 0.33, "Bâton maréchal": 0.5, "Verrouillage semi fixe": 0.1, "Seuil PMR ou seuil plat frappé": 0.5}
        },
        "Persienne": {
            "types": {"Persiennes nue (temps par VTL)": 1.0, "Persiennes équipées (temps par VTL)": 1.25},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Grilles Air Frais": 0.33, "Fixation de composé": 0.5, "Verrouillage semi fixe": 0.1, "Ferméture encastré pour persiennes ": 0.5}
        }
    },
    "PAAL 70": {
        "Fenêtre": {
            "types": {"Fixe": 1.0, "Française 1 vantail": 1.75, "Française 2 vantaux": 2.75, "Oscillo-battant 1 vantail": 2.25, "Oscillo-battant 2 vantaux": 3.25},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Grilles Air Frais": 0.33, "Mise en place profil en T pour composé": 0.25, "Fixation de composé": 0.5, "Vitrage ouvrant caché": 0.16, "Fabrication et vitrage ouvrant parcloses par vantail": 0.25, "1 Traverse": 0.15, "2 Traverses": 0.3, "3 Traverses": 0.45, "1 Montant": 0.15, "2 Montants": 0.3, "3 Montants": 0.45}
        },
        "Porte": {
            "types": {"Porte 2 vantaux": 7.5, "Coulissant 2 vantaux": 2.25, "Coulissant 3 vantaux": 2.75, "Coulissant 4 vantaux": 3.25, "Galandage 1 vantail": 3.5, "Galandage 2 vantaux sur 1 côté": 4.0, "Galandage 2 vantaux sur 2 côtés": 4.5},
            "options": {"Couvre joint à cliper": 0.16, "Tapée + pattes de fixation 3 côtés": 0.33, "Tapée + pattes de fixation 4 côtés": 0.5, "Bandeau ventouse 1 vtl": 0.33, "Bandeau ventouse 2 vantaux": 0.75, "Bandeau serrure ouvrant caché": 1.0, "Serrure 3 points": 0.5, "Ferme porte": 0.33, "Bâton maréchal": 0.5, "Verrouillage semi fixe": 0.1, "Seuil PMR ou seuil plat frappé": 0.5}
        }
    }
}

# --- 2. GESTION DE L'ÉTAT ET FONCTION PDF ---
if "calcul_fait" not in st.session_state:
    st.session_state.calcul_fait = False

def create_pdf(gamme, serie, type_m, options, qte, t_unit, t_total):
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Logo (si présent)
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 8, 33)
    
    # 2. Titre
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "FICHE D'ESTIMATION TEMPS ATELIER", 0, 1, 'C')
    pdf.ln(10)
    
    # 3. Informations Générales
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Gamme : {gamme}", 0, 1)
    pdf.cell(0, 8, f"Serie : {serie}", 0, 1)
    pdf.cell(0, 8, f"Menuiserie : {type_m}", 0, 1)
    pdf.cell(0, 8, f"Quantite : {qte}", 0, 1)
    pdf.ln(5)
    
    # 4. Détail des temps
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240) # Fond gris clair pour l'entête
    pdf.cell(0, 10, " DETAIL DES TEMPS :", 0, 1, 'L', fill=True)
    
    pdf.set_font("Arial", '', 11)
    t_base = DATABASE[gamme][serie]['types'][type_m]
    pdf.cell(0, 8, f" - Temps de base : {t_base} h", 0, 1)
    
    for opt in options:
        val = DATABASE[gamme][serie]['options'][opt]
        pdf.cell(0, 8, f" - Option {opt} : +{val} h", 0, 1)
    
    # --- LA MODIFICATION ICI : AJOUT DU TOTAL UNITAIRE ---
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f" >> TOTAL PAR UNITE : {t_unit:.2f} h", 0, 1)
    pdf.write(0, "_" * 50) # Petite ligne de séparation
    pdf.ln(8)
    
    # 5. Total Global
    pdf.set_font("Arial", 'B', 14)
    if qte > 1:
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, f"Calcul : {t_unit:.2f}h x {qte} unites", 0, 1, 'R')
    
    pdf.set_text_color(200, 0, 0) # Rouge pour le total final
    pdf.cell(0, 10, f"TOTAL GLOBAL CHANTIER : {t_total:.2f} HEURES", 0, 1, 'R')
    
    # Retourner en bytes pour Streamlit
    return bytes(pdf.output())

# --- 3. INTERFACE ---
image_path = 'logo.png'
if os.path.exists(image_path):
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2: st.image(image_path, width=200)

st.title("Estimation Temps de Fabrication")

col1, col2 = st.columns(2)
with col1:
    gamme_choisie = st.selectbox("Gamme", [""] + list(DATABASE.keys()))
    serie_nom = ""
    if gamme_choisie:
        serie_nom = st.selectbox("Série", [""] + list(DATABASE[gamme_choisie].keys()))
    quantite = st.number_input("Quantité", min_value=1, value=1)

if gamme_choisie and serie_nom:
    donnees = DATABASE[gamme_choisie][serie_nom]
    with col2:
        type_nom = st.selectbox("Type de menuiserie", [""] + list(donnees["types"].keys()))
        options_choisies = st.multiselect("Options", list(donnees["options"].keys()))

    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 Calculer le temps", use_container_width=True):
            if type_nom: st.session_state.calcul_fait = True
            else: st.error("Sélectionnez un type")
    with c2:
        if st.button("🔄 Recommencer", use_container_width=True):
            st.session_state.calcul_fait = False
            st.rerun()

    if st.session_state.calcul_fait:
        t_base = donnees["types"][type_nom]
        t_opt = sum([donnees["options"][o] for o in options_choisies])
        t_unitaire = t_base + t_opt
        t_total = t_unitaire * quantite


    # --- 5. AFFICHAGE DU RÉSULTAT ---
    if st.session_state.calcul_fait:
        t_base = donnees["types"][type_nom]
        t_opt = sum([donnees["options"][o] for o in options_choisies])
        t_unitaire = t_base + t_opt
        t_total = t_unitaire * quantite

        # Affichage du score principal
        st.success(f"### Résultat : {t_total:.2f} heures")
        
        # --- RÉAFFICHAGE DES DÉTAILS ---
        if quantite > 1:
            st.info(f"💡 Détail : {t_unitaire:.2f}h par unité × {quantite} unités")
        
        with st.expander("🔍 Détail du calcul ", expanded=True):
            st.write(f"**Gamme :** {gamme_choisie}")
            st.write(f"**Série :** {serie_nom}")
            st.write(f"**Type choisi :** {type_nom} ({t_base}h)")
            
            if options_choisies:
                st.write("**Options sélectionnées :**")
                for opt in options_choisies:
                    val_opt = donnees["options"][opt]
                    st.write(f"  - {opt} : +{val_opt}h")
            else:
                st.write("*Aucune option sélectionnée*")
        
        st.write("") # Petit espace

        # --- BOUTON TÉLÉCHARGEMENT PDF ---
        # On s'assure de bien convertir en bytes pour éviter l'erreur précédente
        pdf_bytes = bytes(create_pdf(gamme_choisie, serie_nom, type_nom, options_choisies, quantite, t_unitaire, t_total))
        
        st.download_button(
            label="📥 Télécharger la Fiche PDF",
            data=pdf_bytes,
            file_name=f"Fiche_{type_nom.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )