# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency, kruskal, mannwhitneyu


DATA_PATH = Path("Dataset_BobcatsCoyotesFoxes-1.csv")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)


def benjamini_hochberg(pvalues: list[float]) -> list[float]:
    """Benjamini-Hochberg FDR correction."""
    m = len(pvalues)
    sorted_idx = np.argsort(pvalues)
    sorted_p = np.array(pvalues)[sorted_idx]
    adjusted = np.empty(m, dtype=float)

    prev = 1.0
    for i in range(m - 1, -1, -1):
        rank = i + 1
        candidate = sorted_p[i] * m / rank
        prev = min(prev, candidate)
        adjusted[i] = prev

    out = np.empty(m, dtype=float)
    out[sorted_idx] = np.clip(adjusted, 0, 1)
    return out.tolist()


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    # Explicit dtypes for reproducibility.
    categorical_cols = ["Species", "Month", "Site", "Location"]
    binary_cols = ["Ropey", "Segmented", "Flat", "Scrape"]
    integer_cols = ["Year", "Age", "Number"]
    float_cols = ["Length", "Diameter", "Taper", "TI", "Mass", "d13C", "d15N", "CN"]

    for col in categorical_cols:
        df[col] = df[col].astype("category")
    for col in binary_cols + integer_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Analysis excludes contextual / non-trait columns.
    morphological_numeric = ["Length", "Diameter", "Taper", "TI", "Mass"]
    biogeochemical_numeric = ["d13C", "d15N", "CN"]
    morphological_binary = ["Ropey", "Segmented", "Flat", "Scrape"]

    numeric_trait_cols = morphological_numeric + biogeochemical_numeric

    # No missing values were found, but keep complete-case for safety.
    analysis_df = df.dropna(subset=["Species"] + numeric_trait_cols + morphological_binary).copy()

    # Save basic dataset summary for dataset card.
    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "species_counts": df["Species"].value_counts().to_dict(),
        "missing_total": int(df.isna().sum().sum()),
        "missing_by_column": {k: int(v) for k, v in df.isna().sum().to_dict().items()},
    }
    (OUT_DIR / "dataset_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Numerical summaries (all numeric columns).
    numeric_cols = float_cols + integer_cols + binary_cols
    num_summary = df[numeric_cols].describe().T
    num_summary.to_csv(OUT_DIR / "numerical_summary.csv")

    # Categorical summaries.
    cat_rows = []
    for col in categorical_cols:
        vc = df[col].value_counts(dropna=False)
        top = vc.index[0]
        cat_rows.append(
            {
                "feature": col,
                "unique_values": int(df[col].nunique(dropna=False)),
                "most_common_value": str(top),
                "most_common_count": int(vc.iloc[0]),
            }
        )
    pd.DataFrame(cat_rows).to_csv(OUT_DIR / "categorical_summary.csv", index=False)

    # Kruskal-Wallis for continuous traits across 3 species.
    kw_rows = []
    for col in numeric_trait_cols:
        groups = [
            analysis_df.loc[analysis_df["Species"] == sp, col].astype(float).dropna().values
            for sp in analysis_df["Species"].cat.categories
        ]
        stat, pval = kruskal(*groups)
        medians = analysis_df.groupby("Species", observed=True)[col].median().to_dict()
        means = analysis_df.groupby("Species", observed=True)[col].mean().to_dict()
        kw_rows.append(
            {
                "trait": col,
                "test": "Kruskal-Wallis",
                "statistic": float(stat),
                "p_value": float(pval),
                "bobcat_mean": float(means.get("Bobcat", np.nan)),
                "coyote_mean": float(means.get("Coyote", np.nan)),
                "grayfox_mean": float(means.get("GrayFox", np.nan)),
                "bobcat_median": float(medians.get("Bobcat", np.nan)),
                "coyote_median": float(medians.get("Coyote", np.nan)),
                "grayfox_median": float(medians.get("GrayFox", np.nan)),
            }
        )

    kw_df = pd.DataFrame(kw_rows).sort_values("p_value")
    kw_df["p_adj_bh"] = benjamini_hochberg(kw_df["p_value"].tolist())
    kw_df.to_csv(OUT_DIR / "kruskal_results.csv", index=False)

    # Pairwise Mann-Whitney for significant continuous traits.
    pair_rows = []
    species = ["Bobcat", "Coyote", "GrayFox"]
    pairs = [(species[0], species[1]), (species[0], species[2]), (species[1], species[2])]
    for trait in kw_df.loc[kw_df["p_adj_bh"] < 0.05, "trait"]:
        for a, b in pairs:
            xa = analysis_df.loc[analysis_df["Species"] == a, trait].astype(float)
            xb = analysis_df.loc[analysis_df["Species"] == b, trait].astype(float)
            stat, pval = mannwhitneyu(xa, xb, alternative="two-sided")
            pair_rows.append(
                {
                    "trait": trait,
                    "species_a": a,
                    "species_b": b,
                    "statistic": float(stat),
                    "p_value": float(pval),
                    "median_a": float(np.median(xa)),
                    "median_b": float(np.median(xb)),
                }
            )

    if pair_rows:
        pair_df = pd.DataFrame(pair_rows)
        pair_df["p_adj_bh"] = benjamini_hochberg(pair_df["p_value"].tolist())
        pair_df.to_csv(OUT_DIR / "pairwise_mannwhitney.csv", index=False)

    # Chi-square tests for binary morphology variables.
    chi_rows = []
    for col in morphological_binary:
        table = pd.crosstab(analysis_df["Species"], analysis_df[col])
        chi2, pval, dof, _ = chi2_contingency(table)
        prevalence = analysis_df.groupby("Species", observed=True)[col].mean().to_dict()
        chi_rows.append(
            {
                "trait": col,
                "test": "Chi-square",
                "statistic": float(chi2),
                "dof": int(dof),
                "p_value": float(pval),
                "bobcat_rate": float(prevalence.get("Bobcat", np.nan)),
                "coyote_rate": float(prevalence.get("Coyote", np.nan)),
                "grayfox_rate": float(prevalence.get("GrayFox", np.nan)),
            }
        )

    chi_df = pd.DataFrame(chi_rows).sort_values("p_value")
    chi_df["p_adj_bh"] = benjamini_hochberg(chi_df["p_value"].tolist())
    chi_df.to_csv(OUT_DIR / "chi_square_results.csv", index=False)

    # Combined summary table for discussion.
    sig_numeric = kw_df.loc[kw_df["p_adj_bh"] < 0.05, ["trait", "p_value", "p_adj_bh", "bobcat_median", "coyote_median", "grayfox_median"]]
    sig_binary = chi_df.loc[chi_df["p_adj_bh"] < 0.05, ["trait", "p_value", "p_adj_bh", "bobcat_rate", "coyote_rate", "grayfox_rate"]]
    sig_numeric.to_csv(OUT_DIR / "significant_numeric_traits.csv", index=False)
    sig_binary.to_csv(OUT_DIR / "significant_binary_traits.csv", index=False)

    # Figures for report/dataset card.
    sns.set_theme(style="whitegrid")

    # Figure 1: selected numeric trait distributions.
    selected_numeric = kw_df.head(4)["trait"].tolist()
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    for ax, trait in zip(axes.flatten(), selected_numeric):
        sns.boxplot(data=analysis_df, x="Species", y=trait, ax=ax)
        sns.stripplot(data=analysis_df, x="Species", y=trait, color="black", alpha=0.35, size=3, ax=ax)
        p = kw_df.loc[kw_df["trait"] == trait, "p_adj_bh"].iloc[0]
        ax.set_title(f"{trait} (BH-adjusted p={p:.3g})")
        ax.set_xlabel("")
    fig.savefig(OUT_DIR / "figure_numeric_boxplots.png", dpi=200)
    plt.close(fig)

    # Figure 2: biogeochemical pair plot.
    pair = sns.pairplot(
        analysis_df,
        vars=["d13C", "d15N", "CN"],
        hue="Species",
        corner=True,
        plot_kws={"alpha": 0.7, "s": 24},
    )
    pair.fig.suptitle("Biogeochemical Traits by Species", y=1.02)
    pair.savefig(OUT_DIR / "figure_biogeochemical_pairplot.png", dpi=180)
    plt.close(pair.fig)

    # Figure 3: prevalence of binary morphology traits.
    long_bin = analysis_df.melt(id_vars=["Species"], value_vars=morphological_binary, var_name="Trait", value_name="Present")
    prev = long_bin.groupby(["Species", "Trait"], observed=True)["Present"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    sns.barplot(data=prev, x="Trait", y="Present", hue="Species", ax=ax)
    ax.set_ylabel("Proportion with trait present")
    ax.set_ylim(0, 1)
    ax.set_title("Morphological Binary Traits by Species")
    fig.savefig(OUT_DIR / "figure_binary_prevalence.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()
