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
    df_summary = pd.read_csv("cluster_summary_results.csv")
    df_vis = pd.read_csv("cluster_visualization_data.csv")   # DBSCAN PCA
    return df_product, df_customer, df_summary, df_vis

df_product, df_customer, df_summary, df_vis = load_all()

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
            "Customer Clusters"
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

    elif dataset == "Customer Clusters":
        st.subheader("Data Visualisasi (Quantity + Country)")
        st.dataframe(df_vis, use_container_width=True)
        min_quantity = df_vis['Quantity'].min() if 'Quantity' in df_vis.columns else 0
        median_quantity = df_vis['Quantity'].median() if 'Quantity' in df_vis.columns else 0
        max_quantity = df_vis['Quantity'].max() if 'Quantity' in df_vis.columns else 0
        total_records = df_vis.shape[0]
        total_clusters = df_vis['Cluster_DBSCAN'].nunique() if 'Cluster_DBSCAN' in df_vis.columns else 0
        st.markdown(f"**Min Quantity:** {min_quantity}")
        st.markdown(f"**Median Quantity:** {median_quantity}")
        st.markdown(f"**Max Quantity:** {max_quantity}")
        st.markdown(f"**Total Record:** {total_records}")
        st.markdown(f"**Jumlah Cluster:** {total_clusters}")

# ================================
# CHARTS
# ================================
elif menu == "Charts":
    st.title("📈 Visualisasi Statistik Cluster")
    chart_dataset = st.selectbox("Pilih Dataset untuk Chart",
                                 ["Product Recommendation", "Customer Segmentation", "Customer Cluster "])

    if chart_dataset == "Product Recommendation":
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

    elif chart_dataset == "Customer Segmentation":
        st.subheader("Grafik RFM Pelanggan")
        cluster_col = "Cluster_Final" if "Cluster_Final" in df_customer.columns else "cluster"
        fig_r = px.box(df_customer, x=cluster_col, y="Recency", title="Recency per Cluster")
        st.plotly_chart(fig_r, use_container_width=True)
        if "Frequency" in df_customer.columns:
            fig_f = px.box(df_customer, x=cluster_col, y="Frequency", title="Frequency per Cluster")
            st.plotly_chart(fig_f, use_container_width=True)
        fig_m = px.box(df_customer, x=cluster_col, y="Monetary", title="Monetary per Cluster")
        st.plotly_chart(fig_m, use_container_width=True)

    elif chart_dataset == "Customer Cluster":
        st.subheader("Grafik Ringkasan")
        numeric_cols = df_summary.select_dtypes(include="number").columns
        for col in numeric_cols:
            fig = px.bar(df_summary, x="Cluster_Label", y=col, title=f"{col} per Cluster")
            st.plotly_chart(fig, use_container_width=True)

# ================================
# PCA VISUALIZATION
# ================================
elif menu == "Visualization":
    st.title("📐 Visualisasi PCA")
    pca_source = st.selectbox("Pilih Dataset PCA", ["Product PCA", "Customer PCA", "Customer Cluster PC"])

    if pca_source == "Product PCA":
        df = df_product.copy()
        x, y = "PCA1", "PCA2"
        color_col = "Cluster_Label"

    elif pca_source == "Customer PCA":
        df = df_customer.copy()
        x, y = "PC1", "PC2"
        color_col = "Cluster_Final" if "Cluster_Final" in df_customer.columns else "cluster"

    else:
        df = df_vis.copy()
        x, y = "PCA1", "PCA2"
        color_col = "Cluster_DBSCAN" if "Cluster_DBSCAN" in df_vis.columns else "cluster"

    st.subheader(f"PCA Scatter Plot — {pca_source}")
    if color_col in df.columns:
        df[color_col] = df[color_col].astype(str)
    unique_clusters = sorted(df[color_col].unique())
    color_map = {cluster: high_contrast_palette[i % len(high_contrast_palette)] for i, cluster in enumerate(unique_clusters)}
    fig = px.scatter(df, x=x, y=y, color=df[color_col], color_discrete_map=color_map, hover_data=df.columns)
    st.plotly_chart(fig, use_container_width=True)

# ================================
# FULL ANALYSIS
# ================================
else:
    st.title("🧠 Analisis Lengkap Segmentation")
    
    st.markdown("""
    Menu ini menampilkan insight dan analisis dari seluruh dataset, tanpa menampilkan tabel mentah.
    Analisis dibagi berdasarkan kategori data: Product Recommendation, Customer Segmentation, dan Customer Cluster.
    """)

    # ---- Product Recommendation ----
    st.subheader("📦 Product Recommendation")
    top_products = df_product.sort_values("TotalRevenue", ascending=False).head(5)
    low_margin_high_volume = df_product[df_product["Cluster_Label"]=="Low Margin High Volume"].shape[0]
    st.markdown(f"- Total produk: **{df_product.shape[0]}**")
    st.markdown(f"- Total revenue: **{df_product['TotalRevenue'].sum():,.2f}**")
    st.markdown(f"- Produk dengan revenue tertinggi: {top_products.iloc[0]['Description']} (**{top_products.iloc[0]['TotalRevenue']:,.2f}**)")    
    st.markdown(f"- Produk kategori 'Low Margin High Volume': **{low_margin_high_volume}**")
    st.markdown("💡 Insight: Produk dengan volume penjualan tinggi tapi margin rendah perlu strategi bundling atau kampanye promosi untuk meningkatkan profitabilitas.")

    # ---- Customer Segmentation ----
    st.subheader("👥 Customer Segmentation")
    total_customers = df_customer.shape[0]
    top_cluster = df_customer.groupby("Cluster_Final")["Monetary"].mean().idxmax()
    st.markdown(f"- Total pelanggan: **{total_customers}**")
    st.markdown(f"- Cluster dengan nilai monetary rata-rata tertinggi: **{top_cluster}**")
    st.markdown("💡 Insight: Fokus retention dan personalized marketing pada cluster bernilai tinggi dapat meningkatkan lifetime value pelanggan.")

    # ---- Customer Cluster Summary ----
    st.subheader("📊 Customer Cluster Summary")
    highest_demand_cluster = df_summary.sort_values("Avg Quantity (Mean)", ascending=False).iloc[0]["Cluster_Label"]
    st.markdown(f"- Cluster dengan rata-rata quantity tertinggi: **{highest_demand_cluster}**")
    st.markdown(f"- Total record di semua cluster: **{df_summary['Total Count'].sum():,}**")
    st.markdown("💡 Insight: Cluster dengan permintaan tinggi dapat dijadikan prioritas dalam perencanaan stok dan kampanye penjualan.")

    # ---- Kesimpulan Umum ----
    st.subheader("🔍 Kesimpulan Umum")
    st.markdown("""
    - Produk dengan performa tinggi dan volume penjualan tinggi harus mendapat perhatian khusus dalam strategi promosi dan stok.
    - Pelanggan dengan nilai monetary tinggi penting untuk strategi retention dan upselling.
    - Data cluster memberikan insight tentang distribusi demand, sehingga perencanaan stok bisa lebih efisien.
    """)
