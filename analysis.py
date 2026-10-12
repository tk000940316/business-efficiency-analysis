import pandas as pd

df = pd.read_csv("data/work_data_v2.csv")

print("------------------------------")
print("基本情報")
print("------------------------------")
print(df.shape)
print(df.info())
print(df.head())
print(" ")
print("------------------------------")
print("欠損値チェック")
print("------------------------------")
print(df.isnull().sum())
print(" ")
print("------------------------------")
print("作業種類の確認")
print("------------------------------")
print(df["作業名"].nunique())
print(df["作業名"].value_counts())
print(" ")
print("------------------------------")
print("工程の種類")
print("------------------------------")
print(df["工程"].nunique())
print(df["工程"].value_counts())
print(" ")
print("------------------------------")
print("日付範囲")
print("------------------------------")
df["実施日時"] = pd.to_datetime(df["実施日時"])
print(df["実施日時"].min())
print(df["実施日時"].max())
print(" ")
print("------------------------------")
print("作業時間・修正回数")
print("------------------------------")
print(df[["作業時間", "修正回数"]].describe())
print(" ")
print("------------------------------------")
print("工程別の総作業時間")
print("------------------------------------")
print(
    df.groupby("工程")["作業時間"]
      .agg(["sum", "mean", "count"])
      .sort_values("sum", ascending=False)
)
print(" ")
print("------------------------------------")
print("工程別の修正回数")
print("------------------------------------")
print(
    df.groupby("工程")["修正回数"]
      .agg(["sum", "mean", "count"])
      .sort_values("sum", ascending=False)
)
print(" ")
print("------------------------------------")
print("工程別総合分析")
print("------------------------------------")
analysis = df.groupby("工程").agg(
    発生回数=("作業時間", "count"),
    総作業時間=("作業時間", "sum"),
    平均作業時間=("作業時間", "mean"),
    総修正回数=("修正回数", "sum"),
    平均修正回数=("修正回数", "mean")
)
print(analysis.sort_values("総作業時間", ascending=False))
print(" ")
# 時間負荷スコア
analysis["時間負荷スコア"] = (
    analysis["総作業時間"] / analysis["総作業時間"].max()
)

# 修正負荷スコア
analysis["修正負荷スコア"] = (
    analysis["総修正回数"] / analysis["総修正回数"].max()
)
print(" ")
print("------------------------------------")
print("負荷スコア")
print("------------------------------------")
print(
    analysis[
        [
            "発生回数",
            "総作業時間",
            "総修正回数",
            "時間負荷スコア",
            "修正負荷スコア"
        ]
    ].sort_values("時間負荷スコア", ascending=False)
)

analysis["自動化候補スコア"] = (
    analysis["時間負荷スコア"] * 0.6
    + analysis["修正負荷スコア"] * 0.4
)
print(" ")
print("------------------------------------")
print("自動化候補スコア")
print("------------------------------------")

print(
    analysis[
        [
            "発生回数",
            "総作業時間",
            "総修正回数",
            "時間負荷スコア",
            "修正負荷スコア",
            "自動化候補スコア"
        ]
    ].sort_values("自動化候補スコア", ascending=False)
)

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Meiryo"

# ① 工程別の総作業時間
analysis["総作業時間"].sort_values(
    ascending=False
).plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("工程別の総作業時間")
plt.xlabel("工程")
plt.ylabel("総作業時間（分）")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("images/total_work_time.png", dpi=150)
plt.show()
plt.close()

# ② 工程別の総作業時間と総修正回数
analysis.plot(
    kind="scatter",
    x="総作業時間",
    y="総修正回数",
    figsize=(12, 7)
)

for name, row in analysis.iterrows():
    plt.annotate(
        name,
        (row["総作業時間"], row["総修正回数"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )

plt.title("工程別の作業時間と修正回数")
plt.xlabel("総作業時間（分）")
plt.ylabel("総修正回数")
plt.tight_layout()
plt.savefig("images/work_time_vs_corrections.png", dpi=150)
plt.show()
plt.close()