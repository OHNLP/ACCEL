import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Define color palette at the top of the file
COLOR_PALETTE = {
    "deep_red": "#AD0034",
    "light_red": "#DDA5A0",
    "bright_orange": "#ED7353",
    "light_orange": "#F6B69D",
    "bright_yellow": "#FFE44A",
    "light_yellow": "#FBED98",
    "dark_green": "#16713E",
    "light_green": "#95BFA8",
    "dark_blue": "#1B448B",
    "light_blue": "#A2D7E8",
}

# Create a list of colors in the order we want to use them
STREAM_COLORS = [
    COLOR_PALETTE["deep_red"],
    COLOR_PALETTE["dark_blue"],
    COLOR_PALETTE["dark_green"],
    COLOR_PALETTE["bright_orange"],
    COLOR_PALETTE["bright_yellow"],
    COLOR_PALETTE["light_blue"],
    COLOR_PALETTE["light_green"],
    COLOR_PALETTE["light_red"],
    COLOR_PALETTE["light_orange"],
    COLOR_PALETTE["light_yellow"],
]


def create_basic_streamgraph(df, stacked=False):
    plt.figure(figsize=(15, 8))

    years = df["Year"].values
    terms = df.columns[1:]

    term_data = [df[term].values for term in terms]
    colors = STREAM_COLORS  # Use our custom colors instead of Spectral

    if stacked:
        baseline = np.zeros_like(years)
        for idx, (data, term) in enumerate(zip(term_data, terms)):
            plt.fill_between(
                years,
                baseline,
                baseline + data,
                label=term,
                color=colors[idx],
                alpha=0.8,
            )
            baseline += data
    else:
        for idx, (data, term) in enumerate(zip(term_data, terms)):
            plt.fill_between(
                years,
                np.zeros_like(years),
                data,
                label=term,
                color=colors[idx],
                alpha=0.8,
            )

    plt.xlabel("Year")
    plt.ylabel("Annual Count")
    plt.title("DHT Terms Usage Over Time")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.margins(x=0)
    plt.grid(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.savefig(
        f"streamgraph_basic_{'stacked' if stacked else 'unstacked'}.png",
        bbox_inches="tight",
        dpi=300,
    )
    plt.close()


def create_fancy_streamgraph(df, rank=False):
    plt.figure(figsize=(15, 8))

    years = df["Year"].values
    terms = df.columns[1:]

    # Create smooth interpolation with more points for smoother curves
    x_smooth = np.linspace(years.min(), years.max(), 500)

    # Get data and create smooth curves
    layers = []
    max_values = []
    for term in terms:
        y = df[term].values
        f = interp1d(years, y, kind="cubic")
        y_smooth = f(x_smooth)
        layers.append(y_smooth)
        max_values.append(np.max(y))

    layers = np.array(layers)
    colors = STREAM_COLORS

    if rank:
        # First, get rankings at actual year points
        n_terms = len(terms)
        y_range = np.linspace(-8, 8, n_terms)[
            ::-1
        ]

        # Get rankings at each actual year point
        year_positions = []
        # Store term order at start
        ranked_terms_start = []
        # Store term order at end
        ranked_terms_end = []

        for i, year in enumerate(years):
            counts = [df[term].values[i] for term in terms]
            ranked_indices = np.argsort(-np.array(counts))

            # Store term orders at start and end
            if i == 0:  # First year
                ranked_terms_start = [terms[idx] for idx in ranked_indices]
            elif i == len(years) - 1:  # Last year
                ranked_terms_end = [terms[idx] for idx in ranked_indices]

            # Create position mapping based on rank (highest count gets highest y-value)
            position_map = {
                idx: y_range[rank] for rank, idx in enumerate(ranked_indices)
            }
            year_positions.append([position_map[i] for i in range(n_terms)])

        # Create smooth transitions between year positions
        term_positions = []
        for term_idx in range(n_terms):
            term_year_positions = [pos[term_idx] for pos in year_positions]
            f = interp1d(years, term_year_positions, kind="cubic")
            smooth_positions = f(x_smooth)
            term_positions.append(smooth_positions)

        term_positions = np.array(term_positions)

        # Create color mapping to maintain consistent colors
        color_map = {term: colors[i] for i, term in enumerate(terms)}

    else:
        # Calculate fixed vertical spacing
        n_terms = len(terms)
        term_positions = [
            np.full(len(x_smooth), pos) for pos in np.linspace(-8, 8, n_terms)
        ]
        term_positions = np.array(term_positions)
        ranked_terms_start = terms
        ranked_terms_end = terms
        color_map = {term: colors[i] for i, term in enumerate(terms)}

    # Plot layers and normalize by max value
    for i, (layer, positions) in enumerate(zip(layers, term_positions)):
        half_width = layer / np.max(max_values)
        plt.fill_between(
            x_smooth,
            positions - half_width,
            positions + half_width,
            label=terms[i],
            color=colors[i],
            alpha=0.8,
        )

    # Add terms on both sides at their stream's positions
    y_positions = np.linspace(-8, 8, len(terms))[
        ::-1
    ]

    # Add labels in ranked order
    for i, (term_start, term_end) in enumerate(
        zip(ranked_terms_start, ranked_terms_end)
    ):
        plt.text(
            years.min() - 0.5,
            y_positions[i],
            term_start,
            ha="right",
            va="center",
            color=color_map[term_start],
        )
        plt.text(
            years.max() + 0.5,
            y_positions[i],
            term_end,
            ha="left",
            va="center",
            color=color_map[term_end],
        )

    # Customize the plot
    plt.xlabel("Year")
    plt.xticks(years)
    plt.margins(x=0)
    plt.grid(False)

    # Remove all spines and labels
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.ylabel("")

    # Set y-axis limits with more padding and remove y-axis ticks
    plt.ylim(-10, 10)
    plt.yticks([])

    # Add vertical lines for each year
    ylim = plt.gca().get_ylim()
    xlim = plt.gca().get_xlim()
    for year in years:
        plt.vlines(
            year,
            ylim[0],
            ylim[1],
            colors="gray",
            linestyles="solid",
            alpha=0.2,
            linewidth=0.5,
        )

    # Add top x-axis with visible ticks and labels
    ax2 = plt.gca().twiny()
    ax2.set_xlim(xlim)
    ax2.set_xticks(years)
    ax2.set_xticklabels([str(int(year)) for year in years])
    ax2.tick_params(axis="x", which="both", length=4, pad=2)
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)

    plt.gca().spines["bottom"].set_visible(False)
    plt.subplots_adjust(top=0.95)

    plt.savefig(
        f"streamgraph_fancy_{'ranked' if rank else 'unranked'}.png",
        bbox_inches="tight",
        dpi=300,
    )
    plt.close()


# Read the data and create both visualizations
df = pd.read_csv("Top10overallTermbyYear_andProjected.csv")
create_basic_streamgraph(df, stacked=True)
create_fancy_streamgraph(df, rank=True)
