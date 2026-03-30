
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import re
import requests


def normalizar(texto):
    texto = str(texto).lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def normalizar_colunas(df):
    df.columns = [normalizar(col) for col in df.columns]
    return df

def converter_tempo(tempo):
    try:
        tempo = str(tempo).lower().strip()
        numero = float(re.findall(r'\d+\.?\d*', tempo)[0])
        if 'mes' in tempo or 'mês' in tempo:
            return numero * 30
        elif 'semana' in tempo:
            return numero * 7
        elif 'dia' in tempo:
            return numero
        else:
            return None
    except:
        return None

def dias_no_mes(mes, ano):
    import calendar
    return calendar.monthrange(int(ano), int(mes))[1]

def perfil_leitora_dinamico(genero, autor):
    perfis = {
        "romance": "Você é uma leitora romântica 💖 — se apaixona pelas histórias e vive cada emoção dos personagens.",
        "fantasia": "Você é uma leitora sonhadora ✨ — adora mundos mágicos e aventuras que vão além da realidade.",
        "suspense": "Você é uma leitora investigativa 🔍 — adora um mistério e não consegue parar até descobrir o final.",
        "existencialismo": "Você é uma leitora reflexiva 🌙 — busca profundidade nas leituras e gosta de questionar o mundo.",
        "gotico": "Você é uma leitora sombria 🖤 — se atrai pelo obscuro, pelo misterioso e pelo perturbador.",
        "distopico": "Você é uma leitora crítica 🌍 — gosta de histórias que questionam a sociedade e o futuro.",
        "terror psicologico": "Você é uma leitora corajosa 😱 — não tem medo de explorar os cantos mais sombrios da mente humana.",
        "contos": "Você é uma leitora eclética 📖 — aprecia histórias curtas e intensas que dizem muito em pouco.",
        "infantil": "Você é uma leitora nostálgica 🌈 — guarda no coração a magia das histórias da infância.",
        "diario": "Você é uma leitora humanista 🤍 — se conecta com histórias reais e experiências de vida.",
        "ficcao cientifica": "Você é uma leitora futurista 🚀 — adora explorar o que ainda está por vir e os limites da ciência.",
        "classico": "Você é uma leitora clássica 🏛️ — valoriza obras que atravessaram o tempo e continuam relevantes.",
        "young adult": "Você é uma leitora apaixonada 💫 — se conecta com histórias de descoberta, identidade e crescimento.",
        "misterio": "Você é uma leitora detetive 🕵️ — adora desvendar pistas e chegar à resposta antes do autor revelar.",
        "nao ficcao": "Você é uma leitora curiosa 🧠 — busca conhecimento real e aprender com histórias verdadeiras.",
        "literatura brasileira": "Você é uma leitora brasileira 🌿 — valoriza histórias que refletem nossa cultura e realidade.",
        "romance gotico": "Você é uma leitora sombria e apaixonada 🌹 — ama histórias que misturam amor e obscuridade.",
    }
    genero_norm = normalizar(genero)

 
    frase = perfis.get(genero_norm)

   
    if not frase:
        for chave, valor in perfis.items():
            if chave in genero_norm or genero_norm in chave:
                frase = valor
                break


    if not frase:
        frase = f"Você é uma leitora de {genero} 📚 — explora universos únicos e continua expandindo seu repertório."

    return frase + f"\n\n✍️ Sua autora favorita é **{autor}**."



st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background-color: #fff5f8;
    background-image: radial-gradient(#ffd6e7 1px, transparent 1px);
    background-size: 30px 30px;
}

h1 {
    color: #d45c7a !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #c2486a !important;
}

p, li, span, label, div {
    color: inherit;
}

[data-testid="stMetric"] {
    background-color: #ffe4ef;
    border: 2px solid #ffaacb;
    border-radius: 18px;
    padding: 16px;
}

[data-testid="stMetricLabel"] {
    color: #d45c7a !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {
    color: #c2486a !important;
}

[data-testid="stTabs"] button {
    color: #c2486a !important;
    font-weight: 700 !important;
}

.stButton > button {
    background-color: #ffaacb !important;
    color: #fff !important;
    border: none !important;
    border-radius: 30px !important;
    font-weight: 700 !important;
    padding: 10px 28px !important;
    transition: 0.3s !important;
}

.stButton > button:hover {
    background-color: #d45c7a !important;
    transform: translateY(-2px) !important;
}

