import streamlit as st
import os
from fpdf import FPDF
import base64

st.set_page_config(page_title="Calculateur Menuiserie", layout="centered")

# Code pour masquer le menu GitHub et le pied de page + REMONTER LE LOGO
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Cette ligne aspire le logo vers le haut de la page */
        .stImage { margin-top: -60px; } 
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



#1.BASE DE DONNEES
DATABASE = {
    "PAAL": {
        "PAAL 52": {
            "Coulissant": {
                "types": {
                    "Coulissant 2 vantaux": 2.0,
                    "Coulissant 3 vantaux": 2.5,
                    "Coulissant 4 vantaux": 3.0,
                    "Galandage 1 vantail": 3.5,
                    "Galandage 2 vantaux sur 1 côté": 4.0,
                    "Galandage 2 vantaux sur 2 côtés": 4.5
                },
                "options": {
                    "Couvre joint à cliper": 0.16,
                    "Fabrication et vitrage ouvrant parcloses par vtl": 0.25,
                    "Fixation de composé": 0.5,
                    "Grilles Air Frais": 0.33,
                    "Mise en place profil en T pour composé": 0.25,
                    "Seuil PMR sur coulissant": 1.0,
                    "TH3 sur coulissant": 0.5,
                    "Tapée + pattes de fixation 3 côtés": 0.33,
                    "Tapée + pattes de fixation 4 côtés": 0.5,
                    "Vitrage ouvrant caché": 0.16
                }
            },
            "Fenêtre": {
                "types": {
                    "Fixe": 0.75,
                    "Française 1 vantail": 1.5,
                    "Française 2 vantaux": 2.5,
                    "Oscillo-battant 1 vantail": 2.0,
                    "Oscillo-battant 2 vantaux": 3.0,
                    "Séparation": 0.5
                },
                "options": {
                    "1 Montant": 0.15,
                    "1 Traverse": 0.15,
                    "2 Montants": 0.3,
                    "2 Traverses": 0.3,
                    "3 Montants": 0.45,
                    "3 Traverses": 0.45,
                    "Bandeau serrure dans ouvrant caché": 2.0,
                    "Couvre joint à cliper": 0.16,
                    "Fabrication et vitrage ouvrant parcloses par vtl": 0.25,
                    "Fixation de composé": 0.5,
                    "Grilles Air Frais": 0.33,
                    "Mise en place profil en T pour composé": 0.25,
                    "Seuil PMR ou seuil plat frappe": 0.5,
                    "Tapée + pattes de fixation 3 côtés": 0.33,
                    "Tapée + pattes de fixation 4 côtés": 0.5,
                    "Verrouillage semi fixe": 0.1,
                    "Vitrage ouvrant caché": 0.16,
                    "Vitrage ouvrant portefeuille": 0.25
                }
            },
            "Persienne": {
                "types": {
                    "Persiennes équipées (temps par VTL)": 1.25,
                    "Persiennes nue (temps par VTL)": 1.0
                },
                "options": {
                    "Couvre joint à cliper": 0.16,
                    "Fabrication et vitrage ouvrant parcloses par vantail": 0.25,
                    "Fixation de composé": 0.5,
                    "Ferméture encastré pour persiennes ": 0.5,
                    "Grilles Air Frais": 0.33,
                    "Mise en place profil en T pour composé": 0.25,
                    "Seuil PMR ou seuil plat frappe": 0.5,
                    "Tapée + pattes de fixation 3 côtés": 0.33,
                    "Tapée + pattes de fixation 4 côtés": 0.5,
                    "Verrouillage semi fixe": 0.5,
                    "Vitrage ouvrant caché": 0.16
                }
            },
            "Porte": {
                "types": {
                    "Porte 1 vantail": 4.0,
                    "Porte 2 vantaux": 6.0
                },
                "options": {
                    "Bandeau serrure dans ouvrant caché": 2.0,
                    "Bandeau ventouse 1 vantail": 0.33,
                    "Bandeau ventouse 2 vantaux": 0.75,
                    "Bâton maréchal": 0.5,
                    "Couvre joint à cliper": 0.16,
                    "Fabrication et vitrage ouvrant parcloses par vtl": 0.25,
                    "Ferme porte": 0.33,
                    "Fixation de composé": 0.5,
                    "Grilles Air Frais": 0.33,
                    "Mise en place profil en T pour composé": 0.25,
                    "Serrure 3 points": 0.5,
                    "Seuil PMR ou seuil plat frappe": 0.5,
                    "Tapée + pattes de fixation 3 côtés": 0.33,
                    "Tapée + pattes de fixation 4 côtés": 0.5,
                    "Verrouillage semi fixe": 0.5,
                    "Vitrage ouvrant caché": 0.16
                }
            }
        },
        "PAAL 70": {
            "Coulissant": {
                "types": {
                    "Coulissant 2 vantaux": 2.25,
                    "Coulissant 3 vantaux": 2.75,
                    "Coulissant 4 vantaux": 3.25,
                    "Galandage 1 vantail": 3.5,
                    "Galandage 2 vantaux sur 1 côté": 4.0,
                    "Galandage 2 vantaux sur 2 côtés": 4.5
                },
                "options": {
                    "Bandeau serrure dans ouvrant caché": 2.0,
                    "Couvre joint à cliper": 0.16,
                    "Fabrication et vitrage ouvrant par vtl": 0.25,
                    "Fixation de composé": 0.5,
                    "Grilles Air Frais": 0.33,
                    "Mise en place profil en T pour composé": 0.25,
                    "Seuil PMR sur coulissant": 1.0,
                    "TH3 sur coulissant": 0.5,
                    "Tapée + pattes de fixation 3 côtés": 0.33,
                    "Tapée + pattes de fixation 4 côtés": 0.5,
                    "Vitrage ouvrant caché": 0.16
                }
            },
            "Fenêtre": {
                "types": {
                    "Fixe": 1.0,
                    "Française 1 vantail": 1.75,
                    "Française 2 vantaux": 2.75,
                    "Oscillo-battant 1 vantail": 2.25,
                    "Oscillo-battant 2 vantaux": 3.25
                },
                "options": {
                    "1 Montant": 0.15,
                    "1 Traverse": 0.15,
                    "2 Montants": 0.3,
                    "2 Traverses": 0.3,
                    "3 Montants": 0.45,
                    "3 Traverses": 0.45,
                    "Couvre joint à cliper": 0.16,
                    "Fabrication et vitrage ouvrant parcloses par vantail": 0.25,
                    "Fixation de composé": 0.5,
                    "Grilles Air Frais": 0.33,
                    "Mise en place profil en T pour composé": 0.25,
                    "Seuil PMR ou seuil plat frappe": 0.5,
                    "Tapée + pattes de fixation 3 côtés": 0.33,
                    "Tapée + pattes de fixation 4 côtés": 0.5,
                    "Verrouillage semi fixe": 0.5,
                    "Vitrage ouvrant caché": 0.16
                }
            },
            "Porte": {
                "types": {
                    "Porte 1 vantail": 4.0,
                    "Porte 2 vantaux": 7.5
                },
                "options": {
                    "Bandeau serrure dans ouvrant caché": 2.0,
                    "Bandeau ventouse 1 vantail": 0.33,
                    "Bandeau ventouse 2 vantaux": 0.75,
                    "Bâton maréchal": 0.5,
                    "Couvre joint à cliper": 0.16,
                    "Fabrication et vitrage ouvrant par vtl": 0.25,
                    "Ferme porte": 0.33,
                    "Fixation de composé": 0.5,
                    "Grilles Air Frais": 0.33,
                    "Mise en place profil en T pour composé": 0.25,
                    "Serrure 3 points": 0.5,
                    "Seuil PMR ou seuil plat frappe": 0.5,
                    "Tapée + pattes de fixation 3 côtés": 0.33,
                    "Tapée + pattes de fixation 4 côtés": 0.5,
                    "Verrouillage semi fixe": 0.5,
                    "Vitrage ouvrant caché": 0.16
                }
            }
        }
    },
    "SCHÜCO": {
        "ASS 39 SC": {
            "types": {
                "Coulissant 2 vantaux": 2.0,
                "Coulissant 3 vantaux": 2.5,
                "Coulissant 4 vantaux": 3.0,
                "Galandage 1 vantail": 3.5,
                "Galandage 2 vantaux sur 1 côté": 4.0,
                "Galandage 2 vantaux sur 2 côté": 4.5
            },
            "options": {
                "Bandeau serrure dans ouvrant caché": 2.0,
                "Couvre joint à cliper": 0.16,
                "Fabrication et vitrage ouvrant parcloses par vtl": 0.25,
                "Fixation de composé": 0.5,
                "Grilles Air Frais": 0.33,
                "Mise en place profil en T pour composé": 0.25,
                "Seuil PMR sur coulissant": 1.0,
                "TH3 sur coulissant": 0.5,
                "Tapée + pattes de fixation 3 côtés": 0.33,
                "Tapée + pattes de fixation 4 côtés": 0.5,
                "Vitrage ouvrant caché": 0.16
            }
        },
        "ASS 41 SC": {
            "types": {
                "Coulissant 2 vantaux": 2.0,
                "Coulissant 3 vantaux": 2.5,
                "Coulissant 4 vantaux": 3.0,
                "Coulissant 6 vantaux": 4.0,
                "Galandage 1 vantail": 3.5,
                "Galandage 2 vantaux sur 1 côté": 4.0,
                "Galandage 2 vantaux sur 2 côté": 4.5
            },
            "options": {
                "Bandeau serrure dans ouvrant caché": 2.0,
                "Couvre joint à cliper": 0.16,
                "Fabrication et vitrage ouvrant parcloses par vtl": 0.25,
                "Fixation de composé": 0.5,
                "Grilles Air Frais": 0.33,
                "Mise en place profil en T pour composé": 0.25,
                "Seuil PMR sur coulissant": 1.0,
                "TH3 sur coulissant": 0.5,
                "Tapée + pattes de fixation 3 côtés": 0.33,
                "Tapée + pattes de fixation 4 côtés": 0.5,
                "Vitrage ouvrant caché": 0.16
            }
        },
        "Fenêtre AWS 60 /BD": {
            "types": {
                "Fixe": 0.75,
                "Française 1 vantail": 1.5,
                "Française 2 vantaux": 2.5,
                "Oscillo-battant 1 vantail": 2.0,
                "Oscillo-battant 2 vantaux": 3.0
            },
            "options": {
                "Bandeau serrure dans ouvrant caché": 2.0,
                "Couvre joint à cliper": 0.16,
                "Fabrication et vitrage ouvrant parcloses par vtl": 0.25,
                "Fixation de composé": 0.5,
                "Grilles Air Frais": 0.33,
                "Mise en place profil en T pour composé": 0.25,
                "Seuil PMR ou seuil plat frappe": 0.5,
                "Tapée + pattes de fixation 3 côtés": 0.33,
                "Tapée + pattes de fixation 4 côtés": 0.5,
                "Verrouillage semi fixe": 0.1,
                "Vitrage ouvrant caché": 0.16
            }
        },
        "Porte ADS 60": {
            "types": {
                "Porte 1 vantail": 4.0,
                "Porte 2 vantaux": 7.5
            },
            "options": {
                "Bandeau serrure dans ouvrant caché": 2.0,
                "Bandeau ventouse 1 vantail": 0.33,
                "Bandeau ventouse 2 vantaux": 0.75,
                "Bâton maréchal": 0.5,
                "Couvre joint à cliper": 0.16,
                "Fabrication et vitrage ouvrant parcloses par vtl": 0.25,
                "Ferme porte": 0.33,
                "Fixation de composé": 0.5,
                "Grilles Air Frais": 0.33,
                "Mise en place profil en T pour composé": 0.25,
                "Serrure 3 points": 0.5,
                "Seuil PMR ou seuil plat frappe": 0.5,
                "Tapée + pattes de fixation 3 côtés": 0.33,
                "Tapée + pattes de fixation 4 côtés": 0.5,
                "Verrouillage semi fixe": 0.5,
                "Vitrage ouvrant caché": 0.16
            }
        },
        "Porte fenêtre": {
            "types": {
                "1 vantail": 2.0
            },
            "options": {
                "Bandeau serrure dans ouvrant caché": 2.0,
                "Bandeau ventouse 1 vantail": 0.33,
                "Bandeau ventouse 2 vantaux": 0.75,
                "Bâton maréchal": 0.5,
                "Couvre joint à cliper": 0.16,
                "Fabrication et vitrage ouvrant parcloses par vtl": 0.25,
                "Ferme porte": 0.33,
                "Fixation de composé": 0.5,
                "Grilles Air Frais": 0.33,
                "Mise en place profil en T pour composé": 0.25,
                "Serrure 3 points": 0.5,
                "Seuil PMR ou seuil plat frappe": 0.5,
                "Tapée + pattes de fixation 3 côtés": 0.33,
                "Tapée + pattes de fixation 4 côtés": 0.5,
                "Verrouillage semi fixe": 0.5,
                "Vitrage ouvrant caché": 0.16
            }
        }
    }
}







