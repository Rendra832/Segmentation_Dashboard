import streamlit as st
import pandas as pd
import plotly.express as px

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(page_title="Segmentation Dashboard", layout="wide")

# ================================
# LOAD DATA
# ================================
@st.cache_data
def load_all():
    df_product = pd.read_csv("product_recommendation.csv")
    df_customer = pd.read_csv("final_customer_cluster.csv")
    return df_product, df_customer

df_product, df_customer = load_all()

# ================================
# HIGH-CONTRAST COLOR PALETTE (40 warna)
# ================================
high_contrast_palette = [
    "#000000","#FF0000","#00FF00","#0000FF","#FFFF00","#FF00FF","#00FFFF",
    "#800000","#008000","#000080","#808000","#800080","#008080","#C00000",
    "#00C000","#0000C0","#C0C000","#C000C0","#00C0C0","#FF8000","#80FF00",
    "#0080FF","#FF0080","#00FF80","#8000FF","#FF80FF","#80FFFF","#FFFF80",
    "#404040","#606060","#A00000","#00A000","#0000A0","#A0A000","#A000A0",
    "#00A0A0","#FF4040","#40FF40","#4040FF"
]

# ================================
# SIDEBAR NAVIGATION
# ================================
st.sidebar.title("Menu Navigasi")
menu = st.sidebar.radio("Pilih Menu", [
    "Home",
    "Charts",
    "Visualization",
    "Analysis"
])

# ================================
# HOME
# ================================
if menu == "Home":
    st.title("📊 Segmentation Dashboard - Home")
    dataset = st.selectbox(
        "Pilih Dataset yang Ditampilkan",
        [
            "Product Recommendation",
            "Customer Segmentation",
        ]
    )

    if dataset == "Product Recommendation":
        st.subheader("Data Rekomendasi Produk")
        st.dataframe(df_product, use_container_width=True)
        total_products = df_product.shape[0]
        total_sales = df_product['TotalSales'].sum() if 'TotalSales' in df_product.columns else 0
        total_revenue = df_product['TotalRevenue'].sum() if 'TotalRevenue' in df_product.columns else 0
        total_clusters = df_product['Cluster_Label'].nunique() if 'Cluster_Label' in df_product.columns else 0
        st.markdown(f"**Total Produk:** {total_products}")
        st.markdown(f"**Total Sales:** {total_sales}")
        st.markdown(f"**Total Revenue:** {total_revenue:,.2f}")
        st.markdown(f"**Jumlah Label Cluster:** {total_clusters}")

    elif dataset == "Customer Segmentation":
        st.subheader("Data Segmentasi Pelanggan")
        st.dataframe(df_customer, use_container_width=True)
        max_recency = df_customer['Recency'].max() if 'Recency' in df_customer.columns else 0
        max_frequency = df_customer['Frequency'].max() if 'Frequency' in df_customer.columns else 0
        max_monetary = df_customer['Monetary'].max() if 'Monetary' in df_customer.columns else 0
        total_clusters = df_customer['Cluster_Final'].nunique() if 'Cluster_Final' in df_customer.columns else 0
        st.markdown(f"**Recency Terbesar:** {max_recency}")
        st.markdown(f"**Frequency Terbesar:** {max_frequency}")
        st.markdown(f"**Monetary Terbesar:** {max_monetary:,.2f}")
        st.markdown(f"**Jumlah Cluster:** {total_clusters}")

# ================================
# CHARTS
# ================================
elif menu == "Charts":
    st.title("📈 Visualisasi Statistik Cluster")
    chart_dataset = st.selectbox("Pilih Dataset untuk Chart",
                                 ["Product", "Customer"])

    if chart_dataset == "Product":
        st.subheader("Grafik Penjualan per Cluster Produk")
        if "Cluster_Label" in df_product.columns:
            fig1 = px.bar(
                df_product.groupby("Cluster_Label")["TotalRevenue"].sum().reset_index(),
                x="Cluster_Label", y="TotalRevenue",
                title="Total Revenue per Product Cluster"
            )
            st.plotly_chart(fig1, use_container_width=True)
            if "Quantity" in df_product.columns:
                fig2 = px.bar(
                    df_product.groupby("Cluster_Label")["Quantity"].sum().reset_index(),
                    x="Cluster_Label", y="Quantity",
                    title="Total Quantity per Product Cluster"
                )
                st.plotly_chart(fig2, use_container_width=True)

    elif chart_dataset == "Customer":
        st.subheader("Grafik RFM Pelanggan")
        cluster_col = "Cluster_Final" if "Cluster_Final" in df_customer.columns else "cluster"
        fig_r = px.box(df_customer, x=cluster_col, y="Recency", title="Recency per Cluster")
        st.plotly_chart(fig_r, use_container_width=True)
        if "Frequency" in df_customer.columns:
            fig_f = px.box(df_customer, x=cluster_col, y="Frequency", title="Frequency per Cluster")
            st.plotly_chart(fig_f, use_container_width=True)
        fig_m = px.box(df_customer, x=cluster_col, y="Monetary", title="Monetary per Cluster")
        st.plotly_chart(fig_m, use_container_width=True)

# ================================
# VISUALIZATION (PCA + UMAP)
# ================================
elif menu == "Visualization":
    st.title("📐 Visualisasi Dimensionality Reduction")
    plot_type = st.selectbox("Pilih Jenis Plot", ["PCA", "UMAP"])
    dataset_viz = st.selectbox("Pilih Dataset", ["Product", "Customer"])

    if dataset_viz == "Product":
        df = df_product.copy()
        if plot_type == "PCA":
            x, y = "PCA1", "PCA2"
        else:
            x, y = "UMAP1", "UMAP2"
        color_col = "Cluster_Label"

    elif dataset_viz == "Customer":
        df = df_customer.copy()
        if plot_type == "PCA":
            x, y = "PC1", "PC2"
        else:
            x, y = "UMAP1", "UMAP2"
        color_col = "Cluster_Final" if "Cluster_Final" in df_customer.columns else "cluster"

    st.subheader(f"{plot_type} Scatter Plot — {dataset_viz}")
    if color_col in df.columns:
        df[color_col] = df[color_col].astype(str)
    unique_clusters = sorted(df[color_col].unique())
    color_map = {cluster: high_contrast_palette[i % len(high_contrast_palette)] for i, cluster in enumerate(unique_clusters)}
    fig = px.scatter(
        df, x=x, y=y, color=df[color_col],
        color_discrete_map=color_map,
        hover_data=df.columns,
        title=f"{plot_type} Scatter Plot"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================================
# FULL ANALYSIS
# ================================
else:
    st.title("🧠 Analisis Lengkap Segmentation")
    st.markdown("""
    Menu ini hanya menampilkan insight/analisis berdasarkan data, tanpa menampilkan tabel.
    Anda bisa menambahkan visualisasi, ringkasan statistik, dan insight penting di sini.
    """)