[data-testid="stFileUploader"] {
    background-color: #fff0f5 !important;
    border: 2px dashed #ffaacb !important;
    border-radius: 18px !important;
    padding: 20px !important;
}

[data-testid="stExpander"] {
    background-color: #fff0f5 !important;
    border: 2px solid #ffaacb !important;
    border-radius: 18px !important;
}

[data-testid="stDataFrame"] {
    border: 2px solid #ffaacb !important;
    border-radius: 14px !important;
}

hr {
    border-color: #ffaacb !important;
}

@media (prefers-color-scheme: dark) {
    .stApp {
        background-color: #2d1a22 !important;
        background-image: radial-gradient(#4a2535 1px, transparent 1px) !important;
    }
    h1, h2, h3 {
        color: #ffaacb !important;
    }
    [data-testid="stMetric"] {
        background-color: #3d1f2d !important;
    }
    [data-testid="stMetricLabel"] {
        color: #ffaacb !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffd6e7 !important;
    }
}

</style>
""", unsafe_allow_html=True)



st.set_page_config(page_title="Book Tracker", page_icon="🌸", layout="wide")



st.markdown("# 🌸 Book Tracker")
st.markdown("""
### Transforme sua planilha de leituras em análises personalizadas

Faça upload da sua planilha e em segundos você terá:

🌸 **Biblioteca completa** com filtros por gênero e nota  
📊 **Estatísticas do seu perfil** — gênero favorito, média de notas, modo de leitura  
📅 **Evolução mensal** — veja como foram suas leituras mês a mês  
🎯 **Acompanhamento de meta** — defina sua meta e veja seu progresso  
🔮 **Recomendador** — descubra novas leituras com base no que você já amou  
""")

st.divider()



with st.expander("🌸 Como usar — clique aqui para ver o formato da planilha"):
    st.markdown("""
    Sua planilha pode ter **qualquer combinação dessas colunas**:

    | titulo | mes | ano | autor | genero | nota | modo | tempo | motivo de leitura | quantidade de paginas | categoria |
    |---|---|---|---|---|---|---|---|---|---|---|

    **Regras importantes:**
    - O arquivo deve ser **.xlsx** ou **.csv**
    - A coluna **mes** deve ser número sem zero na frente (ex: 9, não 09)
    - A coluna **nota** deve ser número (ex: 8 ou 7.5)
    - Livros sem nota ou com nota 0 serao classificados como **Leituras futuras**
    - Novas colunas opcionais: **motivo de leitura**, **quantidade de paginas**, **categoria**
    """)



arquivo = st.file_uploader("🌸 Faça upload da sua planilha aqui", type=["xlsx", "csv"])

if arquivo is not None:

    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    df = normalizar_colunas(df)

 
    if "titulo" not in df.columns:
        st.error("🌸 Sua planilha precisa ter pelo menos a coluna: titulo")
        st.stop()

   
    for col in ["nota", "ano", "mes", "quantidade de paginas"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "tempo" in df.columns:
        df["tempo_dias"] = df["tempo"].apply(converter_tempo)
    else:
        df["tempo_dias"] = None


    if "nota" in df.columns:
        df["status"] = df["nota"].apply(
            lambda x: "Leituras futuras" if pd.isna(x) or x == 0 else "Lido"
        )
    else:
        df["status"] = "Lido"

    st.success(f"🌸 Planilha carregada com sucesso! {len(df)} livros encontrados.")

    aba1, aba2, aba3 = st.tabs(["🌸 Biblioteca", "📊 Estatísticas", "🔮 Recomendador"])

  

    with aba1:

        st.subheader("🌸 Todos os livros")

        col1, col2, col3 = st.columns(3)

        with col1:
            if "genero" in df.columns:
                generos = ["Todos"] + sorted(df["genero"].dropna().unique().tolist())
                genero_filtro = st.selectbox("Filtrar por gênero", generos)
            else:
                genero_filtro = "Todos"

        with col2:
            if "nota" in df.columns:
                nota_minima = st.slider("Nota mínima", 0, 10, 0)
            else:
                nota_minima = 0

        with col3:
            status_filtro = st.selectbox("Status", ["Todos", "Lidos", "Leituras futuras"])

        df_filtrado = df.copy()

        if genero_filtro != "Todos" and "genero" in df.columns:
            df_filtrado = df_filtrado[df_filtrado["genero"] == genero_filtro]

        if status_filtro == "Lidos":
            df_filtrado = df_filtrado[df_filtrado["status"] == "Lido"]
        elif status_filtro == "Leituras futuras":
            df_filtrado = df_filtrado[df_filtrado["status"] == "Leituras futuras"]

        if "nota" in df.columns:
            df_filtrado = df_filtrado[
                (df_filtrado["nota"] >= nota_minima) | (df_filtrado["nota"].isna())
            ]

        if "nota" in df.columns:
            df_filtrado = df_filtrado.sort_values("nota", ascending=False)

        colunas_exibir = [c for c in ["titulo", "autor", "genero", "nota", "modo", "tempo", "ano", "status", "categoria", "motivo de leitura", "quantidade de paginas"] if c in df_filtrado.columns]

        st.dataframe(
            df_filtrado[colunas_exibir],
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"🌸 Mostrando {len(df_filtrado)} livros")

 

    with aba2:

        st.subheader("📊 Seu perfil de leitora")

        df_lidos = df[df["status"] == "Lido"].copy()

 
        m1, m2, m3 = st.columns(3)
        m4, m5, m6 = st.columns(3)

        m1.metric("🌸 Total de livros lidos", len(df_lidos))

        if "nota" in df.columns:
            m2.metric("⭐ Média geral", f"{df_lidos['nota'].mean(skipna=True):.1f}")
        else:
            m2.metric("⭐ Média geral", "—")

        if "genero" in df.columns and len(df_lidos) > 0:
            genero_top = df_lidos["genero"].value_counts().idxmax()
            m3.metric("📚 Gênero favorito", genero_top)
        else:
            genero_top = "—"
            m3.metric("📚 Gênero favorito", "—")

        if "autor" in df.columns and len(df_lidos) > 0:
            autor_top = df_lidos["autor"].value_counts().idxmax()
            m4.metric("✍️ Autor(a) mais lido", autor_top)
        else:
            autor_top = "—"
            m4.metric("✍️ Autor(a) mais lido", "—")

       
        if "mes" in df.columns and "ano" in df.columns and len(df_lidos) > 0:
            meses_com_leitura = df_lidos.dropna(subset=["mes", "ano"]).groupby(["ano", "mes"]).size().reset_index()
            qtd_meses = len(meses_com_leitura)
            media_por_mes = len(df_lidos) / qtd_meses if qtd_meses > 0 else 0
            m5.metric("📅 Média de livros por mês", f"{media_por_mes:.1f}")
        else:
            m5.metric("📅 Média de livros por mês", "—")

      
        if "quantidade de paginas" in df.columns and "mes" in df.columns and "ano" in df.columns:
            df_paginas = df_lidos.dropna(subset=["quantidade de paginas", "mes", "ano"]).copy()
            if len(df_paginas) > 0:
                df_paginas["dias_mes"] = df_paginas.apply(
                    lambda r: dias_no_mes(r["mes"], r["ano"]), axis=1
                )
                total_paginas = df_paginas["quantidade de paginas"].sum()
                total_dias = df_paginas["dias_mes"].sum()
                media_pag_dia = total_paginas / total_dias if total_dias > 0 else 0
                m6.metric("📖 Média de páginas por dia", f"{media_pag_dia:.0f}")
            else:
                m6.metric("📖 Média de páginas por dia", "—")
        else:
           
            if genero_top != "—" and autor_top != "—":
                frase_perfil = perfil_leitora_dinamico(genero_top, autor_top)
                with m6:
                    st.markdown(f"""
                    <div style='background-color:#ffe4ef; border:2px solid #ffaacb; border-radius:18px; padding:16px;'>
                        <div style='color:#d45c7a; font-weight:700; font-size:13px;'>🧠 Perfil de leitora</div>
                        <div style='color:#c2486a; font-size:13px; margin-top:6px;'>{frase_perfil}</div>
                    </div>
                    """, unsafe_allow_html=True)

       
        if "quantidade de paginas" in df.columns and genero_top != "—" and autor_top != "—":
            frase_perfil = perfil_leitora_dinamico(genero_top, autor_top)
            st.markdown(f"""
            <div style='background-color:#ffe4ef; border:2px solid #ffaacb; border-radius:18px; padding:16px; margin-top:16px;'>
                <div style='color:#d45c7a; font-weight:700; font-size:14px;'>🧠 Perfil de leitora</div>
                <div style='color:#c2486a; font-size:13px; margin-top:6px;'>{frase_perfil}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

     
        if "nota" in df.columns and len(df_lidos) > 0:
            st.markdown("**🏆 Destaques de leitura**")

            d1, d2 = st.columns(2)

            df_dest = df_lidos.dropna(subset=["nota"]).copy()
            if "ano" in df.columns and "mes" in df.columns:
                df_dest = df_dest.sort_values(["ano", "mes"], ascending=[False, False])

            with d1:
                if len(df_dest) > 0:
                    maior_nota = df_dest["nota"].max()
                    melhor = df_dest[df_dest["nota"] == maior_nota].iloc[0]
                    titulo_melhor = melhor.get("titulo", "—")
                    autor_melhor = melhor.get("autor", "—") if "autor" in melhor else "—"
                    st.markdown(f"""
                    <div style='background-color:#ffe4ef; border:2px solid #ffaacb; border-radius:18px; padding:16px;'>
                        <div style='color:#d45c7a; font-weight:700; font-size:13px;'>Melhor avaliado</div>
                        <div style='color:#c2486a; font-size:18px; font-weight:800; margin-top:6px;'>⭐ {maior_nota}</div>
                        <div style='color:#c2486a; font-size:13px; margin-top:4px;'>{titulo_melhor}</div>
                        <div style='color:#d45c7a; font-size:12px;'>{autor_melhor}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with d2:
                if len(df_dest) > 0:
                    menor_nota = df_dest["nota"].min()
                    pior = df_dest[df_dest["nota"] == menor_nota].iloc[0]
                    titulo_pior = pior.get("titulo", "—")
                    autor_pior = pior.get("autor", "—") if "autor" in pior else "—"
                    st.markdown(f"""
                    <div style='background-color:#ffe4ef; border:2px solid #ffaacb; border-radius:18px; padding:16px;'>
                        <div style='color:#d45c7a; font-weight:700; font-size:13px;'>Menor avaliado</div>
                        <div style='color:#c2486a; font-size:18px; font-weight:800; margin-top:6px;'>⭐ {menor_nota}</div>
                        <div style='color:#c2486a; font-size:13px; margin-top:4px;'>{titulo_pior}</div>
                        <div style='color:#d45c7a; font-size:12px;'>{autor_pior}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()

  
        if "genero" in df.columns:
            g1, g2 = st.columns(2)

            with g1:
                st.markdown("**🌸 Livros por gênero**")
                generos_count = df_lidos["genero"].value_counts()
                fig, ax = plt.subplots(figsize=(6, 4))
                fig.patch.set_facecolor("#fff5f8")
                ax.set_facecolor("#fff5f8")
                generos_count.plot(kind="bar", color="#ffaacb", ax=ax)
                ax.set_xlabel("")
                ax.set_ylabel("Quantidade")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)

            with g2:
                if "nota" in df.columns:
                    st.markdown("**⭐ Média de nota por gênero**")
                    media_genero = df_lidos.groupby("genero")["nota"].mean(numeric_only=True).sort_values(ascending=False)
                    fig2, ax2 = plt.subplots(figsize=(6, 4))
                    fig2.patch.set_facecolor("#fff5f8")
                    ax2.set_facecolor("#fff5f8")
                    media_genero.plot(kind="bar", color="#c87d87", ax=ax2)
                    ax2.set_xlabel("")
                    ax2.set_ylabel("Média")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    st.pyplot(fig2)

       
        g3, g4 = st.columns(2)

        with g3:
            if "ano" in df.columns:
                st.markdown("**📅 Livros lidos por ano**")
                por_ano = df_lidos["ano"].value_counts().sort_index()
                fig3, ax3 = plt.subplots(figsize=(6, 4))
                fig3.patch.set_facecolor("#fff5f8")
                ax3.set_facecolor("#fff5f8")
                por_ano.plot(kind="bar", color="#ec9c9d", ax=ax3)
                ax3.set_xlabel("")
                ax3.set_ylabel("Quantidade")
                plt.xticks(rotation=0)
                plt.tight_layout()
                st.pyplot(fig3)

        with g4:
            if "modo" in df.columns:
                st.markdown("**💝 Modo de leitura favorito**")
                modos = df_lidos["modo"].value_counts()
                fig4, ax4 = plt.subplots(figsize=(6, 4))
                fig4.patch.set_facecolor("#fff5f8")
                modos.plot(kind="pie", autopct="%1.1f%%", colors=["#ffaacb", "#c87d87", "#ec9c9d", "#f0c4cb", "#ffd6e7"], ax=ax4)
                ax4.set_ylabel("")
                plt.tight_layout()
                st.pyplot(fig4)

      
        if "motivo de leitura" in df.columns:
            st.divider()
            st.markdown("**💡 Motivo de leitura**")
            motivos = df_lidos["motivo de leitura"].value_counts()
            fig_mot, ax_mot = plt.subplots(figsize=(8, 4))
            fig_mot.patch.set_facecolor("#fff5f8")
            ax_mot.set_facecolor("#fff5f8")
            motivos.plot(kind="bar", color="#f0c4cb", ax=ax_mot)
            ax_mot.set_xlabel("")
            ax_mot.set_ylabel("Quantidade")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig_mot)

      
        if "mes" in df.columns and "ano" in df.columns:
            st.divider()
            st.markdown("**📅 Livros lidos por mês**")

            anos_disponiveis = sorted(df_lidos["ano"].dropna().unique().astype(int).tolist(), reverse=True)

            if anos_disponiveis:
                ano_selecionado = st.selectbox("Selecione o ano", anos_disponiveis)
                df_ano = df_lidos[df_lidos["ano"] == ano_selecionado]
                livros_por_mes = df_ano.groupby("mes").size().reindex(range(1, 13), fill_value=0)
                nomes_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
                livros_por_mes.index = nomes_meses

                fig5, ax5 = plt.subplots(figsize=(10, 4))
                fig5.patch.set_facecolor("#fff5f8")
                ax5.set_facecolor("#fff5f8")
                bars = ax5.bar(livros_por_mes.index, livros_por_mes.values, color="#ffaacb")

                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        ax5.text(bar.get_x() + bar.get_width() / 2., height,
                                f'{int(height)}', ha='center', va='bottom', fontweight='bold', color="#d45c7a")

                ax5.set_xlabel("")
                ax5.set_ylabel("Livros lidos")
                ax5.set_title(f"Leituras mês a mês em {ano_selecionado}", color="#d45c7a", fontweight="bold")
                plt.tight_layout()
                st.pyplot(fig5)

      
        if "mes" in df.columns and "ano" in df.columns:
            st.divider()
            st.markdown("**Meta de leitura**")

            col_meta1, col_meta2 = st.columns(2)

            nomes_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

            with col_meta1:
                tipo_meta = st.radio("Tipo de meta", ["Anual", "Mensal"])

            with col_meta2:
                meta = st.number_input("Quantos livros é sua meta?", min_value=1, max_value=500, value=20)

            anos_disponiveis_meta = sorted(df_lidos["ano"].dropna().unique().astype(int).tolist(), reverse=True) if len(df_lidos) > 0 else [2026]

            if tipo_meta == "Anual":
                ano_meta = st.selectbox("Ano da meta", anos_disponiveis_meta, key="ano_meta")
                df_meta = df_lidos[df_lidos["ano"] == ano_meta]
                livros_por_mes_meta = df_meta.groupby("mes").size().reindex(range(1, 13), fill_value=0)
                livros_por_mes_meta.index = nomes_meses
                lidos_total = int(livros_por_mes_meta.sum())

              
                import calendar
                dias_por_mes = [calendar.monthrange(ano_meta, m)[1] for m in range(1, 13)]
                total_dias_ano = sum(dias_por_mes)
                linha_meta = [(meta * d / total_dias_ano) for d in dias_por_mes]
                label_meta = f"Meta anual {ano_meta} — {lidos_total} de {meta} livros ({min(lidos_total/meta*100, 100):.0f}%)"

            else:
                ano_meta = st.selectbox("Ano", anos_disponiveis_meta, key="ano_meta2")
                mes_meta = st.selectbox("Mês", list(range(1, 13)), format_func=lambda x: nomes_meses[x-1])
                df_meta_m = df_lidos[(df_lidos["ano"] == ano_meta) & (df_lidos["mes"] == mes_meta)]
                lidos_total = len(df_meta_m)
                livros_por_mes_meta = pd.Series([lidos_total], index=[nomes_meses[mes_meta-1]])
                linha_meta = [meta]
                label_meta = f"Meta mensal {nomes_meses[mes_meta-1]}/{ano_meta} — {lidos_total} de {meta} livros"

            fig6, ax6 = plt.subplots(figsize=(10, 4))
            fig6.patch.set_facecolor("#fff5f8")
            ax6.set_facecolor("#fff5f8")

            bars6 = ax6.bar(livros_por_mes_meta.index, livros_por_mes_meta.values, color="#ffaacb", label="Livros lidos", zorder=2)

            ax6.plot(livros_por_mes_meta.index, linha_meta, color="#d45c7a", linewidth=2.5,
                    linestyle="--", marker="o", markersize=5, label="Meta", zorder=3)

            for bar in bars6:
                height = bar.get_height()
                if height > 0:
                    ax6.text(bar.get_x() + bar.get_width() / 2., height,
                            f'{int(height)}', ha='center', va='bottom', fontweight='bold', color="#d45c7a")

            ax6.set_xlabel("")
            ax6.set_ylabel("Livros")
            ax6.set_title(label_meta, color="#d45c7a", fontweight="bold")
            ax6.legend()
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig6)

 

    with aba3:

        st.subheader("🔮 Recomendador de leitura")
        st.markdown("Escolha um gênero **ou** uma categoria e descubra novas leituras que você ainda não leu! 🌸")

        tipo_busca = st.radio("Buscar por:", ["Gênero", "Categoria"], horizontal=True)

        if tipo_busca == "Gênero":
            if "genero" in df.columns:
                opcoes = sorted(df["genero"].dropna().unique().tolist())
            else:
                opcoes = ["Fantasia", "Suspense", "Romance", "Existencialismo"]
            termo_busca = st.selectbox("🌸 Escolha um gênero", opcoes)

        else:
            categorias_disponiveis = [
                "Ficcao cientifica", "Classico", "Fantasia", "Ficcao contemporanea",
                "Romance", "Suspense", "Young Adult", "Diario",
                "Literatura brasileira", "Misterio", "Romance Gotico", "Nao ficcao"
            ]
            if "categoria" in df.columns:
                cats_planilha = df["categoria"].dropna().unique().tolist()
                todas_cats = sorted(list(set(categorias_disponiveis + cats_planilha)))
            else:
                todas_cats = sorted(categorias_disponiveis)
            termo_busca = st.selectbox("🌸 Escolha uma categoria", todas_cats)

        if st.button("🌸 Recomendar"):

            ja_lidos = df["titulo"].str.lower().str.strip().tolist()

            with st.spinner("🌸 Buscando sugestões para você..."):

                try:
                    termo_url = normalizar(termo_busca).replace(" ", "_")
                    url = f"https://openlibrary.org/subjects/{termo_url}.json?limit=30"
                    resposta = requests.get(url, timeout=10)
                    dados_api = resposta.json()
                    livros_api = dados_api.get("works", [])

                    novos = []
                    for livro in livros_api:
                        titulo = livro.get("title", "")
                        autores = livro.get("authors", [])
                        autor = autores[0].get("name", "Autor desconhecido") if autores else "Autor desconhecido"
                        if titulo.lower().strip() not in ja_lidos:
                            novos.append(f"{titulo} — {autor}")

                    if not novos:
                        st.info(f"🌸 Não encontramos sugestões novas para **{termo_busca}** agora. Tente outro!")
                    else:
                        st.markdown(f"**📚 Sugestões de {termo_busca} para você explorar:**")
                        st.markdown("")
                        for livro in novos[:10]:
                            st.markdown(f"🌸 {livro}")
                        st.markdown("")
                        st.caption("Sugestões buscadas automaticamente — livros que ainda não estão na sua biblioteca!")

                except Exception as e:
                    st.warning("🌸 Não conseguimos buscar sugestões agora. Verifique sua conexão e tente novamente!")

else:
    st.markdown("""
    <div style='text-align:center; padding: 60px 20px;'>
        <div style='font-size: 60px;'>🌸</div>
        <h2 style='color:#d45c7a;'>Bem-vinda ao Book Tracker!</h2>
        <p style='color:#c2486a; font-size:18px;'>Faça upload da sua planilha acima para começar sua análise 🌸</p>
    </div>
    """, unsafe_allow_html=True)