# ***********************************************A NE PAS TOUCHER *****************************************************#

# --- 2. GESTION DE L'ÉTAT ET FONCTION PDF ---
if "calcul_fait" not in st.session_state:
    st.session_state.calcul_fait = False

def create_pdf(gamme_p, sous_g, serie, type_m, options, qte, t_unit, t_total):
    pdf = FPDF()
    pdf.add_page()
    
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 8, 33)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "FICHE D'ESTIMATION TEMPS ATELIER", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 12)
    # Affichage intelligent du nom de la gamme dans le PDF
    libelle_gamme = f"{gamme_p} ({sous_g})" if sous_g else gamme_p
    pdf.cell(0, 8, f"Gamme : {libelle_gamme}", 0, 1)
    pdf.cell(0, 8, f"Serie : {serie}", 0, 1)
    pdf.cell(0, 8, f"Menuiserie : {type_m}", 0, 1)
    pdf.cell(0, 8, f"Quantite : {qte}", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, " DETAIL DES TEMPS :", 0, 1, 'L', fill=True)
    
    pdf.set_font("Arial", '', 11)
    
    # Ciblage correct de la BDD pour le PDF
    if sous_g:
        donnees_pdf = DATABASE["PAAL"][sous_g][serie]
    else:
        donnees_pdf = DATABASE["SCHÜCO"][serie]
        
    t_base = donnees_pdf['types'][type_m]
    pdf.cell(0, 8, f" - Temps de base : {t_base} h", 0, 1)
    
    for opt in options:
        val = donnees_pdf['options'][opt]
        pdf.cell(0, 8, f" - Option {opt} : +{val} h", 0, 1)
    
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f" >> TOTAL PAR UNITE : {t_unit:.2f} h", 0, 1)
    pdf.write(0, "_" * 50)
    pdf.ln(8)
    
    pdf.set_font("Arial", 'B', 14)
    if qte > 1:
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, f"Calcul : {t_unit:.2f}h x {qte} unites", 0, 1, 'R')
    
    pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 10, f"TOTAL GLOBAL CHANTIER : {t_total:.2f} HEURES", 0, 1, 'R')
    
    return bytes(pdf.output())

