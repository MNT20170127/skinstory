import streamlit as st
from deepface import DeepFace
import tempfile
import os
import cv2
from PIL import Image

st.set_page_config(page_title="SkinStory - Analyse AI", layout="centered")

st.title("🌿 SkinStory")
st.markdown("Découvrez votre **âge facial** et **émotion dominante** grâce à l'IA.")
st.markdown("📤 **Téléversez une photo claire de votre visage**")

uploaded_file = st.file_uploader("Choisissez une image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        temp_path = tmp_file.name
        img = Image.open(uploaded_file)
        img.save(temp_path)

    try:
        # Entrée âge réel
        real_age = st.number_input("Quel est votre âge réel ?", min_value=5, max_value=100, step=1)

        # Analyse IA
        result = DeepFace.analyze(img_path=temp_path, actions=["age", "gender", "emotion"], enforce_detection=False)
        face = result[0]

        st.success("✅ Analyse terminée")
        st.image(temp_path, caption="Image analysée", use_column_width=True)

        # Âge facial
        est_age = int(face['age'])
        st.subheader("🌟 Âge facial estimé")
        st.markdown(f"**Votre âge facial estimé :** {est_age} ans")
        st.markdown("👁️ **Précision estimée : ±2 ans**")

        if real_age:
            diff = est_age - real_age
            if diff < -2:
                st.success(f"🧬 Vous paraissez {abs(diff)} ans plus jeune que votre âge réel. Bravo ! 🎉")
            elif diff > 2:
                st.warning(f"🧬 Vous paraissez {abs(diff)} ans plus âgé(e) que votre âge réel. 💡 Pensez à optimiser votre routine bien-être.")
            else:
                st.info("🧬 Vous paraissez votre âge réel — équilibre parfait !")


        # Émotion dominante
        emotion = face['dominant_emotion']
        emotion_messages = {
            "happy": {
                "fr": "Votre expression dégage de la joie — cela vous rajeunit naturellement !",
                "tip": "🌞 Continuez à sourire — c'est votre meilleur soin beauté !"
            },
            "neutral": {
                "fr": "Votre visage semble calme et posé — un signe de sérénité.",
                "tip": "💡 Sourire légèrement peut améliorer la perception de jeunesse de 3 à 5 ans."
            },
            "sad": {
                "fr": "Vous semblez un peu pensif(ve) — pensez à vous accorder un moment de douceur.",
                "tip": "🌸 Prendre soin de soi passe aussi par le bien-être intérieur."
            },
            "angry": {
                "fr": "Un air sérieux détecté — peut-être est-ce le moment de vous détendre un peu ?",
                "tip": "😌 Une pause, un thé, un moment pour respirer..."
            },
            "surprise": {
                "fr": "Une touche de surprise peut indiquer une grande vivacité.",
                "tip": "✨ Garder un esprit curieux entretient la jeunesse."
            },
            "fear": {
                "fr": "Une légère tension semble présente — soyez indulgent(e) envers vous-même.",
                "tip": "🧘 Un moment de calme intérieur peut faire toute la différence."
            },
            "disgust": {
                "fr": "Votre visage exprime peut-être une gêne momentanée.",
                "tip": "🌿 Essayez un massage facial ou un soin apaisant."
            }
        }

        st.subheader("😐 Émotion dominante")
        em_data = emotion_messages.get(emotion, {
            "fr": f"Émotion détectée : {emotion.capitalize()}",
            "tip": "💡 Pensez à vous détendre et prendre soin de vous."
        })
        st.markdown(f"**{em_data['fr']}**")
        st.markdown(em_data['tip'])

    except Exception as e:
        st.error(f"❌ Erreur lors de l’analyse : {str(e)}")

    # Nettoyage de l’image temporaire
    os.remove(temp_path)



    