# --- 3. INTERFACE (LOGO COMPACT ET TITRE CENTRÉS) ---
image_path = 'logo.png'

if os.path.exists(image_path):
    _, _, col_logo, _, _ = st.columns([2, 1, 2, 1, 2])
    with col_logo:
        st.image(image_path, width=140)

st.markdown("<h1 style='text-align: center; margin-top: -5px; margin-bottom: 0px;'>Estimation Temps de Fabrication</h1>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("---")


# --- 4. CONFIGURATEUR DYNAMIQUE ---
col1, col2 = st.columns(2)
with col1:
    gamme_choisie = st.selectbox("Gamme", [""] + list(DATABASE.keys()))
    
    # Variables de contrôle indispensables
    sous_gamme_choisie = ""
    serie_nom = ""
    donnees = None

    if gamme_choisie == "PAAL":
        # Étape intermédiaire spécifique pour PAAL
        sous_gamme_choisie = st.selectbox("Version PAAL", [""] + list(DATABASE["PAAL"].keys()))
        if sous_gamme_choisie:
            serie_nom = st.selectbox("Série", [""] + list(DATABASE["PAAL"][sous_gamme_choisie].keys()))
            if serie_nom:
                donnees = DATABASE["PAAL"][sous_gamme_choisie][serie_nom]
                
    elif gamme_choisie == "SCHÜCO":
        # Accès direct classique pour Schüco
        serie_nom = st.selectbox("Série", [""] + list(DATABASE["SCHÜCO"].keys()))
        if serie_nom:
            donnees = DATABASE["SCHÜCO"][serie_nom]

    quantite = st.number_input("Quantité", min_value=1, value=1)

# La colonne 2 s'affiche dès qu'on a pu récupérer le dictionnaire "donnees"
if gamme_choisie and serie_nom and donnees:
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

    # --- 5. CALCULS ET AFFICHAGE DU RÉSULTAT ---
    if st.session_state.calcul_fait and type_nom:
        t_base = donnees["types"][type_nom]
        t_opt = sum([donnees["options"][o] for o in options_choisies])
        t_unitaire = t_base + t_opt
        t_total = t_unitaire * quantite

        st.success(f"### Résultat : {t_total:.2f} heures")
        
        if quantite > 1:
            st.info(f"💡 Détail : {t_unitaire:.2f}h par unité × {quantite} unités")
        
        with st.expander("🔍 Détail du calcul ", expanded=True):
            libelle_affichage = f"{gamme_choisie} - {sous_gamme_choisie}".strip(" -")
            st.write(f"**Gamme :** {libelle_affichage}")
            st.write(f"**Série :** {serie_nom}")
            st.write(f"**Type choisi :** {type_nom} ({t_base}h)")
            
            if options_choisies:
                st.write("**Options sélectionnées :**")
                for opt in options_choisies:
                    val_opt = donnees["options"][opt]
                    st.write(f"  - {opt} : +{val_opt}h")
            else:
                st.write("*Aucune option sélectionnée*")
        
        st.write("")

        # Génération propre du PDF avec les nouveaux paramètres
        pdf_bytes = bytes(create_pdf(gamme_choisie, sous_gamme_choisie, serie_nom, type_nom, options_choisies, quantite, t_unitaire, t_total))
        
        st.download_button(
            label="📥 Télécharger la Fiche PDF",
            data=pdf_bytes,
            file_name=f"Fiche_{type_nom.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.write("<br>" * 3, unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: right; padding-right: 20px; padding-bottom: 20px;">
        <span style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
                     font-size: 11px; 
                     font-weight: 200; 
                     letter-spacing: 1.5px; 
                     color: #a0a0a0;">
            @TMMN
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)